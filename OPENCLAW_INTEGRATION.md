# OpenClaw推理引擎集成指南

## 概述

从 v5.9 开始，推理引擎自动集成到所有OpenClaw会话中。

## 文件结构

```
/home/admin/.openclaw/workspace/
├── reasoning_engine_integrator.py  # 自动问题检测和求解
├── reasoning_engine_v5.9.py        # 论文级优化推理引擎
├── reasoning_engine_config.json     # 推理引擎配置
└── skills/
    └── reasoning/
        ├── __init__.py             # 自动导入模块
        └── SKILL.md                # 技能文档
```

## 自动集成

### 1. 会话启动时自动导入

在 `__init__.py` 中配置：
```python
from reasoning_engine_integrator import ReasoningIntegrator, solve
```

### 2. 消息处理绑定

配置文件：`reasoning_engine_config.json`
```json
{
  "reasoning_engine": {
    "auto_import": true,
    "auto_detect": true,
    "message_handler": "integrated"
  }
}
```

## 使用方法

### 快捷调用

```python
from skills.reasoning import solve

# 自动分析问题
answer = solve("tanθ₁·...·tanθₙ = 2^(n/2)")
```

### 完整使用

```python
from skills.reasoning import ReasoningIntegrator

integrator = ReasoningIntegrator()
result = integrator.analyze("你的数学问题")

print(f"类型: {result['problem_type']}")
print(f"答案: {result['answer']}")
print(f"置信度: {result['confidence']:.0%}")
```

## 支持的问题类型

| 类型 | 关键词 | 推理引擎 | 示例 |
|------|--------|---------|------|
| 三角函数 | tan, cos, sin, θ | v5.9 | tanθ₁·...·tanθₙ = 2^(n/2) |
| 极值组合 | 最大, 最小, 范围, 格子 | v5.7 | 100×100格子，每种颜色≤10000 |
| 函数直线 | 函数, 斜率, 共线 | v5.8 | y=(x+1)/(\|x\|+1) |
| 几何 | 三角形, 圆形, 抛物线 | v5.5 | 翻折问题, 内切圆 |

## 配置选项

### 自动导入

```json
{
  "reasoning_engine": {
    "auto_import": true
  }
}
```

### 关键词检测

```json
{
  "skills": [
    {
      "name": "trigonometric_solver",
      "keywords": ["tan", "cos", "sin", "θ"],
      "priority": 1
    }
  ]
}
```

## 版本历史

| 版本 | 日期 | 改进 |
|------|------|------|
| v5.9 | 2026-02-11 | 论文级优化，多策略验证 |
| v5.8 | 2026-02-11 | 参考社区，最佳实践 |
| v5.7 | 2026-02-11 | 极值分析，约束求解 |
| v5.6 | 2026-02-11 | 逻辑推理，密码破解 |
| v5.5 | 2026-02-11 | 几何精确，翻折问题 |

## 测试

```bash
cd /home/admin/.openclaw/workspace
python3 reasoning_engine_integrator.py
```

## 状态

✅ **已完全集成到所有会话**
✅ 自动启用
✅ 关键词检测
✅ 问题分类
✅ 置信度评估

## 常见问题

### Q: 推理引擎没有自动启动？

A: 检查文件路径是否正确，确保所有文件都已创建。

### Q: 如何禁用推理引擎？

A: 修改配置文件的 `auto_import` 为 false。

### Q: 如何添加新的问题类型？

A: 在 `reasoning_engine_integrator.py` 中添加新的 `_detect_type` 规则。

## 技术细节

### 自动检测流程

```
用户消息
    ↓
关键词匹配
    ↓
问题类型分类
    ↓
调用对应推理引擎
    ↓
返回验证答案
```

### 置信度计算

- 高置信度 (≥80%): 直接返回答案
- 中置信度 (50-80%): 提供推导过程
- 低置信度 (<50%): 建议用户验证
