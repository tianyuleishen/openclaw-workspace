#!/usr/bin/env python3
"""
直接调用通义万相API生成图片
"""

import os
import requests
import json

API_KEY = "sk-1d3af48425824e41981816390583d437"

print("🦞 直接调用通义万相API")
print("="*60)

# 文生图API
url = "https://dashscope.aliyuncs.com/compatible-mode/v1/images/generations"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "wanx-style-pixel",
    "prompt": "Cute little lobster character in virtual office, holographic screens, neon lights, 9:16",
    "size": "720*1280",
    "style": "动漫"
}

print("\n📤 发送请求...")
response = requests.post(url, headers=headers, json=data, timeout=60)

print(f"📥 响应状态: {response.status_code}")

if response.status_code == 200:
    result = response.json()
    print("✅ 成功!")
    print(json.dumps(result, indent=2, ensure_ascii=False)[:500])
else:
    print(f"❌ 失败: {response.status_code}")
    print(response.text[:500])
