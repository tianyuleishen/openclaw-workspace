#!/bin/bash
# 🦞 小爪记忆管理系统
# 自动备份和恢复重要记忆

MEMORY_DIR="/home/admin/.openclaw/workspace/memory"
BACKUP_DIR="/home/admin/.openclaw/workspace/.backup"

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 需要备份的关键文件
CRITICAL_FILES=(
    "clawlet_fixed_style.md"
    "MEMORY_SYSTEM_FIX.md"
    "MEMORY.md"
)

echo "🧠 小爪记忆管理系统"
echo "===================="

# 备份关键文件
backup_file() {
    local file=$1
    if [ -f "$MEMORY_DIR/$file" ]; then
        cp "$MEMORY_DIR/$file" "$BACKUP_DIR/${file}.backup.$(date +%Y%m%d)"
        echo "✅ 备份: $file"
    else
        echo "⚠️ 缺失: $file"
    fi
}

# 列出所有记忆文件
list_memories() {
    echo "\n📁 记忆文件列表:"
    ls -lh "$MEMORY_DIR"/*.md 2>/dev/null | awk '{print $9, "(" $5 ")"}'
}

# 查找关键词
search_memory() {
    local keyword=$1
    echo "\n🔍 搜索: $keyword"
    grep -r "$keyword" "$MEMORY_DIR"/*.md 2>/dev/null | head -10
}

# 显示今日记录
show_today() {
    local today=$(date +%Y-%m-%d)
    local file="$MEMORY_DIR/$today.md"
    if [ -f "$file" ]; then
        cat "$file"
    else
        echo "今日记录为空"
    fi
}

case "$1" in
    backup)
        echo "💾 备份关键文件..."
        for file in "${CRITICAL_FILES[@]}"; do
            backup_file "$file"
        done
        ;;
    list)
        list_memories
        ;;
    search)
        search_memory "$2"
        ;;
    today)
        show_today
        ;;
    restore)
        echo "🔄 从备份恢复..."
        ls "$BACKUP_DIR"/*.backup.* 2>/dev/null | tail -5
        ;;
    *)
        echo "使用方法:"
        echo "  $0 backup     - 备份关键文件"
        echo "  $0 list       - 列出记忆文件"
        echo "  $0 search <词> - 搜索关键词"
        echo "  $0 today      - 查看今日记录"
        echo "  $0 restore    - 查看可用备份"
        ;;
esac
