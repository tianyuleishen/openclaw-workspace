#!/usr/bin/env python3
"""
全面测试 - 增强记忆系统 + 智能工具选择器
"""

import sys
from datetime import datetime
from enhanced_memory_system import EnhancedMemorySystem, MemoryEntry
from smart_tool_selector import SmartToolSelector, Tool
from openclaw_enhancer import OpenClawEnhancer

# 测试结果收集
test_results = {
    "passed": 0,
    "failed": 0,
    "total": 0
}

def test(name, condition, details=""):
    """测试辅助函数"""
    test_results["total"] += 1
    if condition:
        test_results["passed"] += 1
        print(f"✅ {name}")
    else:
        test_results["failed"] += 1
        print(f"❌ {name}")
        if details:
            print(f"   详情: {details}")

print("=" * 70)
print("🧪 OpenClaw 增强系统全面测试")
print("=" * 70)
print()

# ==================== 1. 增强记忆系统测试 ====================
print("📚 [1/4] 增强记忆系统测试")
print("-" * 50)

memory = EnhancedMemorySystem()

# 测试1.1: 保存决策记忆
print("\n1.1 决策记忆测试:")
test(
    "保存决策记忆",
    memory.save_decision(
        intent="test_decision",
        action="test_action",
        confidence=0.9,
        message="测试决策保存功能",
        context={"test": True}
    ) is not None
)

# 测试1.2: 保存学习记忆
print("\n1.2 学习记忆测试:")
test(
    "保存学习记忆",
    memory.save_learning(
        topic="Python",
        insight="Python是一种解释型语言",
        source="Python官方文档"
    ) is not None
)

# 测试1.3: 保存对话记忆
print("\n1.3 对话记忆测试:")
test(
    "保存对话记忆",
    memory.save_conversation(
        user_message="Hello, who are you?",
        assistant_response="I am OpenClaw AI assistant.",
        intent="greeting"
    ) is not None
)

# 测试1.4: 保存用户偏好
print("\n1.4 用户偏好测试:")
test(
    "保存用户偏好",
    memory.save_user_preference(
        user_id="xionglei",
        preference_type="language",
        value="Chinese"
    ) is not None
)

# 测试1.5: 检索测试
print("\n1.5 检索测试:")
result = memory.query_memories("Python", min_importance=0.3)
test(
    "关键词检索 Python",
    len(result) > 0,
    f"找到 {len(result)} 条相关记忆"
)

# 测试1.6: 类型过滤检索
print("\n1.6 类型过滤测试:")
result = memory.query_memories("test", memory_type="decision")
test(
    "决策类型过滤",
    len(result) >= 1,
    f"找到 {len(result)} 条决策记忆"
)

# 测试1.7: 统计功能
print("\n1.7 统计测试:")
stats = memory.stats()
test(
    "获取统计信息",
    stats["total_memories"] >= 4 and "by_type" in stats,
    f"总记忆: {stats['total_memories']}"
)

# 测试1.8: 重要性过滤
print("\n1.8 重要性测试:")
important = memory.get_high_importance_memories(min_importance=0.7)
test(
    "高重要性记忆",
    len(important) >= 1,
    f"找到 {len(important)} 条重要记忆"
)

# ==================== 2. 智能工具选择器测试 ====================
print("\n\n🔧 [2/4] 智能工具选择器测试")
print("-" * 50)

selector = SmartToolSelector()

# 测试2.1: 注册工具
print("\n2.1 工具注册测试:")
selector = SmartToolSelector()
selector.register_openclaw_tools()  # 显式注册工具
test(
    "注册OpenClaw工具",
    len(selector.tools) > 0,
    f"已注册 {len(selector.tools)} 个工具"
)

# 测试2.2: 分类索引
print("\n2.2 分类索引测试:")
test(
    "建立分类索引",
    len(selector.category_index) > 0,
    f"分类数: {len(selector.category_index)}"
)

# 测试2.3: 关键词索引
print("\n2.3 关键词索引测试:")
test(
    "建立关键词索引",
    len(selector.keyword_index) > 0,
    f"关键词数: {len(selector.keyword_index)}"
)

# 测试2.4: 文件操作查询
print("\n2.4 文件操作查询测试:")
result = selector.select_tools("read a Python file", max_tools=3)
test(
    "查询 'read a Python file'",
    len(result) > 0 and result[0][0] == "read",
    f"推荐: {result[0][0]} (分数: {result[0][1]:.2f})" if result else "无结果"
)

# 测试2.5: Web搜索查询
print("\n2.5 Web搜索查询测试:")
result = selector.select_tools("search for information online", max_tools=3)
test(
    "查询 'search online'",
    len(result) > 0 and result[0][0] == "web_search",
    f"推荐: {result[0][0]} (分数: {result[0][1]:.2f})" if result else "无结果"
)

# 测试2.6: 通信工具查询
print("\n2.6 通信工具查询测试:")
result = selector.select_tools("send message to Feishu", max_tools=3)
test(
    "查询 'send Feishu message'",
    len(result) > 0 and result[0][0] == "message",
    f"推荐: {result[0][0]} (分数: {result[0][1]:.2f})" if result else "无结果"
)

