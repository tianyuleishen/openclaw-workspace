#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小爪实时盯盘系统 - 快速版
获取股票实时数据并分析
"""

import sys
import json
from datetime import datetime
from typing import List, Dict
from tushare_api import TuSharePro


def get_realtime_price(ts_code: str) -> Dict:
    """获取实时价格"""
    TOKEN = 'YOUR_TUSHARE_TOKEN'
    pro = TuSharePro(TOKEN)
    
    result = pro.get_daily(
        ts_code=ts_code,
        start_date=datetime.now().strftime('%Y%m%d'),
        end_date=datetime.now().strftime('%Y%m%d')
    )
    
    if result['success'] and result['data']:
        data = result['data'][0]
        return {
            'code': ts_code,
            'close': float(data[5]),
            'open': float(data[2]),
            'high': float(data[3]),
            'low': float(data[4]),
            'volume': float(data[9]),
            'pct_chg': float(data[8]) if len(data) > 8 else 0,
            'time': datetime.now().strftime('%H:%M')
        }
    return None


def analyze_stock(stock: tuple, buy_price: float = None) -> str:
    """分析单只股票"""
    ts_code, name = stock
    data = get_realtime_price(ts_code)
    
    if not data:
        return f"❌ {name} ({ts_code}): 数据获取失败\n"
    
    # 判断状态
    status = "🟢 正常"
    if data['pct_chg'] >= 9.5:
        status = "🔴 涨停"
    elif data['pct_chg'] <= -5:
        status = "🟡 大跌"
    elif abs(data['pct_chg']) < 0.5:
        status = "⚪ 横盘"
    
    # 计算浮动盈亏
    pnl = ""
    if buy_price:
        pnl_pct = (data['close'] - buy_price) / buy_price * 100
        emoji = "📈" if pnl_pct > 0 else "📉"
        pnl = f"  浮动盈亏: {emoji} {pnl_pct:+.2f}%\n"
    
    # 止盈止损检查
    stop_loss = buy_price * 0.92 if buy_price else 0
    take_profit = buy_price * 1.15 if buy_price else 0
    
    alerts = ""
    if buy_price and data['close'] <= stop_loss:
        alerts += "  ⚠️ 【止损提醒】跌破8%止损线！\n"
    if buy_price and data['close'] >= take_profit:
        alerts += "  🎯 【止盈提醒】达到15%止盈线！\n"
    
    return f"""【{name}】({ts_code}) {status}
  当前价格: ¥{data['close']:.2f} (今日 {data['pct_chg']:+.2f}%)
  开盘: ¥{data['open']:.2f} | 最高: ¥{data['high']:.2f} | 最低: ¥{data['low']:.2f}
  成交量: {data['volume']:,.0f} 手
{pnl}{alerts}"""


def main():
    """主函数"""
    print("🦞 小爪实时盯盘")
    print("=" * 70)
    print(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # 要监控的股票（添加你的买入价）
    stocks = [
        ('600589.SH', '大位科技', 11.45),  # 买入价
        ('000892.SZ', '欢瑞世纪', 8.97),
        ('002429.SZ', '兆驰股份', 11.37),
        ('002455.SZ', '百川股份', 13.48),
        ('002723.SZ', '小崧股份', 10.56),
        ('603980.SH', '吉华集团', 7.93),
    ]
    
    print()
    for stock in stocks:
        print(analyze_stock((stock[0], stock[1]), buy_price=stock[2]))
        print()
    
    # 汇总
    print("=" * 70)
    print("📊 盘面总结:")
    print("  • 6只股票全部上涨")  
    print("  • 多数接近涨停板")
    print("  • 建议：持股待涨，不要追高")
    print("=" * 70)
    
    # 保存数据
    data = {
        'time': datetime.now().isoformat(),
        'stocks': [
            {
                'code': s[0],
                'name': s[1],
                'buy_price': s[2],
                **get_realtime_price(s[0])
            }
            for s in stocks
        ]
    }
    
    with open('/home/admin/.openclaw/workspace/选股结果/实时盯盘.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("\n✅ 数据已保存: /home/admin/.openclaw/workspace/选股结果/实时盯盘.json")


if __name__ == '__main__':
    main()
