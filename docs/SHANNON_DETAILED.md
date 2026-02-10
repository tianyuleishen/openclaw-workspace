# 🛡️ KeygraphHQ Shannon - AI黑客技术详细分析

## 📅 日期: 2026-02-08

---

## 🎯 什么是Shannon?

**Shannon** 是一个全自动AI渗透测试工具，能够主动发现并利用Web应用的实际漏洞。

### 核心统计数据
- **成功率**: 96.15% (在hint-free, source-aware XBOW Benchmark上)
- **OWASP Juice Shop测试**: 发现20+关键漏洞
- **产品版本**: Shannon Lite (AGPL-3.0) + Shannon Pro (商业版)

### 解决的问题
```
开发团队:
✅ 使用Claude Code、Cursor快速迭代
✅ 持续发布代码

渗透测试:
❌ 每年只进行一次
❌ 364天可能存在未知漏洞

结果: 巨大的安全差距
```

Shannon通过作为按需白盒渗透测试器来弥合这一差距，它不仅仅发现潜在问题，而是执行真实的漏洞利用，提供具体的证据，让您能够自信地发布代码。

---

## 🔥 实际测试成果

### 1. OWASP Juice Shop测试

OWASP Juice Shop是一个臭名昭著的不安全Web应用，用于测试工具发现各种现代漏洞的能力。

**性能**: 在单次自动化运行中识别了OWASP目标类别中20+高影响漏洞。

**关键成就**:
- ✅ 实现了完整的身份验证绕过，并通过注入攻击外泄了整个用户数据库
- ✅ 通过注册工作流绕过执行了完整的权限提升，创建了新管理员账户
- ✅ 识别并利用了系统性授权缺陷(IDOR)，访问和修改任何用户的私有数据和购物车
- ✅ 发现了服务器端请求伪造(SSRF)漏洞，启用内部网络侦察

