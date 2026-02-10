# Clawlet Video Generator 🎬

自动化小爪短视频生成技能。

## 快速开始

```bash
# 安装
./install.sh

# 生成视频
clawlet-video-generator --model wan2.5 --resolution 1080 --duration 5
```

## 功能特性

| 功能 | 说明 |
|------|------|
| 模型 | wan2.5-i2v-preview, wan2.6-i2v-flash |
| 清晰度 | 720P, 1080P |
| 时长 | 5秒, 10秒, 15秒 |
| 配音 | 自动配音 |

## 使用示例

```bash
# 默认参数生成 (wan2.5, 720P, 5秒, 自动配音)
clawlet-video-generator

# 高清版本
clawlet-video-generator --resolution 1080

# 10秒视频
clawlet-video-generator --duration 10

# 不带配音
clawlet-video-generator --voice no

# 自定义提示词
clawlet-video-generator --prompt "小爪在太空站工作"
```

## 参数说明

| 参数 | 描述 | 默认值 | 可选值 |
|------|------|--------|--------|
| --model | AI模型 | wan2.5 | wan2.5, wan2.6 |
| --resolution | 分辨率 | 720 | 720, 1080 |
| --duration | 视频时长 | 5 | 5, 10, 15 |
| --voice | 自动配音 | yes | yes, no |
| --prompt | 提示词 | 自动生成 | 自定义文本 |
| --set-standard | 设置标准模型 | - | 图片路径 |

## 输出

- 视频保存到: `/tmp/clawlet_video_YYYY-MM-DD_HHMMSS.mp4`
- 最新链接: `/home/admin/.openclaw/workspace/clawlet_latest.mp4`
- 下载服务: `http://8.130.18.239:8080/clawlet_latest.mp4`

## 成本参考

| 模型 | 720P | 1080P |
|------|------|--------|
| wan2.5 | ¥0.75 | ¥1.50 |
| wan2.6 | ¥0.75 | ¥1.50 |

## 标准模型

技能使用 `/tmp/clawlet_model_standard.png` 作为默认图片。

更新标准模型:
```bash
clawlet-video-generator --set-standard /path/to/your_image.png
```

## 文件结构

```
clawlet-video-generator/
├── SKILL.md           # 技能说明
├── README.md          # 本文件
├── install.sh         # 安装脚本
└── clawlet-video-generator.sh  # 主脚本
```

## 要求

- Python 3
- curl
- 阿里云API Key (设置 DASHSCOPE_API_KEY 环境变量)
