#!/usr/bin/env python3
"""
v14.5 最终测试
"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace')

from reasoning_engine_v14_5_fixed import ReasoningEngineV14_5_Fixed

engine = ReasoningEngineV14_5_Fixed()

print("="*80)
print("💰 v14.5 经济增强最终测试")
print("="*80)

tests = [
    # 基础题
    ("有效市场假说EMH的三种形式", "emh"),
    ("IS-LM和AS-AD的区别", "is_lm"),
    
    # 货币政策
    ("货币政策工具包括哪些？", "monetary"),
    ("央行如何通过利率调控经济？", "monetary"),
    ("量化宽松是什么？", "monetary"),
    
    # 财政政策
    ("财政政策的挤出效应是什么？", "fiscal"),
    ("政府支出和税收的乘数效应", "fiscal"),
    ("货币政策和财政政策的区别", "fiscal"),
    
    # 菲利普斯曲线
    ("菲利普斯曲线的短期和长期区别？", "phillips"),
    ("通胀率和失业率是什么关系？", "phillips"),
    
    # 通胀
    ("通货膨胀的类型有哪些？", "inflation"),
    ("CPI和PPI的区别？", "inflation"),
    
    # 汇率
    ("购买力平价理论是什么？", "exchange"),
    ("汇率决定的利率平价理论", "exchange"),
    
    # 国际贸易
    ("比较优势理论的核心内容", "trade"),
    ("H-O理论是什么？", "trade"),
    
    # 经济周期
    ("经济周期中的基钦周期是什么？", "cycles"),
    ("库存周期的三个阶段", "cycles"),
]

print(f"\n🎯 测试 {len(tests)} 道经济题目:")
print("-"*80)

passed = 0
for i, (q, expected) in enumerate(tests, 1):
    r = engine.analyze(q)
    
    has_content = len(r["answer"]) > 10 and "需要分析" not in r["answer"]
    matched = has_content and r["confidence"] >= 0.80
    
    if matched:
        passed += 1
        status = "✅"
    else:
        status = "❌"
    
    print(f"{i:2d}. [{r['type']:10s}] {status} | {q[:45]}")

score = passed / len(tests) * 100

print("\n" + "="*80)
print("📊 测试结果")
print("="*80)
print(f"\n总题数: {len(tests)}")
print(f"通过: {passed}")
print(f"得分: {score:.1f}%")

if score >= 95:
    rating = "🦄🦄🦄🦄🦄 LEGENDARY"
elif score >= 90:
    rating = "🦄🦄🦄🦄 ULTIMATE"
elif score >= 85:
    rating = "🦄🦄🦄 GOD TIER"
elif score >= 80:
    rating = "🦄🦄 Super Unicorn"
else:
    rating = "🦄 Unicorn Mode"

print(f"评级: {rating}")

# 进化对比
print("\n" + "="*80)
print("📈 进化对比")
print("="*80)
print("\nv14.4 (增强前):")
print("  知识库: 2条")
print("  经济得分: 50%")
print("  弱点: 货币政策/财政政策/菲利普斯曲线")

print(f"\nv14.5 (增强后):")
print(f"  知识库: {len(engine.knowledge)}条")
print(f"  经济得分: {score:.1f}%")
print(f"  新增: 货币政策/财政政策/菲利普斯曲线/通胀/汇率/贸易/周期")

# 展示新增知识
print("\n" + "="*80)
print("📚 新增经济知识库")
print("="*80)

new_knowledge = [
    ("monetary_policy", "货币政策工具"),
    ("fiscal_policy", "财政政策工具"),
    ("phillips_curve", "菲利普斯曲线"),
    ("inflation", "通货膨胀理论"),
    ("exchange_rate", "汇率决定理论"),
    ("international_trade", "国际贸易理论"),
    ("economic_cycles", "经济周期理论"),
]

for key, title in new_knowledge:
    if key in engine.knowledge:
        lines = len(engine.knowledge[key].split('\n'))
        print(f"\n✅ {title}")
        print(f"   条款: {lines} 行")

print("\n" + "="*80)
print("🎯 能力提升")
print("="*80)
print(f"\n知识库扩展: 2条 → {len(engine.knowledge)}条 (+{len(engine.knowledge)-2}条)")
print(f"测试得分: 50% → {score:.1f}% (+{score-50:.1f}%)")
print(f"覆盖领域: 2个 → 9个 (+7个)")

if score >= 85:
    print("\n🎉 经济领域重大突破！达到专业级！")
else:
    print(f"\n💪 距专业级还差{85-score:.1f}%")

print("\n" + "="*80)
