#!/usr/bin/env python3
"""
小爪系统 Phase 2 - 增强版
基于 funNLP 理念设计
"""

import re
from typing import List, Dict, Optional
from datetime import datetime
from collections import deque


# ==================== 增强版内容安全模块 ====================

class ContentSafetyModule:
    """内容安全模块 v1.1"""
    
    def __init__(self):
        self.sensitive_words = {
            'political': [],
            'profanity': [],
            'spam': [],
            'other': []
        }
        self.stats = {
            'total_checks': 0,
            'blocked_count': 0,
            'warning_count': 0
        }
    
    def check(self, text: str) -> Dict:
        self.stats['total_checks'] += 1
        text_lower = text.lower()
        matched = []
        
        for category, words in self.sensitive_words.items():
            for word in words:
                if word in text_lower:
                    matched.append({'word': word, 'category': category})
        
        if not matched:
            return {'safe': True, 'level': 'safe', 'matched_words': [], 'suggestion': None}
        
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
        result = text
        for category, words in self.sensitive_words.items():
            for word in words:
                pattern = re.compile(re.escape(word), re.IGNORECASE)
                result = pattern.sub('*' * len(word), result)
        return result
    
    def get_stats(self) -> Dict:
        return {
            'total_checks': self.stats['total_checks'],
            'blocked': self.stats['blocked_count'],
            'warnings': self.stats['warning_count'],
            'safe_rate': (
                (self.stats['total_checks'] - self.stats['warning_count']) 
                / max(self.stats['total_checks'], 1) * 100
            )
        }


# ==================== 增强版意图识别模块 (12类) ====================

class IntentClassifierV2:
    """意图识别模块 v2.0 - 12类意图"""
    
    def __init__(self):
        # 扩展到12类意图
        self.intent_patterns = {
            'coding': ['写代码', 'python', '编程', '函数', '代码', 'debug', '实现', '开发'],
            'search': ['搜索', '查找', '找', '查询', '搜', '找一下'],
            'chat': ['聊天', '你好', '在吗', '干嘛', '聊', '说话', '嗨'],
            'help': ['帮助', '怎么', '如何', '教程', '使用', '使用说明'],
            'system': ['状态', '性能', '内存', 'CPU', '监控', '检查'],
            'file': ['文件', '读取', '写入', '保存', '打开', '创建'],
            'translate': ['翻译', '翻译成', '英译', '中译', 'language'],
            'analysis': ['分析', '统计', '总结', '报告', '评估'],
            'creative': ['创作', '写诗', '写歌', '故事', '创意', '写文章', '写一首'],
            'education': ['学习', '教程', '解释', '原理', '概念', '学'],
            'entertainment': ['笑话', '故事', '游戏', '娱乐', '有趣', '娱乐一下'],
            'news': ['新闻', '最新', '热点', '消息', '时事'],
            'shopping': ['购买', '买', '价格', '推荐', '商品'],
        }
        
        self.intent_stats = {intent: 0 for intent in self.intent_patterns}
        self.intent_descriptions = {
            'coding': '编程开发',
            'search': '信息搜索',
            'chat': '日常聊天',
            'help': '寻求帮助',
            'system': '系统查询',
            'file': '文件操作',
            'translate': '翻译服务',
            'analysis': '分析总结',
            'creative': '创意创作',
            'education': '教育培训',
            'entertainment': '娱乐消遣',
            'news': '新闻资讯',
            'shopping': '购物推荐',
        }
    
    def classify(self, text: str) -> Dict:
        text_lower = text.lower()
        scores = {}
        
        for intent, keywords in self.intent_patterns.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                scores[intent] = score
        
        if not scores:
            return {
                'intent': 'unknown',
                'confidence': 0.0,
                'keywords': [],
                'description': '未知意图'
            }
        
        best_intent = max(scores, key=scores.get)
        max_score = scores[best_intent]
        confidence = min(max_score / 3, 1.0)
        
        self.intent_stats[best_intent] += 1
        
        return {
            'intent': best_intent,
            'confidence': confidence,
            'keywords': [kw for kw in self.intent_patterns[best_intent] 
                        if kw in text_lower],
            'description': self.intent_descriptions.get(best_intent, '其他')
        }
    
    def get_stats(self) -> Dict:
        total = sum(self.intent_stats.values())
        return {
            'total': total,
            'distribution': dict(self.intent_stats),
            'top_intents': sorted(
                self.intent_stats.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:5]
        }


