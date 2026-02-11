# Whisper 语音识别配置指南

**日期**: 2026-02-10  
**状态**: 需要手动配置

---

## 🎤 Whisper 配置方案

### 方案1: 本地安装 (推荐)

#### Linux/macOS

```bash
# 1. 安装 ffmpeg
sudo apt-get update
sudo apt-get install -y ffmpeg

# 2. 安装 Whisper
pip install --user openai-whisper

# 3. 使用
whisper audio.ogg --model small --language Chinese
```

#### Windows

```powershell
# 1. 安装 ffmpeg
winget install ffmpeg

# 2. 安装 Whisper
pip install --user openai-whisper

# 3. 使用
whisper audio.ogg --model small --language Chinese
```

---

### 方案2: Docker (推荐用于服务器)

```bash
# 运行 Whisper Docker 容器
docker run -it --rm \
  -v $(pwd):/workspace \
  -w /workspace \
  registry.cn-beijing.aliyuncs.com/ai-samples/whisper:base \
  whisper audio.ogg \
  --model small \
  --language Chinese \
  --output_dir /workspace/output
```

---

### 方案3: 在线 API (需要 Key)

#### 阿里云语音识别

```bash
# 安装 SDK
pip install aliyun-python-sdk-core-nls
```

#### 讯飞语音

```bash
# 安装 SDK
pip install xfyun
```

---

## 📝 当前服务器状态

**问题**: Python 环境限制 (PEP 668)

**解决方案**:
1. 使用 `--user` 标志
2. 使用虚拟环境
3. 使用 Docker

---

## 🎯 推荐方案

对于当前服务器，推荐使用 **方案2 (Docker)**:

```bash
# 快速使用 Whisper
docker run -it --rm \
  -v /home/admin/.openclaw/media:/media \
  -w /media \
  openai/whisper:latest \
  whisper latest.ogg \
  --model small \
  --language Chinese \
  --output_dir /media/outbound
```

---

## 💡 使用场景

| 场景 | 推荐方案 |
|------|---------|
| **偶尔使用** | 方案3 (在线 API) |
| **频繁使用** | 方案1 (本地安装) |
| **服务器环境** | 方案2 (Docker) |

---

## 📖 相关文档

- Whisper 官方文档: https://github.com/openai/whisper
- 模型选择: https://github.com/openai/whisper#available-models-and-languages

---

**创建时间**: 2026-02-10
