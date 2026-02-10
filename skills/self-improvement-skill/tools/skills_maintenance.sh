#!/bin/bash
# Skills Maintenance Script
# 技能维护脚本

echo "🛠️ 技能维护工具"
echo "=================================="
echo ""

SKILLS_DIR="/home/admin/.openclaw/workspace/skills"

# 功能选择
case "${1:-status}" in
    status)
        echo "📊 技能状态:"
        echo ""
        
        # 列出所有技能
        echo "已安装的技能:"
        ls -d "$SKILLS_DIR"/*/ 2>/dev/null | while read dir; do
            NAME=$(basename "$dir")
            
            # 检查 SKILL.md
            if [ -f "$dir/SKILL.md" ]; then
                HAS_SKILL="✅"
            else
                HAS_SKILL="❌"
            fi
            
            # 检查 README.md
            if [ -f "$dir/README.md" ]; then
                HAS_README="✅"
            else
                HAS_README="❌"
            fi
            
            # 检查 scripts 目录
            if [ -d "$dir/scripts" ]; then
                HAS_SCRIPTS="✅"
            else
                HAS_SCRIPTS="❌"
            fi
            
            # 获取最后修改时间
            LAST_MOD=$(stat -c %y "$dir" 2>/dev/null | cut -d' ' -f1)
            
            echo "  🦞 $NAME"
            echo "      SKILL.md: $HAS_SKILL | README.md: $HAS_README | scripts: $HAS_SCRIPTS"
            echo "      最后更新: $LAST_MOD"
            echo ""
        done
        
        # 统计
        TOTAL=$(ls -d "$SKILLS_DIR"/*/ 2>/dev/null | wc -l)
        WITH_SKILL=$(find "$SKILLS_DIR" -name "SKILL.md" 2>/dev/null | wc -l)
        echo "📈 统计: $TOTAL 个技能, $WITH_SKILL 个有 SKILL.md"
        ;;
        
    check)
        echo "🔍 检查技能完整性..."
        echo ""
        
        ls -d "$SKILLS_DIR"/*/ 2>/dev/null | while read dir; do
            NAME=$(basename "$dir")
            ISSUES=()
            
            if [ ! -f "$dir/SKILL.md" ]; then
                ISSUES+=("缺少 SKILL.md")
            fi
            
            if [ ! -f "$dir/README.md" ]; then
                ISSUES+=("缺少 README.md")
            fi
            
            if [ ${#ISSUES[@]} -gt 0 ]; then
                echo "❌ $NAME:"
                for issue in "${ISSUES[@]}"; do
                    echo "   - $issue"
                done
            else
                echo "✅ $NAME - 完整"
            fi
        done
        ;;
        
    audit)
        echo "🔒 安全审计..."
        echo ""
        
        # 检查敏感信息
        echo "检查敏感信息暴露:"
        SENSITIVE_COUNT=$(grep -r "api_key\|apikey\|secret\|password\|token" "$SKILLS_DIR" --include="*.md" 2>/dev/null | grep -v "REDACTED\|MASKED\|\*\*\*" | wc -l)
        if [ "$SENSITIVE_COUNT" -gt 0 ]; then
            echo "  ⚠️ 发现 $SENSITIVE_COUNT 个可能敏感的内容"
            grep -r "api_key\|apikey\|secret\|password\|token" "$SKILLS_DIR" --include="*.md" 2>/dev/null | grep -v "REDACTED\|MASKED\|\*\*\*" | head -5
        else
            echo "  ✅ 未发现明显的敏感信息"
        fi
        echo ""
        
        # 检查 git 忽略
        echo "Git 忽略检查:"
        if [ -f "$SKILLS_DIR/.gitignore" ]; then
            echo "  ✅ .gitignore 存在"
        else
            echo "  ⚠️ .gitignore 不存在"
        fi
        ;;
        
    update)
        echo "📦 更新技能文档..."
        echo ""
        
        # 更新 skills 索引
        echo "生成 skills 索引..."
        ls -d "$SKILLS_DIR"/*/ 2>/dev/null | while read dir; do
            NAME=$(basename "$dir")
            echo "  - $NAME"
        done > "$SKILLS_DIR/.skills_index"
        
        echo "✅ 已更新技能索引到 .skills_index"
        ;;
        
    *)
        echo "用法: $0 [status|check|audit|update]"
        echo ""
        echo "命令:"
        echo "  status  - 显示所有技能状态"
        echo "  check   - 检查技能完整性"
        echo "  audit   - 安全审计"
        echo "  update  - 更新技能索引"
        ;;
esac

echo ""
echo "=================================="
