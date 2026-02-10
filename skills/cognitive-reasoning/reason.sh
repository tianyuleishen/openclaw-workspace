#!/bin/bash
#=========================================
# Cognitive Reasoning CLI - Think First Tool
#=========================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_header() {
    echo ""
    echo -e "${CYAN}🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠"
    echo -e "🧠  COGNITIVE REASONING FRAMEWORK"
    echo -e "🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠"
    echo ""
}

print_thinking() {
    echo -e "${BLUE}🤔 Thinking...${NC}"
}

print_intent() {
    echo -e "${GREEN}🎯 Intent: $1${NC}"
}

print_ambiguity() {
    echo -e "${YELLOW}🔍 Ambiguity: $1${NC}"
}

print_confidence() {
    echo -e "${CYAN}📊 Confidence: $1%${NC}"
}

print_status() {
    local status=$1
    if [[ "$status" == "ready" ]]; then
        echo -e "${GREEN}✅ HIGH CONFIDENCE - Ready to execute${NC}"
    else
        echo -e "${YELLOW}⚠️ LOW CONFIDENCE - Clarification needed${NC}"
    fi
}

# Example think process
think_example() {
    print_header
    print_thinking
    echo ""
    
    echo -e "${BLUE}User: \"检查服务器\"${NC}"
    echo ""
    
    print_intent "CHECK_STATUS (85%)"
    print_ambiguity "What aspect? (Health/Logs/Performance)"
    print_confidence "65"
    echo ""
    print_status "clarification"
    echo ""
    
    echo -e "${YELLOW}🤔 Questions for clarification:${NC}"
    echo "  1. What should I check?"
    echo "     [1] Health (ports, ping)"
    echo "     [2] Logs (error/access)"
    echo "     [3] Performance (CPU/memory)"
    echo "     [4] All of the above"
    echo ""
    
    echo -e "${BLUE}💡 Recommended: Start with option [1]${NC}"
}

# Main usage
usage() {
    cat << EOF
🧠 Cognitive Reasoning Tool

用法: $(basename "$0") [命令]

命令:
  think "用户消息"    - 分析消息，理解意图
  example           - 显示思考过程示例
  status            - 检查当前置信度
  log               - 查看推理日志

示例:
  $(basename "$0") think "检查服务器状态"
  $(basename "$0") example

特点:
  - 推理前先思考
  - 意图分类
  - 歧义检测
  - 澄清循环
  - 置信度评估

EOF
}

case "${1:-}" in
    think)
        shift
        print_header
        print_thinking
        echo ""
        echo -e "${BLUE}User: \"$*\"${NC}"
        echo ""
        print_intent "ANALYZING..."
        print_confidence "Calculating..."
        echo ""
        ;;
    example)
        think_example
        ;;
    status)
        print_header
        echo -e "${GREEN}🧠 Reasoning System: ACTIVE${NC}"
        echo -e "${CYAN}Confidence Threshold: 70%${NC}"
        ;;
    log)
        echo -e "${BLUE}📝 Recent reasoning logs:${NC}"
        ls -la ~/.openclaw/workspace/memory/reasoning_*.json 2>/dev/null | tail -5 || echo "No logs found"
        ;;
    *)
        usage
        ;;
esac
