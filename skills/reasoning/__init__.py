# -*- coding: utf-8 -*-
"""
推理引擎技能
自动集成到所有会话

Usage:
    from skills.reasoning import solve
    
    answer = solve("你的数学问题")
"""

import sys
import os

# 添加workspace到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 自动导入推理引擎集成器
try:
    from reasoning_engine_integrator import ReasoningIntegrator, solve
    print("✅ 推理引擎已加载 v5.9")
except ImportError as e:
    print(f"⚠️ 推理引擎加载失败: {e}")
    solve = None
