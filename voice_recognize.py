#!/usr/bin/env python3
"""
统一语音识别脚本

支持多个语音识别 API:
1. Google Speech-to-Text
2. 讯飞语音
3. 阿里云语音

使用方法:
python3 voice_recognize.py <音频文件> [--api google|xunfei|aliyun]
"""

import sys
import os
import argparse

def recognize_google(audio_path):
    """Google 语音识别"""
    print(f"🎤 使用 Google 识别: {audio_path}")
    
    # 检查认证
    if not os.path.exists(os.path.expanduser("~/.config/gcloud/application_default_credentials.json")):
        print("❌ 未配置 Google 认证")
        print("   请运行: gcloud auth application-default login")
        return None
    
    # 使用 gcloud CLI
    cmd = [
        "gcloud", "ml", "speech", "recognize",
        audio_path,
        "--language-code=zh-CN",
        "--enable-word-time-offsets"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout
    else:
        print(f"❌ 识别失败: {result.stderr}")
        return None

def recognize_xunfei(audio_path):
    """讯飞语音识别"""
    print(f"🎤 使用讯飞识别: {audio_path}")
    print("⚠️ 请配置 API Key")
    print("   参考: memory/xunfei_speech_config.md")
    return None

def recognize_aliyun(audio_path):
    """阿里云语音识别"""
    print(f"🎤 使用阿里云识别: {audio_path}")
    print("⚠️ 请配置 API Key")
    print("   参考: memory/aliyun_speech_config.md")
    return None

def main():
    parser = argparse.ArgumentParser(description='语音识别')
    parser.add_argument('audio', help='音频文件路径')
    parser.add_argument('--api', choices=['google', 'xunfei', 'aliyun'], 
                        default='google', help='选择 API 提供商')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.audio):
        print(f"❌ 文件不存在: {args.audio}")
        sys.exit(1)
    
    # 选择识别方法
    if args.api == 'google':
        result = recognize_google(args.audio)
    elif args.api == 'xunfei':
        result = recognize_xunfei(args.audio)
    elif args.api == 'aliyun':
        result = recognize_aliyun(args.audio)
    
    if result:
        print("
✅ 识别结果:")
        print(result)
    else:
        print("
❌ 识别失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
