#!/usr/bin/env python3
"""
小爪智能选股模型 v1.0
基于小爪超短交易系统
自动筛选符合交易条件的股票

作者: 小爪 🦞
日期: 2026-02-10
版本: v1.0
"""

import tushare as ts
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import json
import time
import os

# ==================== 配置 ====================

@dataclass
class Config:
    """系统配置"""
    # Tushare Token
    token: str = "your_token_here"
    
    # 选股评分门槛
    min_score: int = 60  # 及格线
    strong_score: int = 75  # 强烈建议线
    
    # 仓位配置
    max_positions: int = 5  # 最大持仓数
    max_single_position: float = 0.3  # 单只最大仓位
    
    # 情绪周期配置
    market_sentiment_threshold: int = 50  # 市场情绪门槛
    
    # 量能配置
    volume_ratio_buy: float = 1.5  # 买入量比
    turnover_rate_min: float = 3.0  # 最小换手率
    turnover_rate_max: float = 15.0  # 最大换手率
    
    # 形态配置
    ma_score_threshold: int = 3  # 均线多头分数
    pattern_score_threshold: int = 60  # 形态评分门槛


class MarketPhase(Enum):
    """市场情绪周期"""
    冰点 = "冰点"
    复苏 = "复苏"
    回暖 = "回暖"
    高潮 = "高潮"
    过热 = "过热"
    退潮 = "退潮"


@dataclass
class StockData:
    """股票数据"""
    code: str
    name: str
    close: float
    open: float
    high: float
    low: float
    volume: float
    amount: float
    turnover_rate: float
    pe: float
    pb: float
    market_cap: float
    
    # 额外数据
    ma5: float = 0
    ma10: float = 0
    ma20: float = 0
    ma60: float = 0
    volume_ratio: float = 1.0
    up_limit_count: int = 0
    down_limit_count: int = 0
    market_sentiment: int = 50
    
    # 计算字段
    price_change: float = 0
    is_leader: bool = False
    trend: str = "震荡"
    pattern_score: int = 0
    ma_multi: bool = False
    wait_days: int = 0
    divergence_degree: float = 0
    acceleration_degree: float = 0
    trend_broken: bool = False


@dataclass
class StockScore:
    """股票评分结果"""
    stock: StockData
    total_score: int
    score_breakdown: Dict[str, int]
    buy_signal: bool
    buy_timing: str
    sell_signal: bool
    sell_timing: str
    position建议: str
    stop_loss: float
    target_price: float


