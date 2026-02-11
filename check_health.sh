#!/bin/bash
# 小爪健康检查脚本
# 用法: bash /home/admin/.openclaw/workspace/check_health.sh

echo "🏥 小爪健康检查"
echo "================"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 颜色
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 检查函数
check_service() {
    local name=$1
    local cmd=$2
    local result=$(eval $cmd 2>/dev/null)
    
    if [ -z "$result" ]; then
        echo -e "${RED}❌ $name: 无法连接${NC}"
        return 1
    elif [[ "$result" == *"200"* ]] || [[ "$result" == *"healthy"* ]]; then
        echo -e "${GREEN}✅ $name: 正常${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠️ $name: $result${NC}"
        return 2
    fi
}

# 1. OpenClaw Gateway
echo "🔍 服务状态:"
check_service "OpenClaw (3003)" "curl -s -o /dev/null -w '%{http_code}' http://localhost:3003/api/status 2>/dev/null"
check_service "安全系统 (3009)" "curl -s http://localhost:3009/health 2>/dev/null | grep -o '\"status\":\"[^\"]*\"'"

# 2. 系统资源
echo ""
echo "💻 系统资源:"
echo "  CPU负载: $(top -b -n 1 | grep 'Cpu(s)' | awk '{print $2}')"
MEM=$(free -h | grep Mem:)
echo "  内存: $MEM"

# 3. 磁盘空间
echo ""
echo "💾 磁盘使用:"
df -h /home/admin/.openclaw/workspace | tail -1 | awk '{print "  使用率: " $5 " / 可用: " $4}'

# 4. Git状态
echo ""
echo "📦 Git状态:"
UNCOMMITTED=$(git status --short 2>/dev/null | wc -l)
echo "  待提交: $UNCOMMITTED"

# 5. 进程数
echo ""
echo "🔄 进程:"
PROCS=$(ps aux | grep -E "python|node" | grep -v grep | wc -l)
echo "  Python/Node进程: $PROCS"

# 总结
echo ""
echo "================"
echo "✅ 健康检查完成!"
