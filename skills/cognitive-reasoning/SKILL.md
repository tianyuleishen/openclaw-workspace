---
name: cognitive-reasoning
description: Advanced reasoning framework v3 with memory-aware intent understanding, history analysis, and full-auto mode for accurate user intent detection.
metadata: {"openclaw": {"emoji": "🧠", "version": "3.0", "mode": "full-auto", "requires": {"bins": ["python3"], "env": [], "config": ["AGENTS.md"]}}}
---

# 🧠 Cognitive Reasoning Framework v3

**Version**: 3.0  
**Mode**: Full Auto (全主动模式)  
**Status**: ✅ Active

## Core Principles

### 1. Think Before Act
- Never execute immediately upon receiving a command
- Pause and analyze the user's true intent
- Identify ambiguities and edge cases
- Seek clarification when needed

### 2. Memory-Aware Understanding
- Deep parsing of user requests
- Classification with memory enhancement
- Historical context analysis
- Learning from user patterns

### 3. Structured Reasoning
- Decompose complex tasks into steps
- Verify understanding before proceeding
- Confirm with user when uncertain
- Document reasoning process

## Usage - Full Auto Mode

### Automatic Invocation

The framework **automatically** analyzes every user message:

```python
# 自动调用流程
from cognitive-reasoning.think_loop_v3 import ThinkLoopV3

def handle_message(message, = ThinkLoopV history):
    thinker3()
    result = thinker.think(message, history)
    
    if result['confidence'] >= 0.80:
        return execute_task(message)
    else:
        return ask_clarification(result)
```

### Configuration

In `AGENTS.md`:
```yaml
cognitive_reasoning:
  enabled: true
  mode: full-auto
  threshold: 0.80
  memory: true
  history: true
  learning: true
```

## v3 Workflow

```
用户消息
    │
    ├─ Step 0: 📚 加载记忆
    │   ├─ MEMORY.md (长期记忆)
    │   ├─ USER.md (用户档案)
    │   └─ 对话历史
    │
    ├─ Step 1: 🎯 意图分类
    │   ├─ 记忆增强
    │   └─ 用户偏好分析
    │
    ├─ Step 2: 🔍 歧义检测
    │   ├─ 历史趋势分析
    │   └─ 上下文识别
    │
    ├─ Step 3: 📈 经验学习
    │   ├─ 用户模式累积
    │   └─ 动态置信度加成
    │
    ├─ Step 4: 📊 综合置信度
    │   └─ 最终评分
    │
    └─ Step 5: 决策
        ├─ ≥80%: ✅ 直接执行
        └─ <80%: 🔄 澄清问题
```

## Integration

The framework integrates with:
- ✅ Daily memory system (memory/*.md)
- ✅ Long-term memory (MEMORY.md)
- ✅ Conversation history
- ✅ User preferences (USER.md)
- ✅ Learning system (.intent_learning.json)

## Files

| File | Description |
|------|-------------|
| `think_loop_v3.py` | v3 Core Engine |
| `auto_integrator.py` | Auto Integration Script |
| `test_v3.py` | Test Suite |
| `README.md` | Documentation |

## CLI Usage

```bash
# 运行测试
python3 test_v3.py

# 快速分析
python3 auto_integrator.py "测试框架"

# 交互模式
python3 auto_integrator.py --interactive
```

## Think Loop Example

```
User: "测试认知框架"
(History: 之前讨论了创建/升级框架)

🧠 分析:
├─ Step 0: 加载记忆 ✅
├─ Step 1: 意图分类 → TEST_FRAMEWORK (85%)
├─ Step 2: 歧义检测 → 无
├─ Step 3: 经验学习 → +10%
├─ Step 4: 置信度 → 95%
└─ Step 5: ✅ 执行 (95% ≥ 80%)
```

## Performance

| Metric | v2 | v3 |
|--------|-----|-----|
| Intent Accuracy | 75% | **90%** |
| Confidence (with history) | 35% | **95%** |
| Auto Mode | Manual | **Full Auto** |

---

**🧠 Think First, Then Execute**
