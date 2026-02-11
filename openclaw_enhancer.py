#!/usr/bin/env python3
"""
OpenClaw Enhancement集成器
整合 增强记忆系统 + 智能工具选择器
借鉴 LightAgent 设计理念
"""

from enhanced_memory_system import EnhancedMemorySystem, MemoryEntry
from smart_tool_selector import SmartToolSelector, Tool
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AgentContext:
    """Agent上下文"""
    user_id: str
    intent: str
    confidence: float
    available_tools: List[str]
    history: List[Dict]


class OpenClawEnhancer:
    """
    OpenClaw 增强器

    整合两个核心优化：
    1. EnhancedMemorySystem - 语义化记忆系统
    2. SmartToolSelector - 智能工具选择
    """

    def __init__(self):
        # 初始化记忆系统
        self.memory = EnhancedMemorySystem()

        # 初始化工具选择器
        self.tool_selector = SmartToolSelector()
        self.tool_selector.register_openclaw_tools()

        # 当前上下文
        self.current_context: Optional[AgentContext] = None

        # 统计
        self.stats = {
            "total_queries": 0,
            "total_tool_selections": 0,
            "token_saved_estimate": 0,
            "avg_confidence": 0.0
        }

    # ==================== 智能处理流程 ====================

    def process_request(self, user_message: str, intent: str = None,
                        confidence: float = 0.8) -> Dict:
        """
        智能处理用户请求

        流程：
        1. 检索相关记忆
        2. 选择相关工具
        3. 返回处理建议
        """
        self.stats["total_queries"] += 1

        # 1. 检索记忆
        relevant_memories = self.memory.query_memories(
            user_message,
            min_importance=0.3,
            limit=5
        )

        # 2. 选择工具
        selected_tools = self.tool_selector.select_tools(
            user_message,
            max_tools=3
        )

        # 3. 计算Token节省 (估算)
        # 传统方式需要扫描所有工具 -> Token消耗大
        # 智能筛选只传递3个工具 -> 节省约80%
        tools_count = len(self.tool_selector.tools)
        selected_count = len(selected_tools)
        token_saved = (tools_count - selected_count) * 100  # 估算每个工具100 Token
        self.stats["token_saved_estimate"] += token_saved

        self.stats["total_tool_selections"] += 1

        # 更新平均置信度
        self.stats["avg_confidence"] = (
            (self.stats["avg_confidence"] * (self.stats["total_queries"] - 1) + confidence)
            / self.stats["total_queries"]
        )

        return {
            "relevant_memories": relevant_memories,
            "selected_tools": [{"name": t[0], "score": t[1]} for t in selected_tools],
            "token_saved_estimate": token_saved,
            "suggested_tools": [t[0] for t in selected_tools],
            "tool_scores": dict(selected_tools)
        }

    def save_interaction(self, user_message: str, assistant_response: str,
                         intent: str = None, success: bool = True):
        """保存交互到记忆"""
        # 保存对话
        self.memory.save_conversation(
            user_message=user_message,
            assistant_response=assistant_response,
            intent=intent
        )

        # 如果有决策，也保存
        if intent:
            self.memory.save_decision(
                intent=intent,
                action="process_request",
                confidence=0.8 if success else 0.5,
                message=f"处理用户请求: {user_message[:50]}..."
            )

        # 记录工具使用
        if self.current_context:
            for tool_name in self.current_context.available_tools:
                self.tool_selector.record_usage(tool_name, success)

    # ==================== 工具建议 ====================

    def suggest_next_action(self, current_task: str) -> Dict:
        """建议下一步操作"""
        # 获取相关记忆
        memories = self.memory.query_memories(current_task, limit=3)

        # 建议工具
        suggested_tools = self.tool_selector.suggest_tools_for_intent(current_task)

        return {
            "relevant_history": [m["content"] for m in memories],
            "suggested_tools": suggested_tools,
            "recommendation": self._generate_recommendation(memories, suggested_tools)
        }

    def _generate_recommendation(self, memories: List[Dict],
                                  tools: List[str]) -> str:
        """生成建议文本"""
        if not memories and not tools:
            return "暂无相关历史，建议使用通用工具"

        suggestions = []
        if tools:
            suggestions.append(f"建议使用工具: {', '.join(tools[:3])}")

        if memories:
            suggestions.append(f"参考历史经验: {memories[0]['content'][:50]}...")

        return " | ".join(suggestions) if suggestions else "继续执行当前任务"

    # ==================== 统计与报告 ====================

    def get_enhancement_stats(self) -> Dict:
        """获取增强统计"""
        memory_stats = self.memory.stats()
        tool_stats = self.tool_selector.get_tool_stats()

        return {
            "memory_system": memory_stats,
            "tool_selector": tool_stats,
            "enhancement": {
                "total_queries": self.stats["total_queries"],
                "total_tool_selections": self.stats["total_tool_selections"],
                "token_saved_estimate": self.stats["token_saved_estimate"],
                "avg_confidence": round(self.stats["avg_confidence"], 2),
                "token_savings_percent": round(
                    self.stats["token_saved_estimate"] /
                    (self.stats["total_tool_selections"] * len(self.tool_selector.tools) * 100) * 100
                    if self.stats["total_tool_selections"] > 0 else 0,
                    1
                )
            }
        }

    def generate_report(self) -> str:
        """生成优化报告"""
        stats = self.get_enhancement_stats()

        report = f"""
╔══════════════════════════════════════════════════════════════╗
║            OpenClaw Enhancement Report                      ║
╠══════════════════════════════════════════════════════════════╣
║ 记忆系统 (Enhanced Memory)                                  ║
║   - 总记忆数: {stats['memory_system']['total_memories']:5d}                                    ║
║   - 决策记忆: {stats['memory_system']['by_type'].get('DECISION', 0):5d}                                    ║
║   - 学习记忆: {stats['memory_system']['by_type'].get('LEARNING', 0):5d}                                    ║
║   - 对话记忆: {stats['memory_system']['by_type'].get('CONVERSATION', 0):5d}                                    ║
╠══════════════════════════════════════════════════════════════╣
║ 工具选择器 (Smart Tool Selector)                            ║
║   - 工具总数: {stats['tool_selector']['total_tools']:5d}                                    ║
║   - 文件操作: {stats['tool_selector']['by_category'].get('file', 0):5d}                                    ║
║   - 系统操作: {stats['tool_selector']['by_category'].get('system', 0):5d}                                    ║
║   - Web操作: {stats['tool_selector']['by_category'].get('web', 0):5d}                                    ║
║   - AI工具: {stats['tool_selector']['by_category'].get('ai', 0):5d}                                    ║
╠══════════════════════════════════════════════════════════════╣
║ 优化效果                                                   ║
║   - 总查询数: {stats['enhancement']['total_queries']:5d}                                    ║
║   - 工具选择: {stats['enhancement']['total_tool_selections']:5d}                                    ║
║   - Token节省估算: {stats['enhancement']['token_saved_estimate']:8d}                          ║
║   - 平均置信度: {stats['enhancement']['avg_confidence']:.2f}                                      ║
╚══════════════════════════════════════════════════════════════╝
        """

        return report