# ==================== 情感分析模块 ====================

class SentimentAnalyzer:
    """情感分析模块 v1.0"""
    
    def __init__(self):
        # 情感词库
        self.positive_words = [
            '好', '棒', '赞', '优秀', '开心', '高兴', '喜欢', '感谢',
            '棒极了', '完美', '出色', '强大', '有用', '帮助', '感谢'
        ]
        
        self.negative_words = [
            '坏', '差', '糟', '糟糕', '生气', '愤怒', '讨厌', '麻烦',
            '错误', '问题', '失败', '困难', '困惑', '不懂'
        ]
        
        self.intensifiers = ['非常', '特别', '极其', '相当', '很']
        self.negators = ['不', '没', '无', '非']
        
        self.stats = {
            'total_analyzed': 0,
            'positive': 0,
            'negative': 0,
            'neutral': 0
        }
    
    def analyze(self, text: str) -> Dict:
        """分析文本情感"""
        self.stats['total_analyzed'] += 1
        
        text_lower = text.lower()
        
        # 简单情感分析
        pos_count = sum(1 for word in self.positive_words if word in text_lower)
        neg_count = sum(1 for word in self.negative_words if word in text_lower)
        
        # 判断情感极性
        if pos_count > neg_count:
            sentiment = 'positive'
            self.stats['positive'] += 1
        elif neg_count > pos_count:
            sentiment = 'negative'
            self.stats['negative'] += 1
        else:
            sentiment = 'neutral'
            self.stats['neutral'] += 1
        
        # 计算情感强度
        intensity = (pos_count + neg_count) / max(len(text.split()), 1)
        intensity = min(intensity * 2, 1.0)
        
        return {
            'sentiment': sentiment,
            'confidence': min(pos_count + neg_count, 1.0),
            'intensity': intensity,
            'positive_score': pos_count,
            'negative_score': neg_count,
            'suggestion': self._get_suggestion(sentiment)
        }
    
    def _get_suggestion(self, sentiment: str) -> str:
        """根据情感给出建议"""
        suggestions = {
            'positive': '用户情绪积极，可以保持友好互动',
            'negative': '用户可能遇到问题，需要耐心帮助',
            'neutral': '用户语气平和，保持正常服务'
        }
        return suggestions.get(sentiment, '')
    
    def get_stats(self) -> Dict:
        total = max(self.stats['total_analyzed'], 1)
        return {
            'total': self.stats['total_analyzed'],
            'positive_rate': self.stats['positive'] / total * 100,
            'negative_rate': self.stats['negative'] / total * 100,
            'neutral_rate': self.stats['neutral'] / total * 100
        }


# ==================== 对话管理器 ====================

