#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦞 小爪办公室视频生成器
使用通义万相首尾帧技术生成视频
"""

import os
import sys
import json
import base64
import time
from datetime import datetime

# 检查dashscope
try:
    import dashscope
    from dashscope import VideoSynthesis
    DASHSCOPE_AVAILABLE = True
except ImportError:
    DASHSCOPE_AVAILABLE = False

# API密钥
API_KEY = os.getenv("DASHSCOPE_API_KEY", "sk-1d3af48425824e41981816390583d437")

print("="*70)
print("🦞 小爪办公室首尾帧视频生成器")
print("="*70)

# 关键帧图片（已压缩）
START_IMAGE = "/tmp/office_start_small.jpg"
END_IMAGE = "/tmp/office_end_small.jpg"

def read_image_base64(path):
    """读取图片并返回base64"""
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def generate_keyframe_video():
    """使用首尾帧生成视频"""
    
    if not DASHSCOPE_AVAILABLE:
        print("❌ dashscope未安装")
        return None
    
    # 检查图片
    if not os.path.exists(START_IMAGE):
        print(f"❌ 首帧图片不存在: {START_IMAGE}")
        return None
    if not os.path.exists(END_IMAGE):
        print(f"❌ 末帧图片不存在: {END_IMAGE}")
        return None
    
    # 读取图片
    start_b64 = read_image_base64(START_IMAGE)
    end_b64 = read_image_base64(END_IMAGE)
    
    print(f"\n📦 图片已加载:")
    print(f"   首帧: {len(start_b64)} 字符")
    print(f"   末帧: {len(end_b64)} 字符")
    
    # 检查大小
    if len(start_b64) > 61440:
        print(f"❌ 首帧太大，需要进一步压缩")
        return None
    if len(end_b64) > 61440:
        print(f"❌ 末帧太大，需要进一步压缩")
        return None
    
    print("\n🎬 提交首尾帧视频生成任务...")
    
    try:
        # 设置API密钥
        dashscope.api_key = API_KEY
        
        # 调用首尾帧视频生成API
        # 注意：通义万相的首尾帧API调用方式
        response = VideoSynthesis.call(
            model='wanx2.1-kf2v-plus',  # 首尾帧模型
            input={
                'first_frame_image': f"data:image/jpeg;base64,{start_b64}",
                'last_frame_image': f"data:image/jpeg;base64,{end_b64}",
                'duration': 5,  # 5秒视频
            },
            parameters={
                'size': '720*1280',  # 9:16竖屏
            }
        )
        
        print(f"\n📡 API响应:")
        print(f"   状态码: {response.status_code}")
        
        if response.status_code == 200:
            task_id = response.output.get('task_id')
            print(f"   任务ID: {task_id}")
            
            # 等待生成完成
            print(f"\n⏳ 等待视频生成...")
            result = VideoSynthesis.wait(task_id)
            
            print(f"\n✅ 生成完成!")
            print(f"   视频URL: {result.output.get('video_url')}")
            print(f"   任务ID: {task_id}")
            
            return result.output.get('video_url')
        else:
            print(f"❌ 生成失败: {response.message}")
            return None
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return None

# 使用示例
if __name__ == "__main__":
    video_url = generate_keyframe_video()
    
    if video_url:
        print(f"\n🎉 视频生成成功!")
        print(f"   URL: {video_url}")
    else:
        print(f"\n⚠️  视频生成失败或未完成")
