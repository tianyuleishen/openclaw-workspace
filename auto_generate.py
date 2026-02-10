#!/usr/bin/env python3
"""
自动生成元宇宙视频脚本
使用通义万相API
"""

import os
import requests
import json
import base64
from datetime import datetime

API_KEY = "sk-1d3af48425824e41981816390583d437"

def generate_with_bailian():
    """使用百炼API"""
    print("\n🦞 使用阿里云百炼API生成...")
    
    # 百炼文生图API
    url = "https://bailian.aliyuncs.com/v2/image/generate"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "wanx-image-generation",
        "prompt": "Cute little lobster character in virtual office, 9:16, anime style",
        "size": "720*1280"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        print(f"状态: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 成功!")
            print(json.dumps(result, indent=2, ensure_ascii=False)[:500])
            return True
        else:
            print(f"响应: {response.text[:300]}")
            return False
    except Exception as e:
        print(f"异常: {e}")
        return False

def main():
    print("="*70)
    print("🦞 元宇宙虚拟办公室视频生成器")
    print("="*70)
    
    # 尝试使用百炼API
    success = generate_with_bailian()
    
    if not success:
        print("\n" + "="*70)
        print("⚠️  API暂不可用，请手动生成:")
        print("="*70)
        print("\n📖 操作步骤:")
        print("   1. 访问: https://tongyi.aliyun.com/wanxiang/")
        print("   2. 文生图 → 720×1280 → 动漫风格")
        print("   3. 首帧提示词:")
        print("      Cute little lobster in virtual office, holographic screens")
        print("   4. 末帧提示词:")
        print("      Cute little lobster in virtual office, victory pose")
        print("   5. 图生视频 → 首尾帧 → 15秒 → 720p")
        print("\n💰 预计成本: ¥0.06")
        print("="*70)

if __name__ == "__main__":
    main()
