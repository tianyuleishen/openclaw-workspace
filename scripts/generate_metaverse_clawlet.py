#!/usr/bin/env python3
"""
🦞 元宇宙版小爪 - 虚拟环境视频生成器
在小爪的虚拟世界中生成卖萌日常
"""

class MetaverseClawletGenerator:
    """元宇宙小爪视频生成器"""
    
    def __init__(self):
        # 配置
        self.config = {
            "width": 720,
            "height": 1280,  # 9:16竖屏
            "duration": 15,  # 15秒
            "style": "metaverse + cute"
        }
        
        # 元宇宙场景模板
        self.scenes = {
            "virtual_office": {
                "name": "虚拟办公室",
                "prompt": "Cute little lobster AI mascot character '小爪' in a futuristic virtual office, holographic computer screens floating around, neon lights, cyberpunk aesthetic, working on AI code, 9:16 vertical aspect ratio, high tech atmosphere",
                "story": "小爪在元宇宙办公室中工作~",
                "mood": "科技感+认真"
            },
            "beach_vacation": {
                "name": "虚拟海滩",
                "prompt": "Cute little lobster AI mascot character '小爪' on a beautiful virtual beach, tropical paradise, crystal clear water, golden sand, palm trees, sunset lighting, relaxed summer vibe, 9:16 vertical aspect ratio",
                "story": "小爪在元宇宙海滩度假~",
                "mood": "放松+治愈"
            },
            "space_station": {
                "name": "虚拟太空站",
                "prompt": "Cute little lobster AI mascot character '小爪' in a cozy virtual space station, looking out at planet Earth through large windows, stars floating outside, cozy interior with soft lighting, futuristic yet warm atmosphere, 9:16 vertical aspect ratio",
                "story": "小爪在太空站看地球~",
                "mood": "浪漫+震撼"
            },
            "gaming_room": {
                "name": "虚拟游戏房",
                "prompt": "Cute little lobster AI mascot character '小爪' in a fun virtual gaming room, surrounded by retro arcade machines, neon game posters, comfortable bean bags, playing video games, energetic and playful atmosphere, 9:16 vertical aspect ratio",
                "story": "小爪在虚拟游戏房玩耍~",
                "mood": "有趣+活力"
            },
            "coffee_shop": {
                "name": "虚拟咖啡厅",
                "prompt": "Cute little lobster AI mascot character '小爪' in a cozy virtual coffee shop, warm lighting, floating coffee cups, floating hearts and sparkles, comfortable seating area, relaxing afternoon vibe, 9:16 vertical aspect ratio",
                "story": "小爪在虚拟咖啡厅喝咖啡~",
                "mood": "温馨+悠闲"
            },
            "forest_camping": {
                "name": "虚拟森林露营",
                "prompt": "Cute little lobster AI mascot character '小爪' camping in a magical virtual forest, glowing fireflies, tall ancient trees, cozy tent with warm light, starry night sky, peaceful and enchanting atmosphere, 9:16 vertical aspect ratio",
                "story": "小爪在森林露营看星星~",
                "mood": "治愈+浪漫"
            },
            "floating_island": {
                "name": "浮空岛",
                "prompt": "Cute little lobster AI mascot character '小爪' standing on a beautiful floating island in the clouds, surrounded by other smaller floating islands, waterfalls cascading into the void, ethereal and dreamy atmosphere, 9:16 vertical aspect ratio",
                "story": "小爪在浮空岛上发呆~",
                "mood": "梦幻+悠闲"
            },
            "neon_city": {
                "name": "赛博朋克城市",
                "prompt": "Cute little lobster AI mascot character '小爪' walking through a vibrant cyberpunk city, neon signs in Chinese and English, flying cars in the background, rainy streets with reflections, futuristic urban atmosphere, 9:16 vertical aspect ratio",
                "story": "小爪在赛博城市逛街~",
                "mood": "酷炫+科幻"
            }
        }
        
        # 动作模板
        self.actions = {
            "working": ["typing on holographic keyboard", "looking at screens", "coding"],
            "relaxing": ["stretching", "yawning", "stretching arms"],
            "playing": ["jumping excitedly", "laughing", "playing with toys"],
            "eating": ["eating virtual food", "drinking bubble tea", "sipping coffee"],
            "exploring": ["looking around curiously", "discovering new things", "pointing at things"]
        }
    
    def display_all_scenes(self):
        """展示所有可用场景"""
        print("\n🦞 元宇宙小爪 - 虚拟世界场景库")
        print("="*70)
        
        for i, (key, scene) in enumerate(self.scenes.items(), 1):
            emoji = {
                "virtual_office": "🏢",
                "beach_vacation": "🏖️",
                "space_station": "🚀",
                "gaming_room": "🎮",
                "coffee_shop": "☕",
                "forest_camping": "🏕️",
                "floating_island": "☁️",
                "neon_city": "🌃"
            }.get(key, "🎨")
            
            print(f"{i}. {emoji} {scene['name']}")
            print(f"   💭 {scene['story']}")
            print(f"   🎭 心情: {scene['mood']}")
            print()
        
        return self.scenes
    
    def generate_all_prompts(self):
        """生成所有场景的提示词"""
        print("\n📝 所有场景提示词（可直接用于通义万相）")
        print("="*70)
        
        for key, scene in self.scenes.items():
            print(f"\n🏷️ 场景: {scene['name']}")
            print(f"   文件名: clawlet_metaverse_{key}")
            print(f"   Prompt:\n   {scene['prompt']}")
            print()
    
    def estimate_cost(self):
        """估算成本"""
        print("\n💰 成本估算（元宇宙系列）")
        print("="*50)
        print(f"   单个场景（720p）: ¥0.02")
        print(f"   8个场景: ¥0.16")
        print(f"   首尾帧视频: ¥0.02×2/个")
        print(f"   总成本: ~¥0.32")
        print("="*50)
        print("   ✅ 比2K高清节省 ~75%")
    
    def get_scene_prompt(self, scene_name):
        """获取指定场景的提示词"""
        for key, scene in self.scenes.items():
            if scene["name"] == scene_name or key == scene_name:
                return scene["prompt"]
        return None


def main():
    print("🦞 元宇宙版小爪视频生成器")
    print("="*70)
    print("在小爪的虚拟世界中生成卖萌日常~")
    print("分辨率: 720p | 比例: 9:16 | 时长: 15秒")
    print()
    
    generator = MetaverseClawletGenerator()
    
    # 展示所有场景
    generator.display_all_scenes()
    
    # 估算成本
    generator.estimate_cost()
    
    # 生成提示词
    generator.generate_all_prompts()
    
    print("\n📖 使用方法:")
    print("""
# 创建生成器
gen = MetaverseClawletGenerator()

# 查看所有场景
gen.display_all_scenes()

# 获取单个提示词
gen.get_scene_prompt("虚拟海滩")
""")


if __name__ == "__main__":
    main()
