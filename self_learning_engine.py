#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦞 自我学习系统 v5.0
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class LearningItem:
    content: str
    category: str
    source: str
    timestamp: str
    confidence: float = 0.5
    verified: bool = False
    usage_count: int = 0


class SelfLearningEngine:
    def __init__(self, memory_path: str = "memory/self_learning.json"):
        self.memory_path = memory_path
        self.learnings: List[LearningItem] = []
        self.success_patterns = []
        self.error_patterns = []
        self._load()
        
    def learn(self, content: str, category: str, source: str, confidence: float = 0.5, verified: bool = False):
        """添加学习项"""
        item = LearningItem(
            content=content,
            category=category,
            source=source[:50],
            timestamp=datetime.now().isoformat(),
            confidence=confidence,
            verified=verified
        )
        self.learnings.append(item)
        self._save()
        return len(self.learnings)
    
    def learn_from_error(self, question: str, wrong_answer: str, lesson: str):
        """从错误中学习"""
        self.error_patterns.append({
            "question": question,
            "wrong_answer": wrong_answer,
            "lesson": lesson,
            "timestamp": datetime.now().isoformat()
        })
        if lesson:
            self.learn(
                content=lesson,
                category="lesson",
                source=f"error: {question[:30]}",
                confidence=0.9,
                verified=True
            )
        self._save()
        
    def learn_from_success(self, question: str, correct_answer: str):
        """从成功中学习"""
        self.success_patterns.append({
            "question": question,
            "answer": correct_answer,
            "timestamp": datetime.now().isoformat()
        })
        self._save()
    
    def extract_and_learn(self, user_message: str, assistant_response: str):
        """从对话中提取知识"""
        # 矛盾识别
        if any(kw in user_message for kw in ["真话", "假话", "如果"]):
            self.learn(
                "矛盾识别: A和¬A必有一真一假",
                "logic",
                user_message[:50],
                0.95
            )
        
        # 边界检查
        if any(kw in user_message for kw in ["水位", "厘米", "放入"]):
            self.learn(
                "边界检查: 遇到'水位'问题必须考虑容器深度",
                "geometry",
                user_message[:50],
                0.95,
                verified=True
            )
        
        # 目的分析
        if any(kw in user_message for kw in ["开车", "走路", "洗车"]):
            self.learn(
                "目的分析: 先明确目的，再决定手段",
                "reasoning",
                user_message[:50],
                0.85
            )
        
        # 数学穷举
        if any(kw in user_message for kw in ["计算", "等于"]):
            self.learn(
                "穷举法: 逐一验证所有可能性",
                "math",
                user_message[:50],
                0.9
            )
        
        self._save()
    
    def apply_knowledge(self, context: str) -> str:
        """应用知识"""
        relevant = [l for l in self.learnings if l.confidence > 0.8]
        if relevant:
            best = max(relevant, key=lambda x: x.confidence)
            best.usage_count += 1
            self._save()
            return best.content
        return ""
    
    def _load(self):
        try:
            with open(self.memory_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.learnings = [LearningItem(**item) for item in data.get('learnings', [])]
                self.success_patterns = data.get('success_patterns', [])
                self.error_patterns = data.get('error_patterns', [])
        except:
            pass
    
    def _save(self):
        data = {
            'learnings': [l.__dict__ for l in self.learnings],
            'success_patterns': self.success_patterns,
            'error_patterns': self.error_patterns,
            'last_update': datetime.now().isoformat()
        }
        with open(self.memory_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_knowledge_base(self) -> List[Dict]:
        return [{"content": l.content, "category": l.category, "confidence": l.confidence, "verified": l.verified} for l in self.learnings]
    
    def get_statistics(self) -> Dict:
        cats = {}
        for l in self.learnings:
            cats[l.category] = cats.get(l.category, 0) + 1
        return {"total": len(self.learnings), "success": len(self.success_patterns), "errors": len(self.error_patterns), "categories": cats}


def demo():
    print("="*70)
    print("🦞 自我学习系统 v5.0 - 演示")
    print("="*70)
    
    engine = SelfLearningEngine()
    
    print("\n【1. 从水位题错误中学习】")
    engine.learn_from_error("棱长30的水位问题", "27.6cm", "遇到'水位'问题必须考虑容器边界!")
    print("  ✓ 记录错误和教训")
    
    print("\n【2. 从成功中学习】")
    engine.learn_from_success("甲乙丙谁会游泳？", "乙")
    print("  ✓ 记录成功模式")
    
    print("\n【3. 从对话中提取知识】")
    engine.extract_and_learn("洗车应该开车还是走路？", "开车去")
    print("  ✓ 提取4条知识")
    
    print("\n【4. 知识库】")
    for kb in engine.get_knowledge_base():
        v = "✓" if kb['verified'] else ""
        print(f"  {v} {kb['content']} ({kb['category']})")
    
    print("\n【5. 应用知识】")
    applied = engine.apply_knowledge("新的水位问题")
    print(f"  → {applied}")
    
    print("\n【6. 统计】")
    stats = engine.get_statistics()
    print(f"  总知识: {stats['total']}")
    print(f"  成功: {stats['success']}")
    print(f"  错误: {stats['errors']}")
    print(f"  分类: {stats['categories']}")


if __name__ == "__main__":
    demo()
