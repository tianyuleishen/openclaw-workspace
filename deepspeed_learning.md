# DeepSpeed 使用学习笔记

## 2026-02-10

### 仓库信息

| 属性 | 值 |
|------|-----|
| **仓库** | deepspeedai/DeepSpeed |
| **Stars** | ⭐ 41,588 |
| **Forks** | 🍴 4,710 |
| **描述** | Deep learning optimization library for distributed training and inference |
| **链接** | https://github.com/deepspeedai/DeepSpeed |

---

## 什么是 DeepSpeed?

DeepSpeed 是微软开源的深度学习优化库，让分布式训练和推理变得简单、高效、有效。

```
┌─────────────────────────────────────────────────────────────────┐
│                        DeepSpeed                                │
├─────────────────────────────────────────────────────────────────┤
│  🚀 分布式训练          │  ⚡ 高效推理          │  💾 显存优化 │
│  • ZeRO                 │  • MII                │  • 量化      │
│  • 流水线并行           │  • 推理优化           │  • 混合精度  │
│  • 数据并行              │  • 压缩               │  • 梯度检查点│
└─────────────────────────────────────────────────────────────────┘
```

---

## 核心特性

### 1. ZeRO (Zero Redundancy Optimizer)

ZeRO 是 DeepSpeed 的核心技术创新，通过消除训练过程中的冗余来大幅提升效率。

#### ZeRO 三个阶段

| 阶段 | 优化内容 | 显存节省 |
|------|---------|---------|
| **ZeRO-1** | 优化器状态分片 | ~50% |
| **ZeRO-2** | + 梯度分片 | ~75% |
| **ZeRO-3** | + 参数分片 | ~8x (线性扩展) |

```
┌─────────────────────────────────────────────────────────────┐
│                    ZeRO 原理图                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  传统训练 (FP32 优化器)                                    │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ 优化器状态 (Adam)    │ 梯度 (Grad)  │ 参数 (Param) │ │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
│  ZeRO-1 (优化器状态分片)                                   │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │ Optimizer  │ │ Optimizer   │ │ Optimizer   │          │
│  │ Shard 1    │ │ Shard 2    │ │ Shard 3    │          │
│  └─────────────┘ └─────────────┘ └─────────────┘          │
│  节省: 50% 显存                                            │
│                                                             │
│  ZeRO-2 (+ 梯度分片)                                       │
│  节省: 75% 显存                                            │
│                                                             │
│  ZeRO-3 (+ 参数分片)                                      │
│  节省: 8倍 (线性扩展)                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. 流水线并行 (Pipeline Parallelism)

将大模型分布在多个 GPU 上：

```
┌─────────────────────────────────────────────────────────┐
│              流水线并行示意图                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  GPU 0          GPU 1          GPU 2          GPU 3    │
│  ┌───┐         ┌───┐         ┌───┐         ┌───┐    │
│  │L1 │────────►│L4 │────────►│L7 │────────►│L10 │    │
│  │L2 │         │L5 │         │L8 │         │L11 │    │
│  │L3 │         │L6 │         │L9 │         │L12 │    │
│  └───┘         └───┘         └───┘         └───┘    │
│    │             │             │             │        │
│   Data         Data          Data          Data       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 3. 推理优化 (Inference Optimization)

#### MII (Model Implementations for Inference)

```python
# 使用 DeepSpeed MII 加速推理
import mii

# 部署模型
mii.deploy(
    task="text-generation",
    model="microsoft/Phi-3-mini-4k-instruct",
    deployment_name="phi3_deployment"
)
```

#### 量化推理

```python
import torch
from deepspeed import InferenceEngine

# 加载量化模型
model = InferenceEngine(
    model="microsoft/Phi-3-mini-4k-instruct",
    dtype=torch.int8,  # INT8 量化
    tensor_parallelism=2  # 张量并行
)

# 推理
output = model.generate("Hello, world!")
```

---

## 安装 DeepSpeed

### 1. 基础安装

```bash
# pip 安装
pip install deepspeed

# conda 安装
conda install -c conda-forge deepspeed
```

### 2. 从源码安装

```bash
git clone https://github.com/microsoft/DeepSpeed.git
cd DeepSpeed
pip install .

# 安装 Megatron
pip install .

# 使用 GPU 优化
DS_BUILD_OPS=1 pip install .
```

### 3. 验证安装

