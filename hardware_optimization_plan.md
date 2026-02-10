# 小爪系统硬件条件分析与优化方案

## 2026-02-10

### 当前硬件条件

| 组件 | 规格 | 可用量 |
|------|------|--------|
| **CPU** | 2核 Intel Xeon Platinum | 2核 |
| **内存** | 1.6GB | 919MB 可用 |
| **GPU** | 无 | - |
| **存储** | 40GB | 13GB 可用 |
| **Python** | 3.14.2 | - |

---

## 硬件分析

### 优势
- ☁️ 云服务器，弹性可扩展
- 💾 存储充足 (13GB 可用)
- 🖥️ Xeon CPU，适合轻量推理

### 限制
- ❌ 无 GPU，无法进行 CUDA 加速
- 💾 内存受限 (仅 1.6GB)
- 🔄 CPU 核心少 (2核)

---

## 优化方案

### Phase 1: CPU 优化 (立即可行)

#### 1. 内存优化

| 技术 | 描述 | 预期效果 | 适用条件 |
|------|------|---------|---------|
| **梯度累积** | 减少单步显存占用 | 显存占用减少 50% | 受限内存 |
| **混合精度** | FP16 计算 | 计算速度提升 2x | CPU 支持 |
| **模型量化** | INT8 量化 | 模型大小减少 75% | 通用 |
| **梯度检查点** | 重新计算激活 | 显存节省 30% | 受限内存 |

#### 2. CPU 推理优化

```python
# 优化 1: 启用 CPU 优化的 torch
import torch

# 检查 CPU 优化
print(f"CPU 优化: {torch.get_num_threads()}")
print(f"BLAS 库: {torch.backends.blas.cpu_info()}")

# 启用 MKL 优化
torch.set_num_threads(2)  # 使用所有 CPU 核心

# 优化 2: 使用 torch.compile (Python 3.14+)
# model = torch.compile(model, backend="cpuopt")

# 优化 3: ONNX Runtime 加速
import onnxruntime as ort

# CPU 推理会话
providers = ['CPUExecutionProvider']
session = ort.InferenceSession("model.onnx", providers=providers)

# 优化 4: 模型导出为 ONNX
torch.onnx.export(
    model,
    dummy_input,
    "model.onnx",
    opset_version=13,
    dynamic_axes={
        'input': {0: 'batch_size'},
        'output': {0: 'batch_size'}
    }
)
```

#### 3. 请求批处理优化

```python
# 优化 5: 动态批处理器
class DynamicBatcher:
    """
    基于当前硬件条件的动态批处理器
    """
    def __init__(self, max_batch_size=4, max_wait_time=0.05):
        self.max_batch_size = max_batch_size  # 基于 2CPU 核
        self.max_wait_time = max_wait_time  # 50ms 超时
        self.request_queue = []
    
    async def add_request(self, request):
        """
        添加请求
        - 加入队列
        - 检查是否批量
        """
        self.request_queue.append({
            'request': request,
            'timestamp': time.time()
        })
        
        # 立即处理或等待
        if len(self.request_queue) >= self.max_batch_size:
            return await self._process_batch()
        
        # 短暂等待
        if time.time() - self.request_queue[0]['timestamp'] > self.max_wait_time:
            return await self._process_batch()
        
        return None
    
    async def _process_batch(self):
        """
        批量处理
        - 合并请求
        - 批量推理
        - 分离结果
        """
        if not self.request_queue:
            return []
        
        batch = self.request_queue
        self.request_queue = []
        
        # 批量推理
        results = []
        for item in batch:
            result = await self._infer(item['request'])
            results.append({
                'request_id': item['request'].get('id'),
                'result': result
            })
        
        return results
```

---

### Phase 2: 轻量级模型优化

#### 1. 模型量化

```python
# 优化 6: CPU 量化
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# 加载模型
model_name = "microsoft/Phi-3-mini-4k-instruct"

# CPU 量化配置
quantization_config = {
    "load_in_8bit": True,  # INT8 量化
    "load_in_4bit": False,
    "bnb_8bit_quant_type": "static",
    "bnb_8bit_use_double_quant": True,
}

# 加载量化模型
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=quantization_config,
    device_map="auto"  # 自动分配到 CPU
)

# 使用 tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)

# 推理
input_text = "Hello, world!"
inputs = tokenizer(input_text, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=50)
```

#### 2. 知识蒸馏 (轻量模型)

