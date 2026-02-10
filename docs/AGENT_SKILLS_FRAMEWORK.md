# 🤖 OpenClaw Agent Skills Framework

## 概述

**OpenClaw Agent Skills** 是模块化、可扩展的能力包，用于扩展 OpenClaw AI 助手的功能。每个技能都是一个自包含的"知识包"，为特定领域或任务提供专业化知识、工作流和工具集成。

**核心思想**：技能将通用 AI 转变为专业化代理，具备模型无法完全拥有的程序性知识。

---

## 📁 技能目录结构

```
/home/admin/.npm-global/lib/node_modules/openclaw/skills/
├── github/                    # GitHub CLI 集成
├── coding-agent/              # 编码代理控制
├── skill-creator/             # 技能创建工具
├── security-system/           # 安全扫描
├── weather/                   # 天气查询
├── github/                    # GitHub 操作
├── gog/                       # Google Workspace
├── obsidian/                  # Obsidian 笔记
├── himalaya/                  # 邮件管理
├── healthcheck/               # 安全审计
├── tmux/                      # Tmux 会话管理
├── sonoscli/                  # Sonos 音箱控制
├── openhue/                  # Philips Hue 灯控制
├── eightctl/                 # Eight Sleep 控制
├── ordercli/                 # 外卖订单
├── video-frames/             # 视频处理
├── nano-pdf/                 # PDF 编辑
├── oracle/                   # AI 提示工程
├── clawhub/                  # ClawHub 技能市场
├── blogwatcher/             # RSS 监控
└── ... (共 54 个技能)

总计：54 个可用技能
```

---

## 🏗️ 技能架构

### 标准技能结构

```
skill-name/
├── SKILL.md (必需)
│   ├── YAML 前言元数据 (必需)
│   │   ├── name: 技能名称
│   │   └── description: 描述
│   └── Markdown 指令 (必需)
├── scripts/ (可选)
│   └── 可执行脚本 (Python/Bash 等)
├── references/ (可选)
│   └── 参考文档 (按需加载到上下文)
└── assets/ (可选)
    └── 资源文件 (模板、图标等)
```

### SKILL.md 详解

每个技能的核心文件，包含：

#### 1. YAML 前言 (必需)

```yaml
---
name: github
description: "Interact with GitHub using the `gh` CLI..."
metadata:
  {
    "openclaw":
      {
        "emoji": "🐙",
        "requires": { "bins": ["gh"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "gh",
              "bins": ["gh"],
              "label": "Install GitHub CLI (brew)",
            },
          ],
      },
  }
```

#### 2. Markdown 主体

使用 Markdown 编写，包含：

- **使用示例**：代码片段和命令
- **工作流**：多步骤流程
- **最佳实践**：注意事项和规则
- **参考链接**：指向 references/ 的链接

---

## 🎯 渐进式披露设计

技能使用三级加载系统管理上下文：

```
Level 1: 元数据 (name + description)
         ↓ 技能触发时加载
Level 2: SKILL.md 主体 (<5k words)
         ↓ 按需加载
Level 3:  bundled resources (scripts, references, assets)
         ↓ 可直接执行，无需读入上下文
```

### 设计模式

#### 模式 1：高层指南 + 参考文件

```markdown
# PDF Processing

## Quick start

Extract text with pdfplumber:
[code example]

## Advanced features

- **Form filling**: See [FORMS.md](FORMS.md) for complete guide
- **API reference**: See [REFERENCE.md](REFERENCE.md) for all methods
- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for common patterns
```

#### 模式 2：按领域组织

```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── finance.md (收入、账单指标)
    ├── sales.md (机会、管道)
    ├── product.md (API 用法、功能)
    └── marketing.md (活动、归因)
```

#### 模式 3：条件细节

