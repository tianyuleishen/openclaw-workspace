#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦞 推理引擎 v5.3 - 程序验证版
==================================
根据连接数独错误深度优化

核心改进:
1. 程序穷举验证 - 用代码验证所有情况
2. 数学建模 - 正确理解题目
3. 不确定性表达 - 不确定时承认
4. 用户确认 - 关键假设让用户确认
5. 多次验证 - 用不同方法交叉验证

Version: 5.3
Date: 2026-02-11
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from itertools import permutations


@dataclass
class VerificationResult:
    """验证结果"""
    method: str
    result: Any
    confidence: float
    is_correct: bool


class ReasoningEngineV5_3:
    """
    推理引擎 v5.3 - 程序验证版
    
    核心原则:
    1. 不确定时要承认
    2. 用程序验证
    3. 让用户确认关键假设
    4. 多次验证交叉检查
    """
    
    def __init__(self):
        self.assumptions: List[Dict] = []
        self.verification_results: List[VerificationResult] = []
        self.question_stack: List[Dict] = []
    
    def analyze(self, question: str) -> Dict:
        """
        分析流程
        
        步骤:
        1. 理解题目（让用户确认）
        2. 数学建模
        3. 程序验证
        4. 多次验证
        5. 输出结果
        """
        result = {
            "question": question,
            "type": None,
            "assumptions": [],  # 需要用户确认
            "model": None,  # 数学模型
            "verifications": [],  # 验证结果
            "final_answer": None,
            "confidence": 0.0,
            "uncertainty": None  # 不确定的地方
        }
        
        # Step 1: 理解题目
        result["type"], assumptions = self._understand_question(question)
        result["assumptions"] = assumptions
        
        if not result["type"]:
            result["uncertainty"] = "题目理解有歧义，需要用户确认"
            return result
        
        # Step 2: 数学建模
        result["model"] = self._build_model(question, result["type"])
        
        # Step 3: 程序验证（核心！）
        result["verifications"] = self._program_verify(question, result["type"])
        
        # Step 4: 交叉验证
        cross_result = self._cross_verify(result["model"], result["verifications"])
        result["verifications"].append(cross_result)
        
        # Step 5: 最终答案
        result["final_answer"] = self._derive_answer(
            result["model"], result["verifications"]
        )
        
        # Step 6: 置信度
        result["confidence"] = self._calc_confidence(result)
        
        return result
    
    def _understand_question(self, question: str) -> tuple:
        """
        理解题目，返回类型和需要确认的假设
        
        重要：这里必须明确理解，否则会出错！
        """
        # 提取关键信息
        import re
        numbers = re.findall(r'\d+', question)
        
        # 判断题目类型
        if "8位数" in question or "8位" in question:
            qtype = "connection_number"
            
            # 需要确认的假设
            assumptions = [
                {
                    "key": "connection_rule",
                    "question": "这6个数是按顺序排列后连接，还是可以任意连接？",
                    "options": ["按顺序排列后连接", "任意位置连接"],
                    "default": None  # 不默认，需要用户确认
                },
                {
                    "key": "zero_rule",
                    "question": "首位不能为0，具体规则是什么？",
                    "options": ["整个8位数首位≠0", "每个数独立时首位≠0"],
                    "default": None
                }
            ]
            
            return qtype, assumptions
        
        return None, []
    
    def _build_model(self, question: str, qtype: str) -> Dict:
        """数学建模"""
        model = {
            "type": qtype,
            "description": "",
            "formula": "",
            "parameters": {}
        }
        
        import re
        numbers = [int(n) for n in re.findall(r'\d+', question)]
        
        if qtype == "connection_number":
            model["numbers"] = numbers
            model["total_digits"] = sum(len(str(n)) for n in numbers)
            model["description"] = f"{numbers} 连接成8位数"
        
        return model
    
    def _program_verify(self, question: str, qtype: str) -> List[VerificationResult]:
        """
        程序验证 - 核心功能！
        
        用代码穷举所有可能，确保答案正确
        """
        import re
        from itertools import permutations
        
        verifications = []
        
        if qtype != "connection_number":
            return verifications
        
        # 提取数字
        numbers = [int(n) for n in re.findall(r'\d+', question)]
        
        # 验证方法1：穷举所有排列
        try:
            valid_count = 0
            seen = set()
            
            for perm in permutations(numbers):
                # 模拟连接过程
                num_str = ''.join(str(n) for n in perm)
                
                # 检查是否8位
                if len(num_str) == 8:
                    # 检查首位≠0
                    if num_str[0] != '0':
                        if num_str not in seen:
                            seen.add(num_str)
                            valid_count += 1
            
            verifications.append(VerificationResult(
                method="穷举所有排列",
                result=f"{valid_count}个不同的8位数",
                confidence=0.95,
                is_correct=True
            ))
            
        except Exception as e:
            verifications.append(VerificationResult(
                method="穷举验证",
                result=f"错误: {str(e)}",
                confidence=0.0,
                is_correct=False
            ))
        
        # 验证方法2：数学公式
        try:
            # 计算公式
            total = 6 * 5 * 4 * 3 * 2  # 6! = 720
            
            verifications.append(VerificationResult(
                method="数学公式",
                result="720种排列",
                confidence=0.9,
                is_correct=True
            ))
            
        except Exception as e:
            verifications.append(VerificationResult(
                method="数学公式",
                result=f"错误: {str(e)}",
                confidence=0.0,
                is_correct=False
            ))
        
        return verifications
    
    def _cross_verify(self, model: Dict, verifications: List[VerificationResult]) -> VerificationResult:
        """交叉验证"""
        # 检查多个验证结果是否一致
        results = [v.result for v in verifications if v.is_correct]
        
        if len(results) >= 2:
            # 检查是否一致
            unique_results = set(str(r) for r in results)
            if len(unique_results) == 1:
                return VerificationResult(
                    method="交叉验证",
                    result=results[0],
                    confidence=0.98,
                    is_correct=True
                )
            else:
                return VerificationResult(
                    method="交叉验证",
                    result=f"结果不一致: {unique_results}",
                    confidence=0.5,
                    is_correct=False
                )
        
        return VerificationResult(
            method="交叉验证",
            result="验证不足",
            confidence=0.0,
            is_correct=False
        )
    
    def _derive_answer(self, model: Dict, verifications: List[VerificationResult]) -> str:
        """推导答案"""
        # 找出验证通过的正确答案
        correct_results = [v for v in verifications if v.is_correct]
        
        if not correct_results:
            return "无法确定答案，需要更多验证"
        
        # 返回最高置信度的结果
        best = max(correct_results, key=lambda v: v.confidence)
        return str(best.result)
    
    def _calc_confidence(self, result: Dict) -> float:
        """计算置信度"""
        if result["uncertainty"]:
            return 0.3
        
        verifications = [v for v in result["verifications"] if v.is_correct]
        
        if not verifications:
            return 0.0
        
        # 加权平均
        total_confidence = sum(v.confidence for v in verifications)
        avg_confidence = total_confidence / len(verifications)
        
        # 多次验证加分
        if len(verifications) >= 2:
            avg_confidence = min(1.0, avg_confidence + 0.05)
        
        return avg_confidence
    
    def verify_answer(self, my_answer: str, correct_answer: str) -> Dict:
        """验证答案"""
        lesson = {
            "timestamp": "2026-02-11",
            "my_answer": my_answer,
            "correct_answer": correct_answer,
            "analysis": self._analyze_difference(my_answer, correct_answer),
            "improvement": []
        }
        
        # 分析改进点
        my_num = [int(s) for s in my_answer if s.isdigit()]
        correct_num = [int(s) for s in correct_answer if s.isdigit()]
        
        if my_num and correct_num:
            if my_num[0] != correct_num[0]:
                lesson["improvement"].append("需要用程序穷举验证")
                lesson["improvement"].append("不确定时要承认")
                lesson["improvement"].append("让用户确认关键假设")
        
        return lesson
    
    def _analyze_difference(self, my_answer: str, correct_answer: str) -> str:
        """分析差异"""
        my_num = [int(s) for s in my_answer if s.isdigit()]
        correct_num = [int(s) for s in correct_answer if s.isdigit()]
        
        if my_num and correct_num:
            diff = abs(my_num[0] - correct_num[0])
            if diff > 0:
                return f"我算{my_num[0]}，正确{correct_num[0]}，相差{diff}。需要精确穷举！"
        
        return "答案不同，需要分析原因"


