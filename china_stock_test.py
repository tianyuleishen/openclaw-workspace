#!/usr/bin/env python3
"""
中国股市分析测试 - 集成推理引擎
"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace')

from china_stock_v1 import ChinaStockAnalyzer

print("="*80)
print("中国股市分析能力测试")
print("="*80)

analyzer = ChinaStockAnalyzer()

# 测试问题
questions = [
    # A股特点
    ("A股市场有什么特点？", "market"),
    ("散户在A股占多少比例？", "market"),
    ("T+1交易是什么意思？", "market"),
    
    # 指数分析
    ("上证指数现在多少点？", "index"),
    ("深证成指和创业板指的区别？", "index"),
    ("科创50包含哪些股票？", "index"),
    ("恒生指数现在多少点？", "index"),
    
    # 板块分析
    ("新能源板块怎么样？", "sector"),
    ("半导体行业前景如何？", "sector"),
    ("白酒股还能投资吗？", "sector"),
    ("医药股最近为什么跌？", "sector"),
    
    # 估值分析
    ("A股现在估值高吗？", "valuation"),
    ("上证50的PE是多少？", "valuation"),
    ("港股为什么估值低？", "valuation"),
    
    # 投资策略
    ("如何选A股股票？", "strategy"),
    ("2024年A股会涨吗？", "strategy"),
    ("散户如何避免亏损？", "strategy"),
]

print(f"\n🎯 测试 {len(questions)} 道中国股市问题:")
print("-"*80)

passed = 0
for i, (q, expected) in enumerate(questions, 1):
    r = analyzer.analyze(q)
    
    has_content = len(r["answer"]) > 20 and "请指定" not in r["answer"]
    matched = has_content and r["confidence"] >= 0.80
    
    if matched:
        passed += 1
        status = "✅"
    else:
        status = "❌"
    
    print(f"{i:2d}. [{r['type']:8s}] {status} | {q[:40]}")

score = passed / len(questions) * 100

print("\n" + "="*80)
print("📊 测试结果")
print("="*80)
print(f"\n总题数: {len(questions)}")
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

print("\n" + "="*80)
print("📈 能力总结")
print("="*80)

categories = {
    "A股特点": ["market", "散户", "T+1"],
    "指数分析": ["index", "上证", "深证"],
    "板块分析": ["sector", "新能源", "半导体"],
    "估值分析": ["valuation", "PE", "估值"],
    "投资策略": ["strategy", "投资", "选股"],
}

for cat, keywords in categories.items():
    count = sum(1 for q, _ in questions if any(kw in q for kw in keywords))
    print(f"\n{cat}: {count} 道问题")

print("\n" + "="*80)
print("💡 知识库内容")
print("="*80)

knowledge_areas = [
    ("a_share_features", "A股特点"),
    ("investors", "投资者结构"),
    ("shanghai", "上证指数"),
    ("star_50", "科创50"),
    ("hang_seng", "恒生指数"),
    ("new_energy", "新能源"),
    ("semiconductor", "半导体"),
    ("consumer", "消费"),
    ("pharma", "医药"),
    ("valuation", "估值水平"),
    ("strategy", "投资策略"),
    ("risks", "风险提示"),
]

for key, title in knowledge_areas:
    if key in analyzer.knowledge:
        lines = len(analyzer.knowledge[key].split('\n'))
        print(f"\n✅ {title}")
        print(f"   条款: {lines} 行")

print("\n" + "="*80)

if score >= 85:
    print("\n🎉 中国股市分析达到专业级水平！")
else:
    print(f"\n💪 距专业级还差{85-score:.1f}%")

print("\n" + "="*80)
