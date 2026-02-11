#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦞 基于时间窗口+衰减权重的文档检索系统

核心功能:
1. 时间窗口内计算全局TF-IDF
2. 构建带时间衰减的向量
3. 计算余弦相似度（需≥0.6）

Version: 1.0
Date: 2026-02-11
"""

import math
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
import numpy as np


class TimeWeightedRetriever:
    """
    基于时间窗口+衰减权重的文档检索系统
    """
    
    def __init__(self, window_hours: int = 24, decay_rate: float = 0.1):
        """
        初始化
        
        Args:
            window_hours: 时间窗口大小（小时）
            decay_rate: 时间衰减率
        """
        self.window_hours = window_hours
        self.decay_rate = decay_rate
        self.documents = []  # 文档列表
        self.vocabulary = set()  # 词汇表
        self.idf = {}  # IDF值
        self.index = defaultdict(list)  # 倒排索引
        
    def add_document(self, doc_id: str, content: str, timestamp: datetime):
        """
        添加文档
        
        Args:
            doc_id: 文档ID
            content: 文档内容
            timestamp: 时间戳
        """
        # 预处理
        tokens = self._preprocess(content)
        
        # 添加到文档列表
        self.documents.append({
            'id': doc_id,
            'tokens': tokens,
            'timestamp': timestamp,
            'tf': Counter(tokens)
        })
        
        # 更新词汇表
        self.vocabulary.update(tokens)
        
        # 更新倒排索引
        for token in set(tokens):
            self.index[token].append(doc_id)
        
        # 标记需要重新计算IDF
        self._idf_stale = True
    
    def _preprocess(self, text: str) -> List[str]:
        """
        文档预处理
        
        Steps:
        1. 转小写
        2. 分词
        3. 去停用词
        4. 词干提取
        """
        # 简化：只做基本处理
        tokens = text.lower().split()
        return [token.strip('.,!?()[]') for token in tokens]
    
    def compute_global_tf_idf(self):
        """
        Step 1: 在时间窗口内计算全局TF-IDF
        
        核心步骤:
        1. 筛选窗口内文档
        2. 计算TF（词频）
        3. 计算IDF（逆文档频率）
        4. 计算TF-IDF权重
        """
        # Step 1: 筛选时间窗口内的文档
        now = datetime.now()
        window_start = now - timedelta(hours=self.window_hours)
        window_docs = [
            doc for doc in self.documents 
            if doc['timestamp'] >= window_start
        ]
        
        if not window_docs:
            print("⚠️ 窗口内无文档")
            return
        
        print(f"📊 窗口内文档数: {len(window_docs)}")
        
        # Step 2: 计算IDF
        # IDF = log(N / df)
        N = len(window_docs)
        self.idf = {}
        
        for token in self.vocabulary:
            df = len(set(doc['id'] for doc in window_docs if token in doc['tokens']))
            if df > 0:
                self.idf[token] = math.log(N / df)
            else:
                self.idf[token] = 0
        
        self._idf_stale = False
        
        # Step 3: 计算每个文档的TF-IDF向量
        for doc in window_docs:
            doc['tfidf'] = {}
            max_tf = max(doc['tf'].values()) if doc['tf'] else 1
            
            for token in self.vocabulary:
                # TF-IDF = TF * IDF
                tf = doc['tf'].get(token, 0) / max_tf
                tfidf = tf * self.idf.get(token, 0)
                doc['tfidf'][token] = tfidf
        
        print(f"✅ TF-IDF计算完成，词汇表大小: {len(self.vocabulary)}")
    
    def _compute_time_decay(self, doc_timestamp: datetime) -> float:
        """
        Step 2: 计算时间衰减权重
        
        衰减公式:
        weight = e^(-decay_rate * hours_ago)
        
        最近文档权重 → 1
        越久远权重 → 0
        """
        now = datetime.now()
        hours_ago = (now - doc_timestamp).total_seconds() / 3600
        
        # 指数衰减
        weight = math.exp(-self.decay_rate * hours_ago)
        
        return weight
    
    def build_weighted_vector(self, doc_id: str) -> Dict[str, float]:
        """
        Step 3: 构建带时间衰减的向量
        
        公式:
        weighted_tfidf = TF-IDF * time_decay
        
        核心思想:
        - 新文档权重高
        - 旧文档权重低
        """
        # 获取文档
        doc = next((d for d in self.documents if d['id'] == doc_id), None)
        if not doc:
            return {}
        
        # 计算时间衰减
        decay = self._compute_time_decay(doc['timestamp'])
        
        # 应用衰减权重
        weighted_vector = {}
        for token in self.vocabulary:
            tfidf = doc['tfidf'].get(token, 0)
            weighted_vector[token] = tfidf * decay
        
        return weighted_vector
    
    def cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """
        Step 4: 计算余弦相似度
        
        公式:
        cos(θ) = (A·B) / (||A|| × ||B||)
        
        要求: ≥ 0.6
        """
        # 计算点积
        dot_product = sum(vec1.get(token, 0) * vec2.get(token, 0) 
                        for token in set(vec1.keys()) | set(vec2.keys()))
        
        # 计算范数
        norm1 = math.sqrt(sum(v**2 for v in vec1.values()))
        norm2 = math.sqrt(sum(v**2 for v in vec2.values()))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        # 余弦相似度
        similarity = dot_product / (norm1 * norm2)
        
        return similarity
    
    def search(self, query: str, threshold: float = 0.6) -> List[Tuple[str, float]]:
        """
        Step 5: 检索
        
        核心步骤:
        1. 计算query的TF-IDF向量
        2. 构建带时间衰减的文档向量
        3. 计算余弦相似度
        4. 过滤并排序结果
        """
        # 确保TF-IDF已计算
        if self._idf_stale or not self.idf:
            self.compute_global_tf_idf()
        
        # Step 1: 处理query
        query_tokens = self._preprocess(query)
        query_counter = Counter(query_tokens)
        max_tf = max(query_counter.values()) if query_counter else 1
        
        # 构建query向量（带IDF权重）
        query_vector = {}
        for token in self.vocabulary:
            tf = query_counter.get(token, 0) / max_tf
            query_vector[token] = tf * self.idf.get(token, 0)
        
        # Step 2: 计算每个文档的加权向量
        results = []
        
        for doc in self.documents:
            # 构建带时间衰减的向量
            doc_vector = self.build_weighted_vector(doc['id'])
            
            # 计算余弦相似度
            similarity = self.cosine_similarity(query_vector, doc_vector)
            
            # 过滤阈值
            if similarity >= threshold:
                results.append((doc['id'], similarity))
        
        # 排序
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results


def demo():
    """演示"""
    print("="*70)
    print("🦞 基于时间窗口+衰减权重的文档检索系统")
    print("="*70)
    
    # 初始化（窗口24小时，衰减率0.1）
    retriever = TimeWeightedRetriever(window_hours=24, decay_rate=0.1)
    
    # 添加测试文档
    now = datetime.now()
    
    documents = [
        ("doc1", "Python programming language", now - timedelta(hours=2)),
        ("doc2", "Machine learning algorithms", now - timedelta(hours=5)),
        ("doc3", "Deep neural networks", now - timedelta(hours=12)),
        ("doc4", "Natural language processing", now - timedelta(hours=23)),
        ("doc5", "Computer vision techniques", now - timedelta(hours=48)),  # 窗口外
    ]
    
    print("\n📄 添加文档:")
    for doc_id, content, timestamp in documents:
        hours_ago = (now - timestamp).total_seconds() / 3600
        retriever.add_document(doc_id, content, timestamp)
        print(f"  {doc_id}: {content} ({hours_ago:.1f}小时前)")
    
    # 计算TF-IDF
    print("\n📊 Step 1: 计算全局TF-IDF")
    retriever.compute_global_tf_idf()
    
    # 检索
    print("\n🔍 Step 2: 检索 'neural networks'")
    results = retriever.search("neural networks", threshold=0.6)
    
    print(f"\n结果 (相似度 ≥ 0.6):")
    for doc_id, similarity in results:
        print(f"  {doc_id}: {similarity:.4f}")
    
    # 展示时间衰减
    print("\n⏰ 时间衰减示例:")
    for hours in [0, 1, 5, 10, 24, 48]:
        weight = math.exp(-0.1 * hours)
        print(f"  {hours:2d}小时前: {weight:.4f}")
    
    print("\n" + "="*70)
    print("✅ 演示完成")
    print("="*70)


if __name__ == "__main__":
    demo()
