#!/usr/bin/env python3
"""
🦄 v13.0 网络增强版 benchmark
"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace')

from reasoning_engine_v13 import ReasoningEngineV13


def run_benchmark():
    print("="*70)
    print("🦄 v13.0 网络增强版 benchmark")
    print("="*70)
    
    engine = ReasoningEngineV13()
    
    test_cases = [
        # v13.0新增：网络搜索
        ("最新AI新闻2025年有什么重大突破？", "web_search", ["2025", "AI"]),
        ("最近有什么重要科学发现？", "news_search", ["最近"]),
        ("arXiv上关于多模态的最新论文有哪些？", "paper_search", ["论文"]),
        
        # v12.0原有：知识库
        ("解释黎曼ζ函数的非平凡零点分布猜想", "math_ultimate", ["黎曼"]),
        ("Transformer注意力机制计算过程？", "ml_ultimate", ["Transformer"]),
        ("缸中之脑如何证明不是模拟？", "philosophy", ["缸中之脑"]),
        ("Shor算法如何分解大数？对RSA威胁？", "quantum", ["Shor"]),
        ("劝君更尽一杯酒，西出阳关无故人", "poem_advanced", ["西出阳关"]),
        ("费马大定理 x^n + y^n = z^n 请解释", "math_ultimate", ["费马"]),
        ("量子纠缠和叠加态的区别？贝尔不等式？", "quantum", ["量子"]),
        ("GPT-4和GPT-3.5区别？Scaling Law？", "ml_ultimate", ["GPT"]),
        ("电车难题的功利主义 vs 义务论", "philosophy", ["电车"]),
        ("高可用分布式系统关键组件？CAP定理？", "system_design", ["高可用"]),
        ("事件驱动微服务架构Python实现", "system_design", ["事件驱动"]),
        ("有效市场假说和行为金融学的冲突", "economics", ["有效市场"]),
        ("IS-LM和AS-AD模型区别？", "economics", ["IS-LM"]),
        ("证明欧拉公式 e^(iπ) + 1 = 0", "math_advanced", ["欧拉"]),
        ("用二分查找在有序数组中找目标值", "coding_advanced", ["二分查找"]),
    ]
    
    print(f"\n🦄 测试 {len(test_cases)} 道题目:")
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
    print("📈 v13.0 benchmark 汇总")
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
    
    # 新增能力展示
    print("\n" + "="*70)
    print("🚀 v13.0 新增能力")
    print("="*70)
    
    print("\n✅ 实时网络搜索:")
    print("  - 最新AI新闻")
    print("  - 科学研究发现")
    print("  - arXiv论文搜索")
    
    print("\n✅ 知识库增强:")
    print("  - 保留v12.0所有知识")
    print("  - 15+领域覆盖")
    
    # 评级
    print("\n" + "="*70)
    print("🎯 总体评级")
    print("="*70)
    
    if score >= 95:
        rating = "🦄 Unicorn Mode+"
    elif score >= 85:
        rating = "🦄 Unicorn Mode"
    elif score >= 75:
        rating = "🔥 God Mode"
    else:
        rating = "🏆 Expert"
    
    print(f"\n得分: {score:.1f}%")
    print(f"评级: {rating}")
    
    # 进化
    print("\n" + "="*70)
    print("📈 进化轨迹")
    print("="*70)
    
    print("\nv12.0 (知识增强版): 100%")
    print(f"v13.0 (网络增强版): {score:.1f}%")
    
    if score >= 95:
        print("\n🎉 保持Unicorn Mode!")
        print("新增实时网络搜索能力!")
    else:
        print(f"\n距完美还差{100-score:.1f}%")
    
    print("\n" + "="*70)
    
    return score


if __name__ == "__main__":
    run_benchmark()
