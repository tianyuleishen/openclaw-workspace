#!/usr/bin/env python3
"""
Smart Tool Selector - 借鉴 LightAgent 自适应工具筛选
智能筛选相关工具，减少Token消耗
"""

import re
from typing import Dict, List, Any, Tuple, Set
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class Tool:
    """工具定义"""
    name: str
    description: str
    parameters: Dict = field(default_factory=dict)
    category: str = "general"
    keywords: Set[str] = field(default_factory=set)
    usage_count: int = 0
    success_rate: float = 1.0
    last_used: str = None


class SmartToolSelector:
    """
    智能工具选择器

    借鉴 LightAgent 的自适应工具筛选机制：
    1. 从大量工具中智能筛选相关工具
    2. 减少80% Token消耗
    3. 提升52%响应速度
    """

    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self.category_index: Dict[str, Set[str]] = defaultdict(set)
        self.keyword_index: Dict[str, Set[str]] = defaultdict(set)
        self.usage_stats: Dict[str, Dict] = defaultdict(lambda: {
            "total_uses": 0,
            "successes": 0,
            "avg_confidence": 0.5
        })

        # 初始化默认工具分类
        self._init_default_categories()

    def _init_default_categories(self):
        """初始化默认工具分类"""
        self.default_categories = {
            "file": ["read", "write", "edit", "list", "delete", "copy", "move"],
            "system": ["exec", "process", "cron", "gateway"],
            "web": ["web_search", "web_fetch", "browser"],
            "communication": ["message", "sessions_send", "feishu_doc", "feishu_wiki"],
            "development": ["github", "git", "coding_agent"],
            "media": ["tts", "canvas", "video_frames"],
            "data": ["memory_search", "memory_get", "feishu_bitable"],
            "ai": ["openai_whisper", "gog", "tencent_finance"]
        }

    # ==================== 工具注册 ====================

    def register_tool(self, tool: Tool):
        """注册工具"""
        self.tools[tool.name] = tool

        # 建立分类索引
        self.category_index[tool.category].add(tool.name)

        # 建立关键词索引
        for keyword in tool.keywords:
            self.keyword_index[keyword.lower()].add(tool.name)

    def register_tool_from_dict(self, name: str, description: str,
                                 category: str = "general",
                                 keywords: List[str] = None):
        """从字典注册工具"""
        tool = Tool(
            name=name,
            description=description,
            category=category,
            keywords=set(kw.lower() for kw in (keywords or []))
        )
        self.register_tool(tool)

    # ==================== 智能筛选 ====================

    def select_tools(self, query: str, max_tools: int = 5,
                     min_score: float = 0.1) -> List[Tuple[str, float]]:
        """
        智能选择相关工具

        Args:
            query: 用户查询
            max_tools: 最大返回工具数
            min_score: 最低分数阈值

        Returns:
            [(tool_name, score), ...] 排序后的工具列表
        """
        query_lower = query.lower()
        query_keywords = set(re.findall(r'\w+', query_lower))

        # 计算每个工具的分数
        tool_scores: Dict[str, float] = {}

        for tool_name, tool in self.tools.items():
            score = 0.0

            # 1. 关键词匹配 (40% 权重)
            keyword_score = self._calc_keyword_score(query_keywords, tool)
            score += keyword_score * 0.4

            # 2. 描述匹配 (30% 权重)
            desc_score = self._calc_description_score(query_lower, tool)
            score += desc_score * 0.3

            # 3. 使用统计 (20% 权重)
            usage_score = self._calc_usage_score(tool_name)
            score += usage_score * 0.2

            # 4. 分类匹配 (10% 权重)
            category_score = self._calc_category_score(query_lower, tool)
            score += category_score * 0.1

            if score >= min_score:
                tool_scores[tool_name] = score

        # 按分数排序
        sorted_tools = sorted(
            tool_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return sorted_tools[:max_tools]

    def _calc_keyword_score(self, query_keywords: Set[str], tool: Tool) -> float:
        """计算关键词匹配分数"""
        if not query_keywords or not tool.keywords:
            return 0.0

        matches = len(query_keywords & tool.keywords)
        total = len(query_keywords)

        return matches / total if total > 0 else 0.0

    def _calc_description_score(self, query: str, tool: Tool) -> float:
        """计算描述匹配分数"""
        if not tool.description:
            return 0.0

        desc_lower = tool.description.lower()

        # 计算查询词在描述中出现的次数
        matches = 0
        for keyword in query.split():
            if len(keyword) > 2 and keyword in desc_lower:
                matches += 1

        return min(matches / 5.0, 1.0)  # 最多5分

    def _calc_usage_score(self, tool_name: str) -> float:
        """计算使用统计分数"""
        stats = self.usage_stats.get(tool_name, {"total_uses": 0, "successes": 0})

        if stats["total_uses"] == 0:
            return 0.5  # 默认分数

        # 成功率
        success_rate = stats["successes"] / stats["total_uses"]

        # 使用频率 (使用次数越多分数越高，但有上限)
        usage_freq = min(stats["total_uses"] / 100, 1.0)

        return success_rate * 0.7 + usage_freq * 0.3

    def _calc_category_score(self, query: str, tool: Tool) -> float:
        """计算分类匹配分数"""
        # 检查查询中是否包含分类关键词
        for category, keywords in self.default_categories.items():
            if any(kw in query for kw in keywords):
                if tool.category == category:
                    return 1.0

        return 0.0

    # ==================== 工具建议 ====================

    def suggest_tools_for_intent(self, intent: str) -> List[str]:
        """根据意图建议工具"""
        intent_lower = intent.lower()

        suggestions = {
            "file_operation": ["read", "write", "edit", "exec"],
            "web_search": ["web_search", "web_fetch"],
            "communication": ["message", "feishu_doc", "feishu_wiki"],
            "code_development": ["github", "coding_agent", "exec"],
            "media": ["tts", "canvas", "video_frames"],
            "data_query": ["memory_get", "memory_search", "feishu_bitable"],
            "system": ["gateway", "cron", "process"],
            "ai": ["openai_whisper", "gog", "tencent_finance"]
        }

        for intent_type, tools in suggestions.items():
            if intent_type in intent_lower or any(kw in intent_lower for kw in intent_type.split("_")):
                return tools

        return ["exec"]  # 默认

    # ==================== 使用统计 ====================

    def record_usage(self, tool_name: str, success: bool, confidence: float = 1.0):
        """记录工具使用"""
        if tool_name in self.usage_stats:
            self.usage_stats[tool_name]["total_uses"] += 1
            if success:
                self.usage_stats[tool_name]["successes"] += 1

        # 更新工具使用计数
        if tool_name in self.tools:
            self.tools[tool_name].usage_count += 1

    def get_tool_stats(self) -> Dict:
        """获取工具统计"""
        return {
            "total_tools": len(self.tools),
            "by_category": {
                cat: len(tools)
                for cat, tools in self.category_index.items()
            },
            "top_used": sorted(
                [(t.name, t.usage_count) for t in self.tools.values()],
                key=lambda x: x[1],
                reverse=True
            )[:10]
        }

    # ==================== OpenClaw 工具集成 ====================

    def register_openclaw_tools(self):
        """注册 OpenClaw 内置工具"""
        openclaw_tools = [
            # 文件操作
            ("read", "Read file contents", "file", ["read", "file", "content"]),
            ("write", "Write content to file", "file", ["write", "create", "new"]),
            ("edit", "Edit file by replacing text", "file", ["edit", "modify", "change"]),

            # 系统操作
            ("exec", "Execute shell commands", "system", ["exec", "command", "shell", "run"]),
            ("process", "Manage background processes", "system", ["process", "background", "task"]),
            ("cron", "Manage cron jobs", "system", ["cron", "schedule", "timer"]),

            # Web操作
            ("web_search", "Search the web", "web", ["search", "web", "find"]),
            ("web_fetch", "Fetch URL content", "web", ["fetch", "download", "get"]),
            ("browser", "Control web browser", "web", ["browser", "navigate", "click"]),

            # 通信
            ("message", "Send messages via channels", "communication", ["send", "message", "notify"]),
            ("feishu_doc", "Feishu document operations", "communication", ["feishu", "doc", "document"]),
            ("feishu_wiki", "Feishu wiki operations", "communication", ["wiki", "knowledge"]),

            # 开发
            ("github", "GitHub operations", "development", ["github", "git", "pr", "issue"]),
            ("coding_agent", "Run coding agents", "development", ["code", "coding", "program"]),

            # AI
            ("openai_whisper", "Speech to text", "ai", ["whisper", "speech", "audio"]),
            ("gog", "Google Workspace CLI", "ai", ["gmail", "google", "calendar"]),
            ("tencent_finance", "Tencent finance data", "ai", ["stock", "finance", "tencent"]),
        ]

        for name, desc, category, keywords in openclaw_tools:
            self.register_tool_from_dict(name, desc, category, keywords)

        print(f"✅ Registered {len(openclaw_tools)} OpenClaw tools")


# 测试代码
if __name__ == "__main__":
    print("Testing Smart Tool Selector...")

    selector = SmartToolSelector()
    selector.register_openclaw_tools()

    # 测试查询
    test_queries = [
        "Read a Python file from the workspace",
        "Search for information online",
        "Send a message to Feishu",
        "Execute a shell command",
        "Query stock prices"
    ]

    for query in test_queries:
        print(f"\n📝 Query: {query}")
        selected = selector.select_tools(query, max_tools=3)
        for tool, score in selected:
            print(f"  → {tool}: {score:.2f}")

    # 统计
    print(f"\n📊 Tool Stats: {selector.get_tool_stats()}")

    print("\n✅ Smart Tool Selector working!")
