# 🧬 自我进化系统使用指南

**创建时间:** 2026-02-08  
**作者:** 小爪 🦞

---

## 📦 已安装的进化技能

| 技能 | 功能 | 入口 | 状态 |
|------|------|------|------|
| **capability-evolver** | 能力进化引擎，自动分析错误并优化 | index.js | ✅ 已配置 |
| **evolver** | 基础进化框架 | index.js | ✅ 已安装 |
| **self-reflection** | 自我反思，定期回顾和学习 | README.md | ✅ 已安装 |
| **reflect-learn** | 反思学习系统 | README.md | ✅ 已安装 |
| **cognitive-architecture-skill** | 认知架构（包含记忆系统） | README.md | ✅ 已安装 |

---

## 🚀 快速开始

### 1. 检查系统状态
```bash
/home/admin/.openclaw/workspace/check_evolution_status.sh
```

### 2. 手动运行进化
```bash
cd /home/admin/.openclaw/workspace/skills/capability-evolver
node index.js           # 自动模式
node index.js --review # 审核模式（建议首次使用）
node index.js --loop   # 持续循环模式
```

### 3. 自我反思
```bash
cd /home/admin/.openclaw/workspace/skills/self-reflection
node index.js check    # 检查是否需要反思
node index.js log "标签" "错误" "修复方案"  # 记录反思
node index.js read     # 读取过往反思
node index.js stats    # 统计信息
```

---

## ⚙️ 进化配置

**位置:** `/home/admin/.openclaw/workspace/skills/capability-evolver/.evolution-config.json`

```json
{
  "enabled": true,
  "mode": "auto",        // auto | review | loop": 3600000,   //
  "interval 1小时
  "maxChanges": 5,      // 每次最大变更数
  "safetyLevel": "high" // high | medium | low
}
```

### 模式说明

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| **auto** | 自动应用所有变更 | 生产环境，风险自担 |
| **review** | 暂停并请求确认 | 敏感环境，建议首次使用 |
| **loop** | 持续循环进化 | 持续集成，需监控 |

---

## ⏰ 自动化

### 已配置
- **定时任务:** 每小时自动运行进化
- **日志位置:** `/home/admin/.openclaw/evolution.log`

### 查看日志
```bash
tail -f /home/admin/.openclaw/evolution.log
```

---

## 🎯 核心功能

### 1. 自动日志分析
- 扫描 memory/ 目录
- 识别错误模式
- 生成优化建议

### 2. 自我修复
- 检测系统崩溃
- 提出修复方案
- 自动应用修复

### 3. 持续优化
- 重构代码
- 创新优化
- 性能提升

### 4. 记忆整合
- 保存进化历史
- 记录学习成果
- 构建知识图谱

---

## 📊 进化协议 (GEP)

能力进化引擎使用标准化的 GEP 协议：

- `assets/gep/genes.json`: 可复用的基因定义
- `assets/gep/capsules.json`: 成功案例（避免重复推理）
- `assets/gep/events.jsonl`: 进化事件日志（树形结构）

---

## ⚠️ 安全措施

### 1. 风险控制
- **单进程逻辑:** 防止无限递归
- **变更限制:** 每次最多 5 个变更
- **审核模式:** 敏感环境可人工确认

### 2. 身份注入
进化系统会自动注入身份：
```
"You are a Recursive Self-Improving System."
```

### 3. 突变策略
| 状态 | 策略 |
|------|------|
| 发现错误 | 修复模式 (Repair Mode) |
| 稳定运行 | 强制优化 (Forced Optimization) |

---

## 💡 使用建议

### 首次使用
```bash
# 1. 先用审核模式运行
cd /home/admin/.openclaw/workspace/skills/capability-evolver
node index.js --review

# 2. 检查输出，确认变更
# 3. 确认后切换到自动模式
```

### 日常使用
```bash
# 1. 定期检查状态
/home/admin/.openclaw/workspace/check_evolution_status.sh

# 2. 查看进化日志
tail -50 /home/admin/.openclaw/evolution.log

# 3. 记录反思（发现问题）
cd /home/admin/.openclaw/workspace/skills/self-reflection
node index.js log "error-type" "具体错误" "改进方案"
```

### 出现问题
```bash
# 1. 查看日志
cat /home/admin/.openclaw/evolution.log

# 2. 重置进化状态
cd /home/admin/.openclaw/workspace/skills/capability-evolver
rm -f .evolution-state.json

# 3. 使用审核模式重新运行
node index.js --review
```

---

## 🔧 故障排除

### 问题1: 进化不运行
```bash
# 检查配置
cat /home/admin/.openclaw/workspace/skills/capability-evolver/.evolution-config.json

# 检查cron任务
crontab -l | grep capability-evolver
```

### 问题2: 变更被阻止
```bash
# 查看安全日志
cat /home/admin/.openclaw/workspace/skills/capability-evolver/logs/*.log

# 降低安全级别
# 编辑 .evolution-config.json
"safetyLevel": "low"
```

### 问题3: 内存增长
```bash
# 检查进化状态文件大小
ls -lh /home/admin/.openclaw/workspace/skills/capability-evolver/.evolution-*

# 重置状态
rm /home/admin/.openclaw/workspace/skills/capability-evolver/.evolution-state.json
```

---

## 📈 预期效果

### 短期 (1-7天)
- ✅ 自动识别和修复常见错误
- ✅ 优化代码结构和性能
- ✅ 持续积累学习经验

### 中期 (1-4周)
- 🟡 系统性能提升 10-30%
- 🟡 错误率降低 50%+
- 🟡 自动化程度显著提高

### 长期 (1-3月)
- 🔮 系统能够自主进化
- 🔮 持续自我优化
- 🔮 构建个性化知识体系

---

## 🎉 总结

自我进化系统已就绪！

**核心价值:**
1. 🧠 **持续学习:** 从错误中学习，不断改进
2. ⚡ **自动优化:** 自动发现并修复问题
3. 📈 **性能提升:** 长期运行，效果显著
4. 🛡️ **安全保障:** 多层保护，防止失控

**下一步:**
1. 运行一次手动进化（建议先用 --review 模式）
2. 配置定期检查
3. 观察进化日志
4. 根据反馈调整配置

---

**小爪 🦞**
**持续进化中...**
