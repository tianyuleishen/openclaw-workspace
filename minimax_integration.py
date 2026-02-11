#!/usr/bin/env python3
"""
MiniMax API 集成 - 优化器
结合 API Key 使用 MiniMax 模型
"""

import os
import sys
import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import deque
from dataclasses import dataclass


# ==================== API 配置 ====================

class MiniMaxAPI:
    """MiniMax API 封装"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or self._load_key()
        self.base_url = "https://api.minimaxi.com/v1"
        
        # 使用统计
        self.request_count = 0
        self.error_count = 0
        self.total_tokens = 0
        self.last_request = None
        
        # 速率限制跟踪
        self.usage_5h = deque(maxlen=100)
    
    def _load_key(self):
        """加载 API Key"""
        key = os.environ.get('MINIMAX_API_KEY')
        if key:
            return key
        try:
            with open('/home/admin/.openclaw/workspace/.env', 'r') as f:
                for line in f:
                    if line.startswith('MINIMAX_API_KEY='):
                        return line.strip().split('=')[1].strip()
        except:
            pass
        return None
    
    def chat(self, messages: List[Dict], model: str = "MiniMax-M2.1",
             max_tokens: int = 1000, temperature: float = 0.7) -> Dict:
        """
        发送聊天请求
        
        Args:
            messages: [{"role": "user", "content": "..."}]
            model: 模型名称
            max_tokens: 最大输出 tokens
            temperature: 温度参数
        
        Returns:
            API 响应
        """
        if not self.api_key:
            return {"error": "API Key 未配置"}
        
        url = f"{self.base_url}/chat/completions"
        
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        data = json.dumps(payload).encode('utf-8')
        
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
        )
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                # 更新统计
                self.request_count += 1
                self.last_request = datetime.now()
                
                # 记录使用量
                if 'usage' in result:
                    tokens = result['usage'].get('total_tokens', 0)
                    self.total_tokens += tokens
                    self.usage_5h.append({
                        'time': datetime.now(),
                        'tokens': tokens
                    })
                
                return result
                
        except Exception as e:
            self.error_count += 1
            return {"error": str(e)}
    
    def simple_chat(self, user_input: str, system_prompt: str = None) -> str:
        """
        简单对话
        
        Args:
            user_input: 用户输入
            system_prompt: 系统提示（可选）
        
        Returns:
            助手回复
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": user_input})
        
        result = self.chat(messages)
        
        if 'error' in result:
            return f"❌ 错误: {result['error']}"
        
        return result['choices'][0]['message']['content']
    
    def get_stats(self) -> Dict:
        """获取使用统计"""
        # 计算5小时使用量
        cutoff = datetime.now() - timedelta(hours=5)
        usage_5h = sum(u['tokens'] for u in self.usage_5h if u['time'] > cutoff)
        
        return {
            "total_requests": self.request_count,
            "total_tokens": self.total_tokens,
            "tokens_5h": usage_5h,
            "errors": self.error_count,
            "last_request": self.last_request.isoformat() if self.last_request else None
        }


# ==================== 优化器 ====================

