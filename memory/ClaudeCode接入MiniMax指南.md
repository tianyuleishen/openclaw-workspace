# Claude Code 接入 MiniMax 模型 - 官方指南

**日期**: 2026-02-10  
**来源**: https://platform.minimaxi.com/docs/mcp  
**主题**: 多种 AI 编程工具接入 MiniMax-M2.1

---

## ⚠️ 重要前置要求

### 清除环境变量

在配置前，必须清除以下 Anthropic 相关环境变量：

```bash
unset ANTHROPIC_AUTH_TOKEN
unset ANTHROPIC_BASE_URL
```

---

## 🛠️ 方案1: Claude Code (推荐)

### 步骤

#### 1. 安装 Claude Code
参考: https://docs.claude.com/en/docs/claude-code/setup

#### 2. 配置 MiniMax API (两种方法)

**方法A: 使用 cc-switch (推荐)**

```bash
# 安装
brew tap farion1231/ccswitch
brew install --cask cc-switch
```

1. 启动 cc-switch
2. 点击 "+" → 选择 MiniMax 供应商
3. 填写 API Key
4. 模型名称改为 `MiniMax-M2.1`
5. 点击 "启用"

**方法B: 手动配置**

编辑 `~/.claude/settings.json`:

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.minimaxi.com/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "MINIMAX_API_KEY",
    "ANTHROPIC_MODEL": "MiniMax-M2.1",
    "ANTHROPIC_SMALL_FAST_MODEL": "MiniMax-M2.1",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "MiniMax-M2.1",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "MiniMax-M2.1",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "MiniMax-M2.1"
  }
}
```

编辑 `~/.claude.json`:
```json
{
  "hasCompletedOnboarding": true
}
```

#### 3. 启动 Claude Code

```bash
claude
```

---

## 🛠️ 方案2: 其他编程工具

| 工具 | 配置难度 | 推荐度 |
|------|---------|--------|
| **Claude Code** | ⭐⭐ | ⭐⭐⭐⭐⭐ 推荐 |
| **Cursor** | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **TRAE** | ⭐⭐ | ⭐⭐⭐⭐⭐ 内置支持 |
| **OpenCode** | ⭐⭐ | ⭐⭐⭐ |
| **Kilo Code** | ⭐⭐ | ⭐⭐⭐ |
| **OpenClaw** | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Cline** | ⭐⭐ | ⭐⭐⭐ |
| **Roo Code** | ⭐⭐ | ⭐⭐⭐ |

---

## 💡 核心配置参数

| 参数 | 值 |
|------|-----|
| **API 端点** | `https://api.minimaxi.com/v1` 或 `https://api.minimaxi.com/anthropic` |
| **模型名称** | `MiniMax-M2.1` 或 `MiniMax-M2.1-lightning` |
| **API Key 格式** | `mapi_xxxxx` |

---

## 🔧 快速配置命令

```bash
# 清除 Anthropic 环境变量
unset ANTHROPIC_AUTH_TOKEN
unset ANTHROPIC_BASE_URL

# 配置 Claude Code
echo '{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.minimaxi.com/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "YOUR_MINIMAX_API_KEY",
    "ANTHROPIC_MODEL": "MiniMax-M2.1"
  },
  "hasCompletedOnboarding": true
}' > ~/.claude/settings.json

# 启动
claude
```

---

## 📊 OpenClaw 已集成情况

| 项目 | 状态 | 详情 |
|------|------|------|
| **当前模型** | ✅ 已配置 | MiniMax-M2.1 |
| **API 端点** | ✅ 已配置 | https://api.minimaxi.com/v1 |
| **配置路径** | ✅ 已集成 | minimax_integration.py |

---

## 🎯 使用建议

1. **首选 Claude Code** - 功能完整，配置简单
2. **国内用户** - 使用 TRAE (内置支持)
3. **VS Code 用户** - 使用 Cursor 或 Cline
4. **命令行用户** - 使用 OpenCode 或 Claude Code

---

## ⚠️ 常见问题

1. **401 错误** - API Key 无效或未激活
2. **429 错误** - 超过速率限制
3. **配置不生效** - 检查环境变量是否清除

---

**文档完整版**: https://platform.minimaxi.com/docs/mcp
