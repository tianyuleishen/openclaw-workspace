#!/usr/bin/env node
/**
 * Self-Evolution Startup Script
 * 自我进化系统启动器
 */

const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🚀 启动自我进化系统...');
console.log('='.repeat(50));

// 检查技能状态
const skills = [
  { name: '自我反思', dir: 'self-reflection' },
  { name: '能力进化', dir: 'capability-evolver' },
  { name: '认知架构', dir: 'cognitive-architecture-skill' },
  { name: 'Reflect Learn', dir: 'reflect-learn' }
];

console.log('\n📦 已安装的自我进化技能:\n');
skills.forEach(skill => {
  const hasIndex = fs.existsSync("/home/admin/.openclaw/workspace/skills/" + skill.dir + "/index.js");
  const hasSkill = fs.existsSync("/home/admin/.openclaw/workspace/skills/" + skill.dir + "/SKILL.md");
  const status = hasIndex && hasSkill ? '✅' : '❌';
  console.log("  " + status + " " + skill.name);
});

// 创建配置
console.log('\n⚙️  创建进化配置...');
const evolverPath = "/home/admin/.openclaw/workspace/skills/capability-evolver";
if (fs.existsSync(evolverPath)) {
  const config = {
    enabled: true,
    mode: 'auto',
    interval: 3600000,
    maxChanges: 5,
    safetyLevel: 'high'
  };
  fs.writeFileSync(evolverPath + "/.evolution-config.json", JSON.stringify(config, null, 2));
  console.log('✅ 进化配置已创建');
}

// 创建状态检查脚本
const statusScript = `#!/bin/bash
echo "🔍 自我进化系统状态:"
echo ""
for skill in self-reflection capability-evolver cognitive-architecture-skill reflect-learn; do
  if [ -f "/home/admin/.openclaw/workspace/skills/$skill/index.js" ]; then
    echo "✅ $skill"
  else
    echo "❌ $skill"
  fi
done
echo ""
echo "📊 运行状态:"
ps aux | grep "capability-evolver" | grep -v grep || echo "  进化引擎: 未运行"
ps aux | grep "self-reflection" | grep -v grep || echo "  反思系统: 未运行"
`;

fs.writeFileSync('/home/admin/.openclaw/workspace/check_evolution_status.sh', statusScript);
fs.chmodSync('/home/admin/.openclaw/workspace/check_evolution_status.sh', '755');

console.log('✅ 状态检查工具已创建');

// 添加crontab
try {
  exec('(crontab -l 2>/dev/null | grep -v "capability-evolver"; echo "0 * * * * cd /home/admin/.openclaw/workspace/skills/capability-evolver && node index.js >> /home/admin/.openclaw/evolution.log 2>&1") | crontab -');
  console.log('✅ 已配置每小时自动进化任务');
} catch (e) {
  console.log('⚠️  crontab配置失败');
}

console.log('\n' + '='.repeat(50));
console.log('🎉 自我进化系统就绪！');
console.log('');
console.log('📚 使用命令:');
console.log('  ./check_evolution_status.sh    # 检查状态');
console.log('  cd skills/capability-evolver && node index.js  # 手动进化');
