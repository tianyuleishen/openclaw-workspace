#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦞 元宇宙虚拟办公室视频生成器
直接在本地生成视频，提供下载链接
"""

import os
import sys

# 检查dashscope
try:
    import dashscope
    from dashscope import ImageSynthesis, VideoSynthesis
    DASHSCOPE_AVAILABLE = True
    print("✅ dashscope 已安装")
except ImportError:
    DASHSCOPE_AVAILABLE = False
    print("❌ dashscope 未安装")

# 设置API密钥
if DASHSCOPE_AVAILABLE:
    dashscope.api_key = os.getenv("DASHSCOPE_API_KEY", "sk-1d3af48425824e41981816390583d437")

print("\n" + "="*70)
print("🦞 元宇宙虚拟办公室视频生成器")
print("="*70)

# 提示词
START_PROMPT = """Cute little lobster AI mascot character '小爪' in a futuristic virtual office, holographic computer screens floating around, neon lights, cyberpunk aesthetic, working on AI code, 9:16 vertical aspect ratio, high tech atmosphere, front view, cute style"""

END_PROMPT = """Cute little lobster AI mascot character '小爪' in a futuristic virtual office, holographic screens showing completed code, neon lights, cyberpunk aesthetic, raising claw in victory, happy expression, high tech atmosphere, 9:16 vertical aspect ratio, cute style"""

def generate_image(prompt, filename):
    """生成图片"""
    if not DASHSCOPE_AVAILABLE:
        print(f"\n⚠️  无法生成图片: dashscope未安装")
        return None
    
    print(f"\n🎨 生成图片: {filename}")
    
    try:
        response = ImageSynthesis.call(
            model='wanx-image-generation',
            prompt=prompt,
            size='720*1280',
            style='动漫'
        )
        
        if response.status_code == 200:
            image_url = response.output['task_results'][0]['images'][0]['url']
            print(f"✅ 成功: {image_url[:60]}...")
            
            # 下载图片
            import requests
            img_data = requests.get(image_url).content
            img_path = f"/tmp/{filename}.png"
            with open(img_path, 'wb') as f:
                f.write(img_data)
            print(f"📁 保存: {img_path}")
            return img_path
        else:
            print(f"❌ 失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ 异常: {e}")
        return None

def main():
    print("\n📝 视频配置:")
    print("   场景: 元宇宙虚拟办公室")
    print("   分辨率: 720p (720×1280)")
    print("   比例: 9:16 竖屏")
    print("   时长: 15秒")
    print("   技术: 首尾帧")
    
    # 生成首帧
    start_img = generate_image(START_PROMPT, "office_start")
    
    # 生成末帧
    end_img = generate_image(END_PROMPT, "office_end")
    
    if start_img and end_img:
        print("\n" + "="*70)
        print("✅ 首尾帧已生成!")
        print("="*70)
        print(f"\n📁 文件位置:")
        print(f"   首帧: {start_img}")
        print(f"   末帧: {end_img}")
        print(f"\n🔗 下载链接:")
        print(f"   http://8.130.18.239:8080/office_start.png")
        print(f"   http://8.130.18.239:8080/office_end.png")
        print(f"\n💰 成本: ¥0.04 (首帧+末帧)")
    else:
        print("\n❌ 图片生成失败")

if __name__ == "__main__":
    main()
