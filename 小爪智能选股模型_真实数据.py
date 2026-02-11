#!/usr/bin/env python3
"""
小爪智能选股模型 v1.0（真实数据版）
基于小爪超短交易系统
自动筛选符合交易条件的股票

作者: 小爪 🦞
日期: 2026-02-11
版本: v1.0（真实数据版）

使用说明：
1. 安装tushare: pip install tushare
2. 配置Token: 在下方设置你的Tushare Token
3. 运行模型: python3 小爪智能选股模型_真实数据.py

Tushare注册: https://tushare.pro
"""

import tushare as ts
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import time
import os

# ==================== 配置区域 ====================

# 在这里设置你的Tushare Token
# 请替换为你的实际Token
TUSHARE_TOKEN = "YOUR_TUSHARE_TOKEN"  # 已配置Token

# 是否使用真实数据（True=真实数据，False=模拟数据）
USE_REAL_DATA = True

# 选股评分门槛
MIN_SCORE = 60  # 及格线
STRONG_SCORE = 75  # 强烈推荐线

# 仓位配置
MAX_POSITIONS = 5  # 最大持仓数
MAX_SINGLE_POSITION = 0.3  # 单只最大仓位

# 量能配置
VOLUME_RATIO_BUY = 1.5  # 买入量比
TURNOVER_RATE_MIN = 3.0  # 最小换手率
TURNOVER_RATE_MAX = 15.0  # 最大换手率


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
    
    # 额外数据
    ma5: float = 0
    ma10: float = 0
    ma20: float = 0
    ma60: float = 0
    pre_close: float = 0
    
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
    volume_ratio: float = 1.0
    up_limit_count: int = 0
    down_limit_count: int = 0
    market_sentiment: int = 50


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


