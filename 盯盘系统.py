#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小爪实时盯盘系统 v1.0
实时监控股票走势，自动发送提醒

功能：
- 每5分钟自动获取最新数据
- 监测价格异动、成交量变化
- 达到止盈/止损条件时自动提醒
- 监测开板、炸板等特殊情况
"""

import sys
import time
import json
import subprocess
from datetime import datetime, timedelta
from typing import List, Dict
from tushare_api import TuSharePro


class StockMonitor:
    """股票实时监控器"""
    
    def __init__(self, token: str, stocks: List[tuple]):
        """
        初始化
        
        Args:
            token: TuShare Token
            stocks: 股票列表 [(ts_code, name), ...]
        """
        self.pro = TuSharePro(token)
        self.stocks = stocks
        self.last_data = {}  # 上次数据
        
        # 监控参数
        self.check_interval = 300  # 5分钟检查一次
        self.price_alert_threshold = 0.02  # 价格波动2%提醒
        self.volume_alert_ratio = 2.0  # 量比2倍提醒
        
        # 记录文件
        self.log_file = '/home/admin/.openclaw/workspace/选股结果/盯盘日志.txt'
        self.data_file = '/home/admin/.openclaw/workspace/选股结果/盯盘数据.json'
        
    def get_realtime_data(self, ts_code: str) -> Dict:
        """获取实时数据"""
        result = self.pro.get_daily(
            ts_code=ts_code,
            start_date=datetime.now().strftime('%Y%m%d'),
            end_date=datetime.now().strftime('%Y%m%d')
        )
        
        if result['success'] and result['data']:
            data = result['data'][0]
            return {
                'close': float(data[5]),
                'open': float(data[2]),
                'high': float(data[3]),
                'low': float(data[4]),
                'volume': float(data[9]),
                'pct_chg': float(data[8]) if len(data) > 8 else 0,
                'amount': float(data[10]) if len(data) > 10 else 0,
                'time': datetime.now().strftime('%H:%M:%S')
            }
        return None
    
    def analyze_change(self, ts_code: str, name: str, current: Dict) -> List[str]:
        """分析变化，返回提醒列表"""
        alerts = []
        
        if ts_code not in self.last_data:
            self.last_data[ts_code] = current
            return ["【首次监控】" + name]
        
        last = self.last_data[ts_code]
        price_change = (current['close'] - last['close']) / last['close']
        
        # 价格波动提醒
        if abs(price_change) >= self.price_alert_threshold:
            direction = "上涨" if price_change > 0 else "下跌"
            alerts.append(f"【价格异动】{name} {direction} {price_change*100:.2f}%")
        
        # 量能变化提醒
        if last['volume'] > 0:
            volume_ratio = current['volume'] / last['volume']
            if volume_ratio >= self.volume_alert_ratio:
                alerts.append(f("【放量】{name} 量比 {volume_ratio:.1f}倍"))
        
        # 涨停监测
        if current['pct_chg'] >= 9.5 and last['pct_chg'] < 9.5:
            alerts.append(f"【涨停】{name} 接近涨停！当前涨幅 {current['pct_chg']:.2f}%")
        
        # 炸板监测（从涨停板跌落）
        if last['pct_chg'] >= 9.5 and current['pct_chg'] < 9.0:
            alerts.append(f"【炸板】{name} 从涨停板跌落！当前 {current['pct_chg']:.2f}%")
        
        # 更新数据
        self.last_data[ts_code] = current
        
        return alerts
    
    def check_price_level(self, ts_code: str, name: str, buy_price: float, 
                         current_price: float) -> List[str]:
        """检查止盈止损价位"""
        alerts = []
        
        # 止损检查 (-8%)
        stop_loss = buy_price * 0.92
        if current_price <= stop_loss:
            alerts.append(f"【⚠️ 止损提醒】{name} 当前 ¥{current_price:.2f}，跌破止损价 ¥{stop_loss:.2f}")
        
        # 止盈检查 (+15%)
        take_profit = buy_price * 1.15
        if current_price >= take_profit:
            alerts.append(f"【🎯 止盈提醒】{name} 当前 ¥{current_price:.2f}，达到止盈价 ¥{take_profit:.2f}")
        
        return alerts
    
    def monitor_once(self) -> str:
        """执行一次监控，返回监控报告"""
        report = []
        report.append(f"\n{'='*70}")
        report.append(f"⏰ 盯盘时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"{'='*70}")
        
        all_alerts = []
        stock_data = {}
        
        for ts_code, name in self.stocks:
            print(f"  监控 {name} ({ts_code})...")
            current = self.get_realtime_data(ts_code)
            
            if current:
                stock_data[ts_code] = current
                alerts = self.analyze_change(ts_code, name, current)
                all_alerts.extend(alerts)
                
                # 记录当前状态
                pct_emoji = "📈" if current['pct_chg'] > 0 else "📉"
                report.append(f"\n{name} ({ts_code})")
                report.append(f"  当前价格: ¥{current['close']:.2f} {pct_emoji} {current['pct_chg']:+.2f}%")
                report.append(f"  开盘: ¥{current['open']:.2f} | 最高: ¥{current['high']:.2f} | 最低: ¥{current['low']:.2f}")
                report.append(f"  成交量: {current['volume']:,.0f} 手")
        
        # 保存数据
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump({
                'time': datetime.now().isoformat(),
                'data': stock_data
            }, f, ensure_ascii=False, indent=2)
        
        # 输出提醒
        if all_alerts:
            report.append(f"\n{'='*70}")
            report.append("🚨 重要提醒:")
            report.append("="*70)
            for alert in all_alerts:
                report.append(f"  • {alert}")
        
        return '\n'.join(report)
    
    def save_log(self, content: str):
        """保存日志"""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(content + '\n')
    
    def run_monitor(self, duration_minutes: int = 60):
        """
        运行持续监控
        
        Args:
            duration_minutes: 监控时长（分钟）
        """
        print("🦞 小爪实时盯盘系统启动")
        print(f"  监控股票: {len(self.stocks)} 只")
        print(f"  监控时长: {duration_minutes} 分钟")
        print(f"  检查间隔: {self.check_interval} 秒")
        print()
        
        # 计算循环次数
        loop_count = int(duration_minutes * 60 / self.check_interval)
        
        start_time = datetime.now()
        
        for i in range(loop_count):
            print(f"\n[{i+1}/{loop_count}] 执行监控...")
            
            report = self.monitor_once()
            self.save_log(report)
            print(report)
            
            # 等待下次检查
            if i < loop_count - 1:
                time.sleep(self.check_interval)
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        print(f"\n{'='*70}")
        print(f"✅ 盯盘完成！")
        print(f"  总时长: {duration}")
        print(f"  监控次数: {loop_count}")
        print(f"  日志文件: {self.log_file}")
        print(f"{'='*70}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='小爪实时盯盘系统')
    parser.add_argument('--duration', type=int, default=60, help='监控时长（分钟）')
    parser.add_argument('--stocks', type=str, default='', help='股票代码，逗号分隔')
    
    args = parser.parse_args()
    
    # 默认监控股票
    default_stocks = [
        ('600589.SH', '大位科技'),
        ('000892.SZ', '欢瑞世纪'),
        ('002429.SZ', '兆驰股份'),
        ('002455.SZ', '百川股份'),
        ('002723.SZ', '小崧股份'),
        ('603980.SH', '吉华集团'),
    ]
    
    if args.stocks:
        # 解析用户输入
        stock_codes = args.stocks.split(',')
        stocks = []
        for code in stock_codes:
            code = code.strip()
            if code:
                ts_code = code + ('.SZ' if code.startswith('00') or code.startswith('30') else '.SH')
                stocks.append((ts_code, code))
    else:
        stocks = default_stocks
    
    # Token
    TOKEN = 'YOUR_TUSHARE_TOKEN'
    
    # 创建监控器并运行
    monitor = StockMonitor(TOKEN, stocks)
    monitor.run_monitor(duration_minutes=args.duration)


if __name__ == '__main__':
    main()
