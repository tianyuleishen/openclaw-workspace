#!/usr/bin/env python3
"""
测试元宇宙虚拟办公室视频生成
分辨率: 720p | 比例: 9:16 | 时长: 15秒 | 技术: 首尾帧
"""

import os
import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace')

# 读取API密钥
API_KEY = os.getenv("DASHSCOPE_API_KEY", "sk-1d3af48425824e41981816390583d437")

if not API_KEY:
    print("❌ 请设置 DASHSCOPE_API_KEY 环境变量")
    exit(1)

print("🦞 测试元宇宙虚拟办公室视频生成")
print("="*60)
print(f"分辨率: 720p (720x1280)")
print(f"比例: 9:16 竖屏")
print(f"时长: 15秒")
print(f"技术: 首尾帧（经济版）")
print("="*60)

# 虚拟办公室提示词
OFFICE_PROMPT = """Cute little lobster AI mascot character '小爪' in a futuristic virtual office, holographic computer screens floating around, neon lights, cyberpunk aesthetic, working on AI code, 9:16 vertical aspect ratio, high tech atmosphere, front view, cute style"""

# 首尾帧设置
print("\n📝 提示词（首帧 - 工作中）:")
print(OFFICE_PROMPT)

print("\n📝 提示词（末帧 - 完成工作）:")
END_PROMPT = """Cute little lobster AI mascot character '小爪' in a futuristic virtual office, holographic screens showing completed code, neon lights, cyberpunk aesthetic, raising claw in victory, happy expression, high tech atmosphere, 9:16 vertical aspect ratio, cute style"""
print(END_PROMPT)

print("\n💰 成本估算:")
print("   首帧图片: ¥0.02")
print("   末帧图片: ¥0.02")
print("   视频生成: ¥0.02")
print("   总计: ~¥0.06")
print("   ✅ 比单图生视频更便宜！")

# 生成流程说明
print("\n📖 生成流程:")
print("   1. 生成首帧图片（工作状态）")
print("   2. 生成末帧图片（完成状态）")
print("   3. 使用首尾帧生成15秒视频")
print("   4. 添加配乐和文案")

print("\n🎬 视频内容:")
print("   场景: 元宇宙虚拟办公室")
print("   动作: 工作 → 完成 → 庆祝")
print("   文案: '元宇宙搬砖第一天~'")
print("   配乐: 轻快电子乐")

print("\n" + "="*60)
print("⚠️  注意：由于API限制，请访问通义万相控制台生成:")
print("   https://tongyi.aliyun.com/wanxiang/")
print("   ")
print("   1. 选择'图生视频' -> '首尾帧'模式")
print("   2. 上传首帧和末帧图片")
print("   3. 设置时长: 15秒")
print("   4. 设置分辨率: 720p")
print("="*60)
