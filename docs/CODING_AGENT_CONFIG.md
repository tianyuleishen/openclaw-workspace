# 🔧 Coding-Agent 技能配置指南

## 概述

**coding-agent** 技能用于控制外部 AI 编码助手，实现自动化编程任务。

## 当前状态

| 工具 | 状态 | 路径 |
|------|------|------|
| Codex CLI | ❌ 未安装 | - |
| Claude Code | ✅ 已安装 | `/home/admin/.npm-global/bin/claude` |
| Pi Coding Agent | ❌ 未安装 | - |
| OpenCode | ❌ 未安装 | - |

## 配置选项

### 选项 1: Claude Code（推荐）

Claude Code 是 Anthropic 官方推出的 AI 编程助手，功能强大。

#### 安装 Claude Code

Claude Code 已经预装：`/home/admin/.npm-global/bin/claude`

#### 配置 API 密钥

```bash
# 方法 1: 环境变量（临时）
export ANTHROPIC_API_KEY="sk-ant-api03-xxx"

# 方法 2: 写入配置文件
mkdir -p ~/.config/claude-code
cat > ~/.config/claude-code/config.json << 'JSON'
{
  "apiKey": "sk-ant-api03-xxx",
  "model": "claude-sonnet-4-20250506"
}
JSON

# 方法 3: 使用 .env 文件
echo "ANTHROPIC_API_KEY=sk-ant-api03-xxx" >> ~/.env
source ~/.env
```

#### 验证配置

```bash
# 测试 Claude Code
claude --version

# 尝试运行（需要 API 密钥）
claude "Hello, write a simple Python function"
```

### 选项 2: Codex CLI（OpenAI）

#### 安装 Codex CLI

```bash
# 通过 npm 安装
npm install -g @openai/codex

# 验证安装
codex --version
```

#### 配置 API 密钥

```bash
# 设置 OpenAI API 密钥
export OPENAI_API_KEY="sk-xxx"

# 或写入配置文件
mkdir -p ~/.config/codex
cat > ~/.config/codex/config.toml << 'TOML'
apiKey = "sk-xxx"
defaultModel = "gpt-5.2-codex"
TOML
```

#### 使用 Codex

```bash
# 单次任务
codex exec "Create a Python function to calculate fibonacci"

# 自动批准模式
codex --full-auto exec "Build a REST API for todo list"

# YOLO 模式（无沙箱）
codex --yolo exec "Refactor the entire codebase"
```

### 选项 3: Pi Coding Agent

#### 安装 Pi

```bash
# 通过 npm 安装
npm install -g @mariozechner/pi-coding-agent

# 验证
pi --version
```

#### 配置

```bash
# 使用 OpenAI
export OPENAI_API_KEY="sk-xxx"
pi "Build a web scraper"

# 使用 Anthropic
export ANTHROPIC_API_KEY="sk-ant-api03-xxx"
pi --provider anthropic "Build a CLI tool"

# 使用自定义模型
pi --provider openai --model gpt-4o-mini "Your task"
```

### 选项 4: OpenCode

```bash
# 安装
npm install -g opencode-cli

# 配置 API
export OPENAI_API_KEY="sk-xxx"

# 使用
opencode run "Create a Node.js API"
```

## OpenClaw 集成配置

### 1. 配置环境变量

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
cat >> ~/.bashrc << 'BASH'

# Coding Agent 配置
export ANTHROPIC_API_KEY="sk-ant-api03-xxx"  # Claude Code
export OPENAI_API_KEY="sk-xxx"               # Codex / Pi / OpenCode

BASH

# 立即生效
source ~/.bashrc
```

### 2. 测试集成

```bash
# 测试 Claude Code（已安装）
claude --version

# 如果配置了 API_KEY，可以测试
# claude "Write a simple hello world"
```

### 3. 创建测试脚本

```bash
cat > ~/test_coding_agent.sh << 'TEST'
#!/bin/bash
# 测试 coding-agent 技能

