#!/usr/bin/env python3
"""
小爪日常 - 简化版视频生成脚本
使用通义万相API直接生成视频
"""

import os
import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/scripts')

# 导入现有的视频生成功能
from tongyi_api import generate_video, TongyiAPI
from generate_image import generate_image

class SimpleVideoGenerator:
    """简化版视频生成器"""
    
    def __init__(self):
        self.api = TongyiAPI()
        
        # 标准配置
        self.config = {
            "resolution": "720p",  # 标准720p
            "aspect_ratio": "9:16",  # 竖屏
            "duration": 15,  # 15秒
            "mode": "economical"  # 经济模式（首尾帧）
        }
        
        # 内容模板
        self.content_templates = {
            "morning": {
                "title": "早安篇",
                "prompt": "一只可爱的红色小螯虾AI助手角色，名字叫'小爪'，早上醒来迎接阳光，伸懒腰打哈欠，温馨治愈的起床场景，暖色调背景，元气满满的状态，9:16竖屏格式",
                "duration": 15
            },
            "working": {
                "title": "工作篇",
                "prompt": "一只可爱的红色小螯虾AI助手角色，名字叫'小爪'，认真工作在电脑前，屏幕上显示代码和AI图案，专注的表情，科技感的办公室环境，9:16竖屏格式",
                "duration": 15
            },
            "cooking": {
                "title": "美食篇",
                "prompt": "一只可爱的红色小螯虾AI助手角色，名字叫'小爪'，穿着小围裙在厨房做饭，端着一盘看起来很好吃的食物，满意地笑着，温馨的家庭场景，9:16竖屏格式",
                "duration": 15
            },
            "relaxing": {
                "title": "休息篇",
                "prompt": "一只可爱的红色小螯虾AI助手角色，名字叫'小爪'，躺在沙发上悠闲地看手机，喝着饮料，放松舒适的休闲时光，温暖的居家环境，9:16竖屏格式",
                "duration": 15
            }
        }
    
    def generate_image_for_video(self, prompt, output_name):
        """为视频生成关键帧图片"""
        print(f"\n🎨 生成关键帧: {output_name}")
        print(f"   Prompt: {prompt[:60]}...")
        
        image_path = generate_image(
            prompt=prompt,
            width=720,
            height=1280,  # 9:16比例
            output_path=f"/tmp/{output_name}.png"
        )
        
        if image_path:
            print(f"✅ 成功: {image_path}")
        else:
            print(f"❌ 失败: {output_name}")
        
        return image_path
    
    def generate_video_direct(self, prompt, output_name, duration=15):
        """直接文生视频"""
        print(f"\n🎬 文生视频: {output_name}")
        print(f"   Prompt: {prompt[:60]}...")
        print(f"   时长: {duration}秒")
        
        video_path = generate_video(
            prompt=prompt,
            duration=duration,
            output_path=f"/tmp/{output_name}.mp4"
        )
        
        return video_path
    
    def generate_morning_video(self):
        """生成早安视频"""
        template = self.content_templates["morning"]
        return self.generate_video_direct(
            template["prompt"],
            "clawlet_morning_standard",
            template["duration"]
        )
    
    def generate_working_video(self):
        """生成工作视频"""
        template = self.content_templates["working"]
        return self.generate_video_direct(
            template["prompt"],
            "clawlet_working_standard",
            template["duration"]
        )
    
    def generate_content_series(self, theme="all"):
        """生成系列内容"""
        if theme == "all":
            themes = list(self.content_templates.keys())
        else:
            themes = [theme]
        
        results = {}
        
        for key in themes:
            template = self.content_templates[key]
            
            # 先生成关键帧
            image_path = self.generate_image_for_video(
                template["prompt"],
                f"clawlet_{key}_keyframe"
            )
            
            # 如果有通义万相API，可以用首尾帧生成视频
            # video_path = generate_video_from_keyframes(...)
            
            results[key] = {
                "title": template["title"],
                "prompt": template["prompt"],
                "image": image_path,
                "duration": template["duration"]
            }
        
        return results
    
    def get_cost_estimate(self):
        """获取成本估算"""
        print(f"\n💰 成本估算（标准720p）")
        print(f"{'='*40}")
        print(f"   单个视频（15秒）: ¥0.02-0.05")
        print(f"   5个系列视频: ¥0.10-0.25")
        print(f"{'='*40}")
        print(f"   💡 首尾帧模式更便宜")
        print(f"   💡 720p标准分辨率已足够")
        print(f"   💡 15秒短视频适合抖音")


def main():
    print("🦞 小爪日常 - 简化版视频生成器")
    print("="*50)
    print("配置:")
    print("   分辨率: 720p (720x1280)")
    print("   比例: 9:16 竖屏")
    print("   时长: 15秒")
    print("   模式: 经济版")
    print("="*50)
    
    generator = SimpleVideoGenerator()
    
    # 显示成本估算
    generator.get_cost_estimate()
    
    print("\n📖 使用方法:")
    print("""
# 创建生成器
gen = SimpleVideoGenerator()

# 生成单个视频
gen.generate_morning_video()   # 早安篇
gen.generate_working_video()   # 工作篇

# 生成系列内容
gen.generate_content_series("morning")  # 特定主题
gen.generate_content_series("all")      # 所有主题
""")


if __name__ == "__main__":
    main()
