#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小爪智能选股系统 - TuShare Pro真实数据版
基于TuShare Pro API获取真实A股数据

功能：
- 获取真实股票日线行情
- 多因子选股策略
- 涨停股票分析
- 传媒板块重点关注
"""

import sys
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from tushare_api import TuSharePro


class XiaoZhuaStockSelector:
    """小爪智能选股系统"""
    
    def __init__(self, token: str):
        """初始化"""
        self.pro = TuSharePro(token)
        self.cache = {}
        
    def get_stock_daily(self, ts_code: str, days: int = 30) -> List[Dict]:
        """
        获取股票日线数据
        
        Args:
            ts_code: 股票代码
            days: 获取天数
            
        Returns:
            日线数据列表
        """
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
    
    def calculate_factors(self, ts_code: str, name: str) -> Optional[Dict]:
        """
        计算股票多因子得分
        
        Args:
            ts_code: 股票代码
            name: 股票名称
            
        Returns:
            因子分析结果
        """
        daily_data = self.get_stock_daily(ts_code, 30)
        
        if not daily_data or len(daily_data) < 5:
            return None
        
        try:
            # 解析数据
            data = daily_data  # 已经是列表格式
            
            # 提取关键数据
            closes = [float(d[5]) for d in data]  # 收盘价
            opens = [float(d[2]) for d in data]    # 开盘价
            highs = [float(d[3]) for d in data]    # 最高价
            lows = [float(d[4]) for d in data]     # 最低价
            vols = [float(d[9]) for d in data]     # 成交量
            
            # 最新数据
            latest = data[0]
            latest_close = float(latest[5])
            latest_vol = float(latest[9])
            
            # 因子计算
            # 1. 动量因子 (20日涨幅)
            if len(closes) >= 20:
                momentum = (closes[0] - closes[19]) / closes[19] * 100
            elif len(closes) >= 10:
                momentum = (closes[0] - closes[9]) / closes[9] * 100
            else:
                momentum = 0
            
            # 2. 波动率因子 (10日标准差)
            if len(closes) >= 10:
                import statistics
                returns = [(closes[i] - closes[i+1]) / closes[i+1] * 100 
                          for i in range(min(9, len(closes)-1))]
                volatility = statistics.stdev(returns) if len(returns) > 1 else 0
            else:
                volatility = 0
            
            # 3. 量价因子 (放量/缩量)
            avg_vol = sum(vols[:10]) / min(10, len(vols))
            vol_ratio = latest_vol / avg_vol if avg_vol > 0 else 1
            
            # 4. 强度因子 (收盘价/最高价比率)
            avg_high = sum(highs[:5]) / min(5, len(highs))
            strength = latest_close / avg_high if avg_high > 0 else 0.5
            
            # 5. 涨跌因子
            pct_chg = float(latest[8]) if len(latest) > 8 else 0
            
            # 综合评分 (满分100)
            score = 50  # 基础分
            
            # 动量加分 (范围-20到+20)
            score += max(-20, min(20, momentum * 2))
            
            # 波动率加分 (适度的波动性好)
            score += max(-10, min(10, (volatility - 2) * 3))
            
            # 量能加分 (放量好)
            if 1.0 <= vol_ratio <= 2.0:
                score += 5
            elif vol_ratio > 2.0:
                score += 10
            elif vol_ratio < 0.5:
                score -= 5
            
            # 强度加分
            score += (strength - 0.8) * 50
            
            # 今日涨跌
            if pct_chg > 5:
                score += 10
            elif pct_chg > 3:
                score += 5
            elif pct_chg > 0:
                score += 2
            elif pct_chg < -5:
                score -= 10
            
            return {
                'ts_code': ts_code,
                'name': name,
                'close': latest_close,
                'pct_chg': pct_chg,
                'volume': latest_vol,
                'momentum': round(momentum, 2),
                'volatility': round(volatility, 2),
                'vol_ratio': round(vol_ratio, 2),
                'strength': round(strength, 3),
                'score': round(max(0, min(100, score)), 1),
                'data_count': len(daily_data)
            }
            
        except Exception as e:
            print(f"  计算 {name} ({ts_code}) 因子失败: {e}")
            return None
    
    def analyze_sector(self, sector_name: str, stocks: List[tuple]) -> List[Dict]:
        """
        分析行业板块
        
        Args:
            sector_name: 板块名称
            stocks: 股票列表 [(ts_code, name), ...]
            
        Returns:
            排序后的分析结果
        """
        print(f"\n{'='*60}")
        print(f"📊 {sector_name}板块分析")
        print(f"{'='*60}")
        
        results = []
        for ts_code, name in stocks:
            print(f"  分析 {name} ({ts_code})...")
            factors = self.calculate_factors(ts_code, name)
            if factors:
                results.append(factors)
        
        # 按综合评分排序
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return results
    
    def print_results(self, results: List[Dict], top_n: int = 10):
        """
        打印分析结果
        """
        print(f"\n🏆 TOP {min(top_n, len(results))} 股票")
        print("-" * 80)
        print(f"{'排名':<4} {'代码':<12} {'名称':<10} {'收盘价':<10} {'涨幅%':<8} {'动量%':<8} {'评分':<8}")
        print("-" * 80)
        
        for i, r in enumerate(results[:top_n], 1):
            print(f"{i:<4} {r['ts_code']:<12} {r['name']:<10} {r['close']:<10.2f} "
                  f"{r['pct_chg']:<8.2f} {r['momentum']:<8.2f} {r['score']:<8.1f}")
        
        print("-" * 80)
        print(f"\n💡 评分说明:")
        print("  - 动量因子: 近期涨幅趋势")
        print("  - 波动率: 价格波动程度")
        print("  - 量比: 今日量能相对于近期平均水平")
        print("  - 强度: 收盘价相对于近期高点的比率")


def main():
    """主函数"""
    print("🦞 小爪智能选股系统 - TuShare Pro真实数据版")
    print("=" * 60)
    print(f"⏰ 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Token
    TOKEN = 'YOUR_TUSHARE_TOKEN'
    
    # 初始化选股系统
    selector = XiaoZhuaStockSelector(TOKEN)
    
    # 定义关注的板块和股票
    sectors = {
        '📰 传媒板块': [
            ('300364.SZ', '中文在线'),
            ('301231.SZ', '荣信文化'),
            ('603598.SH', '引力传媒'),
            ('603103.SH', '横店影视'),
            ('300251.SZ', '光线传媒'),
            ('300528.SZ', '金溢科技'),
            ('002292.SZ', '博通股份'),
            ('300043.SZ', '星辉娱乐'),
        ],
        '💻 科技板块': [
            ('688981.SH', '华大九天'),
            ('688111.SH', '金山办公'),
            ('002230.SZ', '科大讯飞'),
            ('300364.SZ', '中文在线'),  # 重复计入传媒
        ],
        '🏦 银行板块': [
            ('000001.SZ', '平安银行'),
            ('600000.SH', '浦发银行'),
            ('600015.SH', '华夏银行'),
        ]
    }
    
    # 分析每个板块
    all_results = []
    
    for sector_name, stocks in sectors.items():
        results = selector.analyze_sector(sector_name, stocks)
        all_results.extend(results)
        
        # 打印板块TOP5
        if results:
            selector.print_results(results, top_n=5)
    
    # 全市场TOP10
    if all_results:
        all_results.sort(key=lambda x: x['score'], reverse=True)
        print(f"\n{'='*60}")
        print(f"🌟 全市场综合TOP 10")
        print(f"{'='*60}")
        selector.print_results(all_results, top_n=10)
    
    # 保存结果
    output_file = '/home/admin/.openclaw/workspace/选股结果/小爪选股_真实数据.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'update_time': datetime.now().isoformat(),
            'results': all_results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 结果已保存到: {output_file}")
    
    return all_results


if __name__ == '__main__':
    results = main()
