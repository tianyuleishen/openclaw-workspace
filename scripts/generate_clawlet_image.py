#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成小爪介绍图片 - 文生图
"""

import os
import sys
import dashscope
from http import HTTPStatus
from dashscope import ImageSynthesis
import mimetypes

# 配置
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

# API Key - 请替换为您的阿里云API Key
api_key = os.getenv("DASHSCOPE_API_KEY")

# 如果环境变量没有设置，请在此处填入您的API Key（临时测试用）
# api_key = "sk-您的APIKey"

if not api_key:
    print("❌ 请先设置环境变量 DASHSCOPE_API_KEY")
    print("💡 设置方法：")
    print("   export DASHSCOPE_API_KEY='sk-您的APIKey'")
    print("")
    print("⚠️ 或者在阿里云控制台获取API Key:")
    print("   https://dashscope.console.aliyun.com/manage/overview")
    sys.exit(1)

def generate_clawlet_image():
    """生成小爪的AI助手介绍图片"""
    
    prompt = """一幅精美的手绘风格插画，可爱的小爪子角色介绍卡片。
画面中央是一个卡通风格的机械爪子（🦞），可爱友善的表情，带着科技感的头盔。
爪子穿着工程师的衣服，上面有"AI Assistant"的标签。
背景是充满未来感的科技办公室场景：电脑屏幕、代码符号、机器人助手。
文字"小爪 AI"以可爱的字体显示在图片上方。
整体风格温暖、友好、专业。
长宽比：16:9，清晰度高。"""
    
    print("🎨 正在生成小爪介绍图片...")
    print(f"📝 Prompt: {prompt[:100]}...")
    print("")
    
    # 调用文生图API
    rsp = ImageSynthesis.call(
        api_key=api_key,
        model='wan2.6-t2i',  # 使用最新的wan2.6模型
        prompt=prompt,
        n=1,
        size='1280*720',  # 16:9 比例
        prompt_extend=True,
        watermark=False
    )
    
    print(f"📡 API响应状态: {rsp.status_code}")
    
    if rsp.status_code == HTTPStatus.OK:
        # 保存图片
        for idx, result in enumerate(rsp.output.results):
            file_name = f"clawlet_intro_{idx+1}.png"
            # 下载图片
            import requests
            response = requests.get(result.url)
            if response.status_code == 200:
                with open(file_name, 'wb') as f:
                    f.write(response.content)
                print(f"✅ 图片已保存: {file_name}")
                print(f"🔗 图片URL: {result.url}")
                
                # 保存URL供下一步使用
                with open('/tmp/clawlet_image_url.txt', 'w') as f:
                    f.write(result.url)
                print(f"💾 URL已保存到: /tmp/clawlet_image_url.txt")
            else:
                print(f"❌ 下载失败: {response.status_code}")
    else:
        print(f"❌ 生成失败: {rsp.status_code}, code: {rsp.code}, message: {rsp.message}")
        return None
    
    return rsp

if __name__ == '__main__':
    generate_clawlet_image()