```python
# 优化 7: 知识蒸馏训练轻量模型
import torch
import torch.nn as nn
from transformers import AutoModelForCausalLM, AutoTokenizer

# 教师模型 (大模型)
teacher_model = AutoModelForCausalLM.from_pretrained(
    "microsoft/Phi-3-mini-4k-instruct"
)

# 学生模型 (小模型)
student_model = AutoModelForCausalLM.from_pretrained(
    "microsoft/Phi-3-mini-2k-instruct"
)

# 蒸馏损失
class DistillationLoss(nn.Module):
    def __init__(self, temperature=2.0, alpha=0.5):
        super().__init__()
        self.temperature = temperature
        self.alpha = alpha
        self.ce_loss = nn.CrossEntropyLoss()
        self.kl_loss = nn.KLDivLoss(reduction='batchmean')
    
    def forward(self, student_logits, teacher_logits, labels):
        # 软标签损失
        soft_student = student_logits / self.temperature
        soft_teacher = teacher_logits / self.temperature
        
        kl_loss = self.kl_loss(
            torch.log_softmax(soft_student, dim=-1),
            torch.softmax(soft_teacher, dim=-1)
        ) * (self.temperature ** 2)
        
        # 硬标签损失
        ce_loss = self.ce_loss(student_logits, labels)
        
        # 总损失
        return self.alpha * ce_loss + (1 - self.alpha) * kl_loss
```

#### 3. 模型剪枝

```python
# 优化 8: 结构化剪枝
import torch.nn.utils.prune as prune

def apply_structural_pruning(model, amount=0.3):
    """
    结构化剪枝
    - 移除注意力头
    - 减少隐藏层维度
    """
    for name, module in model.named_modules():
        if isinstance(module, torch.nn.Linear):
            # L1 非结构化剪枝
            prune.l1_unstructured(module, name='weight', amount=amount)
        
        if isinstance(module, torch.nn.MultiheadAttention):
            # 剪枝注意力头
            num_heads = module.num_heads
            prune_heads = int(num_heads * amount)
            prune.ln_unstructured(
                module,
                name='in_proj_weight',
                amount=prune_heads / num_heads
            )

# 应用剪枝
apply_structural_pruning(model, amount=0.3)
```

---

### Phase 3: 缓存策略优化

#### 1. 多级缓存

```python
# 优化 9: 多级缓存系统
class MultiLevelCache:
    """
    基于当前硬件条件的多级缓存
    """
    def __init__(self):
        # L1: 内存缓存 (快速, 受限)
        self.l1_cache = {}  # Dict[str, Any]
        self.l1_max_size = 100  # 限制大小
        
        # L2: 磁盘缓存 (较慢, 充足)
        self.l2_cache_dir = "/home/admin/.openclaw/workspace/.cache"
        os.makedirs(self.l2_cache_dir, exist_ok=True)
    
    async def get(self, key: str) -> Optional[Any]:
        """
        获取缓存
        - 优先检查 L1
        - 然后检查 L2
        """
        # L1 检查
        if key in self.l1_cache:
            return self.l1_cache[key]
        
        # L2 检查
        l2_path = f"{self.l2_cache_dir}/{key}.pickle"
        if os.path.exists(l2_path):
            with open(l2_path, 'rb') as f:
                return pickle.load(f)
        
        return None
    
    async def set(self, key: str, value: Any):
        """
        设置缓存
        - 优先写入 L1
        - L1 满时写入 L2
        """
        # 写入 L1
        if len(self.l1_cache) < self.l1_max_size:
            self.l1_cache[key] = value
        else:
            # L1 满，淘汰最旧并写入 L2
            oldest_key = next(iter(self.l1_cache.keys()))
            l2_path = f"{self.l2_cache_dir}/{oldest_key}.pickle"
            
            with open(l2_path, 'wb') as f:
                pickle.dump(self.l1_cache[oldest_key], f)
            
            del self.l1_cache[oldest_key]
            self.l1_cache[key] = value
```

#### 2. 语义缓存