class XueqiuDataFetcher:
    """从东方财富/同花顺获取数据（模拟）"""
    
    @staticmethod
    def get_stock_list() -> List[Dict]:
        """获取A股列表"""
        # 实际项目中应使用Tushare或东方财富API
        # 这里返回模拟数据
        return [
            {"code": "000001", "name": "平安银行"},
            {"code": "000002", "name": "万 科Ａ"},
            {"code": "000063", "name": "中兴通讯"},
            {"code": "000066", "name": "中国长城"},
            {"code": "000069", "name": "华侨城Ａ"},
            {"code": "000100", "name": "TCL科技"},
            {"code": "000157", "name": "中联重科"},
            {"code": "000158", "name": "常山北明"},
            {"code": "000166", "name": "申万宏源"},
            {"code": "000333", "name": "美的集团"},
            {"code": "000338", "name": "潍柴动力"},
            {"code": "000423", "name": "桂林旅游"},
            {"code": "000425", "name": "徐 工 机"},
            {"code": "000501", "name": "鄂武商Ａ"},
            {"code": "000503", "name": "国新健康"},
            {"code": "000504", "name": "南华生物"},
            {"code": "000506", "name": "京粮控股"},
            {"code": "000507", "name": "粤 金 珠"},
            {"code": "000509", "name": "华塑控股"},
            {"code": "000510", "name": "新 金 路"},
        ]
    
    @staticmethod
    def get_stock_data(code: str, days: int = 20) -> Optional[StockData]:
        """获取单只股票数据"""
        # 模拟数据
        import random
        
        base_price = random.uniform(5, 100)
        data = StockData(
            code=code,
            name=f"股票{code}",
            close=base_price,
            open=base_price * random.uniform(0.95, 1.02),
            high=base_price * random.uniform(1.01, 1.05),
            low=base_price * random.uniform(0.95, 0.99),
            volume=random.uniform(10000000, 100000000),
            amount=random.uniform(100000000, 1000000000),
            turnover_rate=random.uniform(2, 10),
            pe=random.uniform(10, 50),
            pb=random.uniform(1, 5),
            market_cap=random.uniform(5000000000, 50000000000),
        )
        
        # 计算均线
        data.ma5 = base_price * random.uniform(0.98, 1.02)
        data.ma10 = base_price * random.uniform(0.97, 1.03)
        data.ma20 = base_price * random.uniform(0.96, 1.04)
        data.ma60 = base_price * random.uniform(0.95, 1.05)
        
        # 计算其他字段
        data.price_change = random.uniform(-5, 12)
        data.volume_ratio = random.uniform(0.5, 2.5)
        data.is_leader = random.random() < 0.2
        data.trend = random.choice(["上升", "下降", "震荡"])
        data.pattern_score = random.uniform(60, 95)
        data.ma_multi = data.ma5 > data.ma10 > data.ma20 > data.ma60
        data.wait_days = random.randint(1, 10)
        data.divergence_degree = random.uniform(0.3, 0.8)
        data.acceleration_degree = random.uniform(0.2, 0.9)
        data.trend_broken = random.random() < 0.1
        
        return data
    
    @staticmethod
    def get_market_sentiment() -> Tuple[MarketPhase, Dict]:
        """获取市场情绪"""
        import random
        
        # 模拟市场数据
        up_count = random.randint(1500, 3500)
        down_count = 4000 - up_count
        up_limit_count = random.randint(50, 300)
        down_limit_count = random.randint(10, 80)
        
        # 判断情绪周期
        if up_limit_count > 200 and up_count > 3000:
            phase = MarketPhase.高潮
        elif up_limit_count > 100 and up_count > 2500:
            phase = MarketPhase.回暖
        elif up_limit_count > 50 and up_count > 2000:
            phase = MarketPhase.复苏
        elif down_limit_count > 50 and up_count < 1500:
            phase = MarketPhase.冰点
        elif up_limit_count > 150 and up_count > 2800:
            phase = MarketPhase.过热
        else:
            phase = MarketPhase.退潮
        
        market_info = {
            "up_count": up_count,
            "down_count": down_count,
            "up_limit_count": up_limit_count,
            "down_limit_count": down_limit_count,
            "market_sentiment": random.randint(30, 90)
        }
        
        return phase, market_info


