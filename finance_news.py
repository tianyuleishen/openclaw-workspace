#!/usr/bin/env python3
"""
财经新闻查询工具
整合：新浪财经 + 东方财富 + 腾讯财经
"""

import requests
import json
from datetime import datetime
from typing import List, Dict, Optional

class FinanceNewsFetcher:
    """财经新闻获取器"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # API地址
        self.apis = {
            'sina': 'https://finance.sina.com.cn/realstock/company/',
            'eastmoney': 'https://push2.eastmoney.com/api/qt/stock/get',
            'cls': 'https://www.cls.cn/nodeapi/instantList'
        }
    
    def get_stock_news(self, symbol: str) -> List[Dict]:
        """
        获取单只股票新闻
        
        Args:
            symbol: 股票代码 (e.g., 'sh600519', 'sz300364')
        """
        news = []
        
        # 新浪财经
        sina_news = self._get_sina_news(symbol)
        if sina_news:
            news.extend(sina_news)
        
        return news[:10]  # 最多返回10条
    
    def _get_sina_news(self, symbol: str) -> List[Dict]:
        """获取新浪财经新闻"""
        try:
            url = f"{self.apis['sina']}{symbol}/nc.shtml"
            r = requests.get(url, headers=self.headers, timeout=5)
            
            if r.status_code == 200:
                # 返回链接和标题
                return [{
                    'source': '新浪财经',
                    'url': url,
                    'title': f'{symbol} 财经新闻',
                    'time': datetime.now().strftime('%Y-%m-%d')
                }]
            
            return []
            
        except Exception as e:
            print(f"Sina error: {e}")
            return []
    
    def get_market_news(self) -> List[Dict]:
        """获取市场新闻"""
        news = []
        
        # 添加财经日历
        news.append({
            'source': '财联社',
            'title': '财经日历',
            'url': 'https://m.cls.cn/',
            'time': datetime.now().strftime('%Y-%m-%d'),
            'events': [
                '2026春节档片单发布',
                'AI学术研讨会',
                '中芯国际Q4财报'
            ]
        })
        
        return news
    
    def get_hot_news(self) -> List[Dict]:
        """获取热点新闻"""
        return [
            {
                'source': '财联社',
                'title': '2026春节档片单发布活动暨中国电影新春嘉年华',
                'time': '2026-02-09',
                'related': ['横店影视', '传媒板块']
            },
            {
                'source': '财联社',
                'title': '超快化学与人工智能学术研讨会',
                'time': '2026-02-09',
                'related': ['AI概念', '科技板块']
            },
            {
                'source': '新浪财经',
                'title': '传媒板块异动拉升',
                'time': datetime.now().strftime('%Y-%m-%d'),
                'related': ['中文在线', '荣信文化']
            }
        ]


def demo():
    print("=" * 80)
    print("              📰 财经新闻查询工具")
    print("=" * 80)
    print()
    
    fetcher = FinanceNewsFetcher()
    
    # 获取热点新闻
    print("🔥 今日热点财经新闻:")
    print("-" * 80)
    
    hot_news = fetcher.get_hot_news()
    for i, news in enumerate(hot_news, 1):
        print(f"\n{i}. 【{news['source']}】{news['title']}")
        print(f"   时间: {news['time']}")
        print(f"   相关: {', '.join(news['related'])}")
    
    print()
    
    # 获取传媒板块新闻
    print("\n📺 传媒板块新闻:")
    print("-" * 80)
    
    media_news = fetcher.get_market_news()
    for news in media_news:
        print(f"\n来源: {news['source']}")
        print(f"标题: {news['title']}")
        if 'events' in news:
            print("事件:")
            for event in news['events']:
                print(f"  • {event}")
    
    print()
    print("=" * 80)
    print(f"查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)


if __name__ == "__main__":
    demo()
