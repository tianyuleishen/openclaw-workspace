#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦞 RAG知识库连接系统
=====================
检索增强生成 (Retrieval-Augmented Generation)

功能:
1. 知识库管理 (添加/查询/删除)
2. 文本向量化 (TF-IDF简化版)
3. 相似度检索
4. 上下文增强

Version: 1.0
Date: 2026-02-11
"""

import json
import re
import math
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from collections import Counter, defaultdict
import hashlib


@dataclass
class Document:
    """文档"""
    id: str
    content: str
    metadata: Dict = field(default_factory=dict)
    embedding: Optional[List[float]] = None


@dataclass
class RetrievalResult:
    """检索结果"""
    document: Document
    score: float
    snippet: str


class SimpleVectorizer:
    """
    简化版TF-IDF向量化器
    """
    
    def __init__(self):
        self.vocabulary: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}
        
    def fit(self, documents: List[str]):
        """构建词汇表和IDF"""
        # 分词
        all_words = []
        for doc in documents:
            words = self._tokenize(doc)
            all_words.extend(words)
        
        # 构建词汇表
        word_counts = Counter(all_words)
        self.vocabulary = {word: idx for idx, (word, _) in enumerate(word_counts.most_common())}
        
        # 计算IDF
        n = len(documents)
        for word in self.vocabulary:
            df = sum(1 for doc in documents if word in doc.lower())
            self.idf[word] = math.log(n / (1 + df)) + 1
        
    def _tokenize(self, text: str) -> List[str]:
        """分词"""
        text = text.lower()
        words = re.findall(r'\b[a-zA-Z\u4e00-\u9fff]+\b', text)
        return words
    
    def transform(self, text: str) -> List[float]:
        """转换为TF-IDF向量"""
        words = self._tokenize(text)
        word_counts = Counter(words)
        
        tfidf = []
        for word, idx in self.vocabulary.items():
            tf = word_counts.get(word, 0) / len(words) if words else 0
            idf = self.idf.get(word, 1.0)
            tfidf.append(tf * idf)
        
        return tfidf
    
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """余弦相似度"""
        if not vec1 or not vec2:
            return 0.0
        
        dot = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        
        if norm1 * norm2 == 0:
            return 0.0
        
        return dot / (norm1 * norm2)


class KnowledgeBase:
    """
    知识库系统
    """
    
    def __init__(self, name: str = "default"):
        self.name = name
        self.documents: Dict[str, Document] = {}
        self.vectorizer = SimpleVectorizer()
        self.built = False
        
    def add_document(self, content: str, metadata: Dict = None) -> str:
        """添加文档"""
        doc_id = hashlib.md5(content.encode()).hexdigest()[:8]
        
        doc = Document(
            id=doc_id,
            content=content,
            metadata=metadata or {}
        )
        
        self.documents[doc_id] = doc
        self.built = False  # 需要重新构建
        
        return doc_id
    
    def add_documents(self, docs: List[Dict[str, str]]) -> List[str]:
        """批量添加文档"""
        ids = []
        for doc in docs:
            doc_id = self.add_document(doc["content"], doc.get("metadata"))
            ids.append(doc_id)
        return ids
    
    def build(self):
        """构建索引"""
        if not self.documents:
            return
        
        contents = [doc.content for doc in self.documents.values()]
        self.vectorizer.fit(contents)
        
        for doc in self.documents.values():
            doc.embedding = self.vectorizer.transform(doc.content)
        
        self.built = True
        print(f"  [KnowledgeBase] 构建完成: {len(self.documents)} 文档")
    
    def retrieve(self, query: str, top_k: int = 3) -> List[RetrievalResult]:
        """
        检索相关文档
        
        Args:
            query: 查询文本
            top_k: 返回前k个结果
            
        Returns:
            检索结果列表
        """
        if not self.built:
            self.build()
        
        if not self.documents:
            return []
        
        # 查询向量化
        query_vec = self.vectorizer.transform(query)
        
        # 计算相似度
        results = []
        for doc in self.documents.values():
            if doc.embedding is None:
                continue
                
            score = self.vectorizer.cosine_similarity(query_vec, doc.embedding)
            
            # 提取snippet
            snippet = self._extract_snippet(doc.content, query)
            
            results.append(RetrievalResult(
                document=doc,
                score=score,
                snippet=snippet
            ))
        
        # 排序返回top_k
        results.sort(key=lambda x: x.score, reverse=True)
        
        return results[:top_k]
    
    def _extract_snippet(self, content: str, query: str) -> str:
        """提取相关片段"""
        # 简单实现：返回前100字
        return content[:100] + "..." if len(content) > 100 else content
    
    def query(self, question: str) -> str:
        """
        简单问答
        
        Args:
            question: 问题
            
        Returns:
            相关知识
        """
        results = self.retrieve(question, top_k=1)
        
        if results:
            return f"相关知识: {results[0].snippet}"
        
        return "未找到相关知识"


class ReasoningKnowledgeBase:
    """
    推理知识库 - 专门用于存储推理规则和模式
    """
    
    def __init__(self):
        self.kb = KnowledgeBase("reasoning")
        self._init_reasoning_knowledge()
    
    def _init_reasoning_knowledge(self):
        """初始化推理知识"""
        knowledge = [
            {
                "content": "矛盾关系: A和¬A必有一真一假，不能同真或同假",
                "metadata": {"type": "logic", "category": "contradiction"}
            },
            {
                "content": "蕴含关系: A→B，只有当A真B假时，整个蕴含才为假",
                "metadata": {"type": "logic", "category": "implication"}
            },
            {
                "content": "等差数列通项公式: an = a1 + (n-1)d，其中a1为首项，d为公差",
                "metadata": {"type": "math", "category": "sequence"}
            },
            {
                "content": "等比数列通项公式: an = a1 × r^(n-1)，其中r为公比",
                "metadata": {"type": "math", "category": "sequence"}
            },
            {
                "content": "穷举法: 逐一验证所有可能性，找到满足条件的解",
                "metadata": {"type": "method", "category": "exhaustive"}
            },
            {
                "content": "反证法: 假设结论不成立，推导出矛盾，从而证明原结论成立",
                "metadata": {"type": "method", "category": "proof"}
            },
            {
                "content": "归谬法: 通过假设推理导出荒谬结论，从而否定假设",
                "metadata": {"type": "method", "category": "proof"}
            },
            {
                "content": "连锁推理: 如果A→B且B→C，则A→C",
                "metadata": {"type": "logic", "category": "chain"}
            },
            {
                "content": "充分条件: A是B的充分条件意味着A成立则B一定成立",
                "metadata": {"type": "logic", "category": "condition"}
            },
            {
                "content": "必要条件: A是B的必要条件意味着B成立则A一定成立",
                "metadata": {"type": "logic", "category": "condition"}
            }
        ]
        
        self.kb.add_documents(knowledge)
        self.kb.build()
    
    def query(self, question: str) -> List[RetrievalResult]:
        """查询相关推理知识"""
        return self.kb.retrieve(question, top_k=3)
    
    def get_logic_rules(self) -> List[str]:
        """获取所有逻辑规则"""
        results = self.kb.retrieve("矛盾 蕴含 推理", top_k=10)
        return [r.snippet for r in results]


class RAGEngine:
    """
    RAG检索增强生成引擎
    """
    
    def __init__(self):
        self.reasoning_kb = ReasoningKnowledgeBase()
        self.custom_kb = KnowledgeBase("custom")
        
    def enhance_query(self, question: str) -> Dict[str, Any]:
        """
        增强查询
        
        Args:
            question: 用户问题
            
        Returns:
            包含原始问题和检索知识的字典
        """
        # 检索推理知识
        reasoning_results = self.reasoning_kb.query(question)
        
        # 检索自定义知识
        custom_results = self.custom_kb.retrieve(question, top_k=2)
        
        # 构建上下文
        context_parts = ["【推理知识库】"]
        for r in reasoning_results:
            context_parts.append(f"• {r.snippet} (相关性: {r.score:.2f})")
        
        if custom_results:
            context_parts.append("\n【自定义知识库】")
            for r in custom_results:
                context_parts.append(f"• {r.snippet}")
        
        context = "\n".join(context_parts)
        
        return {
            "question": question,
            "context": context,
            "reasoning_knowledge": [r.snippet for r in reasoning_results],
            "custom_knowledge": [r.snippet for r in custom_results],
            "retrieved_count": len(reasoning_results) + len(custom_results)
        }
    
    def add_knowledge(self, content: str, category: str = "general"):
        """添加自定义知识"""
        self.custom_kb.add_document(
            content,
            metadata={"category": category}
        )
        self.custom_kb.build()
    
    def answer(self, question: str) -> str:
        """
        基于知识的问答
        
        Args:
            question: 问题
            
        Returns:
            答案
        """
        enhanced = self.enhance_query(question)
        
        if not enhanced["reasoning_knowledge"]:
            return "未找到相关知识。"
        
        # 简单回答：结合知识和问题
        answer_parts = ["根据检索到的知识："]
        for i, knowledge in enumerate(enhanced["reasoning_knowledge"][:2], 1):
            answer_parts.append(f"{i}. {knowledge}")
        
        answer_parts.append(f"\n相关度: {enhanced['retrieved_count']} 条")
        
        return "\n".join(answer_parts)


def demo():
    """演示"""
    print("="*70)
    print("🦞 RAG知识库系统演示")
    print("="*70)
    
    # 创建RAG引擎
    rag = RAGEngine()
    
    # 查询逻辑题
    print("\n【问题1】甲说'我会'，丙说'甲不会'，这是什么关系？")
    result = rag.enhance_query("矛盾关系 真话 假话")
    print(f"\n检索结果:")
    for knowledge in result["reasoning_knowledge"]:
        print(f"  • {knowledge}")
    
    # 查询数学题
    print("\n【问题2】等差数列如何计算？")
    answer = rag.answer("等差数列 通项公式")
    print(f"\n回答:\n{answer}")
    
    # 添加自定义知识
    print("\n【添加自定义知识】")
    rag.add_knowledge("小爪是一只AI助手，擅长推理和分析", "identity")
    print("  已添加: 小爪的身份信息")
    
    # 查询自定义知识
    print("\n【查询自定义知识】")
    result = rag.enhance_query("小爪 是谁")
    print(f"  自定义知识: {result['custom_knowledge']}")
    
    print("\n" + "="*70)
    print("✅ RAG知识库系统演示完成")
    print("="*70)


if __name__ == "__main__":
    demo()
