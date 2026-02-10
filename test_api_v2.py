#!/usr/bin/env python3
"""
使用正确的通义万相API格式
"""

import os
import requests
import json

API_KEY = "sk-1d3af48425824e41981816390583d437"

print("🦞 测试通义万相API")
print("="*60)

# 尝试多种API格式

# 格式1: OpenAI兼容格式
urls_to_try = [
    "https://dashscope.aliyuncs.com/compatible-mode/v1/images/generations",
    "https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation",
    "https://api.tongyi.aliyun.com/v1/images/generations",
]

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "wanx-image-generation",
    "prompt": "Cute little lobster in virtual office, 9:16 aspect ratio",
    "size": "720*1280"
}

for url in urls_to_try:
    print(f"\n尝试: {url[:60]}...")
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        print(f"状态: {response.status_code}")
        if response.status_code in [200, 400, 401, 404]:
            print(f"响应: {response.text[:200]}")
    except Exception as e:
        print(f"异常: {e}")

print("\n" + "="*60)
print("💡 提示：如果API不通，请直接在浏览器访问:")
print("   https://tongyi.aliyun.com/wanxiang/")
print("   手动生成图片后下载")
