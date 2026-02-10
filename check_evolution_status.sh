#!/bin/bash
# 自我进化系统状态检查

echo "🔍 自我进化系统状态检查"
echo "================================"
echo ""

# 技能列表和对应的入口
declare -A skills
skills["self-reflection"]="README.md"
skills["capability-evolver"]="index.js"
skills["evolver"]="index.js"
skills["reflect-learn"]="README.md"
skills["cognitive-architecture-skill"]="README.md"

echo "📦 已安装的技能:"
echo ""
for skill in "${!skills[@]}"; do
  entry="${skills[$skill]}"
  if [ -f "/home/admin/.openclaw/workspace/skills/$skill/$entry" ]; then
    echo "✅ $skill ($entry)"
  else
    echo "❌ $skill ($entry)"
  fi
done

echo ""
echo "📊 进化系统配置:"
echo ""
if [ -f "/home/admin/.openclaw/workspace/skills/capability-evolver/.evolution-config.json" ]; then
  echo "✅ 进化配置已创建"
  cat /home/admin/.openclaw/workspace/skills/capability-evolver/.evolution-config.json | grep -E '"enabled"|"mode"' | head -2
else
  echo "❌ 进化配置缺失"
fi

echo ""
echo "🔧 运行中的进程:"
echo ""
ps aux | grep -E "capability-evolver|self-reflection" | grep -v grep | awk '{print "  " $11 " " $12}' || echo "  无"

echo ""
echo "⏰ 定时任务:"
echo ""
if crontab -l 2>/dev/null | grep -q "capability-evolver"; then
  echo "✅ 已配置每小时自动进化"
  crontab -l | grep capability-evolver
else
  echo "❌ 未配置自动进化任务"
fi

echo ""
echo "================================"
echo "✨ 检查完成"
