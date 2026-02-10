#!/bin/bash
# Self-Improvement Proactive Agent
# 自我改进主动代理 - 一键执行所有主动行为

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 启动自我改进主动代理"
echo "=================================="
echo ""

# 1. 执行健康检查
echo "📊 Step 1: 系统健康检查"
bash "$SCRIPT_DIR/self_health_check.sh"
echo ""

# 2. Token 使用分析
echo "📈 Step 2: Token 使用分析"
bash "$SCRIPT_DIR/token_monitor.sh"
echo ""

# 3. 技能维护
echo "🛠️ Step 3: 技能维护检查"
bash "$SCRIPT_DIR/skills_maintenance.sh" check
echo ""

# 4. 检查进化循环状态
echo "🧬 Step 4: 进化引擎状态"
if pgrep -f "node index.js --loop" > /dev/null; then
    echo "  ✅ 进化引擎运行中"
    EVOLVE_PID=$(pgrep -f "node index.js --loop" | head -1)
    echo "    PID: $EVOLVE_PID"
    
    # 检查最近的进化日志
    if [ -f /tmp/evolver_loop.log ]; then
        LAST_LINE=$(tail -5 /tmp/evolver_loop.log 2>/dev/null)
        echo "    最后日志: $LAST_LINE"
    fi
else
    echo "  ⚠️ 进化引擎未运行"
    echo "    建议: cd /home/admin/.openclaw/workspace/skills/evolver && nohup node index.js --loop > /tmp/evolver_loop.log 2>&1 &"
fi
echo ""

# 5. 检查 Moltbook 心跳
echo "💓 Step 5: Moltbook 心跳检查"
if [ -f ~/.config/moltbook/last_heartbeat_check ]; then
    LAST_CHECK=$(cat ~/.config/moltbook/last_heartbeat_check)
    echo "  ✅ $LAST_CHECK"
    
    # 计算时间差
    LAST_EPOCH=$(date -d "$LAST_CHECK" +%s 2>/dev/null)
    NOW_EPOCH=$(date +%s)
    DIFF=$((NOW_EPOCH - LAST_EPOCH))
    
    if [ $DIFF -gt 1800 ]; then
        echo "  ⚠️ 超过 30 分钟未检查"
        echo "    建议: 执行心跳检查"
    else
        echo "    距离上次检查: $((DIFF / 60)) 分钟"
    fi
else
    echo "  ⚠️ 从未执行心跳检查"
fi
echo ""

# 6. 检查系统更新
echo "🔄 Step 6: 系统更新检查"
echo "  - 检查 ClawHub 更新..."
npx clawhub --version 2>/dev/null || echo "  ⚠️ 无法检查 ClawHub 版本"
echo ""

# 总结
echo "=================================="
echo "✅ 主动检查完成 - $(date)"
echo ""
echo "💡 建议后续操作:"
echo "  1. 审查 token 使用，优化大文件"
echo "  2. 更新有问题的技能文档"
echo "  3. 如果进化引擎未运行，考虑启动"
echo "  4. 执行 Moltbook 心跳检查"
