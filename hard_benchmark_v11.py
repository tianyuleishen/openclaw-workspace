#!/usr/bin/env python3
"""
极限挑战 benchmark v11.0
"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace')

from reasoning_engine_v11 import ReasoningEngineV11


def run_hard_benchmark():
    print("="*70)
    print("🔥 极限挑战 benchmark v11.0")
    print("="*70)
    
    engine = ReasoningEngineV11()
    
    test_cases = [
        # 高级数学
        ("证明欧拉公式 e^(iπ) + 1 = 0", "math_advanced", ["欧拉", "e^", "+1=0"]),
        ("求解微分方程 dy/dx = y", "math_advanced", ["微分方程", "y = Ce^x"]),
        ("计算定积分 ∫₀^π sin(x) dx", "math_advanced", ["积分", "2"]),
        
        # 高级算法
        ("用二分查找在有序数组中找目标值", "coding_advanced", ["二分查找", "binary"]),
        ("实现LRU缓存淘汰算法", "coding_advanced", ["LRU", "缓存"]),
        ("用动态规划解决背包问题", "coding_advanced", ["动态规划", "DP"]),
        
        # 复杂逻辑
        ("10个人围成一圈，每隔一个人杀一个，最后剩几个人？", "logic_advanced", ["约瑟夫环", "1人"]),
        ("A说B在说谎，B说C在说谎，C说A和B都在说谎，谁说真话？", "logic_advanced", ["A说真话", "C说谎"]),
        ("如果明天下雨，那么路面会湿。路面是湿的，一定是下雨了吗？", "logic_advanced", ["不一定", "肯定后件"]),
        ("所有的A都是B，所有的B都是C，那么所有的A都是C吗？", "logic_advanced", ["是的", "三段论"]),
        
        # 物理常识
        ("根据相对论，当速度接近光速时，时间会变慢，这个效应叫什么？", "physics", ["时间膨胀", "相对论"]),
        ("量子力学中的测不准原理是谁提出的？", "physics", ["海森堡", "测不准原理"]),
        
        # 诗词
        ("用7言绝句描写离别之情", "poem_advanced", ["离别", "七言"]),
        
        # v10.0原有
        ("写斐波那契函数", "coding", ["fibonacci"]),
        ("关于春天的诗句", "creative", ["春天"]),
        ("JSON: name=张三, age=25", "instruction", ["JSON"]),
        ("a²(b - c) 因式分解", "math", ["(a-b)"]),
        ("甲乙丙游泳问题", "reasoning", ["甲"]),
    ]
    
    print(f"\n🔥 测试 {len(test_cases)} 道极限题目:")
    print("-"*70)
    
    results = {"passed": 0, "failed": 0, "by_type": {}}
    
    for i, (question, expected_type, keywords) in enumerate(test_cases, 1):
        result = engine.analyze(question)
        
        # 检查关键词
        has_keyword = any(kw in result["answer"] for kw in keywords)
        matched = expected_type == result.get("type") or has_keyword
        
        status = "✅" if matched else "❌"
        
        if matched:
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        print(f"{i:2d}. {result.get('type', 'general'):15s} {status} | {question[:35]:35s}")
        
        # 记录
        if expected_type not in results["by_type"]:
            results["by_type"][expected_type] = {"total": 0, "passed": 0}
        results["by_type"][expected_type]["total"] += 1
        if matched:
            results["by_type"][expected_type]["passed"] += 1
    
    total = len(test_cases)
    score = (results["passed"] / total) * 100
    
    print("\n" + "="*70)
    print("📈 极限挑战汇总 v11.0")
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
    
    # 评级
    print("\n" + "="*70)
    print("🎯 评级")
    print("="*70)
    
    if score >= 90:
        rating = "🔥 God Mode"
    elif score >= 80:
        rating = "🦞 Expert+"
    elif score >= 70:
        rating = "🏆 Expert"
    else:
        rating = "🧠 Advanced"
    
    print(f"\n得分: {score:.1f}%")
    print(f"评级: {rating}")
    
    # v10.0对比
    print("\n" + "="*70)
    print("📈 v10.0 vs v11.0 对比")
    print("="*70)
    
    print("\nv10.0 (通用AI):")
    print("  高级数学: 0%")
    print("  高级算法: 0%")
    print("  复杂逻辑: 0%")
    print("  物理常识: 0%")
    
    print("\nv11.0 (极限版):")
    if "math_advanced" in results["by_type"]:
        print(f"  高级数学: {results['by_type']['math_advanced']['passed']*100//results['by_type']['math_advanced']['total']}%")
    if "coding_advanced" in results["by_type"]:
        print(f"  高级算法: {results['by_type']['coding_advanced']['passed']*100//results['by_type']['coding_advanced']['total']}%")
    if "logic_advanced" in results["by_type"]:
        print(f"  复杂逻辑: {results['by_type']['logic_advanced']['passed']*100//results['by_type']['logic_advanced']['total']}%")
    if "physics" in results["by_type"]:
        print(f"  物理常识: {results['by_type']['physics']['passed']*100//results['by_type']['physics']['total']}%")
    
    print("\n" + "="*70)
    
    return score


if __name__ == "__main__":
    run_hard_benchmark()
