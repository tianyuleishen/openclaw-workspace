#!/usr/bin/env python3
"""
终极挑战 benchmark v12.0 (最终版)
"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace')

from reasoning_engine_v12_final import ReasoningEngineV12


def run_benchmark():
    print("="*70)
    print("🦄 终极挑战 benchmark v12.0 (最终版)")
    print("="*70)
    
    engine = ReasoningEngineV12()
    
    test_cases = [
        # v12.0新增
        ("解释黎曼ζ函数的非平凡零点分布猜想", "math_ultimate", ["黎曼"]),
        ("费马大定理 x^n + y^n = z^n 请解释", "math_ultimate", ["费马"]),
        ("P vs NP问题为什么重要？", "math_ultimate", ["P", "NP"]),
        ("康托尔对角线论证实数不可列", "math_ultimate", ["康托尔"]),
        ("素数有无穷多个怎么证明？", "math_ultimate", ["素数"]),
        ("量子纠缠和叠加态的区别？贝尔不等式？", "quantum", ["量子"]),
        ("Shor算法如何分解大数？对RSA威胁？", "quantum", ["Shor"]),
        ("Transformer注意力机制计算过程？", "ml_ultimate", ["Transformer"]),
        ("GPT-4和GPT-3.5区别？Scaling Law？", "ml_ultimate", ["GPT"]),
        ("缸中之脑如何证明不是模拟？", "philosophy", ["缸中之脑"]),
        ("电车难题的功利主义 vs 义务论", "philosophy", ["电车"]),
        ("高可用分布式系统关键组件？CAP定理？", "system_design", ["高可用"]),
        ("事件驱动微服务架构Python实现", "system_design", ["事件驱动"]),
        ("有效市场假说和行为金融学的冲突", "economics", ["有效市场"]),
        ("IS-LM和AS-AD模型区别？", "economics", ["IS-LM"]),
        
        # v11.0原有
        ("证明欧拉公式 e^(iπ) + 1 = 0", "math_advanced", ["欧拉"]),
        ("用二分查找在有序数组中找目标值", "coding_advanced", ["二分查找"]),
        ("劝君更尽一杯酒，西出阳关无故人", "poem_advanced", ["西出阳关"]),
    ]
    
    print(f"\n🦄 测试 {len(test_cases)} 道终极挑战:")
    print("-"*70)
    
    results = {"passed": 0, "failed": 0, "by_type": {}}
    
    for i, (question, expected_type, keywords) in enumerate(test_cases, 1):
        result = engine.analyze(question)
        
        has_keyword = any(kw in result["answer"] for kw in keywords)
        matched = expected_type == result.get("type") or has_keyword
        
        status = "✅" if matched else "❌"
        
        if matched:
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        print(f"{i:2d}. {result.get('type', 'general'):15s} {status} | {question[:35]:35s}")
        
        if expected_type not in results["by_type"]:
            results["by_type"][expected_type] = {"total": 0, "passed": 0}
        results["by_type"][expected_type]["total"] += 1
        if matched:
            results["by_type"][expected_type]["passed"] += 1
    
    total = len(test_cases)
    score = (results["passed"] / total) * 100
    
    print("\n" + "="*70)
    print("📈 终极挑战汇总 v12.0 (最终版)")
    print("="*70)
    
    print(f"\n总题数: {total}")
    print(f"通过: {results['passed']}")
    print(f"失败: {results['failed']}")
    print(f"得分: {score:.1f}%")
    
    print("\n📊 分类成绩:")
    for ptype, stats in results["by_type"].items():
        cat_score = (stats["passed"] / stats["total"]) * 100
        bar = "█" * int(cat_score / 10) + "░" * (10 - int(cat_score / 10))
        print(f"  {ptype:18s}: [{bar}] {cat_score:5.1f}%")
    
    # 评级
    print("\n" + "="*70)
    print("🎯 最终评级")
    print("="*70)
    
    if score >= 95:
        rating = "🦄 Unicorn Mode"
    elif score >= 90:
        rating = "🔥 God Mode"
    elif score >= 80:
        rating = "🦞 Expert+"
    else:
        rating = "🏆 Expert"
    
    print(f"\n得分: {score:.1f}%")
    print(f"评级: {rating}")
    
    # 进化
    print("\n" + "="*70)
    print("📈 进化轨迹")
    print("="*70)
    
    print("\nv11.0 (极限版): 11.8%")
    print("v12.0 (知识增强版): {:.1f}%".format(score))
    print(f"提升: +{score-11.8:.1f}%")
    
    print("\n" + "="*70)
    
    return score


if __name__ == "__main__":
    run_benchmark()
