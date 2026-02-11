#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦞 推理引擎 v5.7 - 极值分析版
Version: 5.7
Date: 2026-02-11
"""

from typing import Dict, List


class ReasoningEngineV5_7:
    """推理引擎 v5.7 - 极值分析版"""
    
    def __init__(self):
        self.version = "5.7"
        self.errors = []
    
    def analyze_extremal(self, grid_rows: int = 100, 
                        max_per_color: int = 10000) -> Dict:
        """
        极值组合问题分析
        
        核心逻辑：
        1. k种颜色，每行恰好k种颜色，每种颜色1个块
        2. 每块大小 = grid_rows/k
        3. 1×t跨越 ceil(t / (grid_rows/k)) = ceil(kt/grid_rows) 个k-块
        4. 要恰好2种颜色，需要 ceil(kt/grid_rows) = 2
        """
        results = []
        max_t_prime = 0
        
        for t in range(2, grid_rows + 1):
            analysis = self._analyze_t(t, grid_rows, max_per_color)
            results.append(analysis)
            
            if analysis["is_feasible"] and t > max_t_prime:
                max_t_prime = t
        
        return {
            "results": results,
            "max_t_prime": max_t_prime,
            "answer": max_t_prime + 1
        }
    
    def _analyze_t(self, t: int, grid_rows: int, 
                   max_per_color: int) -> Dict:
        """分析t是否可行"""
        analysis = {
            "t": t,
            "is_feasible": False,
            "feasible_k": None,
            "reason": ""
        }
        
        # 尝试k=2,3,4,...
        for k in range(2, grid_rows + 1):
            k_result = self._analyze_k(t, k, grid_rows, max_per_color)
            
            if k_result["is_feasible"]:
                analysis["is_feasible"] = True
                analysis["feasible_k"] = k
                analysis["reason"] = k_result["reason"]
                break
        
        if not analysis["is_feasible"]:
            analysis["reason"] = "无满足条件的k值"
        
        return analysis
    
    def _analyze_k(self, t: int, k: int, grid_rows: int,
                   max_per_color: int) -> Dict:
        """分析k是否可行"""
        cells_per_color = (grid_rows * grid_rows) / k
        
        if cells_per_color > max_per_color:
            return {
                "k": k,
                "is_feasible": False,
                "reason": f"每种颜色{cells_per_color:.0f} > {max_per_color}"
            }
        
        # 关键条件：ceil(kt/grid_rows) = 2
        blocks = (k * t + grid_rows - 1) // grid_rows
        
        if blocks != 2:
            return {
                "k": k,
                "is_feasible": False,
                "reason": f"ceil({k}×{t}/{grid_rows})={blocks}≠2"
            }
        
        return {
            "k": k,
            "is_feasible": True,
            "reason": f"ceil({k}×{t}/{grid_rows})=2",
            "cells_per_color": cells_per_color,
            "block_size": grid_rows / k
        }
    
    def verify_with_user_answer(self, user_answer: int) -> Dict:
        """用标准答案验证"""
        result = self.analyze_extremal()
        
        return {
            "computed": result["answer"],
            "user": user_answer,
            "is_correct": result["answer"] == user_answer,
            "analysis": result
        }


def demo():
    print("="*70)
    print("🦞 推理引擎 v5.7 - 演示")
    print("="*70)
    
    engine = ReasoningEngineV5_7()
    
    # 分析
    result = engine.analyze_extremal(100, 10000)
    
    print("\n分析结果：")
    print("-"*70)
    print(f"100的约数: 2, 4, 5, 10, 20, 25, 50, 100")
    print("条件: ceil(kt/100) = 2")
    print()
    
    # 显示关键结果
    key_t_values = [2, 10, 11, 12, 20, 25, 50, 100]
    for t in key_t_values:
        if t <= len(result["results"]):
            r = result["results"][t-1]
            status = "✅" if r["is_feasible"] else "❌"
            print(f"t={t}: {status}")
    
    print()
    print("="*70)
    print(f"计算答案: {result['answer']}")
    print("="*70)
    
    # 验证
    print("\n【用标准答案12验证】")
    v = engine.verify_with_user_answer(12)
    print(f"计算答案: {v['computed']}")
    print(f"标准答案: {v['user']}")
    print(f"是否正确: {'✅' if v['is_correct'] else '❌'}")


if __name__ == "__main__":
    demo()
