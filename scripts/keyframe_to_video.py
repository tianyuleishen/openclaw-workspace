#!/usr/bin/env python3
"""
首尾帧视频生成器
使用通义万相的首尾帧技术生成视频
成本更低（只需2张关键帧图片）
"""

import os
import sys
import requests
import json
from datetime import datetime
from pathlib import Path

# 配置
API_KEY = os.getenv("TONGYI_API_KEY", "sk-1d3af48425824e41981816390583d437")
API_BASE = "https://dashscope.aliyuncs.com/api/v1/services/aigc/video generation"

class KeyframeVideoGenerator:
    """首尾帧视频生成器"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_from_keyframes(
        self,
        start_image_path: str,
        end_image_path: str,
        output_path: str = None,
        duration: int = 15,
        resolution: str = "720p"
    ):
        """
        使用首尾帧生成视频
        
        Args:
            start_image_path: 首帧图片路径
            end_image_path: 末帧图片路径  
            output_path: 输出视频路径
            duration: 视频时长（秒）
            resolution: 分辨率 ("360p", "480p", "720p", "1080p")
        
        Returns:
            视频路径或None
        """
        print(f"\n🎬 首尾帧视频生成")
        print(f"   首帧: {start_image_path}")
        print(f"   末帧: {end_image_path}")
        print(f"   时长: {duration}秒")
        print(f"   分辨率: {resolution}")
        
        # 检查图片文件
        if not os.path.exists(start_image_path):
            print(f"❌ 首帧图片不存在: {start_image_path}")
            return None
        
        if not os.path.exists(end_image_path):
            print(f"❌ 末帧图片不存在: {end_image_path}")
            return None
        
        # 读取图片文件并转换为base64
        with open(start_image_path, "rb") as f:
            start_image_base64 = f.read()
        
        with open(end_image_path, "rb") as f:
            end_image_base64 = f.read()
        
        # 生成任务ID
        task_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        if output_path is None:
            output_path = f"/tmp/keyframe_video_{task_id}.mp4"
        
        # 准备API请求
        # 注意：这是模拟代码，实际需要使用通义万相的首尾帧API
        request_data = {
            "model": "wan2.6-i2v-flash",
            "input": {
                "first_frame_image": self._encode_image(start_image_base64),
                "last_frame_image": self._encode_image(end_image_base64),
                "duration": duration,
                "resolution": resolution
            },
            "parameters": {
                "size": self._get_resolution_size(resolution),
                "generate_mode": "keyframe_interpolation"  # 首尾帧模式
            }
        }
        
        print(f"\n📤 提交生成任务...")
        print(f"   任务ID: {task_id}")
        
        # 实际调用API（这里需要替换为真实的通义万相API）
        # response = self._call_api(request_data)
        
        # 由于API限制，这里生成占位符并说明实际使用方法
        return self._create_placeholder_video(
            start_image_path,
            end_image_path,
            output_path,
            duration
        )
    
    def _encode_image(self, image_bytes):
        """将图片编码为base64"""
        import base64
        return base64.b64encode(image_bytes).decode('utf-8')
    
    def _get_resolution_size(self, resolution):
        """获取分辨率尺寸"""
        sizes = {
            "360p": (360, 640),
            "480p": (480, 854),
            "720p": (720, 1280),  # 9:16竖屏
            "1080p": (1080, 1920)
        }
        return sizes.get(resolution, (720, 1280))
    
    def _call_api(self, request_data):
        """调用API"""
        url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
        
        payload = {
            "model": "wan2.6-i2v-flash",
            "messages": [
                {
                    "role": "user",
                    "content": json.dumps(request_data)
                }
            ],
            "max_tokens": 2000
        }
        
        response = requests.post(
            url,
            headers=self.headers,
            json=payload,
            timeout=60
        )
        
        return response.json()
    
    def _create_placeholder_video(
        self,
        start_image_path: str,
        end_image_path: str,
        output_path: str,
        duration: int
    ):
        """
        创建占位符视频说明
        实际使用时需要调用真实的通义万相首尾帧API
        """
        print(f"\n⚠️ 注意：首尾帧API调用说明")
        print(f"   由于API限制，需要使用通义万相控制台或SDK")
        print(f"   ")
        print(f"   使用方法:")
        print(f"   1. 访问 https://tongyi.aliyun.com/wanxiang/")
        print(f"   2. 选择'图生视频' -> '首尾帧'模式")
        print(f"   3. 上传首帧和末帧图片")
        print(f"   4. 设置时长: {duration}秒")
        print(f"   5. 设置分辨率: 720p (9:16)")
        print(f"   6. 提交生成")
        print(f"   ")
        print(f"   SDK调用示例:")
        print(f"   from TongyiAPI import generate_video_from_keyframes")
        print(f"   generate_video_from_keyframes(")
        print(f"       start_image='{start_image_path}',")
        print(f"       end_image='{end_image_path}',")
        print(f"       duration={duration},")
        print(f"       output='{output_path}'")
        print(f"   )")
        
        # 复制首帧作为预览图
        preview_path = output_path.replace(".mp4", "_preview.png")
        import shutil
        shutil.copy(start_image_path, preview_path)
        
        print(f"   ")
        print(f"✅ 已生成预览图: {preview_path}")
        print(f"   （实际视频请通过通义万相控制台生成）")
        
        return None
    
    def estimate_cost(self, duration: int, resolution: str) -> float:
        """估算生成成本"""
        # 首尾帧模式价格（假设）
        base_price = 0.02  # 每张图
        resolution_multiplier = {
            "360p": 1.0,
            "480p": 1.2,
            "720p": 1.5,
            "1080p": 2.0
        }
        
        multiplier = resolution_multiplier.get(resolution, 1.0)
        
        # 首尾帧只需2张图
        total_cost = base_price * 2 * multiplier
        
        return total_cost


# 便捷函数
def generate_keyframe_video(
    start_image: str,
    end_image: str,
    duration: int = 15,
    resolution: str = "720p"
) -> str:
    """
    便捷的首尾帧视频生成函数
    
    Args:
        start_image: 首帧图片路径
        end_image: 末帧图片路径
        duration: 视频时长（秒）
        resolution: 分辨率
    
    Returns:
        视频路径
    """
    generator = KeyframeVideoGenerator()
    
    output_path = f"/tmp/keyframe_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    
    return generator.generate_from_keyframes(
        start_image_path=start_image,
        end_image_path=end_image,
        output_path=output_path,
        duration=duration,
        resolution=resolution
    )


# 使用示例
if __name__ == "__main__":
    print("🎬 首尾帧视频生成器")
    print("="*50)
    
    generator = KeyframeVideoGenerator()
    
    # 估算成本
    cost = generator.estimate_cost(duration=15, resolution="720p")
    print(f"💰 预估成本: ¥{cost:.2f}")
    print(f"   （首尾帧模式：2张关键帧）")
    print()
    
    # 使用示例
    print("📖 使用方法:")
    print("   generate_keyframe_video(")
    print("       start_image='/tmp/clawlet_morning_start.png',")
    print("       end_image='/tmp/clawlet_morning_end.png',")
    print("       duration=15,")
    print("       resolution='720p'")
    print("   )")
