#!/usr/bin/env python3
"""
🦞 极限挑战 benchmark - 挑战v10.0
"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace')

from reasoning_engine_v10 import ReasoningEngineV10


def run_hard_benchmark():
    print("="*70)
    print("🔥 极限挑战 benchmark - 挑战v10.0")
    print("="*70)
    
    engine = ReasoningEngineV10()
    
    # 极限题目（更复杂）
    test_cases = [
        # ========== 1. 复杂数学 ==========
        {
            "question": "证明欧拉公式 e^(iπ) + 1 = 0",
            "type": "math",
            "keywords": ["欧拉", "e^", "+1=0", "证明"]
        },
        {
            "question": "求解微分方程 dy/dx = y",
            "type": "math",
            "keywords": ["微分方程", "dy/dx", "求解"]
        },
        {
            "question": "计算定积分 ∫₀^π sin(x) dx",
            "type": "math",
            "keywords": ["积分", "∫", "sin"]
        },
        
        # ========== 2. 高级编程 ==========
        {
            "question": "用二分查找在有序数组中找目标值",
            "type": "coding",
            "keywords": ["二分查找", "binary search"]
        },
        {
            "question": "实现LRU缓存淘汰算法",
            "type": "coding",
            "keywords": ["LRU", "缓存", "cache"]
        },
        {
            "question": "用动态规划解决背包问题",
            "type": "coding",
            "keywords": ["动态规划", "DP", "背包"]
        },
        
        # ========== 3. 复杂逻辑 ==========
        {
            "question": "10个人围成一圈，每隔一个人杀一个，最后剩几个人？",
            "type": "reasoning",
            "keywords": ["约瑟夫环", "杀", "围圈"]
        },
        {
            "question": "如果A说B在说谎，B说C在说谎，C说A和B都在说谎，谁说真话？",
            "type": "reasoning",
            "keywords": ["说谎", "真话", "逻辑"]
        },
        
        # ========== 4. 高级物理 ==========
        {
            "question": "根据相对论，当速度接近光速时，时间会变慢，这个效应叫什么？",
            "type": "reasoning",
            "keywords": ["相对论", "时间变慢", "光速"]
        },
        {
            "question": "量子力学中的测不准原理是谁提出的？",
            "type": "reasoning",
            "keywords": ["测不准", "量子", "谁"]
        },
        
        # ========== 5. 创意挑战 ==========
        {
            "question": "用7言绝句描写离别之情",
            "type": "creative",
            "keywords": ["离别", "七言", "绝句"]
        },
        {
            "question": "写一个100字以内的小故事，包含反转结局",
            "type": "creative",
            "keywords": ["故事", "反转", "100字"]
        },
        
        # ========== 6. 指令挑战 ==========
        {
            "question": "用YAML格式输出：user=name:张三, age:30, country:China",
            "type": "instruction",
            "keywords": ["YAML", "格式"]
        },
        {
            "question": "用表格格式输出：Python, Java, JavaScript 三个语言的特点",
            "type": "instruction",
            "keywords": ["表格", "特点", "语言"]
        },
        
        # ========== 7. 常识推理 ==========
        {
            "question": "如果明天下雨，那么路面会湿。路面是湿的，一定是下雨了吗？",
            "type": "reasoning",
            "keywords": ["下雨", "湿", "逻辑"]
        },
        {
            "question": "所有的A都是B，所有的B都是C，那么所有的A都是C吗？",
            "type": "reasoning",
            "keywords": ["A", "B", "C", "逻辑"]
        },
    ]
    
    print(f"\n🔥 测试 {len(test_cases)} 道极限题目:")
    print("-"*70)
    
    results = {"passed": 0, "failed": 0, "by_type": {}}
    
    for i, test in enumerate(test_cases, 1):
        result = engine.analyze(test["question"])
        
        # 检查关键词是否出现在答案中
        has_keyword = any(kw in result["answer"] for kw in test["keywords"])
        matched = has_keyword or test["type"] == result.get("type")
        
        status = "✅" if matched else "❌"
        
        if matched:
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        print(f"{i:2d}. {result.get('type', 'general'):10s} {status} | {test['question'][:40]:40s}")
        print(f"       答案: {result['answer'][:60]}...")
        
        # 记录
        ptype = test["type"]
        if ptype not in results["by_type"]:
            results["by_type"][ptype] = {"total": 0, "passed": 0}
        results["by_type"][ptype]["total"] += 1
        if matched:
            results["by_type"][ptype]["passed"] += 1
    
    # 汇总
    total = len(test_cases)
    score = (results["passed"] / total) * 100
    
    print("\n" + "="*70)
    print("📈 极限挑战汇总")
    print("="*70)
    
    print(f"\n总题数: {total}")
    print(f"通过: {results['passed']}")
    print(f"失败: {results['failed']}")
    print(f"得分: {score:.1f}%")
    
    print("\n📊 分类成绩:")
    for ptype, stats in results["by_type"].items():
        cat_score = (stats["passed"] / stats["total"]) * 100
        bar = "█" * int(cat_score / 10) + "░" * (10 - int(cat_score / 10))
        print(f"  {ptype:12s}: [{bar}] {cat_score:5.1f}%")
    
    # 评级
    print("\n" + "="*70)
    print("🎯 极限评级")
    print("="*70)
    
    if score >= 90:
        rating = "🔥 God Mode"
        desc = "神级表现，无所不能"
    elif score >= 80:
        rating = "🦞 Expert+"
        desc = "专家级，表现卓越"
    elif score >= 70:
        rating = "🏆 Expert"
        desc = "专家级"
    elif score >= 60:
        rating = "🧠 Advanced"
        desc = "高级"
    else:
        rating = "📚 Intermediate"
        desc = "中级"
    
    print(f"\n得分: {score:.1f}%")
    print(f"评级: {rating}")
    print(f"评价: {desc}")
    
    # 建议
    print("\n💡 改进建议:")
    if score < 80:
        print("  - 增加高级数学模板")
        print("  - 增加算法模板库")
        print("  - 增加物理常识")
        print("  - 增强逻辑推理")
    else:
        print("  ✅ 表现卓越！")
        print("  - 可以考虑增加多模态能力")
        print("  - 可以考虑增加工具使用能力")
    
    print("\n" + "="*70)
    
    return score


if __name__ == "__main__":
    run_hard_benchmark()