```python
import deepspeed

print(f"DeepSpeed 版本: {deepspeed.__version__}")

# 检查 GPU 支持
print(f"GPU 可用: {torch.cuda.is_available()}")
print(f"GPU 数量: {torch.cuda.device_count()}")
```

---

## DeepSpeed 基础使用

### 1. ZeRO 训练配置

#### JSON 配置文件 (ds_config.json)

```json
{
  "train_batch_size": 32,
  "train_micro_batch_size_per_gpu": 4,
  "steps_per_print": 10,
  
  "optimizer": {
    "type": "Adam",
    "params": {
      "lr": 0.001,
      "betas": [0.9, 0.999],
      "eps": 1e-8
    }
  },
  
  "fp16": {
    "enabled": true,
    "loss_scale": 0,
    "loss_scale_window": 1000,
    "initial_scale_power": 16
  },
  
  "zero_optimization": {
    "stage": 2,
    "allgather_partitions": true,
    "allgather_bucket_size": 5e8,
    "overlap_comm": true,
    "reduce_scatter": true,
    "reduce_bucket_size": 5e8,
    "contiguous_gradients": true
  },
  
  "gradient_accumulation_steps": 8,
  "gradient_clipping": 1.0,
  
  "wall_clock_breakdown": false
}
```

#### 训练脚本

```python
import torch
import torch.nn as nn
import deepspeed
from deepspeed.pipe import PipelineModule

# 定义模型
class MyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(768, 768)
        self.layer2 = nn.Linear(768, 768)
        self.layer3 = nn.Linear(768, 2)
        
    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        return x

# 初始化 DeepSpeed
model = MyModel()

# DeepSpeed 初始化参数
parameters = filter(lambda p: p.requires_grad, model.parameters())

# 使用 ZeRO 训练
engine, optimizer, dataloader, lr_scheduler = deepspeed.initialize(
    args=None,
    model=model,
    model_parameters=parameters,
    training_data=train_dataset,
    config="ds_config.json"
)

# 训练循环
for step, batch in enumerate(dataloader):
    inputs, labels = batch
    
    # 前向传播
    outputs = engine(inputs)
    loss = criterion(outputs, labels)
    
    # 反向传播
    engine.backward(loss)
    
    # 优化器步进
    engine.step()
    
    if step % 100 == 0:
        print(f"Step {step}: Loss = {loss.item():.4f}")
```

### 2. 流水线并行

```python
import deepspeed
from deepspeed.pipe import PipelineModule, LayerSpec

# 定义模型层
class MyPipeModel(PipelineModule):
    def __init__(self, stages):
        self.stages = stages
        
        # 定义层顺序
        layers = []
        for stage in stages:
            layers.extend(stage)
        
        super().__init__(layers=layers, loss_fn=torch.nn.CrossEntropyLoss())

# 配置流水线
model = MyPipeModel(
    stages=[
        [nn.Linear(768, 768), nn.ReLU()],
        [nn.Linear(768, 768), nn.ReLU()],
        [nn.Linear(768, 2)]
    ]
)

# 初始化
engine, _, _, _ = deepspeed.initialize(
    args=args,
    model=model,
    model_parameters=grouped_parameters,
    config="pipeline_config.json"
)

# 训练
engine.train_batch()
```

### 3. 推理优化

#### 基本推理

```python
import torch
from deepspeed import InferenceEngine

# 加载模型 (自动优化)
model = InferenceEngine(
    model="microsoft/Phi-3-mini-4k-instruct",
    dtype=torch.float16,  # 混合精度
    mp_size=1,  # 模型并行数
)

# 推理
input_text = "DeepSpeed is"
output = model.generate(
    input_text,
    max_new_tokens=100,
    temperature=0.9,
    top_p=0.9
)

print(f"Output: {output}")
```

#### 量化推理

```python
import torch
from transformers import AutoModelForCausalLM
from deepspeed.module_inject import replace_module

# 加载模型
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    torch_dtype=torch.float16,
    device_map="auto"
)

# 量化
quantized_model = replace_module(
    model=model,
    orig_class=torch.nn.Linear,
    replace_class=torch.nn.qat.Linear,
    qconfig=torch.quantization.get_default_qconfig('fbgemm')
)

# 推理
output = quantized_model.generate(input_ids)
```

---

## DeepSpeed 进阶功能

### 1. 混合精度训练 (FP16)

