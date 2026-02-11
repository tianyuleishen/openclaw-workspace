#!/usr/bin/env python3
"""
语音识别配置脚本 - 在线 API 方案

支持:
1. 讯飞语音 (需申请)
2. 阿里云语音 (需申请)
3. 百度语音 (需申请)
4. 免费方案: 使用 Google Speech-to-Text

使用方法:
python3 voice_recognition_setup.py
"""

import os
import json
import subprocess

def check_dependencies():
    """检查依赖"""
    print("=" * 60)
    print("🎤 语音识别配置 - 在线 API 方案")
    print("=" * 60)
    
    print("\n1. 检查必要工具...")
    
    # 检查 ffmpeg
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ ffmpeg 已安装")
        else:
            print("❌ ffmpeg 未安装")
            print("   安装: sudo apt-get install ffmpeg")
    except FileNotFoundError:
        print("❌ ffmpeg 未安装")
        print("   安装: sudo apt-get install ffmpeg")
    
    # 检查 curl
    try:
        result = subprocess.run(["curl", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ curl 已安装")
        else:
            print("❌ curl 未安装")
    except FileNotFoundError:
        print("❌ curl 未安装")

def setup_google_speech():
    """配置 Google Speech-to-Text (免费额度)"""
    print("\n" + "=" * 60)
    print("📌 方案1: Google Speech-to-Text (推荐)")
    print("=" * 60)
    
    config = """
# Google Speech-to-Text 配置

## 免费额度
- 每月 60 分钟免费
- 支持中文

## 申请地址
https://cloud.google.com/speech-to-text

## 使用方法

### 1. 安装 gcloud SDK
```bash
# Ubuntu/Debian
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
sudo apt-get update && sudo apt-get install -y google-cloud-cli

# 安装 Speech-to-Text
gcloud components install speech-to-text
```

### 2. 认证
```bash
gcloud auth application-default login
```

### 3. 使用
```bash
# 转换音频格式
ffmpeg -i input.ogg -ar 16000 -ac 1 -acodec pcm_s16le input.wav

# 识别
gcloud ml speech recognize-long-audio input.wav \\
    --language-code=zh-CN \\
    --enable-word-time-offsets
```
"""
    
    with open("/home/admin/.openclaw/workspace/memory/google_speech_config.md", "w") as f:
        f.write(config)
    
    print("✅ 配置文档已保存: memory/google_speech_config.md")
    print("\n📝 提示:")
    print("   需要 Google 账号")
    print("   首次使用需要设置认证")

def setup_xunfei_speech():
    """配置讯飞语音"""
    print("\n" + "=" * 60)
    print("📌 方案2: 讯飞语音 (国内推荐)")
    print("=" * 60)
    
    config = """
# 讯飞语音识别配置

## 申请地址
https://www.xfyun.cn/services/lfasr

## 免费额度
- 每日 500 次调用
- 永久有效

## SDK 安装
```bash
pip install xfyun
```

## 使用示例
```python
import json
from xfyun import Speech

# 配置
appid = "YOUR_APPID"
api_key = "YOUR_API_KEY"
api_secret = "YOUR_API_SECRET"

# 初始化
speech = Speech(appid, api_key, api_secret)

# 识别音频
with open("audio.wav", "rb") as f:
    result = speech.recognize(f, format="wav", rate=16000)

print(result)
```
"""
    
    with open("/home/admin/.openclaw/workspace/memory/xunfei_speech_config.md", "w") as f:
        f.write(config)
    
    print("✅ 配置文档已保存: memory/xunfei_speech_config.md")
    print("\n📝 提示:")
    print("   需要注册讯飞账号")
    print("   创建应用获取 API Key")

def setup_aliyun_speech():
    """配置阿里云语音"""
    print("\n" + "=" * 60)
    print("📌 方案3: 阿里云智能语音")
    print("=" * 60)
    
    config = """
# 阿里云语音识别配置

## 申请地址
https://www.aliyun.com/product/nls

## 免费额度
- 每月 1000 次调用
- 新用户更多优惠

## 安装 SDK
```bash
pip install aliyun-python-sdk-core-nls
```

## 使用示例
```python
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

# 配置
access_key_id = "YOUR_ACCESS_KEY_ID"
access_key_secret = "YOUR_ACCESS_KEY_SECRET"
region_id = "cn-shanghai"

client = AcsClient(access_key_id, access_key_secret, region_id)

# 创建请求
request = CommonRequest()
request.set_method('POST')
request.set_domain('filetrans.cn-shanghai.aliyuncs.com')
request.set_version('2018-08-17')
request.set_action_name('SubmitTask')

# 提交音频转写任务
task_config = {
    "file_link": "https://your-audio-url/audio.wav",
    "enable_words": True,
    "enable_sample_rate_adaptive": True
}

request.add_body_params('Task', json.dumps(task_config))
response = client.do_action_with_exception(request)
print(response)
```
"""
    
    with open("/home/admin/.openclaw/workspace/memory/aliyun_speech_config.md", "w") as f:
        f.write(config)
    
    print("✅ 配置文档已保存: memory/aliyun_speech_config.md")
    print("\n📝 提示:")
    print("   需要阿里云账号")
    print("   开通智能语音服务")

def create_unified_script():
    """创建统一调用脚本"""
    print("\n" + "=" * 60)
    print("📝 创建统一调用脚本")
    print("=" * 60)
    
    script_content = '''#!/usr/bin/env python3
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
        print("\n✅ 识别结果:")
        print(result)
    else:
        print("\n❌ 识别失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
    
    with open("/home/admin/.openclaw/workspace/voice_recognize.py", "w") as f:
        f.write(script_content)
    
    os.chmod("/home/admin/.openclaw/workspace/voice_recognize.py", 0o755)
    print("✅ 创建脚本: /home/admin/.openclaw/workspace/voice_recognize.py")

def show_summary():
    """显示总结"""
    print("\n" + "=" * 60)
    print("📋 配置总结")
    print("=" * 60)
    
    print("\n✅ 已创建配置文件:")
    print("   1. memory/google_speech_config.md - Google Speech")
    print("   2. memory/xunfei_speech_config.md - 讯飞语音")
    print("   3. memory/aliyun_speech_config.md - 阿里云")
    print("   4. workspace/voice_recognize.py - 统一调用脚本")
    
    print("\n🎯 推荐方案:")
    print("   📌 方案1: Google Speech (需翻墙)")
    print("   📌 方案2: 讯飞语音 (国内推荐)")
    print("   📌 方案3: 阿里云语音")
    
    print("\n💡 下一步:")
    print("   1. 选择一个语音识别服务")
    print("   2. 注册账号并获取 API Key")
    print("   3. 按照配置文件设置")
    print("   4. 运行: python3 workspace/voice_recognize.py <音频文件>")

if __name__ == "__main__":
    check_dependencies()
    setup_google_speech()
    setup_xunfei_speech()
    setup_aliyun_speech()
    create_unified_script()
    show_summary()
