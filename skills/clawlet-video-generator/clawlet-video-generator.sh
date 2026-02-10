#!/bin/bash
#=========================================
# Clawlet Video Generator
# 自动生成小爪短视频
#=========================================

set -e

# 配置
API_KEY="${DASHSCOPE_API_KEY:-sk-1d3af48425824e41981816390583d437}"
STANDARD_MODEL="/tmp/clawlet_model_standard.png"
OUTPUT_DIR="/tmp"
WORKSPACE_DIR="/home/admin/.openclaw/workspace"

# 默认参数
MODEL="wan2.5-i2v-preview"
RESOLUTION="720"
DURATION="5"
VOICE="yes"
PROMPT=""
SET_STANDARD=""

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印帮助
show_help() {
    cat << EOF
🎬 Clawlet Video Generator

用法: $(basename "$0") [选项]

选项:
  --model MODEL      模型选择 (wan2.5, wan2.6) [默认: wan2.5]
  --resolution RES   清晰度 (720, 1080) [默认: 720]
  --duration SEC     时长 (5, 10, 15) [默认: 5]
  --voice VOICE      自动配音 (yes, no) [默认: yes]
  --prompt TEXT      自定义提示词 [默认: 自动生成]
  --set-standard IMG 设置标准模型图片路径
  --help             显示帮助

示例:
  $(basename "$0") --model wan2.5 --resolution 1080 --duration 5 --voice yes
  $(basename "$0") --model wan2.6 --resolution 720 --duration 10 --voice no
  $(basename "$0") --set-standard /path/to/new_model.png

EOF
    exit 0
}

# 打印状态
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 解析参数
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --model)
                MODEL="$2"
                shift 2
                ;;
            --resolution)
                RESOLUTION="$2"
                shift 2
                ;;
            --duration)
                DURATION="$2"
                shift 2
                ;;
            --voice)
                VOICE="$2"
                shift 2
                ;;
            --prompt)
                PROMPT="$2"
                shift 2
                ;;
            --set-standard)
                SET_STANDARD="$2"
                shift 2
                ;;
            --help)
                show_help
                ;;
            *)
                log_error "未知参数: $1"
                exit 1
                ;;
        esac
    done
}

# 验证参数
validate_args() {
    # 验证模型
    case $MODEL in
        wan2.5-i2v-preview|wan2.6-i2v-flash)
            ;;
        wan2.5)
            MODEL="wan2.5-i2v-preview"
            ;;
        wan2.6)
            MODEL="wan2.6-i2v-flash"
            ;;
        *)
            log_error "不支持的模型: $MODEL"
            exit 1
            ;;
    esac

    # 验证分辨率
    if [[ ! "$RESOLUTION" =~ ^(720|1080)$ ]]; then
        log_error "不支持的分辨率: $RESOLUTION (支持: 720, 1080)"
        exit 1
    fi

    # 验证时长
    if [[ ! "$DURATION" =~ ^(5|10|15)$ ]]; then
        log_error "不支持的时长: $DURATION (支持: 5, 10, 15)"
        exit 1
    fi

    # 验证配音
    if [[ ! "$VOICE" =~ ^(yes|no)$ ]]; then
        log_error "不支持的配音选项: $VOICE (支持: yes, no)"
        exit 1
    fi
}

# 设置标准模型
set_standard_model() {
    if [[ -z "$SET_STANDARD" ]]; then
        return
    fi

    if [[ ! -f "$SET_STANDARD" ]]; then
        log_error "文件不存在: $SET_STANDARD"
        exit 1
    fi

    cp "$SET_STANDARD" "$STANDARD_MODEL"
    log_success "标准模型已更新: $STANDARD_MODEL"
    log_info "文件大小: $(ls -lh "$STANDARD_MODEL" | awk '{print $5}')"
    exit 0
}

# 生成提示词
generate_prompt() {
    if [[ -n "$PROMPT" ]]; then
        echo "$PROMPT"
        return
    fi

    # 根据时长生成不同的动作描述
    local action=""
    case $DURATION in
        5)
            action="Camera slowly zooms in, little red lobster mascot '小爪' looking curiously at camera, 3D cartoon style"
            ;;
        10)
            action="Camera slowly zooms in, little red lobster mascot '小爪' tilting head好奇地, blinking eyes, looking at camera, 3D cartoon style"
            ;;
        15)
            action="Camera slowly zooms in, little red lobster mascot '小爪' tilting head好奇地, blinking eyes, then waving at camera with claw, 3D cartoon style"
            ;;
    esac

    # 虚拟空间背景
    local background="in futuristic virtual reality space, holographic screens, purple and blue neon lights, digital particles floating, cyberpunk aesthetic"

    echo "$action, $background"
}

