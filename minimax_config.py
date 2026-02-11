#!/usr/bin/env python3
"""
MiniMax 模型调用策略配置
根据 Coding Plan 限制定义调用策略
"""

# ==================== 限制配置 ====================

LIMITS = {
    'coding_plan': {
        'prompt_per_5h': 1000,  # 假设的限额，可调整
        'batch_size': 5,        # 每次批量处理的任务数
        'cache_ttl': 3600,      # 缓存时间（秒）
        'cache_size': 1000,     # 最大缓存条目
    },
    'normal': {
        'rate_limit': 100,  # 每分钟限制
        'retry_after': 60   # 限流后等待时间
    }
}

# ==================== 任务分类策略 ====================

TASK_STRATEGIES = {
    # 编程任务 → 使用 Coding Plan
    'coding': {
        'use_coding_plan': True,
        'priority': 'high',
        'batch_allowed': True,
        'examples': ['code', 'debug', 'refactor', 'review', 'explain_code']
    },
    # 简单任务 → 普通 Key
    'simple': {
        'use_coding_plan': False,
        'priority': 'low',
        'batch_allowed': False,
        'examples': ['chat', 'greeting', 'simple_qa']
    },
    # 通用任务 → 混合策略
    'general': {
        'use_coding_plan': True,
        'priority': 'medium',
        'batch_allowed': True,
        'examples': ['write', 'translate', 'summarize']
    }
}

# ==================== 批量处理规则 ====================

BATCH_RULES = {
    'max_batch_size': 5,
    'similarity_threshold': 0.8,  # 任务相似度阈值
    'max_wait_time': 30,          # 等待更多任务的 最长时间（秒）
    'auto_batch': True            # 是否自动批量
}

# ==================== 缓存策略 ====================

CACHE_RULES = {
    'enabled': True,
    'ttl_seconds': 3600,
    'max_entries': 1000,
    'eviction_policy': 'LRU',  # LRU, LFU, FIFO
    'ignore_fields': ['temperature', 'max_tokens']  # 忽略的参数字段
}

# ==================== 速率控制 ====================

RATE_CONTROL = {
    'window_seconds': 18000,  # 5小时 = 18000秒
    'warning_threshold': 0.8,  # 80% 报警
    'critical_threshold': 0.95,  # 95% 限流
    'auto_throttle': True,     # 自动限流
    'retry_strategy': 'exponential'  # exponential, linear, immediate
}

# =================⃣ 优化建议 ====================

OPTIMIZATION_TIPS = [
    "批量处理多个小任务为一次调用，减少 prompt 消耗",
    "使用缓存避免重复调用相同内容",
    "简单对话使用普通 API Key，保留 Coding Plan 给编程任务",
    "监控5小时使用量，避免触发限额",
    "大任务分解为小任务，充分利用 batch 处理",
    "高峰期降低调用频率，平峰期集中处理",
    "重要任务优先使用 Coding Plan"
]


def get_task_strategy(task_type: str) -> Dict:
    """获取任务策略"""
    task_type_lower = task_type.lower()
    
    for strategy_name, strategy in TASK_STRATEGIES.items():
        if any(keyword in task_type_lower for keyword in strategy['examples']):
            return strategy
    
    return TASK_STRATEGIES['general']


def should_use_coding_plan(task_type: str) -> bool:
    """判断是否使用 Coding Plan"""
    return get_task_strategy(task_type)['use_coding_plan']


def calculate_saved_prompts(total_tasks: int, batch_size: int) -> int:
    """计算节省的 prompt 数量"""
    batches = (total_tasks + batch_size - 1) // batch_size
    without_batch = total_tasks
    with_batch = batches
    return without_batch - with_batch


# ==================== 使用示例配置 ====================

EXAMPLE_CONFIG = """
# MiniMax 模型调用优化配置示例

## 1. 基本配置
CODING_PLAN_KEY = "your_coding_plan_key"  # 编程套餐 Key
NORMAL_KEY = "your_normal_key"            # 普通 Key

## 2. 优化策略

### 编程任务（使用 Coding Plan）
- 代码生成、调试、重构、审查
- 批量处理：每次最多5个任务
- 缓存：1小时有效

### 简单任务（使用普通 Key）
- 日常对话、简单问答
- 不批量，直接调用
- 缓存：30分钟有效

## 3. 监控指标

```python
{
    "usage_5h": 450,        # 5小时使用量
    "usage_percent": 45.0,  # 使用率
    "cache_hits": 128,      # 缓存命中
    "saved_prompts": 256,   # 节省的调用
    "efficiency": 35.5      # 效率提升 %
}
```

## 4. 效果预估

| 指标 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| 每日调用 | 500 | 350 | 30%↓ |
| Token消耗 | 100万 | 70万 | 30%↓ |
| 成本 | $10 | $7 | 30%↓ |
"""


if __name__ == "__main__":
    print("MiniMax Optimization Configuration")
    print("=" * 50)
    print(f"\n📋 任务策略:")
    for name, strategy in TASK_STRATEGIES.items():
        print(f"  {name}: Coding Plan = {strategy['use_coding_plan']}")
    
    print(f"\n💡 优化建议:")
    for tip in OPTIMIZATION_TIPS[:3]:
        print(f"  • {tip}")
    
    print(f"\n📊 批量处理节省计算:")
    saved = calculate_saved_prompts(20, 5)
    print(f"  20个任务 → {saved}次节省")
    
    print("\n✅ Configuration loaded!")