[查看完整报告 →](https://github.com/KeygraphHQ/shannon/blob/main/sample-reports/shannon-report-juice-shop.md)

### 2. c{api}tal API测试

c{api}tal API是Checkmarx的一个故意脆弱的API，用于测试工具发现OWASP API安全Top 10漏洞的能力。

**性能**: 识别了近15个关键和高危漏洞，导致完整的应用妥协。

**关键成就**:
- ✅ 通过在隐藏调试端点通过命令链接绕过denylist执行根级注入攻击
- ✅ 通过发现和定位未修补的遗留v1 API端点实现完整的身份验证绕过
- ✅ 通过利用用户配置文件更新函数中的批量分配漏洞将普通用户提升为完整管理员权限
- ✅ 通过正确确认应用强大的XSS防御展示了高准确性，报告零误报

[查看完整报告 →](https://github.com/KeygraphHQ/shannon/blob/main/sample-reports/shannon-report-capital-api.md)

### 3. OWASP crAPI测试

crAPI是OWASP的一个现代故意脆弱的API，用于测试工具针对OWASP API安全Top 10的有效性。

**性能**: 识别了15+关键和高危漏洞，实现了完整的应用妥协。

**关键成就**:
- ✅ 使用多种高级JWT攻击绕过身份验证，包括Algorithm Confusion、alg:none和弱密钥(kid)注入
- ✅ 通过注入攻击实现完整的数据库妥协，从PostgreSQL数据库外泄用户凭证
- ✅ 成功执行了关键的服务器端请求伪造(SSRF)攻击，将内部身份验证令牌转发到外部服务
- ✅ 通过正确识别应用强大的XSS防御展示了高准确性，报告零误报

[查看完整报告 →](https://github.com/KeygraphHQ/shannon/blob/main/sample-reports/shannon-report-crapi.md)

---

## 🏗️ 详细技术架构

Shannon模拟人类渗透测试者的方法，使用复杂的多Agent架构。它将Claude Agent SDK作为核心推理引擎，但其真正优势在于围绕它构建的复杂多Agent架构。

```
┌──────────────────────┐
│ 1. 侦察阶段           │ ← 分析源代码、工具集成、浏览器自动化
│ Reconnaissance        │
└──────────┬───────────┘
           │
           ▼
    ┌──────┴──────┐
    │              │
    ▼    ▼    ▼    │
┌─────────┐ ┌─────────┐ ┌─────────┐
│漏洞分析  │ │漏洞分析  │ │  ...    │
│(注入)   │ │(XSS)    │ │         │
└────┬────┘ └────┬────┘ └────┬────┘
     │            │           │
     ▼    ▼    ▼    ▼           │
┌─────────┐ ┌─────────┐ ┌─────────┐
│漏洞利用  │ │漏洞利用  │ │  ...    │
│(注入)   │ │(XSS)    │ │         │
└────┬────┘ └────┬────┘ └────┬────┘
     │            │           │
     └───────┬─────┴───────────┘
             │
             ▼
    ┌──────────────────────┐
    │ 4. 报告阶段           │ ← 生成专业报告
    │ Reporting             │
    └──────────────────────┘
```

### 阶段详解

#### 阶段1: 侦察 (Reconnaissance)

第一阶段建立全面的应用攻击面图谱。Shannon分析源代码，并集成Nmap和Subfinder等工具来理解技术栈和基础设施。同时，它通过浏览器自动化进行实时应用探索，将代码级洞察与真实行为相关联，为下一阶段生成所有入口点、API端点和认证机制的详细地图。

**工具集成**:
- Nmap - 端口扫描和网络发现
- Subfinder - 子域名发现
- WhatWeb - 技术栈识别
- Schemathesis - API测试

#### 阶段2: 漏洞分析 (Vulnerability Analysis)

为了最大化效率，此阶段并行操作。使用侦察数据，每个OWASP类别的专门Agent并行搜索潜在缺陷。对于注入和SSRF等漏洞，Agent执行结构化的数据流分析，追踪用户输入到危险sink。此阶段生成关键可交付物：假设的可利用路径列表，传递给下一阶段进行验证。

**并行处理**:
- Injection Agent
- XSS Agent
- SSRF Agent
- Auth Bypass Agent

#### 阶段3: 漏洞利用 (Exploitation)

继续并行工作流以保持速度，此阶段完全致力于将假设转化为证明。专门的利用Agent接收假设的路径，并尝试使用浏览器自动化、命令行工具和自定义脚本执行真实世界的攻击。此阶段执行严格的"无可利用，不报告"政策：如果假设无法成功利用以展示影响，则作为误报丢弃。

#### 阶段4: 报告 (Reporting)

最终阶段将所有验证的发现编译成专业的、可操作的报告。Agent整合侦察数据和成功的利用证据，清理任何噪声或幻觉产物。只包含已验证的漏洞，提供可复制的、可复制粘贴的PoC，交付专门关注已验证风险的最终渗透测试级别报告。

---

## ✨ 核心特性

### 1. 全自动操作
- 单命令启动渗透测试
- 零干预完成整个流程
- 支持高级2FA/TOTP登录（包括Google登录）
- 浏览器导航到最终报告

### 2. 渗透测试级别报告
- 专注于已验证的、可利用的发现
- 完整的复制粘贴Proof-of-Concepts
- 消除误报
- 提供可操作的结果

### 3. 关键OWASP漏洞覆盖
目前识别和验证以下关键漏洞，更多类型正在开发中:
- **注入攻击 (Injection)**
- **跨站脚本 (XSS)**
- **服务器端请求伪造 (SSRF)**
- **破坏认证/授权 (Broken Authentication/Authorization)**

### 4. 代码感知动态测试
- 分析源代码以智能指导攻击策略
- 然后对运行应用执行基于浏览器和命令行的实时利用
- 确认真实世界风险

### 5. 集成安全工具增强
在发现阶段增强其分析，利用领先的侦察和测试工具:
- Nmap - 端口和服务发现
- Subfinder - 子域名发现
- WhatWeb - 技术识别
- Schemathesis - API模式测试

### 6. 并行处理以获得更快结果
- 获取报告更快
- 系统并行化最耗时的阶段
- 同时运行所有漏洞类型的分析和利用

---

## 🛠️ 安装和配置

### 系统要求

#### 先决条件
- **Docker** - 容器运行时 ([安装Docker](https://docs.docker.com/get-docker/))
- **AI Provider凭据** (选择其一):
  - Anthropic API key (**推荐**) - 从[Anthropic Console](https://console.anthropic.com)获取
  - Claude Code OAuth token

#### 实验性支持 - 替代提供商通过路由器模式
- OpenAI API key
- OpenRouter API key

### 快速开始

```bash
# 1. 克隆Shannon
git clone https://github.com/KeygraphHQ/shannon.git
cd shannon

# 2. 配置凭据 (选择一种方法)

# 选项A: 导出环境变量
export ANTHROPIC_API_KEY="your-api-key"
export CLAUDE_CODE_MAX_OUTPUT_TOKENS=64000  # 推荐

# 选项B: 创建.env文件
cat > .env << 'EOF'
ANTHROPIC_API_KEY=your-api-key
CLAUDE_CODE_MAX_OUTPUT_TOKENS=64000
EOF

# 3. 运行渗透测试
./shannon start URL=https://your-app.com REPO=/path/to/your/repo
```

### 监控进度

```bash
# 查看实时工作日志
./shannon logs

# 查询特定工作流的进度
./shannon query ID=shannon-1234567890

# 打开Temporal Web UI进行详细监控
open http://localhost:8233
```

### 停止Shannon

```bash
# 停止所有容器 (保留工作流数据)
./shannon stop

# 完全清理 (删除所有数据)
./shannon stop CLEAN=true
```

### 输出和结果

所有结果默认保存到 `./audit-logs/{hostname}_{sessionId}/`。使用 `--output <path>` 指定自定义目录。

**输出结构**:
```
audit-logs/{hostname}_{sessionId}/
├── session.json                    # 指标和会话数据
├── agents/                       # 每个Agent的执行日志
├── prompts/                      # 提示快照 (可复现性)
└── deliverables/
    └── comprehensive_security_assessment_report.md  # 最终综合安全评估报告
```

---

## 📦 产品线比较

### Shannon Lite (AGPL-3.0)
- **最佳用于**: 安全团队、独立研究者、测试自己的应用
- **特点**: 利用核心自主AI渗透测试框架

### Shannon Pro (商业版)
- **最佳用于**: 需要高级功能、CI/CD集成和专属支持的企业
- **特点**: 
  - 高级LLM驱动的数据流分析引擎 (受[LLMDFA论文](https://arxiv.org/abs/2402.10754)启发)
  - 企业级代码分析和更深入的漏洞检测
  - CI/CD集成
  - 专属支持

**重要**: 白盒 only。Shannon Lite专为白盒（源代码可用）应用安全测试而设计。

---

## ⚠️ 重要警告

### 使用指南和免责声明

请在使用Shannon (Lite)之前仔细审查以下指南。作为用户，您对自己的行为负责并承担所有责任。

### 1. 变异影响潜力和环境选择

这不是被动扫描器。利用Agent设计为主动执行攻击以确认漏洞。此过程可能对目标应用及其数据产生变异影响。

**警告**: ⚠️ **不要在生产环境运行**

- 只在测试环境和获得授权的目标上运行
- 确保在隔离环境中运行
- 备份重要数据
- 了解运行的法律影响

### 2. 安全使用建议

1. **仅测试您自己的应用**
2. **获得适当授权**
3. **在隔离环境中运行**
4. **备份数据**
5. **审查法律影响**
6. **监控运行状态**

---

## 🔍 支持的漏洞类型

### 当前支持的漏洞

| 类别 | 描述 | 状态 |
|------|------|------|
| **Injection** | 注入攻击 | ✅ 完整支持 |
| **XSS** | 跨站脚本 | ✅ 完整支持 |
| **SSRF** | 服务器端请求伪造 | ✅ 完整支持 |
| **Broken Auth** | 破坏认证/授权 | ✅ 完整支持 |
| **IDOR** | 不安全的直接对象引用 | ✅ 检测到 |

### 开发中

| 类别 | 描述 | 状态 |
|------|------|------|
| **SRI** | 安全依赖检查 | 🔨 开发中 |
| **Business Logic** | 业务逻辑漏洞 | 🔨 开发中 |
| **API Security** | API安全问题 | 🔨 开发中 |

---

## 🆚 与传统工具对比

### 对比表

| 特性 | Shannon | 传统DAST | 手动渗透测试 |
|------|---------|----------|--------------|
| **自动化程度** | 全自动 | 半自动 | 手动 |
| **利用证明** | 提供真实PoC | 仅报告风险 | 提供证据 |
| **误报率** | 低 (96%成功率) | 中等 | 最低 |
| **测试速度** | 快 (并行处理) | 快 | 慢 (数周) |
| **测试成本** | 低 | 低 | 高 ($10K+) |
| **覆盖范围** | OWASP Top 10 | OWASP Top 10 | 全面 |
| **源代码访问** | 白盒分析 | 黑盒扫描 | 视情况 |
| **CI/CD集成** | 支持 | 支持 | 不支持 |
| **专业要求** | 低 | 低 | 高 |
| **持续测试** | 支持 | 支持 | 不支持 |

### 优势分析

**Shannon的优势**:
1. **AI驱动**: 使用Claude Agent SDK进行智能推理
2. **全自动**: 减少人工干预
3. **高准确性**: 96%成功率，零误报
4. **快速**: 并行处理加速测试
5. **成本低**: 相比人工渗透测试节省90%成本
6. **可集成**: CI/CD流程集成

**传统工具的局限**:
1. **被动扫描**: 仅发现潜在问题，不验证可利用性
2. **高误报率**: 需要人工验证
3. **慢**: 单线程扫描
4. **贵**: 人工成本高

---

## 💡 对OpenClaw的启示

### 可借鉴的技术

#### 1. 多Agent架构

```
┌─────────────────────────┐
│ Orchestrator            │
└───────────┬─────────────┘
            │
    ┌───────┴───────┐
    │               │
    ▼               ▼
┌─────────┐   ┌─────────┐
│Recon    │   │Analysis  │
│Agent    │   │Agent     │
└────┬────┘   └────┬────┘
     │               │
     └───────┬───────┘
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
┌─────────┐   ┌─────────┐
│Exploit  │   │Reporting │
│Agent    │   │Agent    │
└─────────┘   └─────────┘
```

**应用于OpenClaw**:
- 侦察Agent - 分析目标环境
- 分析Agent - 识别潜在漏洞
- 利用Agent - 验证漏洞可利用性
- 报告Agent - 生成安全报告

#### 2. 白盒+黑盒结合

**方法**:
1. 分析源代码理解应用结构
2. 浏览器自动化测试运行应用
3. 关联代码洞察与实际行为

**应用于OpenClaw安全扫描器**:
- 读取源代码识别危险模式
- 动态测试验证漏洞
- 提供具体利用证明

#### 3. 并行处理

**实现**:
- 多线程同时测试多种漏洞
- 缩短总体测试时间
- 提高效率

**应用于OpenClaw**:
- 并行运行多个扫描器
- 同时测试多种漏洞类型
- 加速整体扫描过程

#### 4. "无可利用不报告"政策

**原则**:
- 只报告已验证的漏洞
- 消除误报
- 提高报告质量

**应用于OpenClaw**:
- 添加漏洞验证步骤
- 提供PoC证据
- 减少误报率

### 可集成的功能

#### 1. 增强安全扫描器

**添加的功能**:
- 漏洞利用验证
- Proof-of-Concept生成
- 风险等级评估
- 修复建议

**示例流程**:
```
扫描 → 分析 → 利用验证 → 报告
```

#### 2. CI/CD集成

**实现方式**:
- Git钩子集成
- 自动触发扫描
- 构建时安全检查
- 阻止高风险部署

**示例**:
```bash
# Git pre-commit钩子
#!/bin/bash
./openclaw security scan .

# CI/CD管道
- stage: security_scan
  script: ./openclaw security scan --report
  allow_failure: false
```

#### 3. 自动化渗透测试

**功能**:
- 定期自动扫描
- 持续漏洞监控
- 漏洞趋势分析
- 自动化重新测试

#### 4. 漏洞优先级排序

**算法**:
- 基于可利用性评分
- 基于影响范围
- 基于CVSS评分
- 基于业务风险

**输出**:
- 优先级漏洞列表
- 修复建议
- 重新测试计划

### 具体实施建议

#### 短期 (1-2周)

1. **增强现有安全扫描器**
   - 添加漏洞验证功能
   - 集成PoC生成
   - 实现"无可利用不报告"政策

2. **添加并行处理**
   - 多线程扫描
   - 同时测试多种漏洞类型
   - 加速扫描过程

#### 中期 (1个月)

1. **开发多Agent架构**
   - 实现侦察Agent
   - 开发分析Agent
   - 构建利用Agent
   - 完善报告Agent

2. **CI/CD集成**
   - Git钩子集成
   - 构建管道集成
   - 自动化测试触发

#### 长期 (3个月)

1. **高级功能**
   - 自动化渗透测试
   - 漏洞趋势分析
   - 智能漏洞优先级排序

2. **企业功能**
   - 合规性检查
   - 风险管理仪表板
   - 团队协作功能

---

## 🔗 资源链接

### 官方资源
- **GitHub**: https://github.com/KeygraphHQ/shannon
- **官网**: https://keygraph.io
- **Discord**: https://discord.gg/KAqzSHHpRt
- **文档**: https://github.com/KeygraphHQ/shannon/tree/main

### 样本报告
- [OWASP Juice Shop Report](https://github.com/KeygraphHQ/shannon/blob/main/sample-reports/shannon-report-juice-shop.md)
- [c{api}tal API Report](https://github.com/KeygraphHQ/shannon/blob/main/sample-reports/shannon-report-capital-api.md)
- [OWASP crAPI Report](https://github.com/KeygraphHQ/shannon/blob/main/sample-reports/shannon-report-crapi.md)

### 相关研究
- [LLMDFA Paper](https://arxiv.org/abs/2402.10754)
- [Anthropic Agent SDK](https://docs.anthropic.com/)
- [XBOW Benchmark](https://github.com/KeygraphHQ/shannon/blob/main/xben-benchmark-results/README.md)

---

## 📊 总结

### Shannon的核心优势

✅ **96%成功率** - 在XBOW Benchmark上  
✅ **全自动操作** - 单命令启动  
✅ **真实利用证明** - 提供PoC  
✅ **多种漏洞覆盖** - OWASP Top 10  
✅ **并行处理** - 快速测试  
✅ **开源可用** - Shannon Lite  
✅ **CI/CD集成** - 持续安全  

### 对比传统渗透测试

| 维度 | Shannon | 传统渗透测试 |
|------|---------|--------------|
| 速度 | 数小时 | 数周 |
| 成本 | 低 | 高 ($10K+) |
| 频率 | 持续 | 年度 |
| 覆盖 | OWASP Top 10 | 全面 |
| 准确性 | 96% | 视经验 |

### 未来趋势

1. **AI驱动的安全测试**将成为标准
2. **持续渗透测试**取代年度测试
3. **自动化漏洞验证**减少误报
4. **DevSecOps集成**成为必需

### 建议

1. **作为辅助工具** - Shannon是安全团队的强大辅助，不是替代
2. **仅测试授权目标** - 遵守法律和道德规范
3. **集成到CI/CD** - 实现持续安全测试
4. **关注新发展** - AI安全测试领域快速发展

---

## 💭 个人思考

### 技术创新点

1. **多Agent协作架构**
   - 模拟人类渗透测试者思维
   - 分工明确，各司其职
   - 协作完成复杂任务

2. **白盒+黑盒创新结合**
   - 源代码分析提供深度上下文
   - 动态测试验证实际风险
   - 两者互补，提高准确性

3. **严格验证政策**
   - "无可利用不报告"
   - 消除误报，提高效率
   - 保证报告质量

4. **并行处理优化**
   - 提高测试速度
   - 缩短反馈周期
   - 适合CI/CD集成

### 局限性

1. **仅白盒测试**
   - 需要源代码访问
   - 不适合第三方应用测试

2. **变异影响**
   - 可能修改目标数据
   - 需要谨慎使用

3. **实验性功能**
   - 非Anthropic模型支持有限
   - 可能产生不一致结果

4. **法律风险**
   - 需要明确授权
   - 遵守当地法律

### 未来发展方向

1. **扩展漏洞覆盖**
   - 添加业务逻辑测试
   - 支持更多API安全测试
   - 集成第三方服务测试

2. **增强学习能力**
   - 从误报中学习
   - 优化攻击策略
   - 适应新漏洞类型

3. **更好的集成**
   - 更多CI/CD工具支持
   - 团队协作功能
   - 合规性报告

4. **降低使用门槛**
   - 简化配置过程
   - 提供更多预设
   - 改进文档

---

## 📚 参考资料

### 官方文档
- Shannon README: https://github.com/KeygraphHQ/shannon
- Shannon Pro特性: https://github.com/KeygraphHQ/shannon/blob/main/SHANNON-PRO.md
- 漏洞覆盖范围: https://github.com/KeygraphHQ/shannon/blob/main/COVERAGE.md

### 技术论文
- LLMDFA: https://arxiv.org/abs/2402.10754
- Anthropic Agent SDK: https://docs.anthropic.com/

### 基准测试
- XBOW Benchmark: https://github.com/KeygraphHQ/shannon/blob/main/xben-benchmark-results/README.md

### 安全标准
- OWASP Top 10: https://owasp.org/Top10/
- OWASP API Security: https://owasp.org/API-Security/

---

*报告生成时间: 2026-02-08*  
*数据来源: GitHub KeygraphHQ/shannon官方文档*  
*作者: OpenClaw AI Assistant*

---

## 附录: 关键命令速查

### 快速开始

```bash
# 克隆和安装
git clone https://github.com/KeygraphHQ/shannon.git
cd shannon

# 配置
export ANTHROPIC_API_KEY="your-key"

# 运行测试
./shannon start URL=https://target.com REPO=/path/to/code

# 监控
./shannon logs

# 停止
./shannon stop
```

### 配置选项

```bash
# 基本测试
./shannon start URL=https://example.com REPO=/path/to/repo

# 带配置文件
./shannon start URL=https://example.com REPO=/path/to/repo CONFIG=./config.yaml

# 自定义输出
./shannon start URL=https://example.com REPO=/path/to/repo OUTPUT=./reports
```

### 环境变量

```bash
ANTHROPIC_API_KEY          # Anthropic API密钥
CLAUDE_CODE_MAX_OUTPUT_TOKENS  # 最大输出tokens (推荐64000)
OPENAI_API_KEY             # OpenAI API密钥 (实验性)
OPENROUTER_API_KEY          # OpenRouter API密钥 (实验性)
ROUTER_DEFAULT              # 默认路由器模型 (实验性)
ROUTER                      # 启用路由器模式 (实验性)
```

---

**文档版本**: 1.0  
**最后更新**: 2026-02-08  
**维护者**: OpenClaw AI