```markdown
# DOCX Processing

## Creating documents

Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

## Editing documents

For simple edits, modify the XML directly.

**For tracked changes**: See [REDLINING.md](REDLINING.md)
**For OOXML details**: See [OOXML.md](OOXML.md)
```

---

## 🔧 技能创建流程

### Step 1: 理解技能需求

通过具体示例理解技能用途：

**示例问题**：
- "这个技能应该支持什么功能？"
- "能给出一些使用示例吗？"
- "用户会如何描述他们的需求？"

**输出**：清晰的功能列表

### Step 2: 规划可复用内容

分析每个示例，识别：

- **scripts/** - 重复使用的脚本
- **references/** - 参考文档
- **assets/** - 模板和资源

### Step 3: 初始化技能

```bash
scripts/init_skill.py <skill-name> --path skills/public [--resources scripts,references,assets] [--examples]
```

### Step 4: 编辑技能

**编写指南**：
- 使用祈使句/不定式形式
- name 和 description 要清晰完整
- 包含所有"何时使用"信息（不在 body 中重复）

**示例 SKILL.md**：

```yaml
---
name: pdf-editor
description: "PDF editing and manipulation. Use when: (1) Rotating pages, (2) Extracting text, (3) Merging files, (4) Editing content"
---
```

### Step 5: 打包技能

```bash
scripts/package_skill.py <path/to/skill-folder>
```

自动验证并创建 `.skill` 文件（zip 格式）

### Step 6: 迭代

使用 → 发现问题 → 更新 → 测试

---

## 📊 技能分类

### 按功能分类

| 类别 | 技能示例 | 描述 |
|------|----------|------|
| **代码开发** | coding-agent, github, skill-creator | 代码开发、版本控制 |
| **系统工具** | tmux, healthcheck, mcporter | 系统管理、监控 |
| **第三方集成** | gog, obsidian, himalaya | 外部服务集成 |
| **智能家居** | sonoscli, openhue, eightctl | 设备控制 |
| **生产力** | weather, ordercli, blogwatcher | 日常工具 |
| **媒体处理** | video-frames, nano-pdf, gifgrep | 媒体编辑 |
| **AI 能力** | oracle, gemini, coding-agent | AI 增强 |

### 按复杂度分类

| 复杂度 | 示例 | 特点 |
|--------|------|------|
| **简单** | weather, github | 单一功能，直接调用 CLI |
| **中等** | coding-agent, obsidian | 需要配置，多步骤流程 |
| **复杂** | skill-creator, healthcheck | 多个子模块，资源管理 |

---

## 🛠️ 核心技能详解

### coding-agent - 编码代理控制

**功能**：控制 Codex CLI、Claude Code、OpenCode、Pi Coding Agent

**关键特性**：
- 必需使用 `pty:true`（伪终端）
- 支持后台模式
- 支持工作目录限制
- 批量 PR 审查并行化

**使用示例**：

```bash
# 单次任务 (必需 PTY!)
bash pty:true command:"codex exec 'Build a REST API'"

# 后台模式
bash pty:true workdir:~/project background:true command:"codex exec 'Build a todo app'"

# 批量审查
bash pty:true workdir:~/project background:true command:"codex review PR #86"
```

### github - GitHub CLI 集成

**功能**：Issues、PRs、CI Runs、API 查询

**使用示例**：

```bash
# PR 检查
gh pr checks 55 --repo owner/repo

# 查看工作流
gh run list --repo owner/repo --limit 10

# API 查询
gh api repos/owner/repo/pulls/55 --jq '.title, .state'
```

### skill-creator - 技能创建工具

**功能**：创建和打包新技能

**核心原则**：
- 简洁为王（保护上下文窗口）
- 设置适当的自由度
- 模块化设计

### security-system - 安全扫描

**功能**：漏洞检测和系统保护

**监控的 CWE**：
- CWE-78: OS 命令注入
- CWE-89: SQL 注入
- CWE-79: XSS
- CWE-94: 代码注入
- CWE-200: 敏感数据暴露
- CWE-506: 恶意代码
- CWE-915: 原型污染

---

## 📈 技能使用流程

### 1. 技能触发

当用户请求匹配技能描述时，技能被触发：

```yaml
# 示例：github skill 的触发条件
description: "Interact with GitHub using the `gh` CLI. 
Use for: issues, PRs, CI runs, and advanced API queries."
```

### 2. 加载元数据

```yaml
---
name: github
description: "GitHub operations..."
metadata:
  {
    "openclaw": {
      "emoji": "🐙",
      "requires": { "bins": ["gh"] },
      "install": [...]
    }
  }
```

### 3. 加载技能内容

- **必需**：技能名称和描述（始终在上下文中）
- **触发后**：SKILL.md 主体（<5k words）
- **按需**：bundled resources

### 4. 执行任务

使用技能提供的工具和知识执行用户请求

---

## 🔄 技能与 OpenClaw 集成

### 技能发现机制

1. **自动发现**：OpenClaw 自动扫描 skills/ 目录
2. **元数据分析**：读取每个技能的 name 和 description
3. **匹配触发**：根据用户请求匹配最相关的技能

### 技能安装

**方式 1：内置技能**
- 预装在 `/home/admin/.npm-global/lib/node_modules/openclaw/skills/`
- 共 54 个内置技能

**方式 2：ClawHub 安装**
```bash
clawhub install <skill-name>
```

**方式 3：手动安装**
```bash
# 克隆技能仓库
git clone <skill-repo> skills/<skill-name>

# 或使用 .skill 文件
clawhub install <skill-name>.skill
```

---

## 🎨 最佳实践

### 1. 技能设计原则

- **简洁优先**：只添加上下文窗口确实需要的内容
- **适当自由度**：根据任务脆弱性设置约束
- **模块化**：分离 concerns（scripts, references, assets）

### 2. 命名规范

- 使用小写字母、数字和连字符
- 长度 < 64 字符
- 优先使用简短、动词导向的短语
- 按工具命名（可选）：`gh-address-comments`

### 3. 文档组织

- SKILL.md < 500 行
- 大文件拆分到 references/
- 避免深层嵌套（references 只一层）
- 长文件添加目录

### 4. 错误处理

- 包含错误恢复指南
- 提供常见问题解决方案
- 链接到详细文档

---

## 🚀 常用命令速查

### 技能管理

```bash
# 列出所有技能
ls /home/admin/.npm-global/lib/node_modules/openclaw/skills/

# 查看技能详情
cat /home/admin/.npm-global/lib/node_modules/openclaw/skills/<skill>/SKILL.md

# 创建新技能
scripts/init_skill.py my-skill --path skills/public

# 打包技能
scripts/package_skill.py <path/to/skill-folder>
```

### 使用技能

```bash
# 在对话中自然触发
# 例如："Help me with GitHub issues" → 触发 github skill

# 手动指定（如果需要）
bash pty:true command:"codex exec 'Coding task'"
```

---

## 📚 相关文档

- **技能创建指南**：`skill-creator/SKILL.md`
- **安全系统**：`security-system/SKILL.md`
- **编码代理**：`coding-agent/SKILL.md`
- **GitHub 集成**：`github/SKILL.md`

---

## 🎯 总结

OpenClaw Agent Skills Framework 提供了：

✅ **模块化设计**：54 个独立技能，可按需使用  
✅ **渐进式披露**：智能加载，减少上下文开销  
✅ **可扩展性**：轻松创建和安装新技能  
✅ **标准化结构**：统一的技能格式和打包流程  
✅ **资源管理**：scripts、references、assets 分离  
✅ **版本友好**：技能独立升级，互不影响

**核心价值**：将通用 AI 转变为领域专家，通过可复用的知识和工具提供专业化服务。

---

**最后更新**: 2026-02-08  
**版本**: 1.0