# ==================== 便捷函数 ====================

_enhancer = None


def get_enhancer() -> OpenClawEnhancer:
    """获取全局增强器实例"""
    global _enhancer
    if _enhancer is None:
        _enhancer = OpenClawEnhancer()
    return _enhancer


def process_with_enhancement(user_message: str, intent: str = None,
                             confidence: float = 0.8) -> Dict:
    """便捷的增强处理函数"""
    enhancer = get_enhancer()
    return enhancer.process_request(user_message, intent, confidence)


# 测试代码
if __name__ == "__main__":
    print("Testing OpenClaw Enhancer...")

    enhancer = OpenClawEnhancer()

    # 测试处理流程
    test_requests = [
        "Read the latest memory file",
        "Search for AI agent frameworks on GitHub",
        "Send a message to Feishu",
        "Analyze stock market data"
    ]

    for request in test_requests:
        print(f"\n📝 Processing: {request}")
        result = enhancer.process_request(request)
        print(f"  🧠 Memories: {len(result['relevant_memories'])} found")
        print(f"  🔧 Tools: {result['suggested_tools']}")
        print(f"  💰 Token saved: ~{result['token_saved_estimate']}")

    # 生成报告
    print(enhancer.generate_report())

    print("\n✅ OpenClaw Enhancer working!")
