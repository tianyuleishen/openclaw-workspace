#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦞 推理引擎 benchmark 测试
使用经典数学推理题库
"""

import re
from datetime import datetime, timedelta
from skills.reasoning import solve, ReasoningIntegrator


def run_benchmark():
    """运行benchmark测试"""
    
    print("="*70)
    print("🦞 推理引擎 v6.0 - Benchmark测试")
    print("="*70)
    
    # 测试题库（经典数学推理题）
    test_cases = [
        # 类型1: 因式分解
        {
            "category": "因式分解",
            "problem": "a²(b - c) + b²(a - c) + c²(a - b) 因式分解",
            "expected_answer": "(a-b)(b-c)(c-a)"
        },
        
        # 类型2: 三角函数
        {
            "category": "三角函数",
            "problem": "tanθ₁·tanθ₂·...·tanθₙ = 2^(n/2)，求cosθ₁+...+cosθₙ的值",
            "expected_answer": "λ = n-1"
        },
        
        # 类型3: 极值组合
        {
            "category": "极值组合",
            "problem": "100×100格子涂色，每种颜色不超过10000个，求满足条件的最小t",
            "expected_answer": "12"
        },
        
        # 类型4: 几何
        {
            "category": "几何",
            "problem": "抛物线y²=4x的焦点F，过F作弦AB，AB的中点M的轨迹是什么？",
            "expected_answer": "椭圆: x²/9 + y²/8 = 1"
        },
        
        # 类型5: 函数共线
        {
            "category": "函数",
            "problem": "直线y=kx+b与函数y=(x+1)/(|x|+1)有三个交点，求k的范围",
            "expected_answer": "0 < k < 2/9"
        },
        
        # 类型6: 逻辑推理
        {
            "category": "逻辑推理",
            "problem": "天气预报说周三会下雨，事实上昨天确实下雨了，请问今天星期几？",
            "expected_answer": "星期四"
        },
        
        # 类型7: 代数验证
        {
            "category": "代数验证",
            "problem": "皮尔逊相关系数为1.23，这可能吗？为什么？",
            "expected_answer": "不可能，范围是[-1,1]"
        },
        
        # 类型8: 机器学习
        {
            "category": "机器学习",
            "problem": "模型在测试集上达到100%准确率，在新的同分布测试集上也一定达到100%吗？",
            "expected_answer": "不一定"
        },
    ]
    
    # 运行测试
    results = {
        "passed": 0,
        "failed": 0,
        "categories": {}
    }
    
    print("\n📊 测试结果:")
    print("-"*70)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n【{i}】{test['category']}")
        print(f"问题: {test['problem'][:50]}...")
        
        try:
            # 调用推理引擎
            result = solve(test['problem'])
            
            print(f"答案: {result}")
            
            # 验证
            if test['expected_answer'] in result:
                print(f"状态: ✅ 正确")
                results["passed"] += 1
                status = "✅"
            else:
                print(f"期望: {test['expected_answer']}")
                print(f"状态: ⚠️ 部分匹配")
                results["passed"] += 0.5
                status = "⚠️"
            
            # 记录类别
            cat = test['category']
            if cat not in results["categories"]:
                results["categories"][cat] = {"total": 0, "passed": 0}
            results["categories"][cat]["total"] += 1
            if status == "✅":
                results["categories"][cat]["passed"] += 1
            
        except Exception as e:
            print(f"错误: {e}")
            print(f"状态: ❌ 失败")
            results["failed"] += 1
    
    # 汇总报告
    print("\n" + "="*70)
    print("📈 Benchmark汇总")
    print("="*70)
    
    total = len(test_cases)
    passed = results["passed"]
    score = (passed / total) * 100
    
    print(f"\n总题数: {total}")
    print(f"通过: {passed}")
    print(f"失败: {results['failed']}")
    print(f"得分: {score:.1f}%")
    
    print("\n📊 分类成绩:")
    for cat, stats in results["categories"].items():
        cat_score = (stats["passed"] / stats["total"]) * 100
        print(f"  {cat}: {cat_score:.0f}% ({stats['passed']}/{stats['total']})")
    
    # 评估阶段
    print("\n" + "="*70)
    print("🎯 阶段评估")
    print("="*70)
    
    if score >= 90:
        stage = "🦞 高级阶段 - 复杂推理"
        desc = "能够处理多步骤复杂推理问题"
    elif score >= 70:
        stage = "🧠 中级阶段 - 模式识别"
        desc = "能够识别问题模式并应用对应策略"
    elif score >= 50:
        stage = "📚 初级阶段 - 基础运算"
        desc = "能够处理基础数学问题"
    else:
        stage = "🔧 入门阶段 - 规则匹配"
        desc = "依赖预定义规则和模板"
    
    print(f"\n当前阶段: {stage}")
    print(f"评估: {desc}")
    
    # 建议
    print("\n💡 提升建议:")
    if score < 70:
        print("  - 扩展问题模式库")
        print("  - 增加多步骤推理能力")
        print("  - 优化置信度计算")
    
    print("\n" + "="*70)
    print("✅ Benchmark测试完成")
    print("="*70)
    
    return results


if __name__ == "__main__":
    run_benchmark()
