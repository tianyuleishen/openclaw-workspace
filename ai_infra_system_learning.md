# AI Infrastructure (AI Infra) 系统学习笔记

## 2026-02-10

### 仓库信息

- **仓库**: HuaizhengZhang/AI-Infra-from-Zero-to-Hero
- **Stars**: 3,675
- **链接**: https://github.com/HuaizhengZhang/AI-Infra-from-Zero-to-Hero

---

## 什么是 AI Infrastructure?

AI 基础设施是支撑 AI 系统运行的所有底层技术和系统组件。

```
┌─────────────────────────────────────────────────────────────┐
│                    AI 应用层                                │
│         (聊天机器人、推荐系统、图像识别等)                  │
├─────────────────────────────────────────────────────────────┤
│                    AI 框架层                                │
│         (PyTorch, TensorFlow, JAX 等)                     │
├─────────────────────────────────────────────────────────────┤
│                    AI 基础设施层                            │
│         (分布式训练、推理优化、资源调度等)                 │
├─────────────────────────────────────────────────────────────┤
│                    硬件层                                    │
│         (GPU、TPU、CPU、存储、网络)                       │
└─────────────────────────────────────────────────────────────┘
```

---

## AI Infra 核心组件

### 1. 训练基础设施 (Training Infra)

| 组件 | 功能 | 关键技术 |
|------|------|---------|
| **分布式训练** | 多GPU/多节点并行 | 数据并行、模型并行 |
| **流水线管理** | 数据预处理 | Apache Beam, tf.data |
| **资源调度** | GPU/CPU 分配 | Kubernetes, Slurm |
| **检查点** | 容错恢复 | 保存/恢复模型状态 |

### 2. 推理基础设施 (Inference Infra)

| 组件 | 功能 | 关键技术 |
|------|------|---------|
| **模型服务** | 在线预测 | TorchServe, Triton |
| **批处理** | 离线推理 | Spark, Dask |
| **量化压缩** | 减小模型大小 | INT8, 动态量化 |
| **缓存** | 加速响应 | Redis, Memcached |

### 3. 数据基础设施 (Data Infra)

| 组件 | 功能 | 关键技术 |
|------|------|---------|
| **数据湖** | 统一存储 | Delta Lake, Iceberg |
| **特征存储** | 实时特征 | Feast, Tecton |
| **数据版本** | 实验追踪 | DVC, MLflow |

---

## 重要会议和论文方向

### 系统会议 (System Conferences)

| 会议 | 简称 | 关注领域 | 重要性 |
|------|------|---------|--------|
| **OSDI** | 操作系统设计与实现 | 存储、调度 | ⭐⭐⭐⭐⭐ |
| **NSDI** | 网络系统设计与实现 | 分布式、网络 | ⭐⭐⭐⭐⭐ |
| **SIGCOMM** | 计算机通信 | 网络优化 | ⭐⭐⭐ |
| **SoCC** | 云计算研讨会 | 云系统 | ⭐⭐⭐⭐ |
| **MLSys** | 机器学习系统 | ML系统 | ⭐⭐⭐⭐⭐ |

### AI 系统论文方向

```
📚 ML/DL Infra (机器学习基础设施)
   ├── 分布式训练系统
   ├── 模型并行化技术
   ├── 内存优化
   └── 数据流水线

📚 LLM Infra (大语言模型基础设施)
   ├── 预训练系统
   ├── 推理优化
   ├── 显存优化
   └── 分布式推理

📚 Domain-Specific (领域特定系统)
   ├── 推荐系统
   ├── 搜索系统
   └── 多模态系统
```

---

## 关键技术详解

### 1. 分布式训练

**数据并行 (Data Parallelism)**
```
原理: 每个GPU有完整模型，处理不同数据
优点: 实现简单，扩展性好
缺点: 通信开销大

示例:
┌─────────────────────────────────────────┐
│                 参数服务器               │
└─────────────────────────────────────────┘
         ↕         ↕         ↕
    ┌───────┐  ┌───────┐  ┌───────┐
    │ GPU 1 │  │ GPU 2 │  │ GPU 3 │
    │ Model │  │ Model │  │ Model │
    │ Data1 │  │ Data2 │  │ Data3 │
    └───────┘  └───────┘  └───────┘
```