class RealDataFetcher:
    """真实数据获取器（使用Tushare）"""
    
    def __init__(self, token: str):
        if token and USE_REAL_DATA:
            ts.set_token(token)
            self.pro = ts.pro_api()
        else:
            self.pro = None
    
    def get_all_stocks(self) -> List[Dict]:
        """获取所有A股列表"""
        if not self.pro or not USE_REAL_DATA:
            return self.get_mock_stock_list()
        
        try:
            # 获取在交易的A股
            df = self.pro.stock_basic(
                exchange='',
                list_status='L',
                fields='ts_code,symbol,name,area,industry,market,exchange,list_date'
            )
            
            # 排除ST股和新股（上市不足30天）
            stocks = []
            for _, row in df.iterrows():
                code = row['ts_code'].replace('SZSE.', '').replace('SSE.', '')
                if not row['name'].startswith('ST') and not row['name'].startswith('*'):
                    stocks.append({
                        'code': code,
                        'name': row['name']
                    })
            
            print(f"   获取到 {len(stocks)} 只股票")
            return stocks
        
        except Exception as e:
            print(f"   获取股票列表失败: {e}")
            return self.get_mock_stock_list()
    
    def get_stock_data(self, code: str) -> Optional[StockData]:
        """获取单只股票数据"""
        if not self.pro or not USE_REAL_DATA:
            return None
        
        try:
            # 获取日线数据
            df = self.pro.daily(
                ts_code=f"{code}.SZ" if code.startswith('0') or code.startswith('3') else f"{code}.SH",
                start_date=(datetime.now() - timedelta(days=30)).strftime('%Y%m%d'),
                end_date=datetime.now().strftime('%Y%m%d')
            )
            
            if df.empty:
                return None
            
            # 最新一天数据
            row = df.iloc[0]
            
            # 获取前5日均量
            avg_volume = df['vol'].iloc[1:6].mean() if len(df) > 5 else row['vol']
            volume_ratio = row['vol'] / avg_volume if avg_volume > 0 else 1.0
            
            # 计算均线
            closes = df['close'].tolist()
            ma5 = sum(closes[:5]) / 5 if len(closes) >= 5 else closes[0]
            ma10 = sum(closes[:10]) / 10 if len(closes) >= 10 else closes[0]
            ma20 = sum(closes[:20]) / 20 if len(closes) >= 20 else closes[0]
            ma60 = sum(closes[:60]) / 60 if len(closes) >= 60 else closes[0]
            
            # 判断均线多头
            ma_multi = ma5 > ma10 > ma20 > ma60
            
            # 判断趋势
            if ma5 > ma10 > ma20 > ma60:
                trend = "上升"
            elif ma5 < ma10 < ma20 < ma60:
                trend = "下降"
            else:
                trend = "震荡"
            
            # 判断是否龙头（模拟：涨停且量比>2）
            is_leader = row['pct_chg'] > 9.5 and volume_ratio > 2
            
            return StockData(
                code=code,
                name="股票",  # 需要额外查询
                close=row['close'],
                open=row['open'],
                high=row['high'],
                low=row['low'],
                volume=row['vol'],
                amount=row['amount'],
                turnover_rate=row['turnover_rate'],
                pe=0,  # 需要额外查询
                pb=0,  # 需要额外查询
                ma5=ma5,
                ma10=ma10,
                ma20=ma20,
                ma60=ma60,
                pre_close=row['pre_close'],
                price_change=row['pct_chg'],
                is_leader=is_leader,
                trend=trend,
                ma_multi=ma_multi,
                volume_ratio=volume_ratio
            )
        
        except Exception as e:
            print(f"   获取 {code} 数据失败: {e}")
            return None
    
    def get_market_sentiment(self) -> Tuple[MarketPhase, Dict]:
        """获取市场情绪"""
        if not self.pro or not USE_REAL_DATA:
            return self.get_mock_market_sentiment()
        
        try:
            # 获取涨跌停数据
            today = datetime.now().strftime('%Y%m%d')
            
            # 涨停家数
            up_limit_df = self.pro.limit_list(
                trade_date=today,
                limit_type='U'
            )
            up_limit_count = len(up_limit_df) if not up_limit_df.empty else 0
            
            # 跌停家数
            down_limit_df = self.pro.limit_list(
                trade_date=today,
                limit_type='D'
            )
            down_limit_count = len(down_limit_df) if not down_limit_df.empty else 0
            
            # 上涨家数
            df = self.pro.daily(
                trade_date=today
            )
            up_count = len(df[df['pct_chg'] > 0]) if not df.empty else 2000
            down_count = len(df[df['pct_chg'] < 0]) if not df.empty else 2000
            
            # 计算市场情绪值
            sentiment = 50 + (up_count - down_count) / 80 + up_limit_count * 0.1
            sentiment = min(100, max(0, int(sentiment)))
            
            # 判断情绪周期
            if up_limit_count > 200 and up_count > 3500:
                phase = MarketPhase.高潮
            elif up_limit_count > 100 and up_count > 3000:
                phase = MarketPhase.回暖
            elif up_limit_count > 50 and up_count > 2500:
                phase = MarketPhase.复苏
            elif down_limit_count > 50 and up_count < 1500:
                phase = MarketPhase.冰点
            elif up_limit_count > 150 and up_count > 3200:
                phase = MarketPhase.过热
            else:
                phase = MarketPhase.退潮
            
            market_info = {
                "up_count": up_count,
                "down_count": down_count,
                "up_limit_count": up_limit_count,
                "down_limit_count": down_limit_count,
                "market_sentiment": sentiment
            }
            
            return phase, market_info
        
        except Exception as e:
            print(f"   获取市场情绪失败: {e}")
            return self.get_mock_market_sentiment()
    
    def get_mock_stock_list(self) -> List[Dict]:
        """获取模拟股票列表"""
        stocks = []
        for i in range(1, 51):
            code = f"{i:06d}"
            stocks.append({
                "code": code,
                "name": f"股票{code}"
            })
        return stocks
    
    def get_mock_market_sentiment(self) -> Tuple[MarketPhase, Dict]:
        """获取模拟市场情绪"""
        import random
        
        up_count = random.randint(1500, 3500)
        down_count = 4000 - up_count
        up_limit_count = random.randint(50, 200)
        down_limit_count = random.randint(10, 50)
        
        if up_limit_count > 150 and up_count > 3000:
            phase = MarketPhase.高潮
        elif up_limit_count > 80 and up_count > 2500:
            phase = MarketPhase.回暖
        elif up_limit_count > 40 and up_count > 2000:
            phase = MarketPhase.复苏
        elif down_limit_count > 50 and up_count < 1500:
            phase = MarketPhase.冰点
        elif up_limit_count > 120 and up_count > 2800:
            phase = MarketPhase.过热
        else:
            phase = MarketPhase.退潮
        
        market_info = {
            "up_count": up_count,
            "down_count": down_count,
            "up_limit_count": up_limit_count,
            "down_limit_count": down_limit_count,
            "market_sentiment": random.randint(40, 80)
        }
        
        return phase, market_info


