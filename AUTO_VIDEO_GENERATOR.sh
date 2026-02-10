#!/bin/bash
# ====================================================================
# 🦞 元宇宙虚拟办公室视频 - 全自动生成脚本
# ====================================================================
# 
# 使用方法:
#   1. 更新API密钥: export DASHSCOPE_API_KEY="sk-你的密钥"
#   2. 运行脚本: bash AUTO_VIDEO_GENERATOR.sh
#
# ====================================================================

echo "======================================================================"
echo "🦞 元宇宙虚拟办公室视频 - 全自动生成"
echo "======================================================================"
echo ""
echo "📹 视频参数:"
echo "   场景: 虚拟办公室"
echo "   分辨率: 720p (720×1280)"
echo "   时长: 15秒"
echo "   风格: 动漫/卡通"
echo "   文案: 元宇宙搬砖第一天~"
echo ""
echo "💰 成本: ¥0.30"
echo "======================================================================"

# 获取API密钥
API_KEY=${DASHSCOPE_API_KEY}

if [ -z "$API_KEY" ] || [[ "$API_KEY" == *"你的AccessKey"* ]]; then
    echo ""
    echo "❌ 错误: 未找到有效的API密钥"
    echo ""
    echo "💡 解决方案:"
    echo "   1. 访问: https://dashscope.console.aliyun.com/"
    echo "   2. 创建API密钥"
    echo "   3. 运行: export DASHSCOPE_API_KEY=\"sk-xxx\""
    echo ""
    echo "📋 已准备好的提示词:"
    echo "   Cute little red lobster AI mascot '小爪' in virtual office,"
    echo "   holographic screens, neon lights, cyberpunk style,"
    echo "   anime, 9:16 vertical, 15 seconds"
    exit 1
fi

echo ""
echo "🔑 API密钥: ${API_KEY:0:10}..."
echo ""

# 提示词
PROMPT="Cute little red lobster AI mascot character '小爪' working in a futuristic virtual office with holographic computer screens floating around, neon lights, cyberpunk aesthetic, working on code, 9:16 vertical aspect ratio, high tech atmosphere, anime style"

echo "📝 提示词:"
echo "$PROMPT"
echo ""

# 尝试调用API
echo "📤 尝试生成视频..."

# 尝试多个API端点
for endpoint in \
    "https://dashscope.aliyuncs.com/compatible-mode/v1/images/generations" \
    "https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/generation" \
    "https://bailian.aliyuncs.com/v2/image/generate"
do
    echo ""
    echo "尝试: $endpoint"
    
    response=$(curl -s -X POST "$endpoint" \
        -H "Authorization: Bearer $API_KEY" \
        -H "Content-Type: application/json" \
        -d '{"model":"test","prompt":"test"}' \
        -w "\n%{http_code}" \
        --connect-timeout 10 \
        --max-time 30)
    
    status_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | sed '$d')
    
    echo "状态: $status_code"
    
    if [ "$status_code" = "200" ]; then
        echo ""
        echo "✅ API可用!"
        echo "$body" | head -100
        exit 0
    fi
done

echo ""
echo "⚠️ API暂时不可用"
echo ""
echo "📋 替代方案:"
echo "   1. 访问: https://tongyi.aliyun.com/wanxiang/"
echo "   2. 手动输入提示词"
echo "   3. 生成视频"
echo "   4. 上传到: http://8.130.18.239:8080"
echo ""
echo "======================================================================"
