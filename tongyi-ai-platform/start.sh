#!/bin/bash

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 启动通义万相 AI 生成平台${NC}"
echo "========================================"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 未找到 Python3，请先安装 Python${NC}"
    exit 1
fi

# 检查依赖
echo -e "${YELLOW}📦 检查依赖...${NC}"
pip install -q flask flask-cors dashscope requests

# 检查环境变量
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  未找到 .env 文件，复制模板...${NC}"
    cp .env.example .env
    echo -e "${RED}请编辑 .env 文件，填入您的 API Key${NC}"
    exit 1
fi

# 检查 API Key
if grep -q "sk-您的APIKey" .env; then
    echo -e "${RED}❌ 请编辑 .env 文件，填入有效的 API Key${NC}"
    exit 1
fi

# 启动服务
echo -e "${GREEN}✅ 启动服务...${NC}"
python3 app.py
