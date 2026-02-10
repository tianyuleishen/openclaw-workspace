#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦞 小爪办公室视频生成器 - v2
使用通义万相首尾帧技术
"""

import os
import sys
import base64
from datetime import datetime

try:
    import dashscope
    from dashscope import VideoSynthesis
    DASHSCOPE_AVAILABLE = True
except ImportError:
    DASHSCOPE_AVAILABLE = False

API_KEY = "sk-1d3af48425824e41981816390583d437"

print("="*70)
print("🦞 小爪办公室首尾帧视频生成器 v2")
print("="*70)

# 关键帧
START_IMG = "/tmp/office_start_small.jpg"
END_IMG = "/tmp/office_end_small.jpg"

def test_keyframe_video():
    """测试首尾帧视频生成"""
    
    if not DASHSCOPE_AVAILABLE:
        print("❌ dashscope未安装")
        return None
    
    # 检查图片
    if not os.path.exists(START_IMG) or not os.path.exists(END_IMG):
        print("❌ 关键帧图片不存在")
        return None
    
    # 读取base64
    with open(START_IMG, 'rb') as f:
        start_b64 = f.read()
    with open(END_IMG, 'rb') as f:
        end_b64 = f.read()
    
    start_url = f"data:image/jpeg;base64,{base64.b64encode(start_b64).decode('utf-8')}"
    end_url = f"data:image/jpeg;base64,{base64.b64encode(end_b64).decode('utf-8')}"
    
    print(f"\n📦 图片已加载")
    print(f"   首帧: {len(start_url)} 字符")
    print(f"   末帧: {len(end_url)} 字符")
    
    print("\n🎬 提交视频生成任务...")
    print(f"   模型: wanx2.1-kf2v-plus")
    print(f"   分辨率: 720*1280")
    print(f"   时长: 5秒")
    
    try:
        dashscope.api_key = API_KEY
        
        response = VideoSynthesis.call(
            model='wanx2.1-kf2v-plus',
            first_frame_url=start_url,
            last_frame_url=end_url,
            prompt='Cute little red lobster AI mascot 小爪 working in virtual office, cyberpunk style, holographic screens',
            extra_input={
                'duration': 5,
                'size': '720*1280'
            }
        )
        
        print(f"\n📡 API响应:")
        print(f"   状态码: {response.status_code}")
        
        if response.status_code == 200:
            task_id = response.output['task_id']
            print(f"   任务ID: {task_id}")
            
            print(f"\n⏳ 等待生成...")
            result = VideoSynthesis.wait(task_id)
            
            if result.status_code == 200:
                print(f"\n✅ 生成成功!")
                print(f"   视频URL: {result.output.get('video_url')}")
                return result.output.get('video_url')
            else:
                print(f"❌ 生成失败: {result.message}")
                return None
        else:
            print(f"❌ 提交失败: {response.message}")
            return None
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    video_url = test_keyframe_video()
    
    if video_url:
        print(f"\n🎉 成功!")
    else:
        print(f"\n⚠️  失败")
