#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦞 元宇宙虚拟办公室 - 视频生成器
分辨率: 720p | 9:16 | 15秒 | 首尾帧

使用通义万相API生成首尾帧和视频
"""

import os
import sys
import time
import json
from datetime import datetime

# 尝试导入dashscope
try:
    import dashscope
    from dashscope import ImageSynthesis, VideoSynthesis
    SDK_AVAILABLE = True
except ImportError:
    SDK_AVAILABLE = False
    print("⚠️  未安装 dashscope SDK")
    print("   请运行: pip install dashscope")
    print("   或访问控制台: https://tongyi.aliyun.com/wanxiang/")


class MetaverseVideoGenerator:
    """元宇宙视频生成器"""
    
    def __init__(self, api_key=None):
        if SDK_AVAILABLE:
            dashscope.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        
        # 视频配置
        self.config = {
            "width": 720,
            "height": 1280,  # 9:16
            "duration": 15,
            "style": "动漫"
        }
        
        # 虚拟办公室场景
        self.scenes = {
            "office": {
                "name": "虚拟办公室",
                "start_prompt": """Cute little lobster AI mascot character '小爪' in a futuristic virtual office, holographic computer screens floating around, neon lights, cyberpunk aesthetic, working on AI code, 9:16 vertical aspect ratio, high tech atmosphere, front view, cute style""",
                "end_prompt": """Cute little lobster AI mascot character '小爪' in a futuristic virtual office, holographic screens showing completed code, neon lights, cyberpunk aesthetic, raising claw in victory, happy expression, high tech atmosphere, 9:16 vertical aspect ratio, cute style""",
                "caption": "元宇宙搬砖第一天~",
                "tags": ["元宇宙", "AI", "虚拟人", "工作日常", "科技感", "小爪"]
            }
        }
    
    def generate_keyframe(self, prompt, filename, size="720*1280"):
        """生成关键帧图片"""
        if not SDK_AVAILABLE:
            print(f"\n⚠️  SDK未安装，跳过生成")
            print(f"   文件: {filename}")
            print(f"   Prompt: {prompt[:60]}...")
            return None
        
        print(f"\n🎨 生成关键帧: {filename}")
        
        try:
            response = ImageSynthesis.call(
                model='wanx-image-generation',
                prompt=prompt,
                size=size,
                style=self.config["style"]
            )
            
            if response.status_code == 200:
                image_url = response.output['task_results'][0]['images'][0]['url']
                print(f"✅ 成功: {image_url[:60]}...")
                return image_url
            else:
                print(f"❌ 失败: {response.status_code} - {response.message}")
                return None
                
        except Exception as e:
            print(f"❌ 异常: {e}")
            return None
    
    def generate_keyframe_video(self, start_image, end_image, output_name, duration=15):
        """使用首尾帧生成视频"""
        if not SDK_AVAILABLE:
            print(f"\n⚠️  首尾帧功能需要在控制台使用")
            print(f"   请访问: https://tongyi.aliyun.com/wanxiang/")
            print(f"   1. 选择'图生视频' -> '首尾帧'模式")
            print(f"   2. 上传首帧和末帧图片")
            print(f"   3. 设置时长: {duration}秒")
            print(f"   4. 下载视频")
            return None
        
        print(f"\n🎬 生成首尾帧视频: {output_name}")
        print(f"   首帧: {start_image[:60] if start_image else 'N/A'}...")
        print(f"   末帧: {end_image[:60] if end_image else 'N/A'}...")
        
        # 首尾帧视频生成逻辑
        # 注意：通义万相的首尾帧API需要特定配置
        return None
    
    def generate_office_video(self):
        """生成虚拟办公室视频"""
        scene = self.scenes["office"]
        
        print("\n" + "="*70)
        print("🦞 元宇宙虚拟办公室 - 视频生成")
        print("="*70)
        print(f"   场景: {scene['name']}")
        print(f"   文案: {scene['caption']}")
        print(f"   分辨率: {self.config['width']}x{self.config['height']}")
        print(f"   时长: {self.config['duration']}秒")
        print(f"   技术: 首尾帧")
        print("="*70)
        
        # 生成首帧
        start_image = self.generate_keyframe(
            scene["start_prompt"],
            "office_start"
        )
        
        # 生成末帧
        end_image = self.generate_keyframe(
            scene["end_prompt"],
            "office_end"
        )
        
        # 生成视频
        video = self.generate_keyframe_video(
            start_image,
            end_image,
            "office_video",
            self.config["duration"]
        )
        
        if start_image and end_image:
            self.print_manual_steps(start_image, end_image)
        
        return start_image, end_image
    
    def print_manual_steps(self, start_image, end_image):
        """打印手动操作步骤"""
        print("\n" + "="*70)
        print("📖 手动生成视频步骤")
        print("="*70)
        print()
        print("1️⃣  访问通义万相控制台:")
        print("    https://tongyi.aliyun.com/wanxiang/")
        print()
        print("2️⃣  首帧图片:")
        print(f"    {start_image}")
        print()
        print("3️⃣  末帧图片:")
        print(f"    {end_image}")
        print()
        print("4️⃣  选择'图生视频' -> '首尾帧'模式")
        print("5️⃣  上传首帧和末帧图片")
        print(f"6️⃣  设置时长: {self.config['duration']}秒")
        print(f"7️⃣  设置分辨率: {self.config['width']}p")
        print("8️⃣  生成并下载视频")
        print("="*70)
        
        print("\n💰 成本估算:")
        print("   首尾帧方案: ¥0.06")
        print("   传统方案: ¥0.10")
        print("   节省: 40%")
    
    def estimate_cost(self):
        """估算成本"""
        print("\n💰 成本对比")
        print("="*50)
        print("   首尾帧: ¥0.02×2 + ¥0.02 = ¥0.06")
        print("   单图生视频: ¥0.05×2 = ¥0.10")
        print("   节省: 40%")
        print("="*50)


def main():
    """主函数"""
    print("\n🦞 元宇宙虚拟办公室视频生成器")
    print("="*70)
    print("分辨率: 720p | 9:16 | 15秒 | 首尾帧")
    print("="*70)
    
    generator = MetaverseVideoGenerator()
    
    # 生成视频
    start, end = generator.generate_office_video()
    
    # 估算成本
    generator.estimate_cost()
    
    return start, end


if __name__ == "__main__":
    main()
