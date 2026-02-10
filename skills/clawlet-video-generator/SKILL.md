---
name: clawlet-video-generator
description: Generate short videos with 小爪 using Tongyi Wanxiang AI. Supports wan2.5/wan2.6 models, 720P/1080P resolution, 5/10/15s duration, and auto voiceover.
metadata: { "openclaw": { "emoji": "🎬", "requires": { "bins": ["python3", "curl"] } } }
---

# Clawlet Video Generator

Automated video generation skill using Tongyi Wanxiang AI.

## Features

- **Models**: wan2.5-i2v-preview, wan2.6-i2v-flash
- **Resolution**: 720P, 1080P
- **Duration**: 5s, 10s, 15s
- **Auto Voiceover**: Yes/No
- **Standard Model**: Uses /tmp/clawlet_model_standard.png

## Usage

### Basic

```bash
clawlet-video-generator --model wan2.5 --resolution 1080 --duration 5 --voice yes
```

### Options

| Option | Values | Default |
|--------|--------|---------|
| --model | wan2.5, wan2.6 | wan2.5 |
| --resolution | 720, 1080 | 720 |
| --duration | 5, 10, 15 | 5 |
| --voice | yes, no | yes |
| --prompt | "custom prompt" | Auto-generated |

## Examples

### Generate 5s video with wan2.5, 1080P, auto voice

```bash
clawlet-video-generator --model wan2.5 --resolution 1080 --duration 5 --voice yes
```

### Generate 10s video without voice

```bash
clawlet-video-generator --model wan2.6 --resolution 720 --duration 10 --voice no
```

### Custom prompt

```bash
clawlet-video-generator --prompt "小爪在太空站工作"
```

## Standard Model

Uses `/tmp/clawlet_model_standard.png` as the source image.

To update standard model:
```bash
clawlet-video-generator --set-standard /path/to/new_image.png
```

## Output

- Videos saved to `/tmp/clawlet_video_YYYY-MM-DD_HHMMSS.mp4`
- Also available at `/home/admin/.openclaw/workspace/clawlet_latest.mp4`
- Download via: `http://8.130.18.239:8080/clawlet_latest.mp4`

## Cost

| Model | Resolution | Price |
|-------|------------|-------|
| wan2.5-i2v-preview | 720P | ¥0.75/video |
| wan2.5-i2v-preview | 1080P | ¥1.50/video |
| wan2.6-i2v-flash | 720P | ¥0.75/video |
| wan2.6-i2v-flash | 1080P | ¥1.50/video |

Auto voice included in price.
