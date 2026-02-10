#!/bin/bash
#=========================================
# Clawlet Video Generator - 安装脚本
#=========================================

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$HOME/.local/bin"

echo "🎬 安装 Clawlet Video Generator 技能"
echo "===================================="

# 创建bin目录
if [[ ! -d "$BIN_DIR" ]]; then
    echo "📁 创建 bin 目录..."
    mkdir -p "$BIN_DIR"
fi

# 复制脚本
echo "📦 安装脚本..."
cp "$SKILL_DIR/clawlet-video-generator.sh" "$BIN_DIR/clawlet-video-generator"
chmod +x "$BIN_DIR/clawlet-video-generator"

# 添加到PATH (如果需要)
SHELL_RC=""
if [[ -f "$HOME/.bashrc" ]]; then
    SHELL_RC="$HOME/.bashrc"
elif [[ -f "$HOME/.zshrc" ]]; then
    SHELL_RC="$HOME/.zshrc"
fi

if [[ -n "$SHELL_RC" ]]; then
    if ! grep -q "$BIN_DIR" "$SHELL_RC" 2>/dev/null; then
        echo "" >> "$SHELL_RC"
        echo "# Clawlet Video Generator" >> "$SHELL_RC"
        echo "export PATH=\"$BIN_DIR:\$PATH\"" >> "$SHELL_RC"
        echo "✅ 已添加到 PATH"
    fi
fi

echo ""
echo "✅ 安装完成!"
echo ""
echo "使用方式:"
echo "--------"
echo "  clawlet-video-generator --help"
echo ""
echo "示例:"
echo "  # 生成5秒视频"
echo "  clawlet-video-generator --model wan2.5 --resolution 1080 --duration 5"
echo ""
echo "  # 设置新的标准模型"
echo "  clawlet-video-generator --set-standard /path/to/new_image.png"
echo ""
echo "标准模型位置: /tmp/clawlet_model_standard.png"