**模型并行 (Model Parallelism)**
```
原理: 不同GPU负责模型不同部分
优点: 可训练超大模型
缺点: 实现复杂，通信频繁
```

### 2. 推理优化

**量化 (Quantization)**
```python
# 示例: 动态量化
import torch

# FP32 模型
model_fp32 = ...  # 完整精度模型

# INT8 量化
model_int8 = torch.quantization.quantize_dynamic(
    model_fp32, 
    {torch.nn.Linear},
    dtype=torch.qint8
)
```

**批处理 (Batching)**
```python
# 动态批处理示例
requests = [
    "Hello",
    "How are you?",
    "What's your name?"
]

# 合并为单个推理请求
batched_output = model.infer(requests)
```

### 3. 显存优化

| 技术 | 描述 | 显存节省 |
|------|------|---------|
| **梯度检查点** | 重新计算激活值 | ~50% |
| **混合精度** | FP16 + FP32 | ~50% |
| **模型分片** | 分片存储模型 | 线性 |
| **CPU Offload** | 将部分数据移到CPU | 可变 |

---

## 实际系统案例

### 1. 训练系统

| 系统 | 公司 | 特点 |
|------|------|------|
| **DeepSpeed** | Microsoft |  ZeRO 优化、流水线并行 |
| **Megatron-LM** | NVIDIA | 模型并行、分布式训练 |
| **FairScale** | Meta | PyTorch 官方扩展 |
| **ColossalAI** | HPC-AI Tech | 异构训练 |

### 2. 推理系统

| 系统 | 公司 | 特点 |
|------|------|------|
| **Triton** | NVIDIA | 多框架支持、动态批处理 |
| **TorchServe** | Meta | PyTorch 官方服务 |
| **TensorRT** | NVIDIA | GPU 优化、INT8 |
| **vLLM** | UC Berkeley | PagedAttention、高吞吐 |

---

## 对小爪的启示

### 1. 短期可应用

```
✅ 推理优化
   - 模型量化 (减小大小)
   - 批处理 (提高吞吐)
   - 缓存 (加速响应)

✅ 系统监控
   - 性能指标收集
   - 资源使用监控
   - 错误日志
```

### 2. 中期可发展

```
🔧 分布式能力
   - 多模型支持
   - 负载均衡
   - 弹性扩缩容

🔧 推理服务化
   - API 服务框架
   - 请求队列
   - A/B 测试
```

### 3. 长期可探索

```
🚀 高级优化
   - 模型压缩
   - 知识蒸馏
   - 自动化机器学习

🚀 系统架构
   - 微服务设计
   - 边缘部署
   - 多云架构
```

---

## 学习路线图

```
入门阶段 (1-2周)
├── 理解分布式训练原理
├── 学习 PyTorch 分布式
└── 阅读关键论文摘要

进阶阶段 (1-2月)
├── 实现分布式训练
├── 优化推理性能
└── 学习模型压缩技术

深入阶段 (3-6月)
├── 阅读顶会论文
├── 贡献开源项目
└── 设计自己的系统
```

---

## 推荐资源

### 书籍
- 《Designing Data-Intensive Applications》
- 《Machine Learning Systems》

### 课程
- CS294-199: Advanced ML Systems (Berkeley)
- CS329S: ML Systems Design (Stanford)

### 论文合集
- MLSys 会议论文
- OSDI/NSDI 经典论文
- MLSys Whitepaper

### 开源项目
- DeepSpeed: https://github.com/microsoft/DeepSpeed
- vLLM: https://github.com/vllm-project/vllm
- Triton: https://github.com/triton-inference-server

---

## 总结

AI Infrastructure 是支撑 AI 应用的关键基础设施，包括：

1. **训练系统**: 分布式训练、资源调度
2. **推理系统**: 模型服务、优化加速
3. **数据系统**: 特征存储、数据管理

掌握 AI Infra 知识可以帮助：
- 更好地理解和优化模型性能
- 设计更高效的 AI 系统
- 为未来商业化打下基础

### 下一步行动

- [ ] 阅读 MLSys 白皮书
- [ ] 学习 DeepSpeed 使用
- [ ] 实践模型量化
- [ ] 探索推理服务化
