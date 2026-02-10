#!/usr/bin/env python3
"""
小爪日常 - 标准版视频生成器
分辨率: 720p (1280x720)
比例: 9:16 (720x1280)
技术: 首尾帧技术（更便宜）
"""

import os
import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/scripts')
from tongyi_api import generate_image, TongyiAPI

class ClawletStandardGenerator:
    """小爪标准版视频生成器"""
    
    def __init__(self):
        self.api = TongyiAPI()
        
        # 标准版配置（更便宜）
        self.config = {
            # 9:16竖屏 (720x1280) - 抖音标准比例
            "width": 720,
            "height": 1280,
            # 首尾帧技术 - 只生成2张关键帧
            "video_duration": 15,  # 15秒短视频
            "fps": 24,
            "use_keyframes_only": True,  # 只生成首尾帧，中间AI插值
        }
        
        # 视频主题模板
        self.templates = {
            "morning": {
                "name": "早安篇",
                "prompt": "Cute little lobster AI mascot character, '小爪', morning scene, soft sunrise lighting, stretching pose, warm cozy atmosphere, 9:16 vertical aspect ratio",
                "keyframe_start": "小爪早上醒来,阳光从窗户照进来,伸懒腰的可爱姿势,温馨治愈",
                "keyframe_end": "小爪元气满满,举起爪子说早安,背景是温暖晨光,充满希望",
                "duration": 15,
                "style": "治愈系"
            },
            "working": {
                "name": "工作篇", 
                "prompt": "Cute little lobster AI mascot character, '小爪', working at computer, coding, tech startup atmosphere, productivity, 9:16 vertical aspect ratio",
                "keyframe_start": "小爪认真盯着电脑屏幕,显示代码,专注工作的表情,科技感",
                "keyframe_end": "小爪完成工作,举起爪子比胜利,身后显示已完成的任务,成就感",
                "duration": 15,
                "style": "科技感"
            },
            "cooking": {
                "name": "美食篇",
                "prompt": "Cute little lobster AI mascot character, '小爪', cooking in kitchen, adorable chef hat, delicious food, 9:16 vertical aspect ratio",
                "keyframe_start": "小爪穿着小围裙,正在切菜,认真可爱的表情,厨房场景",
                "keyframe_end": "小爪端着完成的美食,满意地笑着,看起来很好吃的样子",
                "duration": 15,
                "style": "温馨美食"
            },
            "playing": {
                "name": "玩耍篇",
                "prompt": "Cute little lobster AI mascot character, '小爪', playing with toys, fun and energetic, bright colors, 9:16 vertical aspect ratio",
                "keyframe_start": "小爪在玩具堆里,兴奋地蹦蹦跳跳,充满活力的样子",
                "keyframe_end": "小爪躺在玩具中间,满足地笑着,幸福的画面",
                "duration": 15,
                "style": "萌系可爱"
            },
            "learning": {
                "name": "学习篇",
                "prompt": "Cute little lobster AI mascot character, '小爪', studying, reading books, curiosity, library or study room, 9:16 vertical aspect ratio",
                "keyframe_start": "小爪认真看书,大眼睛充满好奇,沉浸在知识的海洋中",
                "keyframe_end": "小爪学会新知识,开心地举起爪子,灯泡亮起的灵感瞬间",
                "duration": 15,
                "style": "学习成长"
            }
        }
    
    def generate_keyframe(self, prompt, filename):
        """生成关键帧图片"""
        print(f"🎨 生成关键帧: {filename}")
        print(f"   Prompt: {prompt[:50]}...")
        
        image_path = generate_image(
            prompt=prompt,
            width=self.config["width"],
            height=self.config["height"],
            output_path=f"/tmp/{filename}.png"
        )
        
        if image_path:
            print(f"✅ 成功: /tmp/{filename}.png")
            return image_path
        else:
            print(f"❌ 失败: {filename}")
            return None
    
    def generate_video_from_keyframes(self, start_image, end_image, output_name, duration=15):
        """
        使用首尾帧技术生成视频
        从首帧渐变到末帧，中间由AI插值
        成本更低（只需2张图片）
        """
        from wanxiang_video import generate_video
        
        print(f"\n🎬 生成视频: {output_name}")
        print(f"   首帧: {start_image}")
        print(f"   末帧: {end_image}")
        print(f"   时长: {duration}秒")
        print(f"   技术: 首尾帧插值（经济版）")
        
        video_path = generate_video(
            start_image=start_image,
            end_image=end_image,
            duration=duration,
            output_path=f"/tmp/{output_name}.mp4"
        )
        
        if video_path:
            print(f"✅ 视频生成成功: {video_path}")
            return video_path
        else:
            print(f"❌ 视频生成失败")
            return None
    
    def generate_content_video(self, theme="morning"):
        """生成一个完整的主题视频"""
        if theme not in self.templates:
            print(f"❌ 未知主题: {theme}")
            return None
        
        template = self.templates[theme]
        print(f"\n{'='*50}")
        print(f"🎯 生成主题: {template['name']}")
        print(f"   风格: {template['style']}")
        print(f"   时长: {template['duration']}秒")
        print(f"{'='*50}")
        
        # 1. 生成首帧
        start_image = self.generate_keyframe(
            template["keyframe_start"],
            f"clawlet_{theme}_start"
        )
        
        if not start_image:
            return None
        
        # 2. 生成末帧
        end_image = self.generate_keyframe(
            template["keyframe_end"],
            f"clawlet_{theme}_end"
        )
        
        if not end_image:
            return None
        
        # 3. 使用首尾帧技术生成视频
        video_path = self.generate_video_from_keyframes(
            start_image,
            end_image,
            f"clawlet_{theme}_standard",
            template["duration"]
        )
        
        return video_path
    
    def generate_morning_video(self):
        """生成早安视频"""
        return self.generate_content_video("morning")
    
    def generate_working_video(self):
        """生成工作视频"""
        return self.generate_content_video("working")
    
    def generate_cooking_video(self):
        """生成美食视频"""
        return self.generate_content_video("cooking")
    
    def generate_playing_video(self):
        """生成玩耍视频"""
        return self.generate_content_video("playing")
    
    def generate_learning_video(self):
        """生成学习视频"""
        return self.generate_content_video("learning")
    
    def batch_generate(self, themes=None):
        """批量生成多个主题视频"""
        if themes is None:
            themes = ["morning", "working", "cooking", "playing", "learning"]
        
        results = {}
        for theme in themes:
            video_path = self.generate_content_video(theme)
            results[theme] = video_path
        
        # 生成汇总报告
        print(f"\n{'='*50}")
        print(f"📊 批量生成完成")
        print(f"{'='*50}")
        for theme, path in results.items():
            status = "✅" if path else "❌"
            print(f"   {status} {self.templates[theme]['name']}: {path}")
        
        return results


# 使用示例
if __name__ == "__main__":
    generator = ClawletStandardGenerator()
    
    print("🦞 小爪标准版视频生成器")
    print("="*50)
    print("配置:")
    print(f"   分辨率: {generator.config['width']}x{generator.config['height']}")
    print(f"   比例: 9:16 (竖屏)")
    print(f"   技术: 首尾帧")
    print(f"   时长: {generator.config['video_duration']}秒")
    print("="*50)
    
    # 使用示例
    print("\n使用方法:")
    print("1. 生成单个视频:")
    print("   generator.generate_morning_video()  # 早安")
    print("   generator.generate_working_video()  # 工作")
    print()
    print("2. 批量生成:")
    print("   generator.batch_generate(['morning', 'working'])")
    print()
    print("3. 自定义主题:")
    print("   generator.generate_content_video('cooking')")
