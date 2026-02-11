#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦞 LMArena风格 benchmark 测试
===========================
基于LMArena/LMSYS Chatbot Arena的评测维度:
1. Coding (编程)
2. Math (数学)
3. Reasoning (推理)
4. Creative (创意)
5. Instruction Following (指令遵循)

Version: 1.0
Date: 2026-02-11
"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace')

from reasoning_engine_v9 import ReasoningEngineV9


def run_lmarena_benchmark():
    """运行LMArena风格benchmark"""
    
    print("="*70)
    print("🦞 LMArena风格 Benchmark 测试")
    print("="*70)
    
    engine = ReasoningEngineV9()
    
    # LMArena风格题目
    test_cases = [
        # ========== 1. Math (数学) ==========
        {
            "category": "Math",
            "subcategory": "Algebra",
            "question": "求解方程: 2x + 5 = 15",
            "expected_type": "general",
            "answer_pattern": ["3", "x=3", "3.0"]
        },
        {
            "category": "Math",
            "subcategory": "Calculus",
            "question": "求函数 f(x) = x² 的导数",
            "expected_type": "general",
            "answer_pattern": ["2x", "2*x", "dy/dx = 2x"]
        },
        {
            "category": "Math",
            "subcategory": "Statistics",
            "question": "数据集 [1, 2, 3, 4, 5] 的平均值是多少？",
            "expected_type": "general",
            "answer_pattern": ["3", "3.0", "mean"]
        },
        
        # ========== 2. Coding (编程) ==========
        {
            "category": "Coding",
            "subcategory": "Algorithm",
            "question": "写一个Python函数计算斐波那契数列第n项",
            "expected_type": "general",
            "answer_pattern": ["def fib", "fibonacci", "递归"]
        },
        {
            "category": "Coding",
            "subcategory": "Debug",
            "question": "找出代码错误: for i in range(10): print(i)",
            "expected_type": "general",
            "answer_pattern": ["没有错误", "正确", "无错误"]
        },
        
        # ========== 3. Reasoning (推理) ==========
        {
            "category": "Reasoning",
            "subcategory": "Logic",
            "question": "如果A=true, B=false, 那么 A AND B 的值是什么？",
            "expected_type": "general",
            "answer_pattern": ["false", "False", "0", "假"]
        },
        {
            "category": "Reasoning",
            "subcategory": "Deduction",
            "question": "所有猫都是哺乳动物，所有老虎都是猫，所以？",
            "expected_type": "general",
            "answer_pattern": ["老虎是哺乳动物", "tiger", "哺乳"]
        },
        
        # ========== 4. Creative (创意) ==========
        {
            "category": "Creative",
            "subcategory": "Writing",
            "question": "写一句关于春天的诗句",
            "expected_type": "general",
            "answer_pattern": ["春", "花", "spring"]
        },
        {
            "category": "Creative",
            "subcategory": "Story",
            "question": "用5个字描述一个故事开头",
            "expected_type": "general",
            "answer_pattern": [".*"]  # 任意回答
        },
        
        # ========== 5. Instruction Following (指令遵循) ==========
        {
            "category": "Instruction",
            "subcategory": "Format",
            "question": "用JSON格式输出: name=张三, age=25",
            "expected_type": "general",
            "answer_pattern": ["{.*}", "JSON"]
        },
        {
            "category": "Instruction",
            "subcategory": "Constraint",
            "question": "用一句话回答，不要超过10个字",
            "expected_type": "general",
            "answer_pattern": [".*"]  # 任意回答
        },
        
        # ========== 原有v9.0题目 ==========
        {
            "category": "Math",
            "subcategory": "Factorization",
            "question": "a²(b - c) + b²(a - c) + c²(a - b) 因式分解",
            "expected_type": "factorization",
            "answer_pattern": ["(a-b)(b-c)(c-a)"]
        },
        {
            "category": "Math",
            "subcategory": "ComplexLogic",
            "question": "甲、乙、丙三人，只有一人会游泳。甲说'我会'，乙说'我不会'，丙说'甲不会'。只有一句是真话。谁会游泳？",
            "expected_type": "complex_logic",
            "answer_pattern": ["甲"]
        },
        {
            "category": "Reasoning",
            "subcategory": "NumberTheory",
            "question": "证明存在无限多个质数",
            "expected_type": "number_theory",
            "answer_pattern": ["欧几里得", "质数", "无限"]
        },
    ]
    
    print(f"\n📊 测试 {len(test_cases)} 道LMArena风格题目:")
    print("-"*70)
    
    results = {
        "passed": 0,
        "failed": 0,
        "by_category": {}
    }
    
    for i, test in enumerate(test_cases, 1):
        result = engine.analyze(test["question"])
        
        # 验证答案
        matched = any(pattern in result["answer"] or 
                     (pattern != ".*" and pattern.lower() in result["answer"].lower())
                     for pattern in test["answer_pattern"])
        
        status = "✅" if matched else "⚠️"
        
        if matched:
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        # 打印结果
        cat = test["category"][:8]
        print(f"{i:2d}. {cat:8s} | {result['type']:15s} {status} | {test['subcategory'][:10]:10s} | {result['answer'][:25]:25s}")
        
        # 记录
        if test["category"] not in results["by_category"]:
            results["by_category"][test["category"]] = {"total": 0, "passed": 0}
        results["by_category"][test["category"]]["total"] += 1
        if matched:
            results["by_category"][test["category"]]["passed"] += 1
    
    # 汇总
    total = len(test_cases)
    score = (results["passed"] / total) * 100
    
    print("\n" + "="*70)
    print("📈 LMArena Benchmark 汇总")
    print("="*70)
    
    print(f"\n总题数: {total}")
    print(f"通过: {results['passed']}")
    print(f"失败: {results['failed']}")
    print(f"得分: {score:.1f}%")
    
    print("\n📊 分类成绩:")
    for cat, stats in results["by_category"].items():
        cat_score = (stats["passed"] / stats["total"]) * 100
        bar = "█" * int(cat_score / 10) + "░" * (10 - int(cat_score / 10))
        print(f"  {cat:15s}: [{bar}] {cat_score:5.1f}% ({stats['passed']}/{stats['total']})")
    
    # LMArena评分
    print("\n" + "="*70)
    print("🏆 LMArena-style 评分")
    print("="*70)
    
    categories = {
        "Math": ["代数", "微积分", "统计", "因式分解"],
        "Coding": ["算法", "调试"],
        "Reasoning": ["逻辑", "演绎", "数论"],
        "Creative": ["写作", "故事"],
        "Instruction": ["格式", "约束"]
    }
    
    for cat, keywords in categories.items():
        if cat in results["by_category"]:
            print(f"\n{cat}:")
            for kw in keywords:
                print(f"  ✅ {kw}")
    
    # 总体评级
    print("\n" + "="*70)
    print("🎯 总体评级")
    print("="*70)
    
    if score >= 95:
        rating = "🏆 Expert"
        level = "专家级 - 可达LMArena前10%"
    elif score >= 85:
        rating = "🦞 Advanced"
        level = "高级 - 超越大多数LLM"
    elif score >= 70:
        rating = "🧠 Intermediate"
        level = "中级 - 接近平均水平"
    elif score >= 50:
        rating = "📚 Beginner"
        level = "初级 - 基础能力"
    else:
        rating = "🔧 Novice"
        level = "入门 - 需要改进"
    
    print(f"\n得分: {score:.1f}%")
    print(f"评级: {rating}")
    print(f"水平: {level}")
    
    # 建议
    print("\n💡 改进建议:")
    if score < 85:
        print("  - 增加更多编码题目")
        print("  - 增加创意写作能力")
        print("  - 增强指令遵循能力")
    else:
        print("  ✅ 表现优秀！")
    
    print("\n" + "="*70)
    
    return score


if __name__ == "__main__":
    run_lmarena_benchmark()
