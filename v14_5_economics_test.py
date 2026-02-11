#!/usr/bin/env python3
"""
v14.5 经济增强测试
"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace')

from reasoning_engine_v14_5_economics import ReasoningEngineV14_5

engine = ReasoningEngineV14_5()

print("="*80)
print("💰 v14.5 经济领域增强测试")
print("="*80)

tests = [
    # 基础题（必须对）
    ("有效市场假说EMH的三种形式", "emh"),
    ("IS-LM和AS-AD的区别", "is_lm"),
    
    # 新增题
    ("货币政策工具包括哪些", "monetary"),
    ("财政政策的挤出效应", "fiscal"),
    ("菲利普斯曲线的短期和长期", "phillips"),
    ("通胀的类型和衡量指标", "inflation"),
    ("汇率决定的购买力平价理论", "exchange"),
    ("比较优势理论的核心内容", "trade"),
    ("经济周期的基钦周期", "cycles"),
    
    # 组合题
    ("货币政策和财政政策的区别", "fiscal"),
    ("通胀率和失业率的关系", "phillips"),
]

print(f"\n🎯 测试 {len(tests)} 道经济题目:")
print("-"*80)

passed = 0
for i, (q, expected) in enumerate(tests, 1):
    r = engine.analyze(q)
    
    has_content = len(r["answer"]) > 10 and "需要分析" not in r["answer"]
    matched = has_content and (expected in r["type"] or r["confidence"] >= 0.80)
    
    if matched:
        passed += 1
        status = "✅"
    else:
        status = "❌"
    
    print(f"{i:2d}. [{r['type']:12s}] {status} | {q[:40]}")

score = passed / len(tests) * 100

print("\n" + "="*80)
print("📊 测试结果")
print("="*80)
print(f"\n总题数: {len(tests)}")
print(f"通过: {passed}")
print(f"得分: {score:.1f}%")

# 评级
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

# 对比
print("\n" + "="*80)
print("📈 进化对比")
print("="*80)
print("\nv14.4 (经济增强前):")
print("  知识库: 2条")
print("  得分: 50%")
print("  弱点: 货币政策/财政政策/菲利普斯曲线")

print(f"\nv14.5 (经济增强后):")
print(f"  知识库: {len(engine.knowledge)}条")
print(f"  得分: {score:.1f}%")
print(f"  新增: 货币政策/财政政策/菲利普斯曲线/通胀/汇率/贸易/周期")

if score >= 85:
    print("\n🎉 经济领域重大突破！")
else:
    print(f"\n💪 距完美还差{100-score:.1f}%")

print("\n" + "="*80)

# 展示新知识
print("\n📚 新增经济知识:")
print("-"*80)
for key in ["monetary_policy", "fiscal_policy", "phillips_curve", "inflation", "exchange_rate"]:
    if key in engine.knowledge:
        title = engine.knowledge[key].split('\n')[0]
        print(f"\n✅ {title}")
        print(f"   篇幅: {len(engine.knowledge[key])} 字符")

print("\n" + "="*80)
