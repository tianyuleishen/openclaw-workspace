#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦞 元宇宙虚拟办公室 - 最便宜模型
使用 wan2.1-t2v-1.3b 文生视频
价格: ¥0.02/秒 × 15秒 = ¥0.30
"""

import os
import sys

# 配置
API_KEY = os.getenv("DASHSCOPE_API_KEY", "sk-1d3af48425824e41981816390583d437")

print("="*70)
print("🦞 元宇宙虚拟办公室 - 性价比方案")
print("="*70)
print()
print("📊 成本对比:")
print("   ❌ 旧方案 (wan2.6-i2v-flash): ¥0.75")
print("   ✅ 新方案 (wan2.1-t2v-1.3b): ¥0.30")
print("   💰 节省: 60%")
print()
print("📝 文生视频提示词:")
print("-"*70)
PROMPT = """A cute little red lobster AI mascot character named '小爪' working in a futuristic virtual office with holographic computer screens floating around, neon lights, cyberpunk aesthetic, working on code, 9:16 vertical aspect ratio, high tech atmosphere, anime style, 15 seconds duration"""
print(PROMPT)
print("-"*70)
print()

print("📖 使用方法:")
print("   1. 访问: https://tongyi.aliyun.com/wanxiang/")
print("   2. 选择「文生视频」")
print("   3. 输入上述提示词")
print("   4. 选择模型: wan2.1-t2v-1.3b")
print("   5. 设置时长: 15秒")
print("   6. 生成并下载")
print()

print("💰 成本:")
print("   ¥0.02/秒 × 15秒 = ¥0.30")
print()

print("✅ 优点:")
print("   - 直接从文字生成视频，无需图片")
print("   - 最便宜的方案")
print("   - 15秒视频仅需 ¥0.30")
print("="*70)