```python
# ds_config.json
{
  "fp16": {
    "enabled": true,
    "loss_scale": 0,
    "loss_scale_window": 1000,
    "initial_scale_power": 16,
    "hysteresis": 2,
    "consecutive_hysteresis": false
  }
}

# 训练脚本
engine, optimizer, _, _ = deepspeed.initialize(
    args=args,
    model=model,
    model_parameters=params,
    config="ds_config.json"
)

# DeepSpeed 自动处理 FP16
```

### 2. 梯度检查点 (Gradient Checkpointing)

```python
# ds_config.json
{
  "checkpoint": {
    "activation_checkpointing": {
      "enabled": true,
      "checkpointer": "deepspeed",
      "partition_activations": true,
      "cpu_checkpointing": true,
      "contiguous_memory_optimization": true
    }
  }
}
```

### 3. 学习率调度

```python
# ds_config.json
{
  "scheduler": {
    "type": "WarmupLR",
    "params": {
      "warmup_min_lr": 0,
      "warmup_max_lr": 0.001,
      "warmup_num_steps": 1000
    }
  }
}
```

### 4. 评估和测试

```python
# 评估
engine.eval()

with torch.no_grad():
    for batch in eval_dataloader:
        inputs, labels = batch
        outputs = engine(inputs)
        predictions = outputs.argmax(dim=-1)
        correct += (predictions == labels).sum().item()
        
accuracy = correct / len(eval_dataset)
print(f"Accuracy: {accuracy:.4f}")
```

---

## 分布式训练实战

### 1. 单节点多 GPU

```bash
# 启动脚本 (4 GPUs)
deepspeed --num_gpus=4 train.py \
  --deepspeed \
  --deepspeed_config ds_config.json
```

```python
# train.py
import deepspeed

# 初始化
deepspeed.init_distributed()
model = ...
trainloader = ...

# DeepSpeed 训练
engine, optimizer, _, _ = deepspeed.initialize(
    model=model,
    model_parameters=model.parameters(),
    training_data=trainloader,
    config="ds_config.json"
)

for epoch in range(epochs):
    engine.train()
    for batch in trainloader:
        # 训练
```

### 2. 多节点训练

```bash
# 节点 0 (主节点)
deepspeed --num_nodes=2 --num_gpus=8 \
  --node_rank=0 --master_addr=192.168.1.100 \
  train.py --deepspeed_config ds_config.json

# 节点 1
deepspeed --num_nodes=2 --num_gpus=8 \
  --node_rank=1 --master_addr=192.168.1.100 \
  train.py --deepspeed_config ds_config.json
```

### 3. 使用 Megatron-LM 风格的训练

```python
from deepstage.runtime.pipe.topology import PipeDataParallelTopology

# 配置拓扑
topology = PipeDataParallelTopology(
    data_dim=PipeDataParallelTensor.DATA,
    pipe_dim=PipeDataParallelTensor.PIPE,
    model_dim=PipeDataParallelTensor.MODEL
)

# 初始化
engine, _, _, _ = deepspeed.initialize(
    args=args,
    model=model,
    model_parameters=grouped_parameters,
    training_data=train_data,
    pipeline_module_parameters={
        "topology": topology,
        "partition_method": "uniform"
    }
)
```

---

## DeepSpeed 推理服务 (MII)

### 1. 部署模型

```python
import mii

# 部署模型
mii.deploy(
    task="text-generation",
    model="microsoft/Phi-3-mini-4k-instruct",
    deployment_name="phi3_deployment",
    # 可选参数
    tensor_parallel={"tp": 1},  # 张量并行
    replication={"replication": 1},  # 冗余副本
    enable_cuda_graph=True,  # CUDA 图加速
    enable_prefix_caching=True  # 前缀缓存
)

print("模型部署完成!")
```

### 2. 查询服务

```python
import mii

# 客户端查询
generator = mii.mii_query_handle("phi3_deployment")

# 生成文本
response = generator.query(
    {"query": "Explain quantum computing in simple terms:"},
    max_new_tokens=100,
    temperature=0.7
)

print(response)
```

### 3. 批量推理

```python
import mii

# 批量查询
requests = [
    {"query": "What is AI?"},
    {"query": "How does Python work?"},
    {"query": "Explain machine learning"}
]

# 批量推理
responses = mii.mii_query_handle("phi3_deployment").query(
    requests,
    batch_size=3
)

for i, response in enumerate(responses):
    print(f"Response {i+1}: {response}")
```