echo "Testing Claude Code..."
if command -v claude &> /dev/null; then
    claude --version
    echo "✅ Claude Code is available"
else
    echo "❌ Claude Code not found"
fi

echo ""
echo "Testing Codex CLI..."
if command -v codex &> /dev/null; then
    codex --version
    echo "✅ Codex CLI is available"
else
    echo "❌ Codex CLI not found"
fi

echo ""
echo "Testing Pi..."
if command -v pi &> /dev/null; then
    pi --version
    echo "✅ Pi Coding Agent is available"
else
    echo "❌ Pi Coding Agent not found"
fi
TEST

chmod +x ~/test_coding_agent.sh
echo "✅ 测试脚本已创建: ~/test_coding_agent.sh"
```

## 使用方法

### 在 OpenClaw 中使用

#### 1. 基本用法（Claude Code）

```bash
# ✅ 必需使用 pty:true
bash pty:true command:"claude 'Write a Python function to calculate factorial'"
```

#### 2. 指定工作目录

```bash
# 在指定目录中执行
bash pty:true workdir:~/myproject command:"claude 'Add error handling to the API'"
```

#### 3. 后台运行

```bash
# 后台执行长任务
bash pty:true workdir:~/project background:true command:"claude 'Build a full-stack todo app'"

# 获取 sessionId 后监控
process action:list

# 查看输出
process action:log sessionId:<SESSION_ID>

# 如果需要输入
process action:submit sessionId:<SESSION_ID> data:"y"

# 终止任务
process action:kill sessionId:<SESSION_ID>
```

#### 4. 使用 Codex

```bash
# Codex 需要 git 仓库
cd ~/project && git init

# 单次执行（自动批准）
bash pty:true workdir:~/project command:"codex exec --full-auto 'Build a REST API'"

# YOLO 模式（无沙箱，最快）
bash pty:true workdir:~/project command:"codex --yolo 'Refactor the auth module'"
```

### 完整示例

#### 示例 1: 创建新项目

```bash
# 1. 创建临时目录
SCRATCH=$(mktemp -d)
cd $SCRATCH
git init

# 2. 使用 Claude Code 创建项目
bash pty:true workdir:$SCRATCH background:true command:"claude 'Create a simple REST API with Express.js. Include: GET /users, POST /users, and basic error handling.'"

# 3. 监控进度
sleep 5
process action:log sessionId:<LATEST>

# 4. 查看结果
ls -la $SCRATCH
```

#### 示例 2: 修复 Issue

```bash
# 1. 创建工作树
git worktree add -b fix/issue-123 /tmp/issue-123 main

# 2. 使用 Codex 修复
bash pty:true workdir:/tmp/issue-123 command:"codex --yolo 'Fix issue #123: Fix memory leak in connection pool. Commit and push.'"

# 3. 创建 PR
cd /tmp/issue-123
git push -u origin fix/issue-123
gh pr create --head fix/issue-123 --title "Fix: Memory leak in connection pool"

# 4. 清理
git worktree remove /tmp/issue-123
```

## 故障排除

### 问题 1: Claude Code 无法运行

**症状**：`command not found` 或无响应

**解决方案**：

```bash
# 1. 检查安装
which claude
/home/admin/.npm-global/bin/claude --version

# 2. 检查 API 密钥
echo $ANTHROPIC_API_KEY

# 3. 如果未设置，配置密钥
export ANTHROPIC_API_KEY="sk-ant-api03-xxx"

# 4. 重新测试
claude "Hello"
```

### 问题 2: Codex 拒绝运行

**症状**：`Not a git repository`

**解决方案**：

```bash
# Codex 需要在 git 仓库中运行
cd ~/your-project
git init  # 如果还没有