class ConversationManager:
    """对话管理器 v1.0"""
    
    def __init__(self, max_history: int = 10):
        # 对话历史
        self.history = deque(maxlen=max_history)
        # 上下文信息
        self.context = {}
        # 用户信息
        self.user_info = {}
        # 对话状态
        self.state = 'idle'  # idle, active, waiting
    
    def add_message(self, role: str, content: str):
        """添加对话消息"""
        self.history.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_history(self, last_n: int = None) -> List[Dict]:
        """获取对话历史"""
        if last_n:
            return list(self.history)[-last_n:]
        return list(self.history)
    
    def set_context(self, key: str, value):
        """设置上下文"""
        self.context[key] = value
    
    def get_context(self, key: str, default=None):
        """获取上下文"""
        return self.context.get(key, default)
    
    def clear_history(self):
        """清空历史"""
        self.history.clear()
        self.context.clear()
    
    def get_summary(self) -> Dict:
        """获取对话摘要"""
        return {
            'message_count': len(self.history),
            'state': self.state,
            'context_keys': list(self.context.keys()),
            'recent_topics': self._extract_topics()
        }
    
    def _extract_topics(self) -> List[str]:
        """提取话题"""
        topics = []
        for msg in list(self.history)[-5:]:
            content = msg.get('content', '')
            if '代码' in content or 'python' in content.lower():
                topics.append('编程')
            if '搜索' in content or '查找' in content:
                topics.append('搜索')
            if '文件' in content:
                topics.append('文件')
        return list(set(topics))[:3]


# ==================== MiniMax API 集成 ====================

class MiniMax集成:
    """MiniMax API 集成模块 v1.0"""
    
    def __init__(self):
        # API 配置
        self.api_key = None
        self.base_url = "https://api.minimaxi.com/v1"
        
        # 使用统计
        self.stats = {
            'total_requests': 0,
            'total_tokens': 0,
            'chat_requests': 0,
            'coding_requests': 0,
            'search_requests': 0
        }
        
        # 任务类型映射
        self.task_prompts = {
            'coding': "你是一个专业的编程助手，提供清晰、高效的代码解决方案。",
            'chat': "你是一个友好、简洁的助手，回答要简短有力。",
            'search': "你是一个信息检索助手，帮助用户找到所需信息。",
            'analysis': "你是一个数据分析助手，帮助用户总结和分析信息。",
            'creative': "你是一个创意写作助手，帮助用户创作内容。",
            'education': "你是一个教育助手，耐心解释概念和原理。",
            'default': "你是一个helpful的AI助手。"
        }
    
    def configure(self, api_key: str):
        """配置 API Key"""
        self.api_key = api_key
        print(f"✅ MiniMax API 已配置")
    
    def chat(self, user_input: str, task_type: str = 'default', 
             system_prompt: str = None) -> Dict:
        """
        发送聊天请求
        
        Args:
            user_input: 用户输入
            task_type: 任务类型
            system_prompt: 系统提示
        
        Returns:
            {'response': str, 'tokens': int, 'success': bool}
        """
        # 选择系统提示
        if system_prompt is None:
            system_prompt = self.task_prompts.get(
                task_type, 
                self.task_prompts['default']
            )
        
        # 更新统计
        self.stats['total_requests'] += 1
        self.stats[f'{task_type}_requests'] = self.stats.get(f'{task_type}_requests', 0) + 1
        
        # 构建消息
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
        
        # 这里应该调用实际的 API
        # 由于没有真实 API，我们返回模拟响应
        response = self._generate_mock_response(user_input, task_type)
        
        # 估算 token 数
        tokens = len(user_input) + len(response) // 4
        self.stats['total_tokens'] += tokens
        
        return {
            'response': response,
            'tokens': tokens,
            'success': True,
            'task_type': task_type
        }
    
    def _generate_mock_response(self, user_input: str, task_type: str) -> str:
        """生成模拟响应"""
        responses = {
            'coding': f"好的，我来帮你处理编程相关的问题。\n\n关于「{user_input}」，我可以提供代码示例和解决方案。",
            'chat': f"你好！有什么我可以帮你的吗？",
            'search': f"关于「{user_input}」，我来帮你搜索相关信息。",
            'analysis': f"好的，我来帮你分析「{user_input}」。",
            'creative': f"好的，关于「{user_input}」，让我来创作一些内容。",
            'education': f"好的，我来解释「{user_input}」相关的概念。",
            'default': f"我理解你的问题：{user_input}\n\n让我来帮你解答。"
        }
        return responses.get(task_type, responses['default'])
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            'total_requests': self.stats['total_requests'],
            'total_tokens': self.stats['total_tokens'],
            'by_type': {k: v for k, v in self.stats.items() 
                       if k.endswith('_requests')}
        }