---

## 最佳实践

### 1. ZeRO 配置建议

| 模型大小 | ZeRO 阶段 | 优化建议 |
|---------|----------|---------|
| < 1B 参数 | Stage 1-2 | 足够 |
| 1B - 10B | Stage 2 | 推荐 |
| 10B - 70B | Stage 2-3 | 需要 |
| > 70B | Stage 3 | 必须 |

```json
{
  "zero_optimization": {
    "stage": 2,
    "contiguous_gradients": true,
    "overlap_comm": true,
    "reduce_scatter": true,
    "allgather_partitions": true
  }
}
```

### 2. 批大小设置

```python
# 建议的批大小设置
global_batch_size = 1024  # 总批大小
micro_batch_size = 4     # 每个 GPU 的微批大小
gradient_accumulation = global_batch_size // (micro_batch_size * num_gpus)
```

### 3. 通信优化

```json
{
  "communication_data_size": 1000,
  "allgather_bucket_size": 5e8,
  "reduce_bucket_size": 5e8
}
```

### 4. 显存优化

```json
{
  "checkpoint": {
    "activation_checkpointing": {
      "enabled": true
    }
  },
  "fp16": {
    "enabled": true,
    "loss_scale": 0
  }
}
```

---

## 常见问题

### Q1: CUDA 内存不足

```python
# 解决方案1: 减小批大小
"train_micro_batch_size_per_gpu": 2

# 解决方案2: 启用梯度检查点
"checkpoint": {
  "activation_checkpointing": {
    "enabled": true
  }
}

# 解决方案3: 使用 ZeRO-3
"zero_optimization": {
  "stage": 3
}
```

### Q2: 训练速度慢

```python
# 解决方案1: 启用 CUDA 图
"cuda_graph": {
  "enabled": true
}

# 解决方案2: 优化通信
"zero_optimization": {
  "overlap_comm": true,
  "contiguous_gradients": true
}
```

### Q3: 精度损失

```python
# 解决方案1: 使用 FP32 主权重
"fp16": {
  "enabled": true,
  "loss_scale": 0,  # 动态损失缩放
  "auto_cast": false
}

# 解决方案2: 减小学习率
"optimizer": {
  "params": {
    "lr": 0.0005  # 减小 50%
  }
}
```

---

## 对小爪的启示

### 短期可应用

1. **推理优化**
   - 使用 INT8 量化
   - 启用 CUDA 图
   - 实施批次推理

2. **显存优化**
   - 启用梯度检查点
   - 使用混合精度
   - 优化数据加载

### 中期可发展

1. **分布式训练**
   - 实现 ZeRO 优化
   - 支持流水线并行
   - 多节点训练

2. **服务化部署**
   - 集成 MII
   - 构建推理 API
   - 实施监控

### 长期可探索

1. **高级优化**
   - 知识蒸馏
   - 自动化调参
   - 模型压缩

2. **新硬件**
   - 边缘部署
   - 专用加速器
   - 多模态推理

---

## 参考资源

### 官方资源

- **GitHub**: https://github.com/microsoft/DeepSpeed
- **文档**: https://www.deepspeed.ai/
- **教程**: https://www.deepspeed.ai/tutorials/

### 论文

- **ZeRO Paper**: https://arxiv.org/abs/1910.02054
- **DeepSpeed Paper**: https://arxiv.org/abs/2207.00032

### 社区

- **GitHub Issues**: 提问和解答
- **Discord**: 实时讨论
- **Twitter**: @DeepSpeedAI

---

## 总结

DeepSpeed 是微软开源的强大的深度学习优化库，核心特性包括：

1. **ZeRO 优化** - 通过消除冗余实现超大规模训练
2. **流水线并行** - 支持超大模型分布式训练
3. **推理优化** - MII 加速推理部署
4. **易用性** - 只需简单配置即可使用

掌握 DeepSpeed 可以帮助：

- 训练超大模型 (千亿参数)
- 降低训练成本
- 加速推理部署
- 构建生产级 AI 系统

---

## 下一步行动

- [ ] 安装 DeepSpeed 并运行示例
- [ ] 实践 ZeRO 优化配置
- [ ] 学习 MII 推理服务
- [ ] 尝试分布式训练
- [ ] 集成到小爪系统
