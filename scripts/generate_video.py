#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 DashScope VideoSynthesis 生成视频
"""

import os
import json
import time

# 设置 API Key（使用阿里云 AccessKey）
os.environ['DASHSCOPE_API_KEY'] = 'sk-0bb6c2c5c8c84a3bb737476103710000'

from dashscope import VideoSynthesis

def generate_video(prompt: str, model: str = 'wanx-video-01', **kwargs):
    """
    生成视频
    
    参数:
        prompt: 视频描述提示词
        model: 模型名称（默认 wanx-video-01）
        **kwargs: 其他参数
            - size: 视频尺寸（如 '1280*720'）
            - duration: 时长（秒，默认 5）
            - seed: 随机种子
    
    返回:
        dict: API 响应
    """
    print("=" * 70)
    print("🎬 视频生成请求")
    print("=" * 70)
    print(f"\n📝 提示词: {prompt[:100]}...")
    print(f"🤖 模型: {model}")
    
    # 调用 API
    response = VideoSynthesis.call(
        model=model,
        prompt=prompt,
        **kwargs
    )
    
    return response

def main():
    """主函数"""
    # 示例提示词
    prompt = """现代办公室场景，年轻白领使用AI工具快速完成工作，
    科技感画面，蓝色橙色色调，快节奏剪辑，
    最后字幕显示"AI让效率提升10倍"，25秒，女声配音，轻快电子背景音乐。"""
    
    # 生成视频
    response = generate_video(
        prompt=prompt,
        model='wanx-video-01',
        size='1280*720',
        duration=5  # 短视频测试
    )
    
    # 处理响应
    print("\n" + "=" * 70)
    print("📊 API 响应")
    print("=" * 70)
    print(f"\n状态码: {response.status_code}")
    
    if response.status_code == 200:
        print("\n✅ 视频生成成功！")
        print(f"\n任务 ID: {response.output.get('task_id', 'N/A')}")
        
        if response.output.get('video_url'):
            print(f"\n🎥 视频链接: {response.output['video_url']}")
        
        if response.output.get('video_path'):
            print(f"📁 视频路径: {response.output['video_path']}")
        
        if hasattr(response, 'usage') and response.usage:
            print(f"\n📈 用量信息:")
            print(json.dumps(response.usage, ensure_ascii=False, indent=2))
    else:
        print(f"\n❌ 生成失败: {response.message}")
        if hasattr(response, 'code'):
            print(f"错误码: {response.code}")

if __name__ == '__main__':
    main()