class StockSelector:
    """股票评分器"""
    
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
        
        # 回调缩量
        if stock.volume_ratio < 0.8:
            pattern_score += 3
        score_breakdown["回调缩量"] = 3 if stock.volume_ratio < 0.8 else 0
        
        # 量价配合
        if stock.price_change > 0 and stock.volume_ratio > 1:
            pattern_score += 2
        score_breakdown["量价配合"] = 2 if stock.price_change > 0 and stock.volume_ratio > 1 else 0
        
        score_breakdown["形态完美"] = pattern_score
        
        # ==================== 条件五：筹码集中（10分） ====================
        if TURNOVER_RATE_MIN <= stock.turnover_rate <= TURNOVER_RATE_MAX:
            chip_score = 10
        else:
            chip_score = 5
        score_breakdown["筹码集中"] = chip_score
        
        # ==================== 条件六：量能健康（10分） ====================
        volume_score = 0
        
        if stock.volume_ratio > VOLUME_RATIO_BUY:
            volume_score += 5
        score_breakdown["量比>1.5"] = 5 if stock.volume_ratio > VOLUME_RATIO_BUY else 0
        
        if TURNOVER_RATE_MIN <= stock.turnover_rate <= TURNOVER_RATE_MAX:
            volume_score += 3
        score_breakdown["换手率3-15%"] = 3 if TURNOVER_RATE_MIN <= stock.turnover_rate <= TURNOVER_RATE_MAX else 0
        
        if stock.price_change > 0 and stock.volume_ratio > 1:
            volume_score += 2
        score_breakdown["量价健康"] = 2 if stock.price_change > 0 and stock.volume_ratio > 1 else 0
        
        score_breakdown["量能健康"] = volume_score
        
        # ==================== 条件七：分时强势（5分） ====================
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
        
        if total_score >= MIN_SCORE:
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
        elif total_score >= MIN_SCORE:
            position = "轻仓（20-30%）"
        else:
            position = "不参与"
        
        # ==================== 止损位 ====================
        stop_loss = stock.close * 0.95
        
        # ==================== 目标价 ====================
        target_price = stock.close * 1.10
        
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
    
    def __init__(self, token: str = None):
        self.data_fetcher = RealDataFetcher(token)
        self.selector = StockSelector()
        self.results: List[StockScore] = []
    
    def run(self, stock_count: int = 100) -> List[StockScore]:
        """运行选股模型"""
        print("="*80)
        print("小爪智能选股模型 v1.0（真实数据版）")
        print("="*80)
        print(f"数据来源: {'Tushare真实数据' if USE_REAL_DATA else '模拟数据'}")
        print(f"选股数量: {stock_count}")
        print(f"评分门槛: {MIN_SCORE}分（及格）/ {STRONG_SCORE}分（强烈）")
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
        stock_list = self.data_fetcher.get_all_stocks()[:stock_count]
        print(f"   待筛选股票: {len(stock_list)}只")
        print()
        
        # 3. 获取股票数据
        print("【3】获取股票数据...")
        valid_stocks = []
        
        for i, stock_info in enumerate(stock_list, 1):
            stock = self.data_fetcher.get_stock_data(stock_info["code"])
            if stock:
                stock.name = stock_info["name"]
                valid_stocks.append(stock)
            
            if i % 20 == 0 or i == len(stock_list):
                print(f"   已完成: {i}/{len(stock_list)} ({i*100//len(stock_list)}%)")
            
            # 避免请求过快
            if USE_REAL_DATA and i % 50 == 0:
                time.sleep(1)
        
        print(f"   有效股票: {len(valid_stocks)}只")
        print()
        
        # 4. 筛选评分
        print("【4】开始评分...")
        results = []
        
        for stock in valid_stocks:
            score = self.selector.calculate_score(stock, market, market_info)
            results.append(score)
        
        print(f"   评分完成: {len(results)}只")
        print()
        
        # 5. 排序筛选
        print("【5】排序筛选...")
        results.sort(key=lambda x: x.total_score, reverse=True)
        self.results = results
        print()
        
        # 6. 输出结果
        print("【6】选股结果")
        print("="*80)
        
        # 及格股票
        qualified = [r for r in results if r.total_score >= MIN_SCORE]
        print(f"\n✅ 及格股票（≥{MIN_SCORE}分）: {len(qualified)}只\n")
        
        if qualified:
            print("-"*80)
            print(f"{'排名':^4} {'代码':^10} {'名称':^12} {'收盘价':^10} {'涨跌幅':^10} {'量比':^8} {'总分':^6}")
            print("-"*80)
            
            for i, score in enumerate(qualified[:20], 1):
                print(f"{i:^4} {score.stock.code:^10} {score.stock.name:^12} "
                      f"{score.stock.close:^10.2f} {score.stock.price_change:^9.2f}% "
                      f"{score.stock.volume_ratio:^8.2f} {score.total_score:^6}")
        
        # 强烈推荐
        strong = [r for r in results if r.total_score >= STRONG_SCORE]
        print(f"\n🌟 强烈推荐（≥{STRONG_SCORE}分）: {len(strong)}只\n")
        
        if strong:
            print("-"*80)
            print(f"{'排名':^4} {'代码':^10} {'名称':^12} {'收盘价':^10} {'涨跌幅':^10} {'量比':^8} {'换手率':^10} {'目标价':^10}")
            print("-"*80)
            
            for i, score in enumerate(strong[:10], 1):
                print(f"{i:^4} {score.stock.code:^10} {score.stock.name:^12} "
                      f"{score.stock.close:^10.2f} {score.stock.price_change:^9.2f}% "
                      f"{score.stock.volume_ratio:^8.2f} {score.stock.turnover_rate:^9.2f}% "
                      f"{score.target_price:^10.2f}")
        
        # 7. 统计信息
        print("\n" + "="*80)
        print("【7】统计信息")
        print("="*80)
        print(f"总筛选股票: {len(results)}只")
        print(f"及格股票: {len(qualified)}只 ({len(qualified)*100//max(1,len(results))}%)")
        print(f"强烈推荐: {len(strong)}只 ({len(strong)*100//max(1,len(results))}%)")
        print(f"平均分: {sum(r.total_score for r in results)/max(1,len(results)):.1f}分")
        print(f"最高分: {results[0].total_score if results else 0}分")
        
        # 8. 买入建议
        if qualified:
            print("\n" + "="*80)
            print("【8】买入建议（TOP 5）")
            print("="*80)
            
            for i, score in enumerate(qualified[:5], 1):
                print(f"\n{i}. {score.stock.code} {score.stock.name}")
                print(f"   总分: {score.total_score}分")
                print(f"   当前价: {score.stock.close:.2f}元")
                print(f"   目标价: {score.target_price:.2f}元（+{((score.target_price-score.stock.close)/score.stock.close*100):.1f}%）")
                print(f"   止损位: {score.stop_loss:.2f}元（-{((score.stock.close-score.stop_loss)/score.stock.close*100):.1f}%）")
                print(f"   建议仓位: {score.position建议}")
                print(f"   买入时机: {score.buy_timing}")
        
        # 9. 保存结果
        self.save_results(qualified, strong)
        
        return qualified
    
    def save_results(self, qualified: List[StockScore], strong: List[StockScore]):
        """保存结果"""
        output_dir = "/home/admin/.openclaw/workspace/选股结果"
        os.makedirs(output_dir, exist_ok=True)
        
        today = datetime.now().strftime('%Y%m%d')
        
        # 保存及格股票
        with open(f"{output_dir}/及格股票_{today}.txt", "w", encoding='utf-8') as f:
            f.write("小爪智能选股结果\n")
            f.write("="*80 + "\n")
            f.write(f"日期: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"数据来源: {'Tushare真实数据' if USE_REAL_DATA else '模拟数据'}\n")
            f.write(f"评分门槛: {MIN_SCORE}分\n")
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
                f.write(f"   涨跌幅: {score.stock.price_change:.2f}%\n")
                f.write(f"   量比: {score.stock.volume_ratio:.2f}\n")
                f.write(f"   换手率: {score.stock.turnover_rate:.2f}%\n")
                f.write(f"   趋势: {score.stock.trend}\n")
                f.write(f"   均线多头: {'是' if score.stock.ma_multi else '否'}\n")
                f.write("\n")
        
        # 保存强烈推荐
        with open(f"{output_dir}/强烈推荐_{today}.txt", "w", encoding='utf-8') as f:
            f.write("小爪强烈推荐股票\n")
            f.write("="*80 + "\n")
            f.write(f"日期: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"评分门槛: {STRONG_SCORE}分\n")
            f.write("="*80 + "\n\n")
            
            for i, score in enumerate(strong, 1):
                f.write(f"{i}. {score.stock.code} {score.stock.name}\n")
                f.write(f"   总分: {score.total_score}分\n")
                f.write(f"   当前价: {score.stock.close:.2f}元\n")
                f.write(f"   目标价: {score.target_price:.2f}元\n")
                f.write(f"   止损位: {score.stop_loss:.2f}元\n")
                f.write(f"   建议仓位: {score.position建议}\n")
                f.write(f"   买入时机: {score.buy_timing}\n")
                f.write("\n")
        
        print(f"\n✅ 结果已保存到: {output_dir}/")
    
    def get_top_stocks(self, count: int = 5) -> List[StockScore]:
        """获取TOP股票"""
        if not self.results:
            self.run()
        
        return self.results[:count]


def main():
    """主函数"""
    # 创建选股模型（使用配置的Token）
    model = StockSelectionModel(TUSHARE_TOKEN)
    
    # 运行选股
    qualified = model.run(stock_count=100)
    
    # 获取TOP 5
    top5 = model.get_top_stocks(5)
    
    print("\n" + "="*80)
    print("选股完成！")
    print("="*80)
    print(f"共选出 {len(qualified)} 只及格股票")
    print(f"其中 {len([s for s in qualified if s.total_score >= STRONG_SCORE])} 只强烈推荐")
    
    if top5:
        print("\n最佳选择:")
        for i, score in enumerate(top5[:3], 1):
            print(f"  {i}. {score.stock.code} {score.stock.name} - {score.total_score}分 - 买入时机: {score.buy_timing}")
    
    return qualified


if __name__ == "__main__":
    main()
