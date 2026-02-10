#!/usr/bin/env python3
"""
元宇宙虚拟办公室 - 首尾帧视频生成测试
分辨率: 720p | 9:16 | 15秒 | 首尾帧
使用通义万相SDK
"""

import os
import sys
import dashscope
from dashscope import ImageSynthesis, VideoSynthesis

# 设置API密钥
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY", "sk-1d3af48425824e41981816390583d437")

print("🦞 元宇宙虚拟办公室 - 首尾帧生成")
print("="*60)

# 首帧提示词（工作中）
START_PROMPT = """Cute little lobster AI mascot character '小爪' in a futuristic virtual office, holographic computer screens floating around, neon lights, cyberpunk aesthetic, working on AI code, 9:16 vertical aspect ratio, high tech atmosphere, front view, cute style"""

# 末帧提示词（完成工作）
END_PROMPT = """Cute little lobster AI mascot character '小爪' in a futuristic virtual office, holographic screens showing completed code, neon lights, cyberpunk aesthetic, raising claw in victory, happy expression, high tech atmosphere, 9:16 vertical aspect ratio, cute style"""

def generate_image(prompt, filename):
    """生成图片"""
    print(f"\n🎨 生成图片: {filename}")
    print(f"   Prompt: {prompt[:80]}...")
    print(f"   尺寸: 720*1280 (9:16)")
    
    try:
        response = ImageSynthesis.call(
            model='wanx-image-generation',
            prompt=prompt,
            size='720*1280',  # 9:16竖屏
            style='动漫'  # 使用动漫风格更可爱
        )
        
        if response.status_code == 200:
            # 获取图片URL
            image_url = response.output['task_results'][0]['images'][0]['url']
            print(f"✅ 生成成功!")
            print(f"   URL: {image_url[:80]}...")
            return image_url
        else:
            print(f"❌ 生成失败: {response.status_code}")
            print(f"   错误: {response.message}")
            return None
            
    except Exception as e:
        print(f"❌ 异常: {e}")
        return None

def main():
    print("\n📝 视频配置:")
    print(f"   场景: 元宇宙虚拟办公室")
    print(f"   分辨率: 720x1280 (9:16)")
    print(f"   时长: 15秒")
    print(f"   技术: 首尾帧")
    print(f"   文案: '元宇宙搬砖第一天~'")
    print()
    
    # 生成首帧
    start_image = generate_image(START_PROMPT, "office_start")
    
    # 生成末帧
    end_image = generate_image(END_PROMPT, "office_end")
    
    if start_image and end_image:
        print("\n" + "="*60)
        print("✅ 首尾帧已生成!")
        print()
        print("🎬 接下来:")
        print("   1. 访问通义万相控制台:")
        print("      https://tongyi.aliyun.com/wanxiang/")
        print()
        print("   2. 选择'图生视频' -> '首尾帧'模式")
        print()
        print("   3. 上传图片:")
        print(f"      首帧: {start_image[:60]}...")
        print(f"      末帧: {end_image[:60]}...")
        print()
        print("   4. 设置参数:")
        print("      时长: 15秒")
        print("      分辨率: 720p")
        print()
        print("   5. 生成视频后下载")
        print("="*60)
    
    print("\n💰 成本对比:")
    print("   方案A (首尾帧): ¥0.02×2 + ¥0.02 = ¥0.06")
    print("   方案B (单图生视频): ¥0.05×2 = ¥0.10")
    print("   节省: 40%")
    
    return start_image, end_image

if __name__ == "__main__":
    main()
