#!/bin/bash
# Token Usage Monitor
# Token 使用监控脚本

echo "📊 Token 使用统计分析"
echo "=================================="
echo ""

# 1. 检查最近的文件修改
echo "📁 最近修改的文件 (24小时内):"
find /home/admin/.openclaw/workspace -name "*.md" -mtime -1 -exec ls -lh {} \; 2>/dev/null | tail -10
echo ""

# 2. 检查会话日志
echo "💬 会话日志统计:"
if [ -d /home/admin/.openclaw/workspace/.sessions ]; then
    SESSION_COUNT=$(ls /home/admin/.openclaw/workspace/.sessions/*.jsonl 2>/dev/null | wc -l)
    echo "  - 会话文件: $SESSION_COUNT 个"
    
    if [ "$SESSION_COUNT" -gt 0 ]; then
        TOTAL_SIZE=$(du -sh /home/admin/.openclaw/workspace/.sessions 2>/dev/null | cut -f1)
        echo "  - 总大小: $TOTAL_SIZE"
        
        # 最近会话大小
        LATEST_SESSION=$(ls -t /home/admin/.openclaw/workspace/.sessions/*.jsonl 2>/dev/null | head -1)
        if [ -n "$LATEST_SESSION" ]; then
            LATEST_SIZE=$(wc -c < "$LATEST_SESSION")
            echo "  - 最近会话: $((LATEST_SIZE / 1024)) KB"
        fi
    fi
else
    echo "  ⚠️ 会话目录不存在"
fi
echo ""

# 3. 检查 memory 目录
echo "🧠 Memory 目录分析:"
if [ -d /home/admin/.openclaw/workspace/memory ]; then
    MEMORY_COUNT=$(ls /home/admin/.openclaw/workspace/memory/*.md 2>/dev/null | wc -l)
    MEMORY_SIZE=$(du -sh /home/admin/.openclaw/workspace/memory 2>/dev/null | cut -f1)
    echo "  - 文件数: $MEMORY_COUNT"
    echo "  - 总大小: $MEMORY_SIZE"
    
    # 最大的 memory 文件
    echo "  - 最大文件:"
    ls -S /home/admin/.openclaw/workspace/memory/*.md 2>/dev/null | head -3 | while read f; do
        SIZE=$(wc -c < "$f")
        NAME=$(basename "$f")
        echo "    $NAME: $((SIZE / 1024)) KB"
    done
else
    echo "  ⚠️ memory 目录不存在"
fi
echo ""

# 4. 检查技能文档
echo "🛠️ 技能文档统计:"
SKILLS_DIR="/home/admin/.openclaw/workspace/skills"
if [ -d "$SKILLS_DIR" ]; then
    SKILL_COUNT=$(ls -d "$SKILLS_DIR"/*/ 2>/dev/null | wc -l)
    echo "  - 技能数: $SKILL_COUNT"
    
    # 检查 SKILL.md 文件
    SKILL_MD_COUNT=$(find "$SKILLS_DIR" -name "SKILL.md" 2>/dev/null | wc -l)
    echo "  - SKILL.md 文件: $SKILL_MD_COUNT"
    
    # 最大的 SKILL.md
    LARGEST_SKILL=$(find "$SKILLS_DIR" -name "SKILL.md" -exec ls -S {} \; 2>/dev/null | head -1)
    if [ -n "$LARGEST_SKILL" ]; then
        SIZE=$(wc -c < "$LARGEST_SKILL")
        NAME=$(dirname "$LARGEST_SKILL" | xargs -I {} basename {})
        echo "  - 最大 SKILL.md: $NAME ($(($SIZE / 1024)) KB)"
    fi
fi
echo ""

# 5. 建议
echo "💡 优化建议:"
echo "  1. 定期归档旧的 memory 文件"
echo "  2. 合并重复的技能文档"
echo "  3. 使用压缩工具减少文件大小"
echo "  4. 清理不需要的会话日志"
echo ""

echo "=================================="
echo "✅ 分析完成 - $(date)"
