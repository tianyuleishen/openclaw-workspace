# 讯飞语音识别配置指南

**日期**: 2026-02-10 21:15:38

---

## 🎤 讯飞语音识别

### 免费额度
- **每日**: 500 次调用
- **有效期**: 永久
- **适合**: 个人使用

---

## 📝 申请流程

### 1. 注册账号
1. 访问: https://www.xfyun.cn
2. 点击"免费注册"
3. 完成手机号验证

### 2. 开通服务
1. 登录讯飞开放平台
2. 进入"控制台"
3. 点击"创建新应用"
4. 填写应用信息:
   - 应用名称: 小爪语音助手
   - 应用类型: 工具类
   - 功能描述: 语音识别

### 3. 获取 API Key
创建完成后，在应用详情页获取:
- **APPID**: 
- **APIKey**: 
- **APISecret**: 

---

## 🔧 安装 SDK

```bash
# 方法1: 使用 pip (推荐)
pip install --user xfyun

# 方法2: 如果遇到问题
pip install --user RequestsToolbox
```

---

## 💻 使用示例

### 基础用法

```python
#!/usr/bin/env python3
import os
from xfyun import Speech

# 配置
APPID = "your_appid"
APIKey = "your_apikey"
APISecret = "your_apisecret"

# 初始化
speech = Speech(APPID, APIKey, APISecret)

# 音频文件路径
audio_path = "/home/admin/.openclaw/media/inbound/audio.ogg"

# 读取音频
with open(audio_path, "rb") as f:
    audio_data = f.read()

# 识别
result = speech.recognize(
    audio_data,
    format="ogg",  # ogg, wav, mp3
    rate=16000,     # 采样率
    channel=1,     # 单声道
    bie=1,         # 开启表情识别
    lang="zh_cn"   # 中文
)

# 解析结果
if result and "data" in result:
    text = result["data"]
    print(f"识别结果: {text}")
else:
    print(f"识别失败: {result}")
```

---

## 🔄 音频格式转换

如果音频格式不支持，可以使用 ffmpeg 转换:

```bash
# OGG 转 WAV
ffmpeg -i input.ogg -ar 16000 -ac 1 -acodec pcm_s16le output.wav

# MP3 转 WAV
ffmpeg -i input.mp3 -ar 16000 -ac 1 -acodec pcm_s16le output.wav

# FLAC 转 WAV
ffmpeg -i input.flac -ar 16000 -ac 1 -acodec pcm_s16le output.wav
```

---

## 🛠️ 创建快捷脚本

创建一个统一的语音识别脚本:

```bash
#!/bin/bash
# 文件: ~/voice_recognize.sh

AUDIO_FILE="$1"

if [ -z "$AUDIO_FILE" ]; then
    echo "用法: $0 <音频文件>"
    exit 1
fi

# 检查文件
if [ ! -f "$AUDIO_FILE" ]; then
    echo "文件不存在: $AUDIO_FILE"
    exit 1
fi

# 转换音频格式
TEMP_WAV="/tmp/voice_$(date +%s).wav"
ffmpeg -i "$AUDIO_FILE" -ar 16000 -ac 1 -acodec pcm_s16le "$TEMP_WAV" -y 2>/dev/null

# 调用讯飞 API
# (需要填写 API Key)

# 清理
rm -f "$TEMP_WAV"

echo "识别完成"
```

---

## 📊 常见问题

### Q: 识别准确率低?
A: 
- 确保音频清晰
- 说话语速适中
- 环境噪音小

### Q: 返回空结果?
A:
- 检查 API Key 是否正确
- 检查音频格式是否支持
- 查看返回的错误码

### Q: 提示"认证失败"?
A:
- 检查 APPID, APIKey, APISecret 是否匹配
- 确认服务已开通

---

## 🔗 相关链接

- **官网**: https://www.xfyun.cn
- **控制台**: https://www.xfyun.cn/console
- **文档**: https://www.xfyun.cn/doc/interface/asr.html
- **价格**: https://www.xfyun.cn/service/price

---

**创建时间**: 2026-02-10 21:15:38
