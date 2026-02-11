#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦞 推理引擎 v5.6 - 逻辑推理版
==================================
根据密码破解问题深度优化

核心改进:
1. 约束求解 - 处理逻辑推理问题
2. 暴力验证 - 穷举所有可能
3. 多步推理 - 分解复杂问题
4. 唯一解验证 - 确保唯一性

Version: 5.6
Date: 2026-02-11
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from itertools import combinations, permutations


@dataclass
class Constraint:
    """约束条件"""
    name: str
    description: str
    function: str


class ReasoningEngineV5_6:
    """
    推理引擎 v5.6 - 逻辑推理版
    
    核心原则:
    1. 约束建模 - 将问题转化为约束
    2. 穷举验证 - 搜索所有可能
    3. 多步分解 - 分解复杂问题
    4. 唯一性保证 - 确保唯一解
    """
    
    def __init__(self):
        self.version = "5.6"
        self.solutions = []
        self.constraints = []
    
    def solve_password(self, problem: Dict) -> Dict:
        """
        密码破解问题求解
        
        输入:
        - guesses: 4个猜测列表
        - rules: 规则描述
        """
        result = {
            "status": "pending",
            "problem": problem,
            "constraints": [],
            "solutions": [],
            "answer": None,
            "confidence": 0.0
        }
        
        guesses = problem["guesses"]
        
        # Step 1: 建立约束
        constraints = self._build_constraints(guesses)
        result["constraints"] = constraints
        
        # Step 2: 约束求解
        solutions = self._constraint_solve(guesses)
        result["solutions"] = solutions
        
        # Step 3: 验证唯一性
        if len(solutions) == 1:
            result["status"] = "verified"
            result["answer"] = solutions[0]
            result["confidence"] = 0.99
        elif len(solutions) == 0:
            result["status"] = "error"
            result["confidence"] = 0.0
        else:
            result["status"] = "multiple"
            result["solutions"] = solutions[:10]  # 显示前10个
            result["confidence"] = 0.5
        
        return result
    
    def _build_constraints(self, guesses: List[List[int]]) -> List[Constraint]:
        """建立约束"""
        constraints = []
        
        # 约束1: 密码是7个不同数字
        constraints.append(Constraint(
            "all_different",
            "7个数字各不相同",
            "len(set(password)) == 7"
        ))
        
        # 约束2: 每人的猜测恰好2个正确
        constraints.append(Constraint(
            "exactly_two_correct",
            "每人恰好猜对2个",
            "len(correct_positions) == 2"
        ))
        
        # 约束3: 正确的位置不相邻
        constraints.append(Constraint(
            "not_adjacent",
            "正确位置不相邻",
            "|positions[i+1] - positions[i]| != 1"
        ))
        
        return constraints
    
    def _constraint_solve(self, guesses: List[List[int]]) -> List[str]:
        """
        约束求解
        
        策略:
        1. 从0-9中选择7个不同数字
        2. 全排列验证
        3. 筛选满足所有约束的解
        """
        all_nums = list(range(10))
        solutions = []
        
        def check_solution(password):
            """检查密码是否满足所有约束"""
            for guess in guesses:
                correct = [i for i in range(7) if guess[i] == password[i]]
                
                # 约束: 恰好2个正确
                if len(correct) != 2:
                    return False
                
                # 约束: 不相邻
                for i in range(len(correct) - 1):
                    if correct[i+1] - correct[i] == 1:
                        return False
            
            return True
        
        # 枚举排除的3个数字
        for excluded in combinations(all_nums, 3):
            remaining = [n for n in all_nums if n not in excluded]
            
            for perm in permutations(remaining, 7):
                if check_solution(list(perm)):
                    solutions.append(''.join(map(str, perm)))
        
        return solutions
    
    def verify_solution(self, solution: str, problem: Dict) -> Dict:
        """验证解"""
        guesses = problem["guesses"]
        password = [int(c) for c in solution]
        
        result = {
            "solution": solution,
            "checks": [],
            "is_valid": True
        }
        
        for i, guess in enumerate(guesses):
            correct = [j for j in range(7) if guess[j] == password[j]]
            
            check = {
                "guess": f"Guess #{i+1}",
                "correct": correct,
                "count_ok": len(correct) == 2,
                "adjacent_ok": all(
                    correct[j+1] - correct[j] != 1 
                    for j in range(len(correct)-1)
                ) if len(correct) == 2 else False
            }
            
            result["checks"].append(check)
            
            if not (check["count_ok"] and check["adjacent_ok"]):
                result["is_valid"] = False
        
        return result
    
    def analyze(self, problem: str) -> Dict:
        """分析问题"""
        # 解析问题描述
        # 这里简化处理
        
        return {
            "type": "logical_reasoning",
            "status": "pending",
            "message": "需要指定guesses列表"
        }


def demo():
    """演示"""
    print("="*70)
    print("🦞 推理引擎 v5.6 - 演示")
    print("="*70)
    
    engine = ReasoningEngineV5_6()
    
    # 密码破解问题
    problem = {
        "guesses": [
            [9, 0, 6, 2, 4, 3, 7],  # Guess #1
            [8, 5, 9, 3, 6, 2, 4],  # Guess #2
            [4, 2, 8, 6, 9, 1, 5],  # Guess #3
            [3, 4, 5, 0, 9, 8, 2],  # Guess #4
        ],
        "rule": "每人猜对位置不相邻的两个数字"
    }
    
    print("\n问题：密码破解")
    print(f"规则: {problem['rule']}")
    
    # 求解
    print("\n约束求解中...")
    result = engine.solve_password(problem)
    
    print(f"\n找到 {len(result['solutions'])} 个解")
    
    if result['solutions']:
        print(f"\n解: {result['solutions']}")
        
        # 验证
        print("\n验证：")
        verify = engine.verify_solution(result['solutions'][0], problem)
        
        for check in verify['checks']:
            print(f"  {check['guess']}: {check['correct']} "
                  f"✓" if check['count_ok'] and check['adjacent_ok'] else "✗")
        
        print(f"\n状态: {'✅ 有效' if verify['is_valid'] else '❌ 无效'}")
    
    print("\n" + "="*70)
    print("✅ 推理引擎v5.6演示完成")
    print("="*70)


if __name__ == "__main__":
    demo()
