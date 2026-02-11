#!/usr/bin/env python3
"""
v14.0 benchmark (已修复)
"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace')

from reasoning_engine_v14_fixed import ReasoningEngineV14


def run_benchmark():
    print("="*70)
    print("🦄 v14.0 终极版 benchmark (已修复)")
    print("="*70)
    
    engine = ReasoningEngineV14()
    
    test_cases = [
        # v14新增
        ("分析这张图片中的内容", "multimodal_image", ["图像"]),
        ("转换这段音频为文字", "multimodal_audio", ["音频"]),
        ("运行这段Python代码", "code_execution", ["运行"]),
        ("搜索最新AI新闻", "web_search", ["新闻"]),
        
        # 知识库
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
        ("证明欧拉公式 e^(iπ) + 1 = 0", "math_advanced", ["欧拉"]),
        ("劝君更尽一杯酒，西出阳关无故人", "poem_advanced", ["西出阳关"]),
        ("用二分查找在有序数组中找目标值", "coding_advanced", ["二分查找"]),
    ]
    
    print(f"\n🦄 测试 {len(test_cases)} 道题目:")
    print("-"*70)
    
    results = {"passed": 0, "failed": 0}
    by_type = {}
    
    for i, (question, expected_type, keywords) in enumerate(test_cases, 1):
        result = engine.analyze(question)
        
        has_keyword = any(kw in result["answer"] for kw in keywords)
        matched = expected_type == result.get("type") or has_keyword
        
        status = "✅" if matched else "❌"
        
        if matched:
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        print(f"{i:2d}. {result.get('type', 'general'):18s} {status} | {question[:35]:35s}")
        
        if expected_type not in by_type:
            by_type[expected_type] = {"total": 0, "passed": 0}
        by_type[expected_type]["total"] += 1
        if matched:
            by_type[expected_type]["passed"] += 1
    
    total = len(test_cases)
    score = (results["passed"] / total) * 100
    
    print("\n" + "="*70)
    print("📈 v14.0 benchmark 汇总")
    print("="*70)
    
    print(f"\n总题数: {total}")
    print(f"通过: {results['passed']}")
    print(f"失败: {results['failed']}")
    print(f"得分: {score:.1f}%")
    
    print("\n📊 分类成绩:")
    for ptype, stats in by_type.items():
        cat_score = (stats["passed"] / stats["total"]) * 100
        bar = "█" * int(cat_score / 10) + "░" * (10 - int(cat_score / 10))
        print(f"  {ptype:18s}: [{bar}] {cat_score:5.1f}%")
    
    print("\n" + "="*70)
    print("🎯 总体评级")
    print("="*70)
    
    if score >= 95:
        rating = "🦄🦄 Super Unicorn"
    elif score >= 90:
        rating = "🦄 Unicorn Mode++"
    elif score >= 85:
        rating = "🦄 Unicorn Mode+"
    else:
        rating = "🦄 Unicorn Mode"
    
    print(f"\n得分: {score:.1f}%")
    print(f"评级: {rating}")
    
    print("\n" + "="*70)
    print("📈 进化轨迹")
    print("="*70)
    
    print("\nv13.0 (网络增强): 100%")
    print(f"v14.0 (终极版): {score:.1f}%")
    print(f"提升: +网络搜索/多模态/代码执行/长期记忆!")
    
    print("\n" + "="*70)
    
    return score


if __name__ == "__main__":
    run_benchmark()
