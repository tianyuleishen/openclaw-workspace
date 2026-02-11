#!/usr/bin/env python3
"""
小爪内容安全模块 v1.0
基于 funNLP 理念设计
"""

import re
from typing import List, Dict, Optional


class ContentSafetyModule:
    """
    内容安全模块
    功能：敏感词检测、内容过滤、文明对话
    """
    
    def __init__(self):
        # 敏感词库（示例，实际使用时从文件加载）
        self.sensitive_words = {
            # 政治敏感
            'political': [],
            # 脏话粗口
            'profanity': [],
            # 广告垃圾
            'spam': [],
            # 其他不当内容
            'other': []
        }
        
        # 加载默认敏感词
        self._load_default_words()
        
        # 统计
        self.stats = {
            'total_checks': 0,
            'blocked_count': 0,
            'warning_count': 0
        }
    
    def _load_default_words(self):
        """加载默认敏感词库"""
        # 脏话粗口（示例）
        self.sensitive_words['profanity'] = [
            # 这里可以添加实际的敏感词
        ]
    
    def load_words_from_file(self, filepath: str, category: str = 'other'):
        """从文件加载敏感词"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                words = [line.strip() for line in f if line.strip()]
                self.sensitive_words[category].extend(words)
            print(f"✅ 加载 {len(words)} 个敏感词到 {category}")
        except Exception as e:
            print(f"❌ 加载失败: {e}")
    
    def check(self, text: str) -> Dict:
        """
        检查文本内容安全
        
        Returns:
            {
                'safe': bool,
                'level': 'safe'/'warning'/'blocked',
                'matched_words': List[str],
                'suggestion': str
            }
        """
        self.stats['total_checks'] += 1
        
        text_lower = text.lower()
        matched = []
        
        # 检查各类敏感词
        for category, words in self.sensitive_words.items():
            for word in words:
                if word in text_lower:
                    matched.append({
                        'word': word,
                        'category': category
                    })
        
        # 判断安全级别
        if len(matched) == 0:
            return {
                'safe': True,
                'level': 'safe',
                'matched_words': [],
                'suggestion': None
            }
        
        self.stats['warning_count'] += 1
        
        if len(matched) >= 3:
            self.stats['blocked_count'] += 1
            return {
                'safe': False,
                'level': 'blocked',
                'matched_words': matched,
                'suggestion': '内容包含不当词汇，请文明发言'
            }
        
        return {
            'safe': True,
            'level': 'warning',
            'matched_words': matched,
            'suggestion': '请注意用词'
        }
    
    def filter(self, text: str) -> str:
        """过滤敏感词"""
        result = text
        
        for category, words in self.sensitive_words.items():
            for word in words:
                # 替换为 *
                pattern = re.compile(re.escape(word), re.IGNORECASE)
                result = pattern.sub('*' * len(word), result)
        
        return result
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            'total_checks': self.stats['total_checks'],
            'blocked': self.stats['blocked_count'],
            'warnings': self.stats['warning_count'],
            'safe_rate': (
                (self.stats['total_checks'] - self.stats['warning_count']) 
                / max(self.stats['total_checks'], 1) * 100
            )
        }


# ==================== 意图识别模块 ====================

class IntentClassifier:
    """
    意图识别模块
    功能：分类用户意图、快速响应
    """
    
    def __init__(self):
        # 意图关键词
        self.intent_patterns = {
            'coding': ['写代码', 'python', '编程', '函数', '代码', 'debug'],
            'search': ['搜索', '查找', '找', '查询', '搜'],
            'chat': ['聊天', '你好', '在吗', '干嘛'],
            'help': ['帮助', '怎么', '如何', '教程'],
            'system': ['状态', '性能', '内存', 'CPU'],
            'file': ['文件', '读取', '写入', '保存'],
            'translate': ['翻译', '翻译成'],
        }
        
        self.intent_stats = {intent: 0 for intent in self.intent_patterns}
    
    def classify(self, text: str) -> Dict:
        """
        识别用户意图
        
        Returns:
            {
                'intent': str,
                'confidence': float,
                'keywords': List[str]
            }
        """
        text_lower = text.lower()
        scores = {}
        
        # 匹配各类意图
        for intent, keywords in self.intent_patterns.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                scores[intent] = score
        
        if not scores:
            return {
                'intent': 'unknown',
                'confidence': 0.0,
                'keywords': []
            }
        
        # 返回最高分的意图
        best_intent = max(scores, key=scores.get)
        max_score = scores[best_intent]
        confidence = min(max_score / 3, 1.0)  # 归一化
        
        self.intent_stats[best_intent] += 1
        
        return {
            'intent': best_intent,
            'confidence': confidence,
            'keywords': [kw for kw in self.intent_patterns[best_intent] 
                        if kw in text_lower]
        }
    
    def get_stats(self) -> Dict:
        """获取统计"""
        total = sum(self.intent_stats.values())
        return {
            'total': total,
            'distribution': dict(self.intent_stats)
        }


# ==================== 知识图谱模块 ====================

class KnowledgeGraph:
    """
    知识图谱模块
    功能：结构化存储记忆、实体关联
    """
    
    def __init__(self):
        # 实体
        self.entities = {}  # {entity_id: {type, name, properties}}
        # 关系
        self.relations = []  # [(entity1, relation, entity2)]
        # 索引
        self.entity_index = {}  # {type: [entity_ids]}
    
    def add_entity(self, entity_id: str, entity_type: str, name: str, 
                   properties: Dict = None):
        """添加实体"""
        self.entities[entity_id] = {
            'type': entity_type,
            'name': name,
            'properties': properties or {}
        }
        
        # 更新索引
        if entity_type not in self.entity_index:
            self.entity_index[entity_type] = []
        self.entity_index[entity_type].append(entity_id)
    
    def add_relation(self, from_id: str, relation: str, to_id: str):
        """添加关系"""
        self.relations.append((from_id, relation, to_id))
    
    def query(self, entity_type: str = None, entity_id: str = None) -> List[Dict]:
        """查询"""
        results = []
        
        if entity_id and entity_id in self.entities:
            results.append(self.entities[entity_id])
        
        if entity_type and entity_type in self.entity_index:
            for eid in self.entity_index[entity_type]:
                results.append(self.entities[eid])
        
        return results
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            'entities': len(self.entities),
            'relations': len(self.relations),
            'types': list(self.entity_index.keys())
        }


# ==================== 集成模块 ====================

class ClawletSystem:
    """
    小爪系统集成
    整合内容安全、意图识别、知识图谱
    """
    
    def __init__(self):
        self.safety = ContentSafetyModule()
        self.intent = IntentClassifier()
        self.knowledge = KnowledgeGraph()
        
        # 版本
        self.version = "v1.0"
        
        # 初始化知识图谱
        self._init_knowledge()
    
    def _init_knowledge(self):
        """初始化知识图谱"""
        # 添加实体
        self.knowledge.add_entity('user', 'person', '用户', {'role': 'master'})
        self.knowledge.add_entity('system', 'system', '小爪', {'version': self.version})
        self.knowledge.add_entity('memory', 'module', '记忆系统', {'type': 'markdown+json'})
        
        # 添加关系
        self.knowledge.add_relation('user', 'uses', 'system')
        self.knowledge.add_relation('system', 'has', 'memory')
    
    def process(self, user_input: str) -> Dict:
        """
        处理用户输入
        
        流程：安全检查 → 意图识别 → 知识查询 → 响应
        """
        # 1. 安全检查
        safety_result = self.safety.check(user_input)
        
        # 2. 意图识别
        intent_result = self.intent.classify(user_input)
        
        # 3. 知识查询（根据意图）
        related_knowledge = []
        if intent_result['intent'] != 'unknown':
            related_knowledge = self.knowledge.query(
                entity_type=intent_result['intent']
            )
        
        return {
            'input': user_input,
            'safety': safety_result,
            'intent': intent_result,
            'knowledge': related_knowledge,
            'suggested_tools': self._suggest_tools(intent_result['intent'])
        }
    
    def _suggest_tools(self, intent: str) -> List[str]:
        """根据意图推荐工具"""
        tool_map = {
            'coding': ['python', 'shell'],
            'search': ['web_search', 'file_search'],
            'chat': ['chat'],
            'file': ['file_read', 'file_write'],
            'help': ['documentation'],
        }
        return tool_map.get(intent, ['general'])
    
    def get_system_stats(self) -> Dict:
        """获取系统状态"""
        return {
            'version': self.version,
            'safety': self.safety.get_stats(),
            'intent': self.intent.get_stats(),
            'knowledge': self.knowledge.get_stats()
        }


# ==================== 测试 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("🦞 小爪系统优化 - Phase 1: 内容安全模块")
    print("=" * 60)
    
    # 初始化系统
    clawlet = ClawletSystem()
    
    print(f"\n✅ 系统版本: {clawlet.version}")
    print(f"   知识图谱: {clawlet.knowledge.get_stats()['entities']} 实体")
    
    # 测试安全检查
    print("\n📊 安全检查测试:")
    tests = [
        ("你好小爪！", "正常"),
        ("帮我写代码", "正常"),
        ("测试内容", "正常"),
    ]
    
    for text, expected in tests:
        result = clawlet.safety.check(text)
        print(f"   [{expected}] {text[:20]} → {result['level']}")
    
    # 测试意图识别
    print("\n🎯 意图识别测试:")
    tests = [
        "帮我写一个 Python 函数",
        "搜索 AI 论文",
        "你好小爪",
    ]
    
    for text in tests:
        result = clawlet.intent.classify(text)
        print(f"   {text[:20]} → {result['intent']} ({result['confidence']:.2f})")
    
    # 处理用户输入
    print("\n🔄 处理流程测试:")
    result = clawlet.process("帮我搜索 AI 论文")
    print(f"   输入: {result['input']}")
    print(f"   安全: {result['safety']['level']}")
    print(f"   意图: {result['intent']['intent']}")
    print(f"   推荐工具: {result['suggested_tools']}")
    
    # 系统状态
    print("\n📈 系统状态:")
    stats = clawlet.get_system_stats()
    print(f"   版本: {stats['version']}")
    print(f"   安全检查: {stats['safety']['total_checks']}")
    print(f"   意图识别: {stats['intent']['total']}")
    print(f"   知识图谱: {stats['knowledge']['entities']} 实体, {stats['knowledge']['relations']} 关系")
    
    print("\n" + "=" * 60)
    print("✅ 小爪系统优化模块加载成功！")
    print("=" * 60)
