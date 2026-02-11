# AI Infra 论文列表学习笔记

## 2026-02-10

### 仓库信息

| 属性 | 值 |
|------|-----|
| **仓库** | HuaizhengZhang/AI-Infra-from-Zero-to-Hero |
| **Stars** | ⭐ 3,675 |
| **Forks** | 🍴 362 |
| **描述** | AI System Papers and Industry Practice |

### 核心内容分类

#### 1. System for AI (AI 系统)
AI 系统的整体架构和设计原则

#### 2. ML/DL Infra (机器学习/深度学习基础设施)
- 分布式训练系统
- 模型并行化
- 数据流水线
- 资源调度

#### 3. LLM Infra (大语言模型基础设施)
- LLaMA、Mistral 等模型训练
- 推理优化
- 显存优化
- 分布式推理

#### 4. Domain-Specific Infra (领域特定基础设施)
- 推荐系统
- 搜索系统
- 多模态系统

### 重要会议

| 会议 | 全称 | 领域 |
|------|------|------|
| **OSDI** | 操作系统设计与实现 | 系统 |
| **NSDI** | 网络系统设计与实现 | 网络系统 |
| **SIGCOMM** | 计算机通信特别兴趣组 | 网络 |
| **SoCC** | 云计算研讨会 | 云计算 |
| **MLSys** | 机器学习系统 | ML系统 |

### 学习路线

```
入门 → ML/DL Infra → LLM Infra → 领域应用 → 深入研究
```

### 关键论文方向

1. **分布式训练**
   - 数据并行
   - 模型并行
   - 流水线并行

2. **推理优化**
   - 量化
   - 剪枝
   - 蒸馏

3. **资源调度**
   - 弹性调度
   - 负载均衡
   - 成本优化

4. **系统设计**
   - 存储系统
   - 网络通信
   - 容错机制

### 对小爪的启示

1. **系统思维**
   - AI 系统需要端到端优化
   - 基础设施是 AI 能力的基石

2. **可扩展性**
   - 分布式训练和推理
   - 弹性资源调度

3. **性能优化**
   - 量化压缩
   - 显存优化
   - IO 优化

4. **工程实践**
   - MLOps 最佳实践
   - 监控和调试
   - 持续优化

### 推荐学习资源

- 论文：OSDI/NSDI/MLSys 会议论文
- 视频：官方技术讲座
- 课程：MLSys 课程
- 博客：工业界实践分享

### 下一步学习

- [ ] 阅读 MLSys 白皮书
- [ ] 学习 LLM 推理优化
- [ ] 实践分布式训练
- [ ] 了解推理服务化

### 参考链接

- GitHub: https://github.com/HuaizhengZhang/AI-Infra-from-Zero-to-Hero
- 论文列表: https://github.com/HuaizhengZhang/AI-Infra-from-Zero-to-Hero#system-for-ai
