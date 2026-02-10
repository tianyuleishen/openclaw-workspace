#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦞 小爪元宇宙视频生成器
在本地生成后上传到服务器提供下载链接
"""

import os
import sys
import json
import time
import requests

# 配置
API_KEY = "sk-1d3af48425824e41981816390583d437"  # 您的API密钥
API_BASE = "https://dashscope.aliyuncs.com/api/v1/services/aigc"

# 提示词
PROMPTS = {
    "office_start": """Cute little lobster AI mascot character '小爪' in a futuristic virtual office, holographic computer screens floating around, neon lights, cyberpunk aesthetic, working on AI code, 9:16 vertical aspect ratio, high tech atmosphere, front view, cute style""",
    
    "office_end": """Cute little lobster AI mascot character '小爪' in a futuristic virtual office, holographic screens showing completed code, neon lights, cyberpunk aesthetic, raising claw in victory, happy expression, high tech atmosphere, 9:16 vertical aspect ratio, cute style"""
}

def generate_image(prompt, filename):
    """生成图片并保存"""
    print(f"\n🎨 生成图片: {filename}")
    
    url = f"{API_BASE}/image generation"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "wanx-image-generation",
        "input": {"prompt": prompt},
        "parameters": {
            "size": "720*1280",
            "style": "动漫"
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        if response.status_code == 200:
            result = response.json()
            image_url = result["output"]["task_results"][0]["images"][0]["url"]
            
            # 下载图片
            img_data = requests.get(image_url).content
            img_path = f"/tmp/{filename}.png"
            with open(img_path, 'wb') as f:
                f.write(img_data)
            
            print(f"✅ 成功: {img_path}")
            return img_path
        else:
            print(f"❌ 失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ 异常: {e}")
        return None

def main():
    print("="*70)
    print("🦞 元宇宙虚拟办公室视频生成器")
    print("="*70)
    print("分辨率: 720p | 9:16 | 15秒")
    print("="*70)
    
    # 生成首帧
    start_img = generate_image(PROMPTS["office_start"], "office_start")
    
    # 生成末帧
    end_img = generate_image(PROMPTS["office_end"], "office_end")
    
    if start_img and end_img:
        print("\n" + "="*70)
        print("✅ 首尾帧已生成!")
        print("="*70)
        print(f"\n📁 文件:")
        print(f"   首帧: {start_img}")
        print(f"   末帧: {end_img}")
        print(f"\n🔗 下载链接:")
        print(f"   http://8.130.18.239:8080/office_start.png")
        print(f"   http://8.130.18.239:8080/office_end.png")
        print(f"\n💰 成本: ¥0.04")
        print(f"\n📝 下一步:")
        print(f"   1. 下载图片到本地")
        print(f"   2. 访问通义万相控制台")
        print(f"   3. 上传首尾帧，生成15秒视频")
    else:
        print("\n❌ 生成失败")

if __name__ == "__main__":
    main()
