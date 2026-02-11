# 基于时间窗口+衰减权重的文档检索方法

## 核心步骤

### 1. 时间窗口过滤
```
输入: 所有文档 + 时间窗口大小(window_hours)
处理: 筛选 timestamp ≥ now - window_hours 的文档
输出: 窗口内文档集合
```

### 2. 全局TF-IDF计算
```
Step 2.1: 计算TF（词频）
  TF(t,d) = count(t in d) / max(count)

Step 2.2: 计算IDF（逆文档频率）
  IDF(t) = log(N / df(t))
  其中 N = 窗口内文档数
        df(t) = 包含词t的文档数

Step 2.3: 计算TF-IDF权重
  TF-IDF(t,d) = TF(t,d) × IDF(t)
```

### 3. 时间衰减权重
```
衰减公式:
weight(t) = e^(-decay_rate × hours_ago)

示例（decay_rate=0.1）:
  0小时前: 1.0000
  5小时前: 0.6065
  10小时前: 0.3679
  24小时前: 0.0907
```

### 4. 构建带时间衰减的向量
```
加权TF-IDF(t,d) = TF-IDF(t,d) × time_decay(d)

向量表示:
doc_vector = {word1: weighted_tfidf1, word2: weighted_tfidf2, ...}
```

### 5. 余弦相似度计算
```
公式:
cos(θ) = (A · B) / (||A|| × ||B||)

其中:
A · B = Σ Aᵢ × Bᵢ (点积)
||A|| = √Σ Aᵢ² (L2范数)
```

### 6. 阈值过滤
```
条件: similarity ≥ 0.6
输出: 满足条件的文档列表（按相似度降序）
```

## 核心代码

```python
class TimeWeightedRetriever:
    def compute_global_tf_idf(self):
        # 1. 时间窗口过滤
        window_docs = [d for d in self.documents 
                      if d['timestamp'] >= now - window_hours]
        
        # 2. TF-IDF计算
        for doc in window_docs:
            for token in self.vocabulary:
                tf = doc['tf'][token] / max_tf
                idf = math.log(N / df)
                doc['tfidf'][token] = tf × idf
    
    def build_weighted_vector(self, doc_id):
        # 3. 时间衰减
        decay = math.exp(-decay_rate × hours_ago)
        
        # 4. 加权向量
        return {token: tfidf × decay 
                for token, tfidf in doc['tfidf'].items()}
    
    def cosine_similarity(self, vec1, vec2):
        # 5. 余弦相似度
        dot = Σ vec1ᵢ × vec2ᵢ
        norm = √Σ vecᵢ²
        return dot / (norm1 × norm2)
```

## 效果演示

| 查询 | 文档 | 相似度 | 衰减 |
|------|------|--------|------|
| Python programming | doc1 | 0.9129 | 0.8187 |
| machine learning | doc2 | 0.7071 | 0.6065 |
| deep neural | doc3 | 0.9608 | 0.3012 |

## 关键参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| window_hours | 时间窗口大小 | 24h |
| decay_rate | 衰减率 | 0.1 |
| threshold | 相似度阈值 | 0.6 |

## 优势

1. **时效性**: 新文档权重更高
2. **准确性**: TF-IDF捕捉词重要性
3. **可调节**: 参数灵活配置
