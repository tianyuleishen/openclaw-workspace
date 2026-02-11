#!/usr/bin/env python3
"""
🦞 推理引擎 v8.0 - 完整Benchmark
"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace')

from reasoning_engine_v8 import ReasoningEngineV8

def run_benchmark():
    print("="*70)
    print("🦞 推理引擎 v8.0 - Benchmark测试")
    print("="*70)
    
    engine = ReasoningEngineV8()
    
    # 完整测试集
    test_cases = [
        # v7.0原有题目（8道）
        ("因式分解", "a²(b - c) + b²(a - c) + c²(a - b) 因式分解", "factorization"),
        ("三角函数", "tanθ₁·...·tanθₙ = 2^(n/2)，求cosθ₁+...+cosθₙ", "trigonometric"),
        ("极值组合", "100×100格子涂色，每种颜色不超过10000个，求最小t", "extremal"),
        ("几何", "抛物线焦点轨迹", "geometry"),
        ("函数", "y=(x+1)/(|x|+1)三点共线，k的范围", "function"),
        ("逻辑推理", "天气预报说周三会下雨，请问今天星期几？", "logic"),
        ("代数验证", "皮尔逊相关系数为1.23，这可能吗？", "algebra"),
        ("机器学习", "模型在测试集上达到100%准确率，新测试集也100%吗？", "ml"),
        
        # 🎯 v8.0新增题目（5道）
        ("组合座位", "甲乙丙三人座位安排，甲会游泳", "combinatorics"),
        ("物理雨滴", "雨滴从高空下落，求时间", "physics"),
        ("LED显示", "LED显示数字2需要几段", "physics"),
        ("函数极值", "求函数y=x³-3x²+2的极值", "extremal"),
        ("翻折几何", "翻折正方形纸片，二面角角度", "geometry"),
    ]
    
    print(f"\n📊 测试 {len(test_cases)} 道题目:")
    print("-"*70)
    
    results = {"passed": 0, "failed": 0, "by_type": {}}
    
    for i, (name, problem, expected) in enumerate(test_cases, 1):
        result = engine.analyze(problem)
        
        # 匹配检查
        if result["type"] == expected:
            status = "✅"
            results["passed"] += 1
        else:
            status = "❌"
            results["failed"] += 1
        
        print(f"{i:2d}. {name[:8]:8s} {status} {result['type']:12s} | {result['answer'][:30]:30s}")
        
        # 记录
        if expected not in results["by_type"]:
            results["by_type"][expected] = {"total": 0, "passed": 0}
        results["by_type"][expected]["total"] += 1
        if status == "✅":
            results["by_type"][expected]["passed"] += 1
    
    # 汇总
    total = len(test_cases)
    score = (results["passed"] / total) * 100
    
    print("\n" + "="*70)
    print("📈 Benchmark汇总")
    print("="*70)
    
    print(f"\n总题数: {total}")
    print(f"通过: {results['passed']}")
    print(f"失败: {results['failed']}")
    print(f"得分: {score:.1f}%")
    
    print("\n📊 分类成绩:")
    for ptype, stats in results["by_type"].items():
        cat_score = (stats["passed"] / stats["total"]) * 100
        print(f"  {ptype:12s}: {cat_score:5.1f}% ({stats['passed']}/{stats['total']})")
    
    # 阶段评估
    print("\n" + "="*70)
    print("🎯 阶段评估")
    print("="*70)
    
    if score >= 90:
        stage = "🦞 高级阶段 - 复杂推理"
        desc = "能够处理多领域复杂推理问题"
    elif score >= 70:
        stage = "🧠 中级阶段 - 模式识别"
        desc = "能够识别问题模式并应用对应策略"
    else:
        stage = "📚 初级阶段 - 基础运算"
        desc = "能够处理基础数学问题"
    
    print(f"\n当前阶段: {stage}")
    print(f"评估: {desc}")
    
    # 提升
    print("\n📈 升级路径:")
    if score >= 90:
        print("  🎉 已达到高级阶段！")
    else:
        print(f"  距高级阶段还需: {90 - score:.1f}%")
    
    print("\n" + "="*70)
    
    return score


if __name__ == "__main__":
    score = run_benchmark()
    
    if score >= 90:
        print("\n🎉 恭喜！达到🦞高级阶段！")
    else:
        print(f"\n💪 继续努力！当前{score:.1f}%")
