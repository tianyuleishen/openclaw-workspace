#!/usr/bin/env python3
"""
🦞 推理引擎 v9.0 - 挑战版Benchmark
"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace')

from reasoning_engine_v9 import ReasoningEngineV9

def run_benchmark():
    print("="*70)
    print("🦞 推理引擎 v9.0 - 挑战版Benchmark")
    print("="*70)
    
    engine = ReasoningEngineV9()
    
    # 挑战题库
    test_cases = [
        # 🎯 v8.0原有题目（13道）
        ("因式分解", "a²(b - c) + b²(a - c) + c²(a - b) 因式分解", "factorization"),
        ("三角函数", "tanθ₁·...·tanθₙ = 2^(n/2)，求cosθ₁+...+cosθₙ", "trigonometric"),
        ("极值组合", "100×100格子涂色，每种颜色不超过10000个，求最小t", "extremal"),
        ("几何抛物线", "抛物线焦点轨迹", "geometry"),
        ("函数", "y=(x+1)/(|x|+1)三点共线，k的范围", "function"),
        ("逻辑", "天气预报说周三会下雨，请问今天星期几？", "logic"),
        ("代数", "皮尔逊相关系数为1.23，这可能吗？", "algebra"),
        ("机器学习", "模型在测试集上达到100%准确率，新测试集也100%吗？", "ml"),
        ("组合座位", "甲乙丙三人座位安排", "combinatorics"),
        ("物理雨滴", "雨滴下落公式", "physics"),
        ("LED", "LED显示数字", "physics"),
        ("函数极值", "求函数极值", "extremal"),
        ("翻折几何", "翻折正方形，二面角", "geometry"),
        
        # 🎯 v9.0新增挑战题（5道）
        ("复杂逻辑-游泳", "甲、乙、丙三人，只有一人会游泳。甲说'我会'，乙说'我不会'，丙说'甲不会'。只有一句是真话。谁会游泳？", "complex_logic"),
        ("逻辑链-红眼睛", "岛上5个红眼睛，眼睛 taboo，谁最后离开？", "logic_chain"),
        ("证明-1+1", "证明1+1=2", "proof"),
        ("概率-至少", "100人，至少2人生日相同的概率？", "probability"),
        ("数论-质数", "证明存在无限多个质数", "number_theory"),
    ]
    
    print(f"\n📊 测试 {len(test_cases)} 道题目:")
    print("-"*70)
    
    results = {"passed": 0, "failed": 0, "by_type": {}}
    
    for i, (name, problem, expected) in enumerate(test_cases, 1):
        result = engine.analyze(problem)
        
        match = result["type"] == expected
        status = "✅" if match else "❌"
        
        if match:
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        print(f"{i:2d}. {name[:10]:10s} {status} {result['type']:15s} | {result['answer'][:25]:25s}")
        
        # 记录
        if expected not in results["by_type"]:
            results["by_type"][expected] = {"total": 0, "passed": 0}
        results["by_type"][expected]["total"] += 1
        if match:
            results["by_type"][expected]["passed"] += 1
    
    # 汇总
    total = len(test_cases)
    score = (results["passed"] / total) * 100
    
    print("\n" + "="*70)
    print("📈 Benchmark汇总 v9.0")
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
    
    # 阶段评估
    print("\n" + "="*70)
    print("🎯 阶段评估")
    print("="*70)
    
    if score >= 95:
        stage = "🏆 专家级 - 竞赛水平"
        desc = "能够处理竞赛级别的复杂推理问题"
    elif score >= 85:
        stage = "🦞 高级阶段 - 复杂推理"
        desc = "能够处理多领域复杂推理"
    elif score >= 70:
        stage = "🧠 中级阶段 - 模式识别"
        desc = "能够识别问题模式"
    else:
        stage = "📚 初级阶段 - 基础运算"
        desc = "能够处理基础数学问题"
    
    print(f"\n当前阶段: {stage}")
    print(f"评估: {desc}")
    
    # 🎯 挑战成功？
    print("\n🎯 挑战结果:")
    if score >= 95:
        print("  🎉 挑战成功！达到专家级！")
    elif score >= 85:
        print(f"  💪 接近专家级，还需{95-score:.1f}%")
    else:
        print(f"  📈 继续努力！距高级还需{85-score:.1f}%")
    
    print("\n" + "="*70)
    
    return score


if __name__ == "__main__":
    score = run_benchmark()