# ==================== 增强版小爪系统 ====================

class ClawletSystemV2:
    """小爪系统 v2.0 - Phase 2 增强版"""
    
    def __init__(self):
        # 模块
        self.safety = ContentSafetyModule()
        self.intent = IntentClassifierV2()  # v2.0 - 12类意图
        self.sentiment = SentimentAnalyzer()
        self.conversation = ConversationManager()
        self.minimax = MiniMax集成()
        
        # 版本
        self.version = "v2.0"
        
        # 初始化
        self._init_system()
    
    def _init_system(self):
        """初始化系统"""
        print(f"🦞 小爪系统 {self.version} 初始化...")
        print("  ✅ 内容安全模块")
        print("  ✅ 意图识别模块 (12类)")
        print("  ✅ 情感分析模块")
        print("  ✅ 对话管理器")
        print("  ✅ MiniMax 集成")
        print()
    
    def process(self, user_input: str) -> Dict:
        """
        处理用户输入
        
        流程: 安全检查 → 情感分析 → 意图识别 → 对话历史 → 响应生成
        """
        # 1. 安全检查
        safety_result = self.safety.check(user_input)
        
        # 2. 情感分析
        sentiment_result = self.sentiment.analyze(user_input)
        
        # 3. 意图识别 (12类)
        intent_result = self.intent.classify(user_input)
        
        # 4. 更新对话历史
        self.conversation.add_message('user', user_input)
        
        # 5. 生成响应
        if safety_result['level'] == 'blocked':
            response = "抱歉，我无法处理包含不当内容的请求。请文明发言。"
        else:
            # 调用 MiniMax API
            minimax_result = self.minimax.chat(
                user_input, 
                task_type=intent_result['intent']
            )
            response = minimax_result['response']
        
        # 6. 添加助手回复到历史
        self.conversation.add_message('assistant', response)
        
        return {
            'input': user_input,
            'safety': safety_result,
            'sentiment': sentiment_result,
            'intent': intent_result,
            'response': response,
            'conversation': self.conversation.get_summary(),
            'suggested_tools': self._suggest_tools(intent_result['intent'])
        }
    
    def _suggest_tools(self, intent: str) -> List[str]:
        """根据意图推荐工具"""
        tool_map = {
            'coding': ['python', 'shell', 'git'],
            'search': ['web_search', 'file_search', 'ai_paper_search'],
            'chat': ['conversation'],
            'file': ['file_read', 'file_write', 'editor'],
            'system': ['status', 'monitor'],
            'translate': ['translation'],
            'analysis': ['analyzer'],
            'creative': ['generator'],
            'education': ['tutor'],
            'entertainment': ['fun'],
            'news': ['web_search'],
            'shopping': ['recommendation'],
        }
        return tool_map.get(intent, ['general'])
    
    def get_system_stats(self) -> Dict:
        """获取系统状态"""
        return {
            'version': self.version,
            'safety': self.safety.get_stats(),
            'intent': self.intent.get_stats(),
            'sentiment': self.sentiment.get_stats(),
            'conversation': self.conversation.get_summary(),
            'minimax': self.minimax.get_stats()
        }


# ==================== 测试 ====================

