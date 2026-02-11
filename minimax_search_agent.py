#!/usr/bin/env python3
"""
MiniMax 联网搜索演示
展示如何让 MiniMax 模型调用联网搜索工具
"""

import json
from datetime import datetime
from tools.minimax_web_search import minimax_web_search, get_search_tool


class MiniMaxAgent:
    """
    MiniMax 联网搜索 Agent

    模拟 MiniMax 模型的思考和工具调用流程
    """

    def __init__(self):
        self.name = "MiniMax-Search-Agent"
        self.model = "MiniMax-M2.1"
        self.tools = {
            "web_search": {
                "name": "web_search",
                "description": "Search the web for information",
                "parameters": {
                    "query": {"type": "string", "description": "Search query"},
                    "count": {"type": "number", "description": "Number of results"}
                }
            }
        }
        self.search_tool = get_search_tool()

    def think(self, user_input: str) -> Dict:
        """
        思考用户输入，决定是否需要联网搜索

        Returns:
            {
                "reasoning": "思考过程",
                "needs_search": True/False,
                "query": "搜索关键词",
                "response": "直接回答"
            }
        """
        input_lower = user_input.lower()

        # 需要联网搜索的场景
        search_triggers = [
            "latest", "news", "recent", "current",
            "search", "find", "look up", "查询",
            "今天", "最新", "新闻", "最近"
        ]

        needs_search = any(trigger in input_lower for trigger in search_triggers)

        if needs_search:
            query = self._extract_query(user_input)
            return {
                "reasoning": f"用户询问最新信息，需要联网搜索: {query}",
                "needs_search": True,
                "query": query,
                "response": None
            }
        else:
            return {
                "reasoning": "用户问题可以直接回答，不需要搜索",
                "needs_search": False,
                "query": None,
                "response": self._generate_response(user_input)
            }

    def _extract_query(self, user_input: str) -> str:
        """提取搜索关键词"""
        for prefix in ["search for", "查找", "搜索", "查询", "look up"]:
            user_input = user_input.replace(prefix, "").strip()
        return user_input if user_input else user_input

    def _generate_response(self, user_input: str) -> str:
        """生成直接回答"""
        responses = {
            "hello": "你好！我是 MiniMax 联网搜索助手。有什么可以帮你的吗？",
            "hi": "嗨！想搜索什么信息？",
            "help": "我可以帮你联网搜索最新信息。直接告诉我你想查什么！",
        }
        for key, response in responses.items():
            if key in user_input.lower():
                return response
        return "关于这个问题，让我联网帮你搜索一下！"

    def search(self, query: str, count: int = 5) -> str:
        """执行联网搜索"""
        return minimax_web_search(query, count)

    def chat(self, user_input: str) -> str:
        """
        完整的对话流程
        1. 思考是否需要搜索
        2. 如果需要，执行搜索
        3. 返回回答
        """
        print(f"\n{'='*60}")
        print(f"👤 用户: {user_input}")

        # Step 1: 思考
        thinking = self.think(user_input)
        print(f"\n🤔 MiniMax ({self.model}) 思考:")
        print(f"   {thinking['reasoning']}")

        # Step 2: 如果需要搜索
        if thinking['needs_search']:
            print(f"\n🔍 调用 web_search 工具...")
            search_result = self.search(thinking['query'], count=5)
            response = f"📡 联网搜索结果：\n\n{search_result}"
        else:
            response = thinking['response']

        return response

    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "agent": self.name,
            "model": self.model,
            "tools": list(self.tools.keys()),
            "search_stats": self.search_tool.get_stats()
        }


def demo():
    """演示 MiniMax 联网搜索"""
    print("=" * 70)
    print("🚀 MiniMax 联网搜索演示")
    print("=" * 70)
    print("\n模型: MiniMax-M2.1")
    print("工具: web_search")

    agent = MiniMaxAgent()

    # 测试用例
    test_queries = [
        "Hello, who are you?",
        "Search for latest AI agent news",
        "查找今天的科技新闻",
        "What is OpenClaw?",
        "Search for Python programming tutorials",
        "查询最新的AI技术趋势",
    ]

    for query in test_queries:
        response = agent.chat(query)
        print(f"\n{'='*60}")
        print(f"🤖 MiniMax 回答:")
        # 只显示前300字
        if len(response) > 300:
            print(f"   {response[:300]}...")
        else:
            print(f"   {response}")

    # 显示统计
    print(f"\n{'='*70}")
    print("📊 Agent 统计")
    print("="*70)
    stats = agent.get_stats()
    print(f"Agent: {stats['agent']}")
    print(f"模型: {stats['model']}")
    print(f"工具: {', '.join(stats['tools'])}")
    print(f"搜索次数: {stats['search_stats']['total_searches']}")
    print(f"模式: {stats['search_stats']['mode']}")


if __name__ == "__main__":
    demo()