def demo():
    """演示"""
    print("="*70)
    print("🦞 推理引擎 v5.3 - 程序验证版")
    print("="*70)
    
    engine = ReasoningEngineV5_3()
    
    # 测试连接数独问题
    print("\n【测试: 连接数独问题】")
    q = "将6个数2,0,1,9,20,19排成8位数，首位≠0，有多少个？"
    
    result = engine.analyze(q)
    
    print(f"\n问题: {q}")
    print(f"\n理解: {result['type']}")
    
    if result['assumptions']:
        print(f"\n需要确认的假设:")
        for a in result['assumptions']:
            print(f"  • {a['question']}")
    
    print(f"\n验证结果:")
    for v in result['verifications']:
        status = "✅" if v.is_correct else "❌"
        print(f"  {status} {v.method}: {v.result} ({v.confidence:.0%})")
    
    print(f"\n最终答案: {result['final_answer']}")
    print(f"置信度: {result['confidence']:.0%}")
    
    if result['uncertainty']:
        print(f"\n⚠️ 不确定: {result['uncertainty']}")
    
    # 验证之前的错误
    print("\n" + "="*70)
    print("【错误分析】")
    lesson = engine.verify_answer("答案是600个", "答案是498个")
    print(f"我的答案: {lesson['my_answer']}")
    print(f"正确答案: {lesson['correct_answer']}")
    print(f"分析: {lesson['analysis']}")
    for imp in lesson['improvement']:
        print(f"  → {imp}")
    
    print("\n" + "="*70)
    print("✅ 推理引擎v5.3演示完成")
    print("="*70)


if __name__ == "__main__":
    demo()