class StockSelector:
    """股票评分器"""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
    
    def calculate_score(self, stock: StockData, market: MarketPhase, market_info: Dict) -> StockScore:
        """计算股票评分"""
        
        score_breakdown = {}
        
        # ==================== 条件一：情绪周期（20分） ====================
        if market in [MarketPhase.复苏, MarketPhase.回暖, MarketPhase.高潮]:
            emotion_score = 20
        elif market == MarketPhase.过热:
            emotion_score = 10
        else:
            emotion_score = 0
        score_breakdown["情绪周期"] = emotion_score
        
        # ==================== 条件二：板块效应（15分） ====================
        if market_info["up_limit_count"] > 100:
            sector_score = 15
        elif market_info["up_limit_count"] > 50:
            sector_score = 5
        else:
            sector_score = 0
        score_breakdown["板块效应"] = sector_score
        
        # ==================== 条件三：个股地位（20分） ====================
        if stock.is_leader:
            leader_score = 20
        else:
            leader_score = 0
        score_breakdown["个股地位"] = leader_score
        
        # ==================== 条件四：形态完美（15分） ====================
        pattern_score = 0
        
        # 均线多头
        if stock.ma_multi:
            pattern_score += 5
        score_breakdown["均线多头"] = 5 if stock.ma_multi else 0
        
        # 趋势向上
        if stock.trend == "上升":
            pattern_score += 5
        score_breakdown["趋势向上"] = 5 if stock.trend == "上升" else 0
        
        # 回调缩量（假设）
        if stock.volume_ratio < 0.8:
            pattern_score += 3
        score_breakdown["回调缩量"] = 3 if stock.volume_ratio < 0.8 else 0
        
        # 量价配合
        if stock.price_change > 0 and stock.volume_ratio > 1:
            pattern_score += 2
        score_breakdown["量价配合"] = 2 if stock.price_change > 0 and stock.volume_ratio > 1 else 0
        
        score_breakdown["形态完美"] = pattern_score
        
        # ==================== 条件五：筹码集中（10分） ====================
        # 模拟：换手率适中表示筹码相对集中
        if self.config.turnover_rate_min <= stock.turnover_rate <= self.config.turnover_rate_max:
            chip_score = 10
        else:
            chip_score = 5
        score_breakdown["筹码集中"] = chip_score
        
        # ==================== 条件六：量能健康（10分） ====================
        volume_score = 0
        
        if stock.volume_ratio > self.config.volume_ratio_buy:
            volume_score += 5
        score_breakdown["量比>1.5"] = 5 if stock.volume_ratio > self.config.volume_ratio_buy else 0
        
        if self.config.turnover_rate_min <= stock.turnover_rate <= self.config.turnover_rate_max:
            volume_score += 3
        score_breakdown["换手率3-15%"] = 3 if self.config.turnover_rate_min <= stock.turnover_rate <= self.config.turnover_rate_max else 0
        
        # 量价配合
        if stock.price_change > 0 and stock.volume_ratio > 1:
            volume_score += 2
        score_breakdown["量价健康"] = 2 if stock.price_change > 0 and stock.volume_ratio > 1 else 0
        
        score_breakdown["量能健康"] = volume_score
        
        # ==================== 条件七：分时强势（5分） ====================
        # 模拟：收盘在开盘上方表示分时强势
        if stock.close > stock.open:
            minute_score = 5
        else:
            minute_score = 0
        score_breakdown["分时强势"] = minute_score
        
        # ==================== 条件八：情绪信号（5分） ====================
        if market in [MarketPhase.回暖, MarketPhase.高潮]:
            sentiment_score = 5
        else:
            sentiment_score = 0
        score_breakdown["情绪信号"] = sentiment_score
        
        # ==================== 计算总分 ====================
        total_score = (
            emotion_score + 
            sector_score + 
            leader_score + 
            pattern_score + 
            chip_score + 
            volume_score + 
            minute_score + 
            sentiment_score
        )
        
        # ==================== 买入信号 ====================
        buy_signal = False
        buy_timing = ""
        
        if total_score >= self.config.min_score:
            # 判断买入时机
            if stock.trend == "上升" and stock.ma_multi:
                buy_signal = True
                buy_timing = "突破买入/回调买入"
            elif stock.price_change > 5 and stock.volume_ratio > 1.5:
                buy_signal = True
                buy_timing = "半路买入"
            elif stock.is_leader:
                buy_signal = True
                buy_timing = "竞价买入/打板买入"
        
        # ==================== 卖出信号 ====================
        sell_signal = False
        sell_timing = ""
        
        if stock.price_change > 15:
            sell_signal = True
            sell_timing = "达到目标位"
        elif stock.price_change > 0 and stock.volume_ratio < 0.5:
            sell_signal = True
            sell_timing = "量价背离"
        elif market in [MarketPhase.过热, MarketPhase.退潮]:
            sell_signal = True
            sell_timing = "情绪转弱"
        
        # ==================== 仓位建议 ====================
        if total_score >= 80:
            position = "重仓（50-60%）"
        elif total_score >= 70:
            position = "中仓（30-40%）"
        elif total_score >= 60:
            position = "轻仓（20-30%）"
        else:
            position = "不参与"
        
        # ==================== 止损位 ====================
        stop_loss = stock.close * 0.95  # 5%止损
        
        # ==================== 目标价 ====================
        target_price = stock.close * 1.10  # 10%目标
        
        return StockScore(
            stock=stock,
            total_score=total_score,
            score_breakdown=score_breakdown,
            buy_signal=buy_signal,
            buy_timing=buy_timing,
            sell_signal=sell_signal,
            sell_timing=sell_timing,
            position建议=position,
            stop_loss=round(stop_loss, 2),
            target_price=round(target_price, 2)
        )