if __name__ == "__main__":
    print("=" * 70)
    print("🦞 小爪系统 Phase 2 - v2.0 增强版测试")
    print("=" * 70)
    print()
    
    # 初始化系统
    clawlet = ClawletSystemV2()
    
    # 配置 MiniMax (可选)
    # clawlet.minimax.configure("your-api-key")
    
    # ==================== 测试 1: 意图识别 (12类) ====================
    print("\n" + "=" * 70)
    print("🎯 测试 1: 意图识别 (12类)")
    print("=" * 70)
    
    test_cases = [
        ("写一个 Python 函数", "coding"),
        ("帮我搜索 AI 论文", "search"),
        ("你好小爪", "chat"),
        ("怎么使用这个功能", "help"),
        ("检查系统状态", "system"),
        ("读取配置文件", "file"),
        ("翻译成英文", "translate"),
        ("分析今天的日志", "analysis"),
        ("写一首诗", "creative"),
        ("解释机器学习原理", "education"),
        ("讲个笑话", "entertainment"),
        ("今天的新闻", "news"),
        ("推荐一款手机", "shopping"),
    ]
    
    passed = 0
    for text, expected in test_cases:
        result = clawlet.intent.classify(text)
        status = "✅" if result['intent'] == expected else "❌"
        print(f"  {status} [{expected:10}] {text[:20]} → {result['intent']}")
        if result['intent'] == expected:
            passed += 1
    
    print(f"\n📈 意图识别准确率: {passed}/{len(test_cases)}")
    
    # ==================== 测试 2: 情感分析 ====================
    print("\n" + "=" * 70)
    print("😊 测试 2: 情感分析")
    print("=" * 70)
    
    sentiment_tests = [
        ("谢谢你的帮助！", "positive"),
        ("这个问题太难了", "negative"),
        ("今天天气怎么样", "neutral"),
        ("太棒了！", "positive"),
        ("这个功能有问题", "negative"),
    ]
    
    for text, expected in sentiment_tests:
        result = clawlet.sentiment.analyze(text)
        emoji = "😊" if result['sentiment'] == 'positive' else "😞" if result['sentiment'] == 'negative' else "😐"
        print(f"  {emoji} [{expected:8}] {text[:15]} → {result['sentiment']}")
    
    # ==================== 测试 3: 对话管理 ====================
    print("\n" + "=" * 70)
    print("💬 测试 3: 对话管理")
    print("=" * 70)
    
    # 添加对话
    clawlet.conversation.add_message('user', '你好')
    clawlet.conversation.add_message('assistant', '你好！有什么可以帮你？')
    clawlet.conversation.add_message('user', '帮我写代码')
    clawlet.conversation.add_message('assistant', '好的，你想写什么代码？')
    
    summary = clawlet.conversation.get_summary()
    print(f"  📝 对话消息数: {summary['message_count']}")
    print(f"  📝 对话状态: {summary['state']}")
    print(f"  📝 近期话题: {summary['recent_topics']}")
    
    # ==================== 测试 4: 完整处理流程 ====================
    print("\n" + "=" * 70)
    print("🔄 测试 4: 完整处理流程")
    print("=" * 70)
    
    user_input = "帮我搜索 AI 相关的论文"
    result = clawlet.process(user_input)
    
    print(f"\n  👤 输入: {result['input']}")
    print(f"  🔒 安全: {result['safety']['level']}")
    print(f"  😊 情感: {result['sentiment']['sentiment']}")
    print(f"  🎯 意图: {result['intent']['description']} ({result['intent']['confidence']:.2f})")
    print(f"  🤖 响应: {result['response'][:50]}...")
    print(f"  🛠️  工具: {result['suggested_tools']}")
    
    # ==================== 测试 5: 系统状态 ====================
    print("\n" + "=" * 70)
    print("📊 测试 5: 系统状态")
    print("=" * 70)
    
    stats = clawlet.get_system_stats()
    
    print(f"\n  🦞 小爪系统 {stats['version']}")
    print(f"\n  📊 模块统计:")
    print(f"     • 安全检查: {stats['safety']['total_checks']}")
    print(f"     • 意图识别: {stats['intent']['total']}")
    print(f"     • 情感分析: {stats['sentiment']['total']}")
    print(f"     • 对话消息: {stats['conversation']['message_count']}")
    print(f"     • MiniMax 请求: {stats['minimax']['total_requests']}")
    
    print("\n" + "=" * 70)
    print("✅ 小爪系统 v2.0 测试完成！")
    print("=" * 70)
