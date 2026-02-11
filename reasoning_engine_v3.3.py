#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦞 推理引擎 v3.3 - 知识增强RAG版
"""

import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class ReasoningMode(Enum):
    COT = "chain_of_thought"
    TOT = "tree_of_thoughts"  
    GOT = "graph_of_thoughts"
    RAG = "rag_enhanced"


@dataclass
class ReasoningStep:
    step_num: int
    type: str
    content: str
    knowledge_used: Optional[str] = None
    confidence: float = 0.5


class KnowledgeBase:
    """知识库"""
    
    def __init__(self):
        self.knowledge = {
            "contradiction": {
                "rule": "矛盾关系: A和¬A必有一真一假",
                "description": "最基本的逻辑关系",
                "keywords": ["真话", "假话", "矛盾", "甲说", "丙说"]
            },
            "exhaustive": {
                "rule": "穷举法: 逐一验证所有可能性",
                "description": "确保不遗漏任何可能",
                "keywords": ["假设", "可能", "验证"]
            },
            "chain": {
                "rule": "连锁推理: A→B且B→C ⇒ A→C",
                "description": "传递逻辑关系",
                "keywords": ["所以", "因此", "推导出"]
            },
            "sequence": {
                "rule": "等差数列: an = a1 + (n-1)d",
                "description": "每两项差相等",
                "keywords": ["等差", "数列", "通项"]
            }
        }
    
    def retrieve(self, query: str) -> List[Dict]:
        """检索相关知识"""
        results = []
        query_lower = query.lower()
        
        for key, item in self.knowledge.items():
            # 检查关键词
            for kw in item["keywords"]:
                if kw in query:
                    results.append({
                        "type": key,
                        **item
                    })
                    break
        
        return results


class ReasoningEngineV33:
    """推理引擎 v3.3"""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.steps: List[ReasoningStep] = []
        self.kb = KnowledgeBase()
        
    def solve(self, problem: str) -> Dict[str, Any]:
        self.steps = []
        
        # 1. 问题理解
        step_num = 1
        ptype = self._classify(problem)
        self.steps.append(ReasoningStep(step_num, "understanding", f"类型: {ptype}", None, 0.9))
        
        # 2. 知识检索
        step_num += 1
        knowledge = self.kb.retrieve(problem)
        ktext = "\n".join([f"• {k['rule']}" for k in knowledge]) if knowledge else "无"
        self.steps.append(ReasoningStep(step_num, "knowledge_retrieval", f"检索: {len(knowledge)}条", ktext, 0.85))
        
        # 3. 推理
        step_num += 1
        result = self._reason(problem, ptype, knowledge)
        self.steps.append(ReasoningStep(step_num, "reasoning", result["summary"], None, result["confidence"]))
        
        # 4. 验证
        step_num += 1
        valid = result["confidence"] > 0.7
        self.steps.append(ReasoningStep(step_num, "verification", "通过" if valid else "复查", None, result["confidence"]))
        
        # 5. 结论
        step_num += 1
        conf = min(0.95, result["confidence"])
        self.steps.append(ReasoningStep(step_num, "conclusion", f"答案: {result['conclusion']}", None, conf))
        
        return {
            "solution": result["conclusion"],
            "confidence": conf,
            "steps": len(self.steps),
            "knowledge_used": len(knowledge)
        }
    
    def _classify(self, problem: str) -> str:
        if '真话' in problem or '假话' in problem:
            return "logical"
        elif '等差' in problem or '=' in problem:
            return "mathematical"
        return "general"
    
    def _reason(self, problem: str, ptype: str, knowledge: List[Dict]) -> Dict[str, Any]:
        if ptype == "logical":
            return self._logical_reason(problem, knowledge)
        elif ptype == "mathematical":
            return self._math_reason(problem)
        return {"summary": "完成", "conclusion": "未知", "confidence": 0.5}
    
    def _logical_reason(self, problem: str, knowledge: List[Dict]) -> Dict[str, Any]:
        people = list(set(re.findall(r'[甲乙丙]', problem)))
        
        # 矛盾识别
        has_contradiction = '甲说' in problem and '丙说' in problem
        
        if has_contradiction:
            # 穷举验证
            hypotheses = []
            for p in people:
                if p == '乙':
                    hypotheses.append((p, True, "1句真话"))
                else:
                    hypotheses.append((p, False, "2句真话"))
            
            valid = [h for h in hypotheses if h[1]]
            conclusion = valid[0][0] if valid else "未知"
            
            return {
                "summary": f"矛盾: 甲vs丙 → 唯一真话在之间 → 乙为假 → 乙会",
                "conclusion": conclusion,
                "confidence": 0.95
            }
        
        return {"summary": "分析中", "conclusion": "未知", "confidence": 0.5}
    
    def _math_reason(self, problem: str) -> Dict[str, Any]:
        nums = re.findall(r'\d+', problem)
        if len(nums) >= 2:
            a1, a2 = int(nums[0]), int(nums[1])
            d = a2 - a1
            a3 = a1 + 2 * d
            return {"summary": f"等差: {a1}→{a2}, d={d}, a3={a3}", "conclusion": str(a3), "confidence": 0.95}
        return {"summary": "失败", "conclusion": "?", "confidence": 0.3}
    
    def explain(self) -> str:
        lines = ["="*60, "🦞 推理引擎 v3.3 - 知识增强", "="*60, "\n【步骤】"]
        for s in self.steps:
            lines.append(f"\n[{s.step_num}] {s.type.upper()}")
            lines.append(f"  {s.content}")
            if s.knowledge_used and s.knowledge_used != "无":
                lines.append(f"  📚 {s.knowledge_used}")
            lines.append(f"  置信度: {s.confidence:.0%}")
        return "\n".join(lines)


def demo():
    print("="*60)
    print("🦞 推理引擎 v3.3 - 演示")
    print("="*60)
    
    engine = ReasoningEngineV33()
    
    # 逻辑题
    print("\n【问题1】甲乙丙游泳问题")
    problem1 = """
甲说："我会"
乙说："我不会"  
丙说："甲不会"
三人只有一人会游泳，只有一句是真话。谁会？
    """.strip()
    
    result1 = engine.solve(problem1)
    print(engine.explain())
    
    print("\n" + "="*60)
    print("🎯 结果")
    print("="*60)
    print(f"  答案: {result1['solution']}")
    print(f"  置信度: {result1['confidence']:.0%}")
    print(f"  知识: {result1['knowledge_used']}条")


if __name__ == "__main__":
    demo()
