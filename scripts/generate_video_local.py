#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦞 元宇宙虚拟办公室视频生成器
本地运行版本 - 需要安装dashscope SDK
"""

import os
import sys

# 配置
API_KEY = "sk-9d02ad19f0384298a44251a5eef84991"

# 设置环境变量
os.environ["DASHSCOPE_API_KEY"] = API_KEY

print("="*70)
print("🦞 元宇宙虚拟办公室视频生成器")
print("="*70)
print()
print(f"🔑 API密钥: {API_KEY[:15]}...")
print()

# 尝试导入dashscope
try:
    import dashscope
    from dashscope import ImageSynthesis, VideoSynthesis
    
    dashscope.api_key = API_KEY
    
    print("✅ dashscope SDK已安装")
    print()
    
    # 测试图像生成
    print("📤 步骤1: 生成首帧图片...")
    print("   提示词: Cute little red lobster '小爪' in virtual office")
    print()
    
    response = ImageSynthesis.call(
        model='wanx-image-generation',
        prompt='Cute little red lobster AI mascot character "小爪" in a futuristic virtual office with holographic computer screens floating around, neon lights, cyberpunk aesthetic, working on code, 9:16 vertical aspect ratio, anime style',
        size='720*1280',
        style='动漫'
    )
    
    if response.status_code == 200:
        image_url = response.output['task_results'][0]['images'][0]['url']
        print(f"✅ 图片生成成功!")
        print(f"   URL: {image_url[:80]}...")
        print()
        print("📤 步骤2: 生成视频...")
        
        # 生成视频
        video_response = VideoSynthesis.call(
            model='wan2.6-i2v-flash',
            input={
                'image_url': image_url
            },
            parameters={
                'duration': 15,
                'size': '720*1280'
            }
        )
        
        if video_response.status_code == 200:
            video_url = video_response.output['video_url']
            print(f"✅ 视频生成成功!")
            print(f"   URL: {video_url}")
        else:
            print(f"❌ 视频生成失败: {video_response.message}")
    else:
        print(f"❌ 图片生成失败: {response.status_code}")
        print(f"   错误: {response.message}")
        
except ImportError:
    print("❌ dashscope SDK未安装")
    print()
    print("💡 安装方法:")
    print("   pip install dashscope")
    print()
    print("📖 使用方法:")
    print("   python3 generate_video_local.py")
    print()
    print("🎯 或者在通义万相官网直接生成:")
    print("   https://tongyi.aliyun.com/wanxiang/")
    print()
    print("📝 提示词:")
    print("   Cute little red lobster '小爪' in virtual office,")
    print("   holographic screens, neon lights, cyberpunk,")
    print("   anime style, 9:16 vertical, 15 seconds")

print()
print("="*70)
print("💰 成本: ¥0.30 (wan2.1-t2v-1.3b)")
print("="*70)