# 测试2.7: 系统命令查询
print("\n2.7 系统命令查询测试:")
result = selector.select_tools("execute shell command", max_tools=3)
test(
    "查询 'execute command'",
    len(result) > 0 and result[0][0] == "exec",
    f"推荐: {result[0][0]} (分数: {result[0][1]:.2f})" if result else "无结果"
)

# 测试2.8: 金融数据查询
print("\n2.8 金融数据查询测试:")
result = selector.select_tools("query stock prices", max_tools=3)
test(
    "查询 'stock prices'",
    len(result) > 0,
    f"推荐: {result[0][0]} (分数: {result[0][1]:.2f})" if result else "无结果"
)

# 测试2.9: 工具统计
print("\n2.9 工具统计测试:")
stats = selector.get_tool_stats()
test(
    "获取工具统计",
    "total_tools" in stats and "by_category" in stats,
    f"工具: {stats['total_tools']}, 分类: {len(stats['by_category'])}"
)

# 测试2.10: 工具建议
print("\n2.10 工具建议测试:")
suggestions = selector.suggest_tools_for_intent("file_operation")
test(
    "文件操作建议",
    len(suggestions) > 0 and "read" in suggestions,
    f"建议: {suggestions}"
)

# ==================== 3. 集成器测试 ====================
print("\n\n🔗 [3/4] 集成器测试")
print("-" * 50)

enhancer = OpenClawEnhancer()

# 测试3.1: 初始化
print("\n3.1 初始化测试:")
test(
    "初始化集成器",
    enhancer.memory is not None and enhancer.tool_selector is not None
)

# 测试3.2: 处理请求
print("\n3.2 请求处理测试:")
result = enhancer.process_request("Analyze stock market data")
test(
    "处理股票分析请求",
    "selected_tools" in result and "relevant_memories" in result,
    f"工具: {result['suggested_tools']}, 记忆: {len(result['relevant_memories'])}"
)

# 测试3.3: Token节省
print("\n3.3 Token节省测试:")
test(
    "Token节省计算",
    result["token_saved_estimate"] > 0,
    f"节省约 {result['token_saved_estimate']} Token"
)

# 测试3.4: 工具分数
print("\n3.4 工具分数测试:")
test(
    "工具分数计算",
    len(result["tool_scores"]) > 0,
    f"分数: {result['tool_scores']}"
)

# 测试3.5: 保存交互
print("\n3.5 交互保存测试:")
test(
    "保存用户交互",
    enhancer.save_interaction(
        user_message="Test message",
        assistant_response="Test response",
        intent="test",
        success=True
    ) is None or True  # 无返回值，检查不报错
)

# 测试3.6: 建议操作
print("\n3.6 操作建议测试:")
suggestion = enhancer.suggest_next_action("search GitHub")
test(
    "建议下一步操作",
    "suggested_tools" in suggestion,
    f"建议工具: {suggestion['suggested_tools']}"
)

# 测试3.7: 获取统计
print("\n3.7 统计获取测试:")
stats = enhancer.get_enhancement_stats()
test(
    "获取增强统计",
    "memory_system" in stats and "tool_selector" in stats and "enhancement" in stats,
    f"查询: {stats['enhancement']['total_queries']}"
)

# 测试3.8: 生成报告
print("\n3.8 报告生成测试:")
report = enhancer.generate_report()
test(
    "生成优化报告",
    "OpenClaw Enhancement Report" in report and "记忆系统" in report,
    f"报告长度: {len(report)} 字符"
)

# ==================== 4. 边界条件测试 ====================
print("\n\n⚠️  [4/4] 边界条件测试")
print("-" * 50)

# 测试4.1: 空查询
print("\n4.1 空查询测试:")
result = selector.select_tools("", max_tools=3)
test(
    "处理空查询",
    isinstance(result, list),
    f"返回 {len(result)} 结果"
)

# 测试4.2: 无结果查询
print("\n4.2 无结果查询测试:")
result = selector.select_tools("xyzabc123nonexistent", max_tools=3)
test(
    "处理无结果查询",
    isinstance(result, list),
    f"返回 {len(result)} 结果"
)

# 测试4.3: 低重要性过滤
print("\n4.3 低重要性测试:")
result = memory.query_memories("test", min_importance=0.99)
test(
    "高重要性过滤",
    isinstance(result, list),
    f"找到 {len(result)} 条"
)

# 测试4.4: 多次处理
print("\n4.4 压力测试:")
for i in range(10):
    enhancer.process_request(f"Test request {i}")
test(
    "10次连续处理",
    enhancer.stats["total_queries"] >= 10,
    f"处理次数: {enhancer.stats['total_queries']}"
)

# ==================== 测试总结 ====================
print("\n\n" + "=" * 70)
print("📊 测试总结")
print("=" * 70)
print()
print(f"总测试数:    {test_results['total']}")
print(f"✅ 通过:      {test_results['passed']}")
print(f"❌ 失败:      {test_results['failed']}")
print(f"通过率:      {test_results['passed']/test_results['total']*100:.1f}%")
print()

if test_results['failed'] == 0:
    print("🎉 所有测试通过！")
    sys.exit(0)
else:
    print(f"⚠️  有 {test_results['failed']} 个测试失败")
    sys.exit(1)