# 调用API生成视频
generate_video() {
    local prompt="$1"
    local timestamp=$(date +%Y-%m-%d_%H%M%S)
    local output_file="${OUTPUT_DIR}/clawlet_video_${timestamp}.mp4"
    local size="${RESOLUTION}x$((RESOLUTION*16/9))"

    log_info "开始生成视频..."
    log_info "模型: $MODEL"
    log_info "分辨率: ${RESOLUTION}P"
    log_info "时长: ${DURATION}秒"
    log_info "配音: $VOICE"
    log_info "提示词: $prompt"
    echo ""

    # 使用Python调用API
    python3 << PYEOF
import os
import sys
import json
import time
import requests
from datetime import datetime

# 配置
API_KEY = os.getenv("DASHSCOPE_API_KEY", "$API_KEY")
BASE_URL = "https://dashscope.aliyuncs.com/api/v1"
MODEL = "$MODEL"
IMAGE_PATH = "$STANDARD_MODEL"
PROMPT = """$prompt"""
DURATION = $DURATION
SIZE = "$size"
VOICE = "$VOICE" == "yes"
OUTPUT_FILE = "$output_file"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

print("="*60)
print("🎬 开始生成视频")
print("="*60)
print(f"模型: {MODEL}")
print(f"图片: {IMAGE_PATH}")
print(f"时长: {DURATION}秒")
print(f"分辨率: {SIZE}")
print(f"配音: {'是' if VOICE else '否'}")
print("="*60)

# 构建请求
payload = {
    "model": MODEL,
    "input": {
        "img_url": f"file://{IMAGE_PATH}",
        "prompt": PROMPT
    },
    "parameters": {
        "duration": DURATION,
        "size": SIZE,
        "audio": VOICE
    }
}

# 提交任务
print("\n📤 提交任务...")
response = requests.post(
    f"{BASE_URL}/services/aigc/video-generation/generation",
    headers=headers,
    json=payload,
    timeout=60
)

result = response.json()
print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")

if "task_id" not in result.get("output", {}):
    print(f"\n❌ 任务提交失败: {result}")
    sys.exit(1)

task_id = result["output"]["task_id"]
print(f"\n✅ 任务已提交! ID: {task_id}")

# 轮询结果
print("\n⏳ 等待生成...")
poll_interval = 5
max_wait = 300
start_time = time.time()

while time.time() - start_time < max_wait:
    time.sleep(poll_interval)
    
    try:
        status_resp = requests.get(
            f"{BASE_URL}/tasks/{task_id}",
            headers=headers,
            timeout=30
        )
        status_result = status_resp.json()
        status = status_result.get("output", {}).get("task_status", "UNKNOWN")
        
        elapsed = int(time.time() - start_time)
        print(f"[{elapsed}s] 状态: {status}")
        
        if status == "SUCCEEDED":
            video_url = status_result["output"]["video_url"]
            print(f"\n✅ 生成完成!")
            print(f"🎥 视频URL: {video_url}")
            
            # 下载视频
            print("\n📥 下载视频...")
            video_resp = requests.get(video_url, timeout=120)
            
            if video_resp.status_code == 200:
                with open(OUTPUT_FILE, 'wb') as f:
                    f.write(video_resp.content)
                print(f"💾 已保存: {OUTPUT_FILE}")
                print(f"📊 大小: {len(video_resp.content)/1024/1024:.2f} MB")
                
                # 更新latest链接
                latest_link = "/home/admin/.openclaw/workspace/clawlet_latest.mp4"
                if os.path.exists(latest_link):
                    os.remove(latest_link)
                os.symlink(OUTPUT_FILE, latest_link)
                print(f"🔗 更新链接: {latest_link}")
                
                sys.exit(0)
            else:
                print(f"❌ 下载失败: {video_resp.status_code}")
                sys.exit(1)
                
        elif status == "FAILED":
            print(f"\n❌ 任务失败: {status_result}")
            sys.exit(1)
            
    except Exception as e:
        print(f"⚠️ 查询出错: {e}")

print("\n⏰ 等待超时")
sys.exit(1)
PYEOF

    return $?
}

# 主函数
main() {
    echo "🎬 Clawlet Video Generator"
    echo "=========================="
    echo ""

    # 解析参数
    parse_args "$@"

    # 设置标准模型
    set_standard_model

    # 验证参数
    validate_args

    # 检查标准模型
    if [[ ! -f "$STANDARD_MODEL" ]]; then
        log_error "标准模型不存在: $STANDARD_MODEL"
        log_info "请先设置标准模型:"
        log_info "  $(basename "$0") --set-standard /path/to/image.png"
        exit 1
    fi

    # 生成提示词
    local prompt=$(generate_prompt)

    # 生成视频
    generate_video "$prompt"
    local exit_code=$?

    if [[ $exit_code -eq 0 ]]; then
        echo ""
        log_success "视频生成完成!"
        log_info "下载链接: http://8.130.18.239:8080/clawlet_latest.mp4"
    else
        echo ""
        log_error "视频生成失败"
        exit 1
    fi
}

# 运行主函数
main "$@"
