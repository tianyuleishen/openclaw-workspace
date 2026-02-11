
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
gcloud ml speech recognize-long-audio input.wav \
    --language-code=zh-CN \
    --enable-word-time-offsets
```
