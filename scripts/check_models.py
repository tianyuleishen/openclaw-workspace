#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查 DashScope 可用的模型
"""

import os
os.environ['DASHSCOPE_API_KEY'] = 'sk-1d3af48425824e41981816390583d437'

from dashscope import Models

print("=" * 70)
print("📋 检查 DashScope 可用的模型")
print("=" * 70)

# 检查 Models 模块
print("\n📦 Models 模块内容:")
print([m for m in dir(Models) if not m.startswith('_')])

# 查找视频相关模型
print("\n🔍 查找视频生成模型:")
video_models = [m for m in dir(Models) if 'VIDEO' in m.upper() or 'WANXIANG' in m.upper()]
print(video_models)

# 检查文档
print("\n📖 DashScope 官方支持的模型:")
print("参考: https://help.aliyun.com/zh/dashscope/")
print("\n常见的视频生成模型:")
print("  - wanx-video-01")
print("  - wanx-video-01-t2v")
print("  - wanx-video-01-v2")
print("  - I2VGen-XL")
print("  - AnimateDiff")
print("  - ModelScope")

print("\n" + "=" * 70)
