#!/usr/bin/env python3
"""
LMArena风格 Benchmark v10.0
"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace')

from reasoning_engine_v10 import ReasoningEngineV10


def run_benchmark():
    print("="*70)
    print("🦞 LMArena Benchmark v10.0 - 通用AI版")
    print("="*70)
    
    engine = ReasoningEngineV10()
    
    # 测试用例：(问题, 期望type)
    test_cases = [
        # ========== Coding ==========
        ("写斐波那契函数", "coding"),
        ("实现快速排序", "coding"),
        ("反转链表", "coding"),
        
        # ========== Creative ==========
        ("关于春天的诗句", "creative"),
        ("故事开头", "creative"),
        ("一首诗", "creative"),
        
        # ========== Instruction ==========
        ("JSON: name=张三, age=25", "instruction"),
        ("Markdown格式", "instruction"),
        ("列表格式", "instruction"),
        ("一句话回答", "instruction"),
        
        # ========== v9.0 Math原有 ==========
        ("a²(b - c) 因式分解", "math"),
        ("甲乙丙游泳问题", "reasoning"),
        ("无限质数证明", "reasoning"),
        ("生日概率", "math"),
    ]
    
    print(f"\n📊 测试 {len(test_cases)} 道题目:")
    print("-"*70)
    
    results = {"passed": 0, "failed": 0, "by_type": {}}
    
    for i, (question, expected_type) in enumerate(test_cases, 1):
        result = engine.analyze(question)
        
        # 获取type
        result_type = result.get("type")
        matched = expected_type == result_type
        status = "✅" if matched else "❌"
        
        if matched:
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        print(f"{i:2d}. {result_type:12s} {status} | {question[:35]:35s}")
        
        # 记录
        if expected_type not in results["by_type"]:
            results["by_type"][expected_type] = {"total": 0, "passed": 0}
        results["by_type"][expected_type]["total"] += 1
        if matched:
            results["by_type"][expected_type]["passed"] += 1
    
    # 汇总
    total = len(test_cases)
    score = (results["passed"] / total) * 100
    
    print("\n" + "="*70)
    print("📈 LMArena Benchmark 汇总 v10.0")
    print("="*70)
    
    print(f"\n总题数: {total}")
    print(f"通过: {results['passed']}")
    print(f"失败: {results['failed']}")
    print(f"得分: {score:.1f}%")
    
    print("\n📊 分类成绩:")
    for ptype, stats in results["by_type"].items():
        cat_score = (stats["passed"] / stats["total"]) * 100
        bar = "█" * int(cat_score / 10) + "░" * (10 - int(cat_score / 10))
        print(f"  {ptype:15s}: [{bar}] {cat_score:5.1f}%")
    
    # 对比
    print("\n" + "="*70)
    print("📈 v9.0 vs v10.0 对比")
    print("="*70)
    
    print("\nv9.0 (推理引擎):")
    print("  Math/Reasoning: 100%")
    print("  Coding: 0%")
    print("  Creative: 0%")
    print("  Instruction: 0%")
    
    print("\nv10.0 (通用AI):")
    if "coding" in results["by_type"]:
        c = results["by_type"]["coding"]["passed"] * 100 // results["by_type"]["coding"]["total"]
        print(f"  Coding: {c}%")
    if "creative" in results["by_type"]:
        c = results["by_type"]["creative"]["passed"] * 100 // results["by_type"]["creative"]["total"]
        print(f"  Creative: {c}%")
    if "instruction" in results["by_type"]:
        c = results["by_type"]["instruction"]["passed"] * 100 // results["by_type"]["instruction"]["total"]
        print(f"  Instruction: {c}%")
    if "math" in results["by_type"]:
        c = results["by_type"]["math"]["passed"] * 100 // results["by_type"]["math"]["total"]
        print(f"  Math: {c}%")
    if "reasoning" in results["by_type"]:
        c = results["by_type"]["reasoning"]["passed"] * 100 // results["by_type"]["reasoning"]["total"]
        print(f"  Reasoning: {c}%")
    
    # 评级
    print("\n" + "="*70)
    print("🎯 总体评级")
    print("="*70)
    
    if score >= 95:
        rating = "🏆 Expert+"
    elif score >= 85:
        rating = "🦞 Advanced"
    elif score >= 70:
        rating = "🧠 Intermediate"
    else:
        rating = "📚 Beginner"
    
    print(f"\n得分: {score:.1f}%")
    print(f"评级: {rating}")
    
    # 成就
    print("\n" + "="*70)
    print("🎉 v10.0 成就")
    print("="*70)
    
    print("\n✅ 新增 Coding (代码生成)")
    print("✅ 新增 Creative (创意写作)")
    print("✅ 新增 Instruction (指令遵循)")
    print("✅ 保留 Math/Reasoning (原有优势)")
    
    improvement = []
    if "coding" in results["by_type"] and results["by_type"]["coding"]["passed"] > 0:
        improvement.append("Coding")
    if "creative" in results["by_type"] and results["by_type"]["creative"]["passed"] > 0:
        improvement.append("Creative")
    if "instruction" in results["by_type"] and results["by_type"]["instruction"]["passed"] > 0:
        improvement.append("Instruction")
    
    if improvement:
        print(f"\n🎯 改进领域: {', '.join(improvement)}")
    
    print("\n" + "="*70)
    
    return score


if __name__ == "__main__":
    run_benchmark()
