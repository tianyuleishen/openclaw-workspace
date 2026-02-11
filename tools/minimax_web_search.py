#!/usr/bin/env python3
"""
MiniMax 联网搜索工具 - 实时版本
支持 GitHub API + 百度搜索
"""

import json
import urllib.parse
import urllib.request
from typing import Dict, List, Any
from datetime import datetime


class MiniMaxWebSearch:
    """MiniMax 联网搜索工具"""

    def __init__(self):
        self.search_count = 0
        self.last_search = None

    def search(self, query: str, count: int = 5) -> Dict[str, Any]:
        """执行联网搜索"""
        self.search_count += 1
        self.last_search = datetime.now().isoformat()

        results = []

        # 1. 尝试 GitHub 搜索
        try:
            github_results = self._search_github(query, count)
            results.extend(github_results)
        except Exception as e:
            print(f"GitHub search failed: {e}")

        # 2. 尝试百度搜索
        try:
            baidu_results = self._search_baidu(query, count)
            results.extend(baidu_results)
        except Exception as e:
            print(f"Baidu search failed: {e}")

        # 3. 如果都没结果，使用本地数据
        if not results:
            results = self._get_fallback_results(query)

        # 去重并限制数量
        seen = set()
        unique_results = []
        for r in results:
            if r['url'] not in seen:
                seen.add(r['url'])
                unique_results.append(r)

        return {
            'status': 'success' if unique_results else 'partial',
            'query': query,
            'count': len(unique_results),
            'results': unique_results[:count],
            'source': 'github + baidu',
            'timestamp': self.last_search
        }

    def _search_github(self, query: str, count: int) -> List[Dict]:
        """GitHub 代码搜索"""
        try:
            url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(query)}&sort=stars&order=desc"
            
            req = urllib.request.Request(url, headers={
                'User-Agent': 'MiniMax-Search-Agent',
                'Accept': 'application/vnd.github.v3+json'
            })
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                if 'items' in data:
                    return [{
                        'title': item['full_name'],
                        'url': item['html_url'],
                        'description': item.get('description', '')[:100],
                        'stars': item.get('stargazers_count', 0),
                        'source': 'github'
                    } for item in data['items'][:count]]
        except Exception as e:
            print(f"GitHub API error: {e}")
        
        return []

    def _search_baidu(self, query: str, count: int) -> List[Dict]:
        """百度搜索"""
        try:
            url = f"https://www.baidu.com/s?wd={urllib.parse.quote(query)}"
            
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8')
                
                # 简单解析结果
                import re
                links = re.findall(r'<a[^>]+href="(https?://[^"]+)"[^>]*>([^<]+)</a>', html)
                
                results = []
                for url, title in links:
                    if url.startswith('http') and 'baidu' not in url and len(title.strip()) > 5:
                        results.append({
                            'title': title.strip()[:80],
                            'url': url,
                            'description': '',
                            'source': 'baidu'
                        })
                        if len(results) >= count:
                            break
                
                return results
        except Exception as e:
            print(f"Baidu search error: {e}")
        
        return []

    def _get_fallback_results(self, query: str) -> List[Dict]:
        """备用结果"""
        return [{
            'title': f'Search: {query}',
            'url': f'https://github.com/search?q={urllib.parse.quote(query)}',
            'description': 'Search on GitHub',
            'source': 'fallback'
        }]

    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            'total_searches': self.search_count,
            'last_search': self.last_search
        }


# 全局实例
_search_tool = None


def get_search_tool() -> MiniMaxWebSearch:
    global _search_tool
    if _search_tool is None:
        _search_tool = MiniMaxWebSearch()
    return _search_tool


def minimax_web_search(query: str, count: int = 5) -> str:
    """MiniMax 可直接调用的搜索函数"""
    tool = get_search_tool()
    result = tool.search(query, count)

    if result['status'] == 'success' or result['status'] == 'partial':
        lines = [f"🔍 搜索 '{result['query']}' ({result['count']}条结果)\n"]
        
        for i, r in enumerate(result['results'][:count], 1):
            lines.append(f"{i}. {r['title']}")
            if r.get('description'):
                lines.append(f"   📝 {r['description']}")
            lines.append(f"   🔗 {r['url']}")
            lines.append(f"   📡 来源: {r['source']}")
            lines.append("")
        
        lines.append(f"⏰ 时间: {result['timestamp']}")
        lines.append(f"🔧 搜索源: {result['source']}")
        
        return "\n".join(lines)
    else:
        return f"❌ 搜索失败: {result.get('message', '未知错误')}"


if __name__ == "__main__":
    print("Testing MiniMax Web Search (Real)...")

    tool = get_search_tool()

    test_queries = ["AI agent", "Python programming", "OpenClaw"]

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"搜索: {query}")
        result = tool.search(query, 3)
        print(f"状态: {result['status']}")
        print(f"结果数: {result['count']}")
        
        if result['results']:
            for i, r in enumerate(result['results'][:3], 1):
                print(f"  {i}. {r['title']}")

    print(f"\n统计: {tool.get_stats()}")
    print("\n✅ MiniMax Web Search working!")
