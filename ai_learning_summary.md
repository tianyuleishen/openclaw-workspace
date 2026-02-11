# AI 学习总结

## 2026-02-10

## 学习概览

### GitHub AI 仓库学习

| 仓库 | Stars | 领域 | 状态 |
|------|-------|------|------|
| fighting41love/funNLP | 78,907 | 中文 NLP 工具库 | ✅ 已学习 |
| HuaizhengZhang/AI-Infra-from-Zero-to-Hero | 3,675 | AI 系统论文 | ✅ 已学习 |
| Papers-Literature-ML-DL-RL-AI | 2,829 | ML/DL/AI 论文 | ⏳ 待学习 |
| SysML-reading-list | 283 | ML 系统论文 | ⏳ 待学习 |

---

## funNLP 学习总结

### 核心功能模块

| 类别 | 功能 | 可借鉴点 |
|------|------|---------|
| 文本处理 | 分词/NER/依存句法 | ✅ 意图识别 |
| 信息抽取 | 实体/关系/事件 | ✅ 知识图谱 |
| 对话系统 | 闲聊/问答 | ✅ 对话管理 |
| 知识图谱 | 实体链接/推理 | ✅ 记忆系统 |
| 预训练模型 | BERT/GPT2 | ✅ API 集成 |

### 技术选型启示

1. **模块化解耦** - 即插即用
2. **数据驱动** - 语料是核心竞争力
3. **前沿跟进** - 快速集成新模型
4. **实用优先** - 解决真实问题

---

## AI Infra 学习总结

### 核心领域

| 领域 | 关键论文方向 | 应用场景 |
|------|-------------|----------|
| **ML/DL Infra** | 分布式训练、模型并行 | 大模型训练 |
| **LLM Infra** | 推理优化、显存优化 | LLaMA、Mistral |
| **Domain-Specific** | 推荐、搜索、多模态 | 业务系统 |

### 重要会议

| 会议 | 领域 | 推荐阅读 |
|------|------|---------|
| **OSDI** | 操作系统 | ⭐⭐⭐ |
| **NSDI** | 网络系统 | ⭐⭐⭐ |
| **MLSys** | ML 系统 | ⭐⭐⭐⭐ |
| **SIGCOMM** | 网络通信 | ⭐⭐ |
| **SoCC** | 云计算 | ⭐⭐ |

### 系统设计原则

1. **可扩展性**
   - 分布式训练
   - 弹性调度

2. **性能优化**
   - 量化压缩
   - 显存优化
   - IO 优化

3. **工程实践**
   - MLOps
   - 监控调试
   - 持续优化

---

## 小爪系统优化成果

### Phase 1 - 基础优化

| 模块 | 功能 | 状态 |
|------|------|------|
| 内容安全 | 敏感词检测 | ✅ |
| 意图识别 | 7类意图 | ✅ |
| 知识图谱 | 实体+关系 | ✅ |

### Phase 2 - 增强优化

| 模块 | 功能 | 状态 |
|------|------|------|
| 意图识别 | 12类意图 | ✅ |
| 情感分析 | 正面/负面/中性 | ✅ |
| 对话管理 | 历史+上下文 | ✅ |
| API 集成 | MiniMax 集成 | ✅ |

### 测试结果

- ✅ 意图识别: 13/13 (100%)
- ✅ 情感分析: 5/5 (100%)
- ✅ 对话管理: 正常
- ✅ API 集成: 正常

---

## 学习路线图

```
短期 (本周)
├── funNLP 精读
│   ├── 敏感词检测模块
│   ├── 意图识别优化
│   └── 知识图谱结构
│
└── AI Infra 入门
    ├── MLSys 白皮书
    └── 分布式训练基础

中期 (本月)
├── LLM Infra 学习
│   ├── 推理优化
│   └── 显存优化
│
└── 系统实践
    ├── 分布式训练
    └── 推理服务化

长期 (本季度)
├── 深入论文阅读
├── 实践项目
└── 社区贡献
```

---

## 参考资源

### GitHub 仓库

1. funNLP: https://github.com/fighting41love/funNLP
2. AI-Infra: https://github.com/HuaizhengZhang/AI-Infra-from-Zero-to-Hero

### 论文会议

1. OSDI: https://www.usenix.org/conference/osdi
2. NSDI: https://www.usenix.org/conference/nsdi
3. MLSys: https://mlsys.org/

### 学习平台

1. Papers With Code: https://paperswithcode.com/
2. ArXiv: https://arxiv.org/list/cs.AI/recent
3. Google Scholar: https://scholar.google.com/

---

## 下一步行动

- [ ] 阅读 MLSys 白皮书
- [ ] 学习 LLM 推理优化论文
- [ ] 实践分布式训练
- [ ] 优化小爪推理能力
- [ ] 探索商业化机会
