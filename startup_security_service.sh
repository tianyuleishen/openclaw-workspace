#!/bin/bash
# OpenClaw Security System Startup Script

# 设置环境变量
export NODE_PATH=$(npm root -g)
export PATH=$PATH:/usr/local/bin:$HOME/.nvm/versions/node/$(node -v)/bin

# 定义工作目录
WORKSPACE_DIR="$HOME/.openclaw/workspace"
LOG_FILE="$WORKSPACE_DIR/security_service_startup.log"

# 检查Node.js是否可用
if ! command -v node &> /dev/null; then
    echo "$(date): Node.js not found in PATH" >> "$LOG_FILE"
    exit 1
fi

# 检查端口3009是否被占用
if lsof -Pi :3009 -sTCP:LISTEN -t >/dev/null; then
    echo "$(date): Port 3009 already in use, killing existing process" >> "$LOG_FILE"
    lsof -ti:3009 | xargs kill -9 2>/dev/null || true
fi

# 启动安全系统
echo "$(date): Starting OpenClaw Security System..." >> "$LOG_FILE"
cd "$WORKSPACE_DIR"
nohup node start_security_system.js >> "$LOG_FILE" 2>&1 &

# 等待几秒后检查是否启动成功
sleep 5

if lsof -Pi :3009 -sTCP:LISTEN -t >/dev/null; then
    echo "$(date): OpenClaw Security System started successfully on port 3009" >> "$LOG_FILE"
else
    echo "$(date): Failed to start OpenClaw Security System" >> "$LOG_FILE"
fi
