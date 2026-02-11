#!/bin/bash
# 小爪自我净化系统 - 系统清理与优化
# 执行时间: $(date)

echo "🦞 小爪自我净化系统启动"
echo "========================"
echo "🕐 时间: $(date)"
echo ""

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

print_step() {
    echo -e "${BLUE}[步骤]${NC} $1"
}

print_ok() {
    echo -e "${GREEN}[完成]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[警告]${NC} $1"
}

print_err() {
    echo -e "${RED}[错误]${NC} $1"
}

# 1. 清理临时文件
print_step "1. 清理临时文件..."
find /home/admin/.openclaw/workspace -name "*.tmp" -type f -delete 2>/dev/null
find /home/admin/.openclaw/workspace -name ".temp_*" -type d -exec rm -rf {} + 2>/dev/null
print_ok "临时文件清理完成"

# 2. 清理 __pycache__
print_step "2. 清理 Python 缓存..."
find /home/admin/.openclaw/workspace -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find /home/admin/.openclaw/workspace -name "*.pyc" -delete 2>/dev/null
print_ok "Python 缓存清理完成"

# 3. 清理 node_modules 过大目录（可选，注释掉）
# print_step "3. 检查 node_modules..."
# du -sh /home/admin/.openclaw/workspace/node_modules 2>/dev/null

# 4. 清理过期日志
print_step "4. 清理过期日志..."
find /home/admin/.openclaw/workspace/logs -name "*.log" -mtime +7 -delete 2>/dev/null
print_ok "过期日志清理完成"

# 5. 清理 economy_status JSON 文件（保留最近30天）
print_step "5. 清理过期状态文件..."
find /home/admin/.openclaw/workspace -name "economy_status_*.json" -mtime +30 -delete 2>/dev/null
print_ok "过期状态文件清理完成"

# 6. 检查并清理僵尸进程
print_step "6. 检查系统资源..."
echo "   内存使用:"
free -h | grep -E "^Mem:|^Swap:"
echo "   磁盘使用:"
df -h /home/admin/.openclaw/workspace | tail -1

# 7. 检查关键服务状态
echo ""
print_step "7. 检查服务状态..."
echo "   - 安全系统 (3009): $(curl -s -o /dev/null -w "%{http_code}" http://localhost:3009/health 2>/dev/null || echo '未运行')"
echo "   - 进程数量: $(ps aux | grep -E 'node|python' | grep -v grep | wc -l)"

# 8. 内存优化提示
echo ""
print_step "8. 内存优化..."
sync
echo 3 > /proc/sys/vm/drop_caches 2>/dev/null || print_warn "需要root权限，无法清理缓存"

# 9. 清理会话历史
print_step "9. 清理临时会话..."
find /home/admin/.openclaw/workspace -name ".conversation_history.json" -size +1M -exec truncate -s 0 {} \; 2>/dev/null || true

echo ""
echo "========================"
print_ok "🦞 自我净化完成！"
echo "🕐 完成时间: $(date)"
echo ""
echo "💡 提示: 如需深度优化，请重启卡顿的服务"
