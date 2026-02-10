#!/usr/bin/env python3
"""
腾讯财经API - A股实时行情
修正版：正确解析数据格式
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Optional

class TencentFinance:
    """腾讯财经A股实时行情"""
    
    def __init__(self):
        self.base_url = "https://qt.gtimg.cn/q="
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def get_stock(self, symbol: str) -> Optional[Dict]:
        """
        获取单只股票数据
        
        腾讯数据格式:
        - 字段3: 今日开盘价
        - 字段4: 昨日收盘价  
        - 字段5: 当前价格
        - 字段31: 涨跌额
        - 字段32: 涨跌幅%
        - 字段33: 最高价
        - 字段34: 最低价
        """
        url = f"{self.base_url}{symbol}"
        
        try:
            r = requests.get(url, headers=self.headers, timeout=5)
            
            if r.status_code != 200:
                return None
            
            # 解析数据
            data = r.text.strip()
            
            # 分割数据
            parts = data.split('~')
            
            if len(parts) < 33:
                return None
            
            # 提取数据
            return {
                "symbol": symbol,
                "name": parts[1],
                "open": float(parts[3]),
                "pre_close": float(parts[4]),
                "price": float(parts[5]),
                "high": float(parts[33]),
                "low": float(parts[34]),
                "change": float(parts[31]),
                "pct_chg": float(parts[32]),
                "time": parts[30] if len(parts) > 30 else datetime.now().strftime("%H%M%S")
            }
            
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def get_batch(self, symbols: List[str]) -> List[Dict]:
        """批量获取股票数据"""
        results = []
        for symbol in symbols:
            data = self.get_stock(symbol)
            if data:
                results.append(data)
        return results
    
    def get_indices(self) -> List[Dict]:
        """获取主要指数"""
        indices = [
            ("sh000001", "上证指数"),
            ("sz399001", "深证成指"),
            ("sz399006", "创业板指"),
            ("sh000300", "沪深300"),
        ]
        
        results = []
        for symbol, name in indices:
            data = self.get_stock(symbol)
            if data:
                data["name"] = name
                results.append(data)
        
        return results
    
    def get_media_stocks(self) -> List[Dict]:
        """获取传媒板块股票"""
        media_symbols = [
            ("sz300364", "中文在线"),
            ("sz301231", "荣信文化"),
            ("sh603598", "引力传媒"),
            ("sh603103", "横店影视"),
        ]
        
        return self.get_batch([s[0] for s in media_symbols])
    
    def format_output(self, data: Dict) -> str:
        """格式化输出"""
        name = data.get('name', 'N/A')[:8]
        price = data.get('price', 0)
        pct = data.get('pct_chg', 0)
        
        return f"{name:<8} | {price:>8.2f} | {pct:>+.2f}%"


def demo():
    print("=" * 80)
    print("              腾讯财经API - A股实时行情 (修正版)")
    print("=" * 80)
    print()
    
    tf = TencentFinance()
    
    # 获取传媒板块
    print("📺 传媒板块实时行情:")
    print("-" * 80)
    print(f"{'名称':<10} {'当前价':<10} {'涨跌幅':<10}")
    print("-" * 80)
    
    media = tf.get_media_stocks()
    for stock in media:
        if stock:
            print(f"{stock['name'][:8]:<10} {stock['price']:<10.2f} {stock['pct_chg']:>+.2f}%")
        else:
            print("获取失败")
    
    print()
    
    # 获取市场指数
    print("📊 市场指数:")
    print("-" * 80)
    
    indices = tf.get_indices()
    for idx in indices:
        if idx:
            print(f"{idx['name']:<10} {idx['price']:<12.2f} {idx['pct_chg']:>+.2f}%")
    
    print()
    print("=" * 80)
    print(f"查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)


if __name__ == "__main__":
    demo()