# 或创建临时仓库
SCRATCH=$(mktemp -d)
cd $SCRATCH
git init
codex exec "Your task"
```

### 问题 3: PTY 模式问题

**症状**：输出截断、颜色丢失、卡住

**解决方案**：

```bash
# 始终使用 pty:true
bash pty:true command:"claude 'Your task'"

# 不要省略 pty:true
bash command:"claude 'Your task'"  # ❌ 错误
```

### 问题 4: API 密钥错误

**症状**：`Invalid API key` 或 `401 Unauthorized`

**解决方案**：

```bash
# 1. 检查密钥格式
echo $ANTHROPIC_API_KEY | head -c 20

# 2. 重新设置密钥
export ANTHROPIC_API_KEY="sk-ant-api03-正确的密钥"

# 3. 验证密钥有效性
curl -s -H "x-api-key: $ANTHROPIC_API_KEY" \
  https://api.anthropic.com/v1/models | head
```

## 性能优化

### 1. 选择合适的模式

| 模式 | 速度 | 安全 | 适用场景 |
|------|------|------|---------|
| `--full-auto` | 快 | 中 | 构建项目 |
| `--yolo` | 最快 | 低 | 快速重构 |
| default | 中 | 高 | 审查代码 |

### 2. 使用工作目录

```bash
# ✅ 好：指定工作目录，Agent 不会读取无关文件
bash pty:true workdir:~/project command:"claude 'Task'"

# ❌ 差：Agent 可能读取整个主目录
bash pty:true command:"claude 'Task'"
```

### 3. 批量处理

```bash
# 并行运行多个 Agent
bash pty:true workdir:~/project background:true command:"codex exec 'Fix issue #1'"
bash pty:true workdir:~/project background:true command:"codex exec 'Fix issue #2'"
bash pty:true workdir:~/project background:true command:"codex exec 'Fix issue #3'"

# 监控所有
process action:list
```

## 最佳实践

### ✅ 推荐做法

1. **始终使用 `pty:true`** - 避免输出问题
2. **指定 `workdir`** - 防止 Agent 读取无关文件
3. **使用 git 仓库** - Codex 必需
4. **后台模式用于长任务** - 避免超时
5. **监控进度** - 使用 `process action:log`

### ❌ 避免做法

1. **不要省略 `pty:true`**
2. **不要在主目录运行 Codex**
3. **不要让长任务阻塞主会话**
4. **不要忘记设置 API 密钥**
5. **不要在 OpenClaw 主目录运行 Agent** - 它会读取 soul.md

## 快速参考

```bash
# 安装编码助手
npm install -g @openai/codex           # Codex
npm install -g @mariozechner/pi         # Pi
npm install -g opencode-cli            # OpenCode

# Claude Code 已预装
which claude

# 配置 API 密钥
export ANTHROPIC_API_KEY="sk-ant-api03-xxx"  # Claude
export OPENAI_API_KEY="sk-xxx"                # Codex/Pi/OpenCode

# 使用 Claude Code
bash pty:true command:"claude 'Your task'"

# 使用 Codex（需要 git 仓库）
codex init
bash pty:true command:"codex exec --full-auto 'Task'"

# 批量使用
bash pty:true background:true command:"codex exec 'Task 1'"
bash pty:true background:true command:"codex exec 'Task 2'"
```

## 下一步

1. ✅ 查阅本配置指南
2. ⏳ 配置 API 密钥
3. ⏳ 测试编码助手
4. ⏳ 集成到 OpenClaw

## 相关文档

- **coding-agent 技能**：`/home/admin/.npm-global/lib/node_modules/openclaw/skills/coding-agent/SKILL.md`
- **Agent 技能框架**：`/home/admin/.openclaw/workspace/docs/AGENT_SKILLS_FRAMEWORK.md`
- **Claude Code 官网**：https://claude.com/claude-code
- **Codex 文档**：https://platform.openai.com/docs/codex

---

**最后更新**: 2026-02-08
**版本**: 1.0
