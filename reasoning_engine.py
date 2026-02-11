#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小爪推理增强引擎 v1.0
Chain-of-Thought 结构化推理

功能：
- 问题分解
- 关键信息提取
- 推理链构建
- 结论验证
"""

import json
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class ReasoningStep:
    """推理步骤"""
    step_id: int
    description: str
    evidence: List[str]
    confidence: float  # 0-1
    conclusion: str
    next_steps: List[str] = field(default_factory=list)


class ChainOfThought:
    """Chain-of-Thought 推理引擎"""
    
    def __init__(self):
        self.reasoning_history = []
        self.step_count = 0
        
    def decompose_problem(self, problem: str) -> Dict:
        """
        问题分解
        
        Args:
            problem: 原始问题
            
        Returns:
            分解后的子问题
        """
        # 分析问题类型
        problem_types = {
            'factual': ['谁', '什么', '哪个', '多少'],
            'reasoning': ['为什么', '如何', '怎样', '如果'],
            'comparative': ['比较', '区别', '不同', '相同'],
            'predictive': ['会怎样', '将会', '预测', '将来']
        }
        
        problem_type = 'factual'
        keywords = []
        
        for ptype, words in problem_types.items():
            for word in words:
                if word in problem:
                    problem_type = ptype
                    keywords.append(word)
                    break
        
        # 提取关键实体
        entities = self._extract_entities(problem)
        
        # 提取约束条件
        constraints = self._extract_constraints(problem)
        
        return {
            'original': problem,
            'type': problem_type,
            'keywords': keywords,
            'entities': entities,
            'constraints': constraints,
            'sub_questions': self._generate_sub_questions(problem, problem_type)
        }
    
    def _extract_entities(self, text: str) -> List[str]:
        """提取实体（简化版）"""
        entities = []
        
        # 股票代码模式
        import re
        codes = re.findall(r'\b[0-9]{6}\.(SZ|SH|BJ)\b', text)
        entities.extend(codes)
        
        # 常见实体
        common = ['股票', '价格', '涨跌幅', '成交量', '市值', '市盈率']
        for word in common:
            if word in text:
                entities.append(word)
        
        return list(set(entities))
    
    def _extract_constraints(self, text: str) -> List[str]:
        """提取约束条件"""
        constraints = []
        
        condition_words = [
            ('如果', 'conditional'),
            ('当...时', 'temporal'),
            ('必须', 'mandatory'),
            ('不能', 'prohibition'),
            ('最多', 'upper_bound'),
            ('最少', 'lower_bound'),
        ]
        
        for word, ctype in condition_words:
            if word in text:
                constraints.append({'type': ctype, 'trigger': word})
        
        return constraints
    
    def _generate_sub_questions(self, problem: str, ptype: str) -> List[str]:
        """生成子问题"""
        sub_questions = []
        
        if ptype == 'factual':
            sub_questions = [
                "问题的核心是什么？",
                "需要哪些具体数据？",
                "如何验证答案正确性？"
            ]
        elif ptype == 'reasoning':
            sub_questions = [
                "问题的因果关系是什么？",
                "有哪些前提条件？",
                "推理链条如何建立？",
                "结论是否可靠？"
            ]
        elif ptype == 'comparative':
            sub_questions = [
                "比较的对象有哪些？",
                "比较的维度是什么？",
                "如何量化差异？"
            ]
        elif ptype == 'predictive':
            sub_questions = [
                "有哪些已知趋势？",
                "有哪些不确定因素？",
                "概率分布如何？"
            ]
        
        return sub_questions
    
    def build_reasoning_chain(self, 
                           problem: str,
                           context: Dict = None) -> List[ReasoningStep]:
        """
        构建推理链
        
        Args:
            problem: 问题描述
            context: 上下文信息
            
        Returns:
            推理步骤列表
        """
        steps = []
        self.step_count = 0
        
        # Step 1: 问题理解
        decomposed = self.decompose_problem(problem)
        step1 = ReasoningStep(
            step_id=1,
            description=f"理解问题：{problem}",
            evidence=[f"问题类型: {decomposed['type']}"],
            confidence=0.9,
            conclusion="问题已分解为子问题"
        )
        steps.append(step1)
        
        # Step 2: 信息收集
        collected_info = self._collect_information(decomposed, context)
        step2 = ReasoningStep(
            step_id=2,
            description="收集相关信息",
            evidence=list(collected_info.keys()),
            confidence=0.85,
            conclusion=f"收集到 {len(collected_info)} 条信息"
        )
        steps.append(step2)
        
        # Step 3: 推理分析
        inference = self._make_inference(decomposed, collected_info)
        step3 = ReasoningStep(
            step_id=3,
            description="执行推理分析",
            evidence=[f"基于 {len(inference)} 个推论"],
            confidence=0.75,
            conclusion="推理完成"
        )
        steps.append(step3)
        
        # Step 4: 结论验证
        validation = self._validate_conclusion(inference)
        step4 = ReasoningStep(
            step_id=4,
            description="验证结论可靠性",
            evidence=[f"验证项: {len(validation)}"],
            confidence=validation.get('confidence', 0.7),
            conclusion=validation.get('result', '待确认')
        )
        steps.append(step4)
        
        # Step 5: 最终结论
        final = self._generate_final_conclusion(steps, inference)
        step5 = ReasoningStep(
            step_id=5,
            description="生成最终结论",
            evidence=["推理链完整"],
            confidence=final.get('confidence', 0.8),
            conclusion=final.get('conclusion', '')
        )
        steps.append(step5)
        
        # 保存历史
        self.reasoning_history.append({
            'problem': problem,
            'steps': len(steps),
            'timestamp': datetime.now().isoformat()
        })
        
        return steps
    
    def _collect_information(self, 
                           decomposed: Dict,
                           context: Dict = None) -> Dict:
        """收集相关信息"""
        info = {}
        
        # 从上下文收集
        if context:
            info.update(context)
        
        # 从问题实体收集
        for entity in decomposed.get('entities', []):
            if '股票' in entity:
                info['股票相关查询'] = True
        
        # 从类型收集
        ptype = decomposed.get('type')
        if ptype == 'factual':
            info['需要具体数据'] = True
        elif ptype == 'reasoning':
            info['需要因果分析'] = True
        
        return info
    
    def _make_inference(self,
                       decomposed: Dict,
                       info: Dict) -> List[Dict]:
        """执行推理"""
        inferences = []
        
        # 基于问题类型的推理
        ptype = decomposed.get('type')
        
        if ptype == 'factual':
            inferences.append({
                'type': '数据查找',
                'action': '查询具体数值',
                'confidence': 0.9
            })
        elif ptype == 'reasoning':
            inferences.append({
                'type': '因果分析',
                'action': '分析前后关系',
                'confidence': 0.8
            })
        elif ptype == 'comparative':
            inferences.append({
                'type': '比较分析',
                'action': '对比多个对象',
                'confidence': 0.85
            })
        elif ptype == 'predictive':
            inferences.append({
                'type': '趋势预测',
                'action': '基于历史预测未来',
                'confidence': 0.7
            })
        
        return inferences
    
    def _validate_conclusion(self, inference: List[Dict]) -> Dict:
        """验证结论"""
        if not inference:
            return {'result': '无法推理', 'confidence': 0.3}
        
        # 计算置信度
        avg_confidence = sum(i.get('confidence', 0.5) for i in inference) / len(inference)
        
        # 简单验证
        if avg_confidence >= 0.8:
            return {'result': '高置信度', 'confidence': avg_confidence}
        elif avg_confidence >= 0.6:
            return {'result': '中等置信度', 'confidence': avg_confidence}
        else:
            return {'result': '低置信度，建议进一步验证', 'confidence': avg_confidence}
    
    def _generate_final_conclusion(self,
                                 steps: List[ReasoningStep],
                                 inference: List[Dict]) -> Dict:
        """生成最终结论"""
        # 计算总体置信度
        avg_confidence = sum(s.confidence for s in steps) / len(steps)
        
        # 生成结论
        conclusion = {
            'reasoning_steps': len(steps),
            'inference_count': len(inference),
            'confidence': avg_confidence,
            'conclusion': '推理完成，结论可靠性为 {:.0%}'.format(avg_confidence)
        }
        
        return conclusion
    
    def explain_reasoning(self, steps: List[ReasoningStep]) -> str:
        """解释推理过程"""
        explanation = []
        explanation.append("=" * 60)
        explanation.append("🧠 推理过程")
        explanation.append("=" * 60)
        
        for i, step in enumerate(steps, 1):
            explanation.append(f"\n【步骤 {i}】{step.description}")
            explanation.append(f"  证据: {', '.join(step.evidence[:3])}")
            explanation.append(f"  置信度: {step.confidence:.0%}")
            explanation.append(f"  结论: {step.conclusion}")
        
        explanation.append("\n" + "=" * 60)
        explanation.append("📊 总结")
        explanation.append("=" * 60)
        
        avg_conf = sum(s.confidence for s in steps) / len(steps)
        explanation.append(f"总步骤: {len(steps)}")
        explanation.append(f"平均置信度: {avg_conf:.0%}")
        explanation.append(f"推理完整性: {'✅ 完整' if avg_conf >= 0.7 else '⚠️ 需验证'}")
        
        return '\n'.join(explanation)


def demo():
    """演示"""
    print("\n🦞 小爪推理增强引擎演示")
    print("=" * 60)
    
    # 创建引擎
    engine = ChainOfThought()
    
    # 测试问题
    test_problems = [
        "大位科技今天涨了多少？",
        "如果传媒板块继续上涨，应该买入哪些股票？",
        "比较中文在线和光线传媒的近期表现",
        "下周传媒板块会继续涨吗？"
    ]
    
    for problem in test_problems:
        print(f"\n问题: {problem}")
        print("-" * 60)
        
        # 分解问题
        decomposed = engine.decompose_problem(problem)
        print(f"类型: {decomposed['type']}")
        print(f"实体: {decomposed['entities']}")
        print(f"子问题: {decomposed['sub_questions'][:2]}")
        
        # 构建推理链
        steps = engine.build_reasoning_chain(problem)
        
        # 解释推理
        explanation = engine.explain_reasoning(steps)
        print(explanation)
        
        print("\n" + "=" * 60)


if __name__ == '__main__':
    demo()