class StockSelectionModel:
    """选股模型"""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.selector = StockSelector(config)
        self.data_fetcher = XueqiuDataFetcher()
        self.results: List[StockScore] = []
    
    def run(self, stock_count: int = 50) -> List[StockScore]:
        """运行选股模型"""
        print("="*80)
        print("小爪智能选股模型 v1.0")
        print("="*80)
        print(f"选股数量: {stock_count}")
        print(f"评分门槛: {self.config.min_score}分（及格）/ {self.config.strong_score}分（强烈）")
        print("="*80)
        print()
        
        # 1. 获取市场情绪
        print("【1】获取市场情绪...")
        market, market_info = self.data_fetcher.get_market_sentiment()
        print(f"   当前市场周期: {market.value}")
        print(f"   上涨家数: {market_info['up_count']}")
        print(f"   涨停家数: {market_info['up_limit_count']}")
        print(f"   市场情绪值: {market_info['market_sentiment']}")
        print()
        
        # 2. 获取股票列表
        print("【2】获取股票列表...")
        stock_list = self.data_fetcher.get_stock_list()[:stock_count]
        print(f"   待筛选股票: {len(stock_list)}只")
        print()
        
        # 3. 筛选评分
        print("【3】开始评分...")
        results = []
        
        for i, stock_info in enumerate(stock_list, 1):
            # 获取股票数据
            stock = self.data_fetcher.get_stock_data(stock_info["code"])
            if stock:
                stock.name = stock_info["name"]
                
                # 计算评分
                score = self.selector.calculate_score(stock, market, market_info)
                results.append(score)
                
                # 打印进度
                if i % 10 == 0 or i == len(stock_list):
                    print(f"   已完成: {i}/{len(stock_list)} ({i*100//len(stock_list)}%)")
        
        print()
        
        # 4. 排序筛选
        print("【4】排序筛选...")
        results.sort(key=lambda x: x.total_score, reverse=True)
        self.results = results
        print()
        
        # 5. 输出结果
        print("【5】选股结果")
        print("="*80)
        
        # 及格股票
        qualified = [r for r in results if r.total_score >= self.config.min_score]
        print(f"\n✅ 及格股票（≥{self.config.min_score}分）: {len(qualified)}只\n")
        
        if qualified:
            print("-"*80)
            print(f"{'排名':^4} {'代码':^10} {'名称':^12} {'总分':^6} {'评分详情':^40} {'买入时机':^20} {'仓位':^15} {'止损':^10}")
            print("-"*80)
            
            for i, score in enumerate(qualified[:20], 1):  # 只显示前20只
                # 评分详情
                breakdown_str = f"情{score.score_breakdown['情绪周期']:.0f}板{score.score_breakdown['板块效应']:.0f}龙{score.score_breakdown['个股地位']:.0f}形{score.score_breakdown['形态完美']:.0f}筹{score.score_breakdown['筹码集中']:.0f}量{score.score_breakdown['量能健康']:.0f}"
                
                # 买入信号
                buy = "✅" + score.buy_timing if score.buy_signal else "❌"
                
                print(f"{i:^4} {score.stock.code:^10} {score.stock.name:^12} {score.total_score:^6} {breakdown_str:^40} {buy:^20} {score.position建议:^15} {score.stop_loss:^10.2f}")
        
        # 强烈推荐
        strong = [r for r in results if r.total_score >= self.config.strong_score]
        print(f"\n🌟 强烈推荐（≥{self.config.strong_score}分）: {len(strong)}只\n")
        
        if strong:
            print("-"*80)
            print(f"{'排名':^4} {'代码':^10} {'名称':^12} {'收盘价':^10} {'涨跌幅':^10} {'量比':^8} {'换手率':^10} {'目标价':^10}")
            print("-"*80)
            
            for i, score in enumerate(strong[:10], 1):
                print(f"{i:^4} {score.stock.code:^10} {score.stock.name:^12} {score.stock.close:^10.2f} {score.stock.price_change:^10.2f}% {score.stock.volume_ratio:^8.2f} {score.stock.turnover_rate:^10.2f}% {score.target_price:^10.2f}")
        
        # 6. 统计信息
        print("\n" + "="*80)
        print("【6】统计信息")
        print("="*80)
        print(f"总筛选股票: {len(results)}只")
        print(f"及格股票: {len(qualified)}只 ({len(qualified)*100//len(results)}%)")
        print(f"强烈推荐: {len(strong)}只 ({len(strong)*100//len(results)}%)")
        print(f"平均分: {sum(r.total_score for r in results)/len(results):.1f}分")
        print(f"最高分: {results[0].total_score}分")
        
        # 7. 买入建议
        if qualified:
            print("\n" + "="*80)
            print("【7】买入建议（TOP 5）")
            print("="*80)
            
            for i, score in enumerate(qualified[:5], 1):
                print(f"\n{i}. {score.stock.code} {score.stock.name}")
                print(f"   总分: {score.total_score}分")
                print(f"   当前价: {score.stock.close:.2f}元")
                print(f"   目标价: {score.target_price:.2f}元（+{((score.target_price-score.stock.close)/score.stock.close*100):.1f}%）")
                print(f"   止损位: {score.stop_loss:.2f}元（-{((score.stock.close-score.stop_loss)/score.stock.close*100):.1f}%）")
                print(f"   建议仓位: {score.position建议}")
                print(f"   买入时机: {score.buy_timing}")
        
        # 8. 保存结果
        self.save_results(qualified, strong)
        
        return qualified
    
    def save_results(self, qualified: List[StockScore], strong: List[StockScore]):
        """保存结果"""
        output_dir = "/home/admin/.openclaw/workspace/选股结果"
        os.makedirs(output_dir, exist_ok=True)
        
        # 保存及格股票
        with open(f"{output_dir}/及格股票_{datetime.now().strftime('%Y%m%d')}.txt", "w") as f:
            f.write("小爪智能选股结果\n")
            f.write("="*80 + "\n")
            f.write(f"日期: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"评分门槛: {self.config.min_score}分\n")
            f.write("="*80 + "\n\n")
            
            for i, score in enumerate(qualified, 1):
                f.write(f"{i}. {score.stock.code} {score.stock.name}\n")
                f.write(f"   总分: {score.total_score}分\n")
                f.write(f"   当前价: {score.stock.close:.2f}元\n")
                f.write(f"   目标价: {score.target_price:.2f}元\n")
                f.write(f"   止损位: {score.stop_loss:.2f}元\n")
                f.write(f"   建议仓位: {score.position建议}\n")
                f.write(f"   买入时机: {score.buy_timing}\n")
                f.write(f"   评分详情: {score.score_breakdown}\n")
                f.write("\n")
        
        # 保存强烈推荐
        with open(f"{output_dir}/强烈推荐_{datetime.now().strftime('%Y%m%d')}.txt", "w") as f:
            f.write("小爪强烈推荐股票\n")
            f.write("="*80 + "\n")
            f.write(f"日期: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"评分门槛: {self.config.strong_score}分\n")
            f.write("="*80 + "\n\n")
            
            for i, score in enumerate(strong, 1):
                f.write(f"{i}. {score.stock.code} {score.stock.name}\n")
                f.write(f"   总分: {score.total_score}分\n")
                f.write(f"   当前价: {score.stock.close:.2f}元\n")
                f.write(f"   目标价: {score.target_price:.2f}元\n")
                f.write(f"   止损位: {score.stop_loss:.2f}元\n")
                f.write(f"   建议仓位: {score.position建议}\n")
                f.write("\n")
        
        print(f"\n✅ 结果已保存到: {output_dir}/")
    
    def get_top_stocks(self, count: int = 5) -> List[StockScore]:
        """获取TOP股票"""
        if not self.results:
            self.run()
        
        return self.results[:count]


def main():
    """主函数"""
    # 创建配置
    config = Config()
    
    # 创建选股模型
    model = StockSelectionModel(config)
    
    # 运行选股
    qualified = model.run(stock_count=50)
    
    # 获取TOP 5
    top5 = model.get_top_stocks(5)
    
    print("\n" + "="*80)
    print("选股完成！")
    print("="*80)
    print(f"共选出 {len(qualified)} 只及格股票")
    print(f"其中 {len([s for s in qualified if s.total_score >= config.strong_score])} 只强烈推荐")
    
    if top5:
        print("\n最佳选择:")
        for i, score in enumerate(top5[:3], 1):
            print(f"  {i}. {score.stock.code} {score.stock.name} - {score.total_score}分 - 买入时机: {score.buy_timing}")
    
    return qualified


if __name__ == "__main__":
    main()
