#!/usr/bin/env python3
"""
抖音工具 - 简化的使用接口
"""

import requests
import json
import os

# TikHub API（推荐使用，免费额度）
TIKHUB_API = "https://api.tikhub.io/api/v1"

class DouyinTools:
    """抖音工具类"""
    
    def __init__(self, api_key=None):
        """初始化"""
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}" if api_key else "",
            "Content-Type": "application/json"
        }
    
    def get_video_info(self, video_url):
        """获取视频信息"""
        if not self.api_key:
            return {"error": "需要API Key，请注册 TikHub.io 获取"}
        
        try:
            response = requests.post(
                f"{TIKHUB_API}/douyin/video/info",
                headers=self.headers,
                json={"video_url": video_url},
                timeout=30
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def download_video(self, video_url, save_path="douyin_video.mp4"):
        """下载视频"""
        if not self.api_key:
            return {"error": "需要API Key，请注册 TikHub.io 获取"}
        
        try:
            # 获取无水印链接
            info = self.get_video_info(video_url)
            if "error" in info:
                return info
            
            video_url = info.get("video", {}).get("play_addr", {}).get("url")
            if not video_url:
                return {"error": "无法获取视频链接"}
            
            # 下载
            response = requests.get(video_url, timeout=60)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                return {"success": True, "path": save_path}
            else:
                return {"error": f"下载失败: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_trending_videos(self, count=10):
        """获取热门视频"""
        if not self.api_key:
            return {"error": "需要API Key，请注册 TikHub.io 获取"}
        
        try:
            response = requests.get(
                f"{TIKHUB_API}/douyin/trending",
                headers=self.headers,
                params={"limit": count},
                timeout=30
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}

# 简单使用示例
if __name__ == "__main__":
    print("🦞 抖音工具")
    print("=" * 50)
    print("\n使用方法:")
    print("1. 注册 https://tikhub.io 获取 API Key")
    print("2. 设置环境变量: export TIKHUB_API_KEY='your-key'")
    print("3. 使用示例:")
    print("   from douyin_tools import DouyinTools")
    print("   tools = DouyinTools(api_key='your-key')")
    print("   info = tools.get_video_info('抖音视频链接')")
    print("")
    print("或者使用在线工具:")
    print("- 抖音视频解析: https://douyin.wtf/")
    print("- TikHub在线: https://tikhub.io/")
    print("")
    print("=" * 50)