class MiniMaxOptimizer:
    """MiniMax 调用优化器"""
    
    def __init__(self, api_key: str = None):
        self.api = MiniMaxAPI(api_key)
        self.cache = {}
        self.cache_ttl = 3600  # 1小时
    
    def chat_with_cache(self, user_input: str, system_prompt: str = None) -> Dict:
        """
        带缓存的对话
        
        Returns:
            {
                "response": str,
                "cached": bool,
                "tokens": int,
                "cost_saved": bool
            }
        """
        # 检查缓存
        cache_key = self._hash_content(f"{system_prompt}:{user_input}")
        
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            if (datetime.now() - cached['time']).seconds < self.cache_ttl:
                return {
                    "response": cached['response'],
                    "cached": True,
                    "tokens": 0,
                    "cost_saved": True
                }
        
        # 调用 API
        result = self.api.simple_chat(user_input, system_prompt)
        
        if not result.startswith("❌"):
            self.cache[cache_key] = {
                'response': result,
                'time': datetime.now()
            }
        
        return {
            "response": result,
            "cached": False,
            "tokens": self.api.total_tokens,
            "cost_saved": False
        }
    
    def batch_chat(self, conversations: List[Dict], batch_size: int = 5) -> List[Dict]:
        """
        批量对话
        
        Args:
            conversations: [{"role": "user", "content": "..."}]
            batch_size: 批量大小
        
        Returns:
            回复列表
        """
        results = []
        
        for i in range(0, len(conversations), batch_size):
            batch = conversations[i:i + batch_size]
            batch_result = []
            
            for conv in batch:
                result = self.chat_with_cache(
                    conv['content'],
                    conv.get('system')
                )
                batch_result.append(result)
            
            results.extend(batch_result)
        
        return results
    
    def _hash_content(self, content: str) -> str:
        """内容哈希"""
        import hashlib
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    def get_usage_report(self) -> str:
        """生成使用报告"""
        stats = self.api.get_stats()
        
        return f"""
╔══════════════════════════════════════════════════════╗
║     MiniMax API 使用报告                           ║
╚══════════════════════════════════════════════════════╝

📊 总体统计
   总请求数: {stats['total_requests']}
   总 Tokens: {stats['total_tokens']:,}
   错误次数: {stats['errors']}
   最后请求: {stats['last_request'] or '无'}

📈 5小时统计
   Tokens: {stats['tokens_5h']:,}

💾 缓存状态
   缓存条目: {len(self.cache)}
   TTL: {self.cache_ttl}s
        """
    
    def optimize_and_chat(self, user_input: str, task_type: str = "general") -> Dict:
        """
        优化并对话
        
        Args:
            user_input: 用户输入
            task_type: 任务类型 (coding/simple/general)
        
        Returns:
            优化结果
        """
        # 根据任务类型选择策略
        if task_type == "coding":
            system_prompt = "你是一个专业的编程助手，提供清晰、高效的代码解决方案。"
        elif task_type == "simple":
            system_prompt = "你是一个简洁的助手，回答要简短有力。"
        else:
            system_prompt = None
        
        # 调用
        result = self.chat_with_cache(user_input, system_prompt)
        
        return {
            "response": result['response'],
            "cached": result['cached'],
            "task_type": task_type,
            "tokens_used": result['tokens']
        }


# ==================== 全局实例 ====================

_api = None
_optimizer = None


def get_minimax_api() -> MiniMaxAPI:
    """获取 API 实例"""
    global _api
    if _api is None:
        _api = MiniMaxAPI()
    return _api


def get_minimax_optimizer() -> MiniMaxOptimizer:
    """获取优化器实例"""
    global _optimizer
    if _optimizer is None:
        _optimizer = MiniMaxOptimizer()
    return _optimizer


# ==================== 测试 ====================

if __name__ == "__main__":
    print("Testing MiniMax API Integration...")
    
    api = get_minimax_api()
    optimizer = get_minimax_optimizer()
    
    # 测试简单对话
    print("\n1️⃣ 简单对话测试:")
    result = optimizer.optimize_and_chat(
        "用一句话介绍你自己",
        task_type="simple"
    )
    print(f"   回复: {result['response']}")
    print(f"   缓存: {result['cached']}")
    
    # 测试编程任务
    print("\n2️⃣ 编程任务测试:")
    result = optimizer.optimize_and_chat(
        "写一个 Python 函数，计算斐波那契数列",
        task_type="coding"
    )
    print(f"   回复: {result['response'][:100]}...")
    print(f"   任务类型: {result['task_type']}")
    
    # 打印报告
    print(optimizer.get_usage_report())
    
    print("\n✅ MiniMax Integration working!")
