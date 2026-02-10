#!/bin/bash
# Self-Improvement Health Check Script
# 主动健康检查脚本

echo "🔍 执行自我改进健康检查..."
echo "=================================="
echo ""

# 1. 系统资源检查
echo "📊 系统资源状态:"
echo "  - 磁盘空间:"
df -h /home | tail -1 | awk '{print "    " $1 " 使用率: " $5 " (剩余: " $4 ")"}'
echo "  - 内存使用:"
free -h | grep Mem | awk '{print "    已用: " $3 "/" $2 " (" $3/$2*100 "%)"}'
echo ""

# 2. OpenClaw 进程状态
echo "🔄 OpenClaw 进程状态:"
# 使用多种方法检测 OpenClaw
OPENCLAW_PID=""
for proc in "openclaw-gateway" "openclaw"; do
    if PID=$(pgrep -x "$proc" 2>/dev/null | head -1); then
        OPENCLAW_PID=$PID
        break
    fi
done

# 如果没找到，尝试使用进程列表
if [ -z "$OPENCLAW_PID" ]; then
    OPENCLAW_PID=$(ps aux | grep -E "openclaw" | grep -v grep | awk '{print $2}' | head -1)
fi

if [ -n "$OPENCLAW_PID" ]; then
    # 取第一个 PID
    OPENCLAW_PID=$(echo "$OPENCLAW_PID" | head -1)
    echo "  ✅ OpenClaw 运行中"
    UPTIME=$(ps -o etime= -p "$OPENCLAW_PID" 2>/dev/null | tr -d ' ')
    echo "    PID: $OPENCLAW_PID"
    if [ -n "$UPTIME" ]; then
        echo "    运行时间: $UPTIME"
    fi
else
    echo "  ❌ OpenClaw 未运行"
fi
echo ""

# 3. 进化引擎状态
echo "🧬 进化引擎状态:"
if pgrep -f "node index.js --loop" > /dev/null; then
    echo "  ✅ Loop 模式运行中"
    EVOLVE_PID=$(pgrep -f "node index.js --loop" | head -1)
    echo "    PID: $EVOLVE_PID"
else
    echo "  ⚠️ Loop 模式未运行"
fi
echo ""

# 4. 心跳检查
echo "💓 最后心跳检查:"
if [ -f ~/.config/moltbook/last_heartbeat_check ]; then
    LAST_CHECK=$(cat ~/.config/moltbook/last_heartbeat_check)
    echo "  ✅ $LAST_CHECK"
else
    echo "  ⚠️ 从未执行心跳检查"
fi
echo ""

# 5. 技能统计
echo "🛠️ 技能统计:"
SKILLS_COUNT=$(ls /home/admin/.openclaw/workspace/skills/ | wc -l)
echo "  - 已安装技能: $SKILLS_COUNT 个"
echo ""

# 6. 内存文件统计
echo "🧠 记忆系统状态:"
if [ -d /home/admin/.openclaw/workspace/memory ]; then
    MEMORY_FILES=$(ls /home/admin/.openclaw/workspace/memory/*.md 2>/dev/null | wc -l)
    echo "  - 记忆文件: $MEMORY_FILES 个"
    
    # 检查 MEMORY.md
    if [ -f /home/admin/.openclaw/workspace/MEMORY.md ]; then
        MEMORY_SIZE=$(wc -c < /home/admin/.openclaw/workspace/MEMORY.md)
        echo "    MEMORY.md: $((MEMORY_SIZE / 1024)) KB"
    fi
else
    echo "  ⚠️ 记忆目录不存在"
fi
echo ""

# 7. Git 状态 (如果有改动)
echo "📝 Git 工作区状态:"
cd /home/admin/.openclaw/workspace
if git rev-parse --git-dir > /dev/null 2>&1; then
    CHANGES=$(git status --short 2>/dev/null | wc -l)
    if [ "$CHANGES" -gt 0 ]; then
        echo "  📌 $CHANGES 个文件有改动"
        git status --short | head -5
    else
        echo "  ✅ 工作区干净"
    fi
else
    echo "  ⚠️ 非 Git 仓库"
fi
echo ""

echo "=================================="
echo "✅ 健康检查完成 - $(date)"
