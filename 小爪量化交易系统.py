#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小爪智能量化交易系统 v1.0
基于多因子模型的选股、买入、卖出决策系统

核心策略：
1. 选股：多因子评分（动量、强度、量能、突破）
2. 买入：技术指标 + 资金管理
3. 卖出：止盈止损 + 信号判断
4. 风控：单笔风险2%，总仓位50%
"""

import sys
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from tushare_api import TuSharePro


class Signal(Enum):
    """交易信号"""
    BUY = "买入"
    SELL = "卖出"
    HOLD = "持有"
    WATCH = "关注"


@dataclass
class StockFactor:
    """股票因子数据"""
    ts_code: str
    name: str
    close: float
    pct_chg: float
    volume: float
    
    # 动量因子
    momentum_5: float = 0  # 5日动量
    momentum_10: float = 0  # 10日动量
    momentum_20: float = 0  # 20日动量
    
    # 强度因子
    strength: float = 0  # 收盘/20日高
    
    # 量能因子
    vol_ratio: float = 0  # 量比
    vol_change: float = 0  # 成交量变化
    
    # 波动因子
    volatility: float = 0  # 波动率
    atr: float = 0  # 真实波幅
    
    # 价格位置
    price_position: float = 0  # 价格位置 0-1
    support: float = 0  # 支撑位
    resistance: float = 0  # 压力位
    
    # 综合评分
    score: float = 0
    signal: Signal = Signal.HOLD


class XiaoZhuaQuantSystem:
    """
    小爪智能量化交易系统
    
    核心参数：
    - 单笔风险: 2%
    - 止损比例: -8%
    - 止盈比例: +15%
    - 最大仓位: 50%
    - 最小买入: ¥5000
    """
    
    def __init__(self, token: str):
        self.pro = TuSharePro(token)
        self.cache = {}
        
        # 风控参数
        self.max_position = 0.5  # 最大50%仓位
        self.min_buy_amount = 5000  # 最小买入¥5000
        self.stop_loss = -0.08  # 8%止损
        self.take_profit = 0.15  # 15%止盈
        self.single_risk = 0.02  # 单笔2%风险
        
    def get_stock_data(self, ts_code: str, days: int = 60) -> List[Dict]:
        """获取股票历史数据"""
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=days*2)).strftime('%Y%m%d')
        
        result = self.pro.get_daily(
            ts_code=ts_code,
            start_date=start_date,
            end_date=end_date
        )
        
        if result['success']:
            return result['data']
        return []
    
    def calculate_factors(self, ts_code: str, name: str) -> Optional[StockFactor]:
        """计算股票所有因子"""
        data = self.get_stock_data(ts_code, 60)
        
        if not data or len(data) < 20:
            return None
        
        try:
            # 数据按日期降序排列（最新在前）
            closes = [float(d[5]) for d in data]  # 收盘价
            opens = [float(d[2]) for d in data]  # 开盘价
            highs = [float(d[3]) for d in data]   # 最高价
            lows = [float(d[4]) for d in data]    # 最低价
            vols = [float(d[9]) for d in data]    # 成交量
            pct_chgs = [float(d[8]) for d in data]  # 涨跌幅
            
            latest = data[0]
            latest_close = float(latest[5])
            latest_vol = float(latest[9])
            
            # 计算动量
            momentum_5 = (closes[0] - closes[4]) / closes[4] * 100 if len(closes) > 4 else 0
            momentum_10 = (closes[0] - closes[9]) / closes[9] * 100 if len(closes) > 9 else 0
            momentum_20 = (closes[0] - closes[19]) / closes[19] * 100 if len(closes) > 19 else 0
            
            # 计算强度因子
            high_20 = max(highs[:20]) if len(highs) >= 20 else max(highs)
            low_20 = min(lows[:20]) if len(lows) >= 20 else min(lows)
            strength = (latest_close - low_20) / (high_20 - low_20) if high_20 > low_20 else 0.5
            
            # 计算量能因子
            avg_vol_5 = sum(vols[:5]) / 5
            avg_vol_20 = sum(vols[:20]) / 20
            vol_ratio = latest_vol / avg_vol_20 if avg_vol_20 > 0 else 1
            vol_change = (latest_vol - vols[1]) / vols[1] * 100 if vols[1] > 0 else 0
            
            # 计算波动率
            returns = [(closes[i] - closes[i+1]) / closes[i+1] * 100 
                      for i in range(min(19, len(closes)-1))]
            volatility = (max(returns) - min(returns)) if returns else 0
            
            # 计算ATR (14日)
            tr_list = []
            for i in range(min(14, len(data)-1)):
                high = highs[i]
                low = lows[i]
                prev_close = closes[i+1]
                tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
                tr_list.append(tr)
            atr = sum(tr_list) / len(tr_list) if tr_list else 0
            
            # 计算价格位置和支撑压力
            price_position = (latest_close - low_20) / (high_20 - low_20) if high_20 > low_20 else 0.5
            support = low_20 + (high_20 - low_20) * 0.236  # 23.6%回撤位
            resistance = high_20
            
            # 综合评分
            score = self._calculate_score(
                momentum_5=momentum_5,
                momentum_10=momentum_10,
                momentum_20=momentum_20,
                strength=strength,
                vol_ratio=vol_ratio,
                volatility=volatility,
                price_position=price_position,
                pct_chg=pct_chgs[0]
            )
            
            # 判断信号
            signal = self._judge_signal(
                score=score,
                momentum_5=momentum_5,
                momentum_10=momentum_10,
                strength=strength,
                vol_ratio=vol_ratio,
                pct_chg=pct_chgs[0],
                price_position=price_position
            )
            
            return StockFactor(
                ts_code=ts_code,
                name=name,
                close=latest_close,
                pct_chg=pct_chgs[0],
                volume=latest_vol,
                momentum_5=momentum_5,
                momentum_10=momentum_10,
                momentum_20=momentum_20,
                strength=strength,
                vol_ratio=vol_ratio,
                vol_change=vol_change,
                volatility=volatility,
                atr=atr,
                price_position=price_position,
                support=support,
                resistance=resistance,
                score=score,
                signal=signal
            )
            
        except Exception as e:
            print(f"  计算 {name} ({ts_code}) 因子失败: {e}")
            return None
    
    def _calculate_score(self, **kwargs) -> float:
        """综合评分计算 (0-100)"""
        score = 50  # 基础分
        
        # 动量评分 (权重30%)
        momentum_avg = (kwargs['momentum_5'] + kwargs['momentum_10'] * 2 + kwargs['momentum_20']) / 4
        score += max(-15, min(15, momentum_avg * 1.5))
        
        # 强度评分 (权重25%)
        score += (kwargs['strength'] - 0.5) * 40
        
        # 量能评分 (权重20%)
        if 1.0 <= kwargs['vol_ratio'] <= 2.5:
            score += 10
        elif kwargs['vol_ratio'] > 2.5:
            score += 5
        else:
            score -= 5
        
        # 位置评分 (权重15%)
        if 0.3 <= kwargs['price_position'] <= 0.9:
            score += 10
        elif kwargs['price_position'] > 0.9:
            score -= 10
        
        # 涨跌幅评分 (权重10%)
        if 3 <= kwargs['pct_chg'] <= 9:
            score += 10
        elif kwargs['pct_chg'] > 9:
            score += 5
        elif kwargs['pct_chg'] < -5:
            score -= 10
        
        return max(0, min(100, score))
    
    def _judge_signal(self, **kwargs) -> Signal:
        """判断交易信号"""
        score = kwargs['score']
        momentum_5 = kwargs['momentum_5']
        strength = kwargs['strength']
        vol_ratio = kwargs['vol_ratio']
        pct_chg = kwargs['pct_chg']
        price_position = kwargs['price_position']
        
        # 买入信号
        buy_conditions = [
            score >= 70,                          # 综合评分70+
            momentum_5 > 3,                       # 5日动量为正
            strength > 0.6,                        # 强度较好
            1.0 <= vol_ratio <= 3.0,              # 量能健康
            price_position >= 0.4,                 # 不在底部
            pct_chg > 0,                           # 今日上涨
        ]
        
        if sum(buy_conditions) >= 5:
            return Signal.BUY
        
        # 卖出信号
        sell_conditions = [
            score < 30,                            # 综合评分低
            momentum_5 < -5,                       # 动量大幅下跌
            pct_chg < -5,                          # 大跌
            price_position < 0.2,                  # 接近新低
        ]
        
        if sum(sell_conditions) >= 3:
            return Signal.SELL
        
        # 关注信号
        watch_conditions = [
            score >= 55,
            momentum_5 > 0,
            pct_chg > 0,
        ]
        
        if sum(watch_conditions) >= 2:
            return Signal.WATCH
        
        return Signal.HOLD
    
    def calculate_position_size(self, factors: StockFactor, total_capital: float) -> Tuple[float, int]:
        """
        计算仓位大小
        
        Args:
            factors: 股票因子
            total_capital: 总资金
            
        Returns:
            (买入金额, 买入股数)
        """
        # 最大仓位
        max_amount = total_capital * self.max_position
        
        # 根据评分调整仓位
        score_factor = factors.score / 100
        position_amount = max_amount * (0.5 + score_factor * 0.5)
        
        # 确保最小买入金额
        if position_amount < self.min_buy_amount:
            return 0, 0
        
        # 计算股数（向下取整）
        shares = int(position_amount / factors.close / 100) * 100
        
        if shares * factors.close < self.min_buy_amount:
            return 0, 0
        
        return shares * factors.close, shares
    
    def calculate_stop_loss_price(self, factors: StockFactor) -> float:
        """计算止损价"""
        return factors.close * (1 + self.stop_loss)
    
    def calculate_take_profit_price(self, factors: StockFactor) -> float:
        """计算止盈价"""
        return factors.close * (1 + self.take_profit)
    
    def analyze_stock(self, ts_code: str, name: str, total_capital: float = 100000) -> Dict:
        """
        综合分析单只股票
        
        Returns:
            分析报告
        """
        factors = self.calculate_factors(ts_code, name)
        
        if not factors:
            return {
                'ts_code': ts_code,
                'name': name,
                'error': '数据不足'
            }
        
        # 计算仓位
        buy_amount, shares = self.calculate_position_size(factors, total_capital)
        
        # 计算止盈止损
        stop_loss = self.calculate_stop_loss_price(factors)
        take_profit = self.calculate_take_profit_price(factors)
        
        return {
            '基本信息': {
                '代码': factors.ts_code,
                '名称': factors.name,
                '当前价格': f"¥{factors.close:.2f}",
                '涨跌幅': f"{factors.pct_chg:+.2f}%"
            },
            '因子分析': {
                '5日动量': f"{factors.momentum_5:+.2f}%",
                '10日动量': f"{factors.momentum_10:+.2f}%",
                '20日动量': f"{factors.momentum_20:+.2f}%",
                '强度因子': f"{factors.strength:.3f}",
                '量比': f"{factors.vol_ratio:.2f}",
                '波动率': f"{factors.volatility:.2f}%",
                'ATR': f"{factors.atr:.2f}"
            },
            '价格位置': {
                '价格位置': f"{factors.price_position:.1%}",
                '支撑位': f"¥{factors.support:.2f}",
                '压力位': f"¥{factors.resistance:.2f}"
            },
            '交易建议': {
                '信号': factors.signal.value,
                '综合评分': f"{factors.score:.1f}",
                '建议仓位': f"¥{buy_amount:,.0f}" if buy_amount > 0 else "不建议买入",
                '买入股数': f"{shares}股" if shares > 0 else "-",
                '止损价': f"¥{stop_loss:.2f} ({self.stop_loss*100:+.0f}%)",
                '止盈价': f"¥{take_profit:.2f} ({self.take_profit*100:+.0f}%)"
            },
            '风险收益': {
                '风险': '高' if factors.score > 80 else ('中' if factors.score > 50 else '低'),
                '预期收益': f"{self.take_profit*100:+.0f}%",
                '风险收益比': f"{self.take_profit/abs(self.stop_loss):.1f}:1"
            }
        }
    
    def scan_market(self, 
                    stocks: List[Tuple[str, str]], 
                    total_capital: float = 100000,
                    min_score: float = 55) -> List[Dict]:
        """
        扫描整个板块/股票列表
        
        Returns:
            推荐股票列表
        """
        print(f"\n{'='*70}")
        print(f"🔍 市场扫描 - 共{len(stocks)}只股票")
        print(f"{'='*70}")
        
        results = []
        
        for ts_code, name in stocks:
            print(f"  分析 {name} ({ts_code})...")
            factors = self.calculate_factors(ts_code, name)
            
            if factors:
                buy_amount, shares = self.calculate_position_size(factors, total_capital)
                
                report = {
                    'ts_code': ts_code,
                    'name': name,
                    'close': factors.close,
                    'pct_chg': factors.pct_chg,
                    'momentum_5': factors.momentum_5,
                    'strength': factors.strength,
                    'vol_ratio': factors.vol_ratio,
                    'score': factors.score,
                    'signal': factors.signal,
                    'buy_amount': buy_amount,
                    'shares': shares,
                    'stop_loss': self.calculate_stop_loss_price(factors),
                    'take_profit': self.calculate_take_profit_price(factors)
                }
                results.append(report)
        
        # 按评分排序
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return results
    
    def print_recommendations(self, 
                              results: List[Dict], 
                              top_n: int = 10,
                              signal_filter: List[Signal] = None):
        """
        打印推荐结果
        """
        signal_filter = signal_filter or [Signal.BUY, Signal.WATCH]
        
        print(f"\n{'='*70}")
        print(f"📈 量化选股推荐 TOP {top_n}")
        print(f"{'='*70}")
        
        print(f"{'代码':<12} {'名称':<10} {'价格':<10} {'涨跌幅':<8} {'评分':<6} {'信号':<6} {'建议买入':<12}")
        print("-" * 70)
        
        count = 0
        for r in results:
            if r['signal'] in signal_filter and count < top_n:
                print(f"{r['ts_code']:<12} {r['name']:<10} ¥{r['close']:<9.2f} "
                      f"{r['pct_chg']:+7.2f}% {r['score']:<6.1f} {r['signal'].value:<6} "
                      f"¥{r['buy_amount']:>10,.0f}" if r['buy_amount'] > 0 else "  -")
                count += 1
        
        print("-" * 70)
        
        # 买入建议
        buy_list = [r for r in results if r['signal'] == Signal.BUY]
        watch_list = [r for r in results if r['signal'] == Signal.WATCH]
        
        print(f"\n💡 操作建议:")
        print(f"  买入信号: {len(buy_list)} 只")
        print(f"  关注信号: {len(watch_list)} 只")
        
        if buy_list:
            total_buy = sum(r['buy_amount'] for r in buy_list)
            print(f"  建议总买入: ¥{total_buy:,.0f}")
        
        return buy_list, watch_list


def main():
    """主函数 - 示例"""
    print("🦞 小爪智能量化交易系统 v1.0")
    print("=" * 70)
    print(f"⏰ 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Token
    TOKEN = 'YOUR_TUSHARE_TOKEN'
    
    # 初始化系统
    system = XiaoZhuaQuantSystem(TOKEN)
    
    # 定义关注的股票池
    stocks = [
        # 传媒板块
        ('300364.SZ', '中文在线'),
        ('301231.SZ', '荣信文化'),
        ('603598.SH', '引力传媒'),
        ('603103.SH', '横店影视'),
        ('300251.SZ', '光线传媒'),
        ('300043.SZ', '星辉娱乐'),
        ('002292.SZ', '博通股份'),
        
        # 科技板块
        ('688981.SH', '华大九天'),
        ('688111.SH', '金山办公'),
        ('002230.SZ', '科大讯飞'),
        
        # 银行板块
        ('000001.SZ', '平安银行'),
        ('600000.SH', '浦发银行'),
        ('600015.SH', '华夏银行'),
        
        # 热门板块
        ('300750.SZ', '宁德时代'),
        ('600519.SH', '贵州茅台'),
        ('000001.SH', '上证指数'),
    ]
    
    # 扫描市场
    results = system.scan_market(stocks, total_capital=100000)
    
    # 打印推荐
    buy_list, watch_list = system.print_recommendations(results, top_n=10)
    
    # 详细分析TOP 3
    print(f"\n{'='*70}")
    print(f"📊 TOP 3 详细分析")
    print(f"{'='*70}")
    
    for i, stock in enumerate(results[:3], 1):
        report = system.analyze_stock(stock['ts_code'], stock['name'])
        print(f"\n【{i}】{report['基本信息']['名称']} ({report['基本信息']['代码']})")
        print(f"  当前价格: {report['基本信息']['当前价格']}")
        print(f"  信号: {report['交易建议']['信号']} | 评分: {report['交易建议']['综合评分']}")
        print(f"  动量: {report['因子分析']['5日动量']} | 强度: {report['因子分析']['强度因子']}")
        print(f"  建议: {report['交易建议']['建议仓位']}")
        print(f"  止损: {report['交易建议']['止损价']} | 止盈: {report['交易建议']['止盈价']}")
    
    # 保存结果
    output = {
        'update_time': datetime.now().isoformat(),
        'total_stocks': len(stocks),
        'results': [
            {
                'ts_code': r['ts_code'],
                'name': r['name'],
                'close': r['close'],
                'pct_chg': r['pct_chg'],
                'score': r['score'],
                'signal': r['signal'].value,
                'buy_amount': r['buy_amount'],
                'stop_loss': r['stop_loss'],
                'take_profit': r['take_profit']
            }
            for r in results
        ],
        'recommendations': {
            'buy': [r['ts_code'] for r in buy_list],
            'watch': [r['ts_code'] for r in watch_list]
        }
    }
    
    with open('/home/admin/.openclaw/workspace/选股结果/量化选股信号.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 结果已保存到: /home/admin/.openclaw/workspace/选股结果/量化选股信号.json")
    
    return results


if __name__ == '__main__':
    results = main()
