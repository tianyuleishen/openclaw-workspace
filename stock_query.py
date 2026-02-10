#!/usr/bin/env python3
"""
A股实时行情查询工具
使用方法:
  python3 stock_query.py              # 默认传媒板块
  python3 stock_query.py sh600519     # 查询指定股票
"""

import requests
import sys
from datetime import datetime

url_base = "https://qt.gtimg.cn/q="

def query_stock(symbol):
    """查询单只股票"""
    url = f"{url_base}{symbol}"
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
    
    if r.status_code == 200:
        parts = r.text.split('~')
        if len(parts) > 32:
            return {
                'name': parts[1],
                'price': float(parts[5]),
                'pct': float(parts[32])
            }
    return None

def main():
    print("=" * 60)
    
    if len(sys.argv) < 2:
        # 默认传媒板块
        symbols = [
            ("sz300364", "中文在线"),
            ("sz301231", "荣信文化"),
            ("sh603598", "引力传媒"),
            ("sh603103", "横店影视"),
        ]
        print("📺 传媒板块实时行情")
    else:
        # 用户指定
        symbol_input = sys.argv[1]
        symbols = [(symbol_input, symbol_input)]
        print(f"🔍 查询: {symbol_input}")
    
    print(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print(f"{'名称':<12} {'价格':<10} {'涨跌幅':<10}")
    print("-" * 60)
    
    for symbol, name in symbols:
        data = query_stock(symbol)
        if data:
            pct = data['pct']
            
            # 状态判断
            if pct >= 9.9:
                status = "✅ 涨停"
            elif pct >= 5:
                status = "⭐ 大涨"
            elif pct > 0:
                status = "📈 上涨"
            elif pct < 0:
                status = "📉 下跌"
            else:
                status = ""
            
            print(f"{data['name']:<12} {data['price']:<10.2f} {pct:>+8.2f}% {status}")
        else:
            print(f"{name:<12} 获取失败")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