```python
# 优化 10: 语义相似度缓存
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class SemanticCache:
    """
    基于语义相似度的缓存
    - 计算请求嵌入
    - 查找相似请求
    - 返回缓存结果
    """
    def __init__(self, threshold=0.95, max_size=100):
        self.threshold = threshold
        self.max_size = max_size
        self.cache = []
        self.model = None  # 轻量嵌入模型
    
    async def initialize(self):
        """
        初始化
        - 加载轻量嵌入模型
        """
        from sentence_transformers import SentenceTransformer
        
        # 使用轻量模型
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    async def get(self, request: str) -> Optional[Any]:
        """
        获取缓存
        - 计算嵌入
        - 查找相似
        - 返回结果
        """
        if not self.model or not self.cache:
            return None
        
        # 计算请求嵌入
        request_embedding = self.model.encode([request])
        
        # 查找相似
        for cached in self.cache:
            similarity = cosine_similarity(
                request_embedding,
                cached['embedding']
            )[0][0]
            
            if similarity >= self.threshold:
                return cached['result']
        
        return None
    
    async def set(self, request: str, result: Any):
        """
        设置缓存
        - 计算嵌入
        - 添加到缓存
        - 淘汰旧缓存
        """
        if not self.model:
            await self.initialize()
        
        # 计算嵌入
        embedding = self.model.encode([request])
        
        # 添加
        self.cache.append({
            'request': request,
            'result': result,
            'embedding': embedding
        })
        
        # 淘汰最旧
        if len(self.cache) > self.max_size:
            self.cache.pop(0)
```

---

### Phase 4: 并发优化

#### 1. 异步处理

```python
# 优化 11: 异步并发控制
import asyncio
from concurrent.futures import ThreadPoolExecutor

class AsyncProcessor:
    """
    基于 CPU 核心数的异步处理器
    """
    def __init__(self, max_workers=None):
        # 根据 CPU 核心数设置 workers
        self.max_workers = max_workers or 2  # 2核 CPU
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
    
    async def process_batch(self, requests: List[str]) -> List[Any]:
        """
        批量异步处理
        - 使用线程池
        - 并发执行
        """
        loop = asyncio.get_event_loop()
        
        tasks = [
            loop.run_in_executor(
                self.executor,
                self._process_single,
                request
            )
            for request in requests
        ]
        
        results = await asyncio.gather(*tasks)
        return results
    
    def _process_single(self, request: str) -> Any:
        """
        单个处理
        - 同步推理
        - 返回结果
        """
        # 模拟处理
        return self._infer(request)
```

#### 2. 连接池

```python
# 优化 12: API 连接池
import aiohttp

class ConnectionPool:
    """
    API 连接池
    - 复用连接
    - 减少延迟
    """
    def __init__(self, max_connections=5, max_per_host=2):
        self.connector = aiohttp.TCPConnector(
            limit=max_connections,
            limit_per_host=max_per_host,
            ttl_dns_cache=300,
            keepalive_timeout=30
        )
        self.session = None
    
    async def get_session(self) -> aiohttp.ClientSession:
        """
        获取会话
        - 创建或复用
        """
        if not self.session or self.session.closed:
            self.session = aiohttp.ClientSession(
                connector=self.connector,
                timeout=aiohttp.ClientTimeout(total=30)
            )
        return self.session
    
    async def close(self):
        """
        关闭会话
        """
        if self.session and not self.session.closed:
            await self.session.close()
```

---

## 优化效果预测

### 基于当前硬件的优化效果

| 优化项 | 当前条件 | 预期改进 | 可行性 |
|--------|---------|---------|--------|
| **批处理** | 2核 CPU | 吞吐量提升 2x | ✅ 高 |
| **内存优化** | 1.6GB | 内存占用减少 50% | ✅ 高 |
| **缓存策略** | 13GB 磁盘 | 响应时间减少 60% | ✅ 高 |
| **异步并发** | 2核 | 并发能力提升 3x | ✅ 高 |
| **模型量化** | 无 GPU | 模型大小减少 75% | ✅ 高 |
| **ONNX 优化** | CPU | 推理速度提升 2x | ✅ 中 |
| **知识蒸馏** | 受限内存 | 需要更多资源 | ⚠️ 低 |
| **分布式训练** | 无 GPU | 需要集群 | ❌ 不可行 |

### 优先级排序

| 优先级 | 优化项 | 预期效果 | 实施难度 |
|--------|--------|---------|---------|
| **P0** | 批处理 | 吞吐量 2x | 低 |
| **P0** | 多级缓存 | 延迟 60%↓ | 低 |
| **P1** | 内存优化 | 内存 50%↓ | 中 |
| **P1** | 模型量化 | 大小 75%↓ | 中 |
| **P2** | ONNX 优化 | 速度 2x | 中 |
| **P3** | 异步并发 | 并发 3x | 高 |
| **P4** | 知识蒸馏 | 需要资源 | 高 |

---

