#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

快速测试 API Key 和模型
"""

import os
os.environ['DASHSCOPE_API_KEY'] = 'sk-1d3af48425824e41981816390583d437'

from dashscope import VideoSynthesis

print("🔑 API Key: sk-1d3af48425824e41981816390583d437")

# 测试 1: 列出所有可用模型（通过调用失败信息）
print("\n📋 尝试调用，查看错误信息中的可用模型...")
response = VideoSynthesis.call(
    model='wanx-video-01',
    prompt='测试',
    size='1280*720',
    duration=3
)

print(f"状态码: {response.status_code}")
print(f"消息: {response.message}")
print(f"错误码: {response.code}")
print(f"完整响应: {response}")
