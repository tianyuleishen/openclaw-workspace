#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦞 元宇宙虚拟办公室视频 - 最终生成器
"""

import os
import sys

# 加载API密钥
if os.path.exists('/home/admin/.openclaw/workspace/.env'):
    with open('/home/admin/.openclaw/workspace/.env') as f:
        for line in f:
            if '=' in line and 'API_KEY' in line:
                os.environ[line.split('=')[0].strip()] = line.split('=')[1].strip()

API_KEY = os.getenv("DASHSCOPE_API_KEY", "")

print("="*70)
print("🦞 元宇宙虚拟办公室视频生成")
print("="*70)
print(f"🔑 API密钥: {API_KEY[:15]}...")
print()

# 尝试dashscope SDK
try:
    import dashscope
    from dashscope import ImageSynthesis, VideoSynthesis
    dashscope.api_key = API_KEY
    
    print("✅ dashscope SDK可用")
    print()
    
    # 生成图片
    print("📤 步骤1: 生成图片...")
    response = ImageSynthesis.call(
        model='wanx-image-generation',
        prompt='Cute little red lobster AI mascot "小爪" in futuristic virtual office, holographic screens, neon lights, cyberpunk, anime style, 9:16 vertical',
        size='720*1280',
        style='动漫'
    )
    
    if response.status_code == 200:
        image_url = response.output['task_results'][0]['images'][0]['url']
        print(f"✅ 图片生成成功: {image_url[:60]}...")
        print()
        print("📤 步骤2: 生成视频...")
        
        # 生成视频
        video_resp = VideoSynthesis.call(
            model='wan2.6-i2v-flash',
            input={'image_url': image_url},
            parameters={'duration': 15, 'size': '720*1280'}
        )
        
        if video_resp.status_code == 200:
            video_url = video_resp.output.get('video_url', '')
            print(f"✅ 视频生成成功!")
            print(f"📥 下载地址: {video_url}")
        else:
            print(f"❌ 视频生成失败: {video_resp.message}")
    else:
        print(f"❌ 图片生成失败: {response.status_code} - {response.message}")
        
except ImportError:
    print("❌ dashscope SDK未安装")
    print("\n💡 安装方法: pip install dashscope")
    print("\n🎯 或者直接在官网生成:")
    print("   https://tongyi.aliyun.com/wanxiang/")
    print()
    print("📝 提示词:")
    print("   Cute little red lobster '小爪' in virtual office,")
    print("   holographic screens, neon lights, cyberpunk,")
    print("   anime, 9:16 vertical, 15 seconds")

print()
print("="*70)
print("💰 成本: ¥0.30 (wan2.1-t2v-1.3b)")
print("="*70)