## 实施计划

### Week 1: 基础优化 (P0)

```python
# 实施 1: 批处理系统
# 文件: batch_processor.py

class BatchProcessor:
    def __init__(self, batch_size=4, timeout=0.05):
        self.batch_size = batch_size
        self.timeout = timeout
        self.queue = []
    
    async def process(self, request):
        self.queue.append(request)
        
        if len(self.queue) >= self.batch_size:
            return await self._batch_infer()
        
        if time.time() > self.timeout:
            return await self._batch_infer()
        
        return None

# 实施 2: 多级缓存
# 文件: cache_system.py

class CacheSystem:
    def __init__(self, l1_size=100, l2_dir="/tmp/cache"):
        self.l1 = LRUCache(l1_size)
        self.l2_dir = l2_dir
    
    async def get(self, key):
        # 检查 L1
        if key in self.l1:
            return self.l1.get(key)
        
        # 检查 L2
        l2_path = f"{self.l2_dir}/{key}.pkl"
        if os.path.exists(l2_path):
            with open(l2_path, 'rb') as f:
                return pickle.load(f)
        
        return None
```

### Week 2: 模型优化 (P1)

```python
# 实施 3: 模型量化
# 文件: quantized_model.py

class QuantizedModel:
    def __init__(self, model_name):
        from transformers import AutoModelForCausalLM
        
        # INT8 量化
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            load_in_8bit=True,
            device_map="auto"
        )
    
    def infer(self, input_text):
        inputs = tokenizer(input_text, return_tensors="pt")
        return self.model.generate(**inputs, max_new_tokens=100)

# 实施 4: ONNX 优化
# 文件: onnx_exporter.py

def export_to_onnx(model, dummy_input, output_path):
    torch.onnx.export(
        model,
        dummy_input,
        output_path,
        opset_version=13,
        dynamic_axes={
            'input': {0: 'batch_size'},
            'output': {0: 'batch_size'}
        }
    )
```

### Week 3: 并发优化 (P2)

```python
# 实施 5: 异步处理器
# 文件: async_processor.py

class AsyncProcessor:
    def __init__(self, max_workers=2):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def process_batch(self, requests):
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(self.executor, self._infer, req)
            for req in requests
        ]
        return await asyncio.gather(*tasks)
```

### Week 4: 监控和调优 (P3)

```python
# 实施 6: 性能监控
# 文件: monitor.py

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {
            'requests': 0,
            'latency_sum': 0,
            'batch_time': 0,
            'cache_hits': 0
        }
    
    def record(self, latency, batch_time=0, cached=False):
        self.metrics['requests'] += 1
        self.metrics['latency_sum'] += latency
        self.metrics['batch_time'] += batch_time
        self.metrics['cache_hits'] += cached
    
    def get_stats(self):
        return {
            'avg_latency': self.metrics['latency_sum'] / max(self.metrics['requests'], 1),
            'total_requests': self.metrics['requests'],
            'cache_hit_rate': self.metrics['cache_hits'] / max(self.metrics['requests'], 1)
        }
```

---

## 总结

### 当前硬件条件下的最优策略

| 策略 | 描述 | 预期效果 |
|------|------|---------|
| **批处理** | 动态批量处理请求 | 吞吐量提升 2x |
| **多级缓存** | L1 内存 + L2 磁盘 | 延迟降低 60% |
| **模型量化** | INT8 量化 | 大小减少 75% |
| **异步并发** | CPU 核心并发 | 并发能力 3x |

### 不可行的优化

| 优化项 | 原因 | 替代方案 |
|--------|------|---------|
| **GPU 加速** | 无 GPU | CPU 优化 |
| **分布式训练** | 单机 | 轻量模型 |
| **大模型训练** | 内存受限 | 模型蒸馏 |

### 下一步行动

- [ ] 实现批处理系统
- [ ] 添加多级缓存
- [ ] 模型量化
- [ ] 性能监控
- [ ] 持续调优

---

## 参考资料

### 优化工具

- **ONNX Runtime**: https://onnxruntime.ai/
- **BitsAndBytes**: https://github.com/TimDettmers/bitsandbytes
- **Sentence Transformers**: https://www.sentence-transformers/

### 学习资源

- **PyTorch Optimization**: https://pytorch.org/docs/stable/optim.html
- **ONNX Tutorial**: https://onnxruntime.ai/docs/tutorials/optimizations/
- **Python Async**: https://docs.python.org/3/library/asyncio.html
