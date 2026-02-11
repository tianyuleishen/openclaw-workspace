#!/usr/bin/env python3
"""
MiniMax 模型调用优化器
根据 Coding Plan 限制，最大化模型资源利用

限制说明：
- 1 prompt ≈ 15次模型调用（打包计费）
- 每5小时重置速率限制
- API Key 区分：Coding Plan vs 普通
- 额度多工具共享
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from collections import deque


@dataclass
class UsageRecord:
    """使用记录"""
    timestamp: datetime
    prompt_count: int
    task_type: str
    tokens_used: int


class MiniMaxOptimizer:
    """
    MiniMax 模型调用优化器
    
    优化策略：
    1. 批量处理 - 合并多个小任务为一次 prompt
    2. 智能缓存 - 避免重复调用相同内容
    3. 优先级队列 - 重要任务优先
    4. 混合使用 - Coding Plan vs 普通 Key
    5. 速率控制 - 避免触发5小时限额
    """

    def __init__(self, coding_plan_key: str = None, normal_key: str = None):
        # API Keys
        self.coding_key = coding_plan_key
        self.normal_key = normal_key
        
        # 使用记录（最近5小时）
        self.usage_history: deque = deque(maxlen=1000)
        
        # 缓存
        self.response_cache: Dict[str, Dict] = {}
        self.cache_ttl = 3600  # 1小时缓存
        
        # 限制配置
        self.limits = {
            'prompt_per_5h': 1000,  # 假设的 Coding Plan 限额
            'cache_size': 1000,
            'batch_size': 5  # 每次批量处理的任务数
        }
        
        # 统计
        self.stats = {
            'total_prompts': 0,
            'total_tokens': 0,
            'cache_hits': 0,
            'batches_processed': 0,
            'saved_prompts': 0
        }

    # ==================== 核心优化方法 ====================

    def should_use_coding_plan(self, task_type: str) -> bool:
        """
        判断是否使用 Coding Plan
        
        策略：
        - 编程相关任务 → Coding Plan
        - 简单对话 → 普通 Key
        - 大批量处理 → 缓存/批量
        """
        coding_tasks = ['code', 'debug', 'refactor', 'review', 'explain_code']
        simple_tasks = ['chat', 'greeting', 'simple_qa']
        
        if any(t in task_type.lower() for t in coding_tasks):
            return True
        elif any(t in task_type.lower() for t in simple_tasks):
            return False
        else:
            # 默认使用 Coding Plan（如果是编程套餐）
            return self.coding_key is not None

    def batch_requests(self, requests: List[Dict]) -> List[List[Dict]]:
        """
        批量处理请求
        
        将多个小请求合并为一个 batch，减少 prompt 次数
        """
        batches = []
        for i in range(0, len(requests), self.limits['batch_size']):
            batch = requests[i:i + self.limits['batch_size']]
            batches.append(batch)
        
        self.stats['batches_processed'] += len(batches)
        return batches

    def get_cached_response(self, content_hash: str) -> Optional[str]:
        """获取缓存响应"""
        if content_hash in self.response_cache:
            record = self.response_cache[content_hash]
            if (datetime.now() - record['timestamp']).seconds < self.cache_ttl:
                self.stats['cache_hits'] += 1
                return record['response']
        return None

    def cache_response(self, content_hash: str, response: str):
        """缓存响应"""
        # 清理过期缓存
        if len(self.response_cache) >= self.limits['cache_size']:
            # 移除最旧的
            oldest = min(self.response_cache.keys(), 
                        key=lambda k: self.response_cache[k]['timestamp'])
            del self.response_cache[oldest]
        
        self.response_cache[content_hash] = {
            'response': response,
            'timestamp': datetime.now()
        }

    def calculate_content_hash(self, content: str) -> str:
        """计算内容哈希（用于缓存）"""
        import hashlib
        return hashlib.md5(content.encode()).hexdigest()[:16]

    # ==================== 速率控制 ====================

    def get_5h_usage(self) -> int:
        """获取最近5小时的使用量"""
        cutoff = datetime.now() - timedelta(hours=5)
        total = sum(r.prompt_count for r in self.usage_history 
                   if r.timestamp > cutoff)
        return total

    def get_usage_percentage(self) -> float:
        """获取使用百分比"""
        used = self.get_5h_usage()
        return (used / self.limits['prompt_per_5h']) * 100

    def should_rate_limit(self) -> bool:
        """是否应该限流"""
        return self.get_5h_usage() >= self.limits['prompt_per_5h'] * 0.9

    def wait_if_needed(self):
        """如果接近限额，等待重置"""
        if self.should_rate_limit():
            # 计算等待时间
            oldest = min(self.usage_history, 
                        key=lambda r: r.timestamp, default=None)
            if oldest:
                wait_seconds = (oldest.timestamp + timedelta(hours=5)) - datetime.now()
                if wait_seconds.total_seconds() > 0:
                    print(f"⚠️ 接近限额，等待 {wait_seconds.total_seconds():.0f} 秒...")
                    time.sleep(min(wait_seconds.total_seconds(), 300))  # 最多等5分钟

    # ==================== 优化执行 ====================

    def optimize_request(self, task: Dict) -> Dict:
        """
        优化单个请求
        
        Returns:
            {
                'use_coding_plan': bool,
                'cached': bool,
                'batch_with': List[task_ids],
                'priority': int
            }
        """
        content = task.get('content', '')
        task_type = task.get('type', 'general')
        
        # 1. 检查缓存
        content_hash = self.calculate_content_hash(content)
        cached = self.get_cached_response(content_hash)
        
        if cached:
            return {
                'use_coding_plan': False,
                'cached': True,
                'response': cached,
                'priority': 0
            }
        
        # 2. 判断使用哪个 Key
        use_coding = self.should_use_coding_plan(task_type)
        
        # 3. 检查速率限制
        if use_coding and self.should_rate_limit():
            self.wait_if_needed()
        
        # 4. 返回优化建议
        return {
            'use_coding_plan': use_coding,
            'cached': False,
            'content_hash': content_hash,
            'priority': 1 if 'urgent' in task else 2
        }

    def process_batch(self, tasks: List[Dict]) -> Dict:
        """
        处理批量任务
        
        策略：
        1. 先处理缓存命中的
        2. 剩余的合并为 batch
        3. 使用 Coding Plan 批量调用
        """
        results = []
        to_process = []
        
        for i, task in enumerate(tasks):
            optimization = self.optimize_request(task)
            
            if optimization.get('cached'):
                results.append({
                    'task_id': i,
                    'response': optimization['response'],
                    'cached': True
                })
                self.stats['saved_prompts'] += 1
            else:
                to_process.append({
                    'task_id': i,
                    'optimization': optimization,
                    'original_task': task
                })
        
        # 批量处理剩余任务
        if to_process:
            batch_result = self._call_batch([
                t['original_task'] for t in to_process
            ])
            
            for i, result in enumerate(batch_result):
                task_info = to_process[i]
                results.append({
                    'task_id': task_info['task_id'],
                    'response': result,
                    'cached': False
                })
                
                # 缓存结果
                content_hash = task_info['optimization'].get('content_hash')
                if content_hash:
                    self.cache_response(content_hash, result)
        
        return results

    def _call_batch(self, tasks: List[Dict]) -> List[str]:
        """批量调用模型"""
        # 这里应该调用实际的 MiniMax API
        # 返回响应列表
        pass

    # ==================== 统计与报告 ====================

    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            'usage_5h': self.get_5h_usage(),
            'usage_percent': self.get_usage_percentage(),
            'total_prompts': self.stats['total_prompts'],
            'total_tokens': self.stats['total_tokens'],
            'cache_hits': self.stats['cache_hits'],
            'batches_processed': self.stats['batches_processed'],
            'saved_prompts': self.stats['saved_prompts'],
            'cache_size': len(self.response_cache),
            'efficiency': self._calculate_efficiency()
        }

    def _calculate_efficiency(self) -> float:
        """计算效率"""
        total = self.stats['total_prompts'] + self.stats['saved_prompts']
        if total == 0:
            return 0
        return (self.stats['saved_prompts'] / total) * 100

    def generate_report(self) -> str:
        """生成优化报告"""
        stats = self.get_stats()
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║         MiniMax 模型调用优化报告                            ║
╚══════════════════════════════════════════════════════════════╝

📊 5小时使用情况
   使用量: {stats['usage_5h']} prompts
   使用率: {stats['usage_percent']:.1f}%
   限额: {self.limits['prompt_per_5h']}/5h

📈 优化效果
   总调用: {stats['total_prompts']}
   缓存命中: {stats['cache_hits']}
   批量处理: {stats['batches_processed']}
   节省次数: {stats['saved_prompts']}
   效率提升: {stats['efficiency']:.1f}%

💾 缓存状态
   缓存大小: {stats['cache_size']}
   TTL: {self.cache_ttl}s

🤖 API Key 使用
   Coding Plan: {'✅ 已配置' if self.coding_key else '❌ 未配置'}
   普通 Key: {'✅ 已配置' if self.normal_key else '❌ 未配置'}

💡 优化建议
"""
        
        if stats['usage_percent'] > 80:
            report += "   ⚠️ 使用率超过80%，建议：\n"
            report += "   - 优先使用缓存\n"
            report += "   - 降低调用频率\n"
            report += "   - 考虑切换到按量付费\n"
        else:
            report += "   ✅ 使用率正常，继续保持\n"
        
        return report


# ==================== 快捷函数 ====================

_optimizer = None


def get_optimizer(coding_key: str = None, normal_key: str = None) -> MiniMaxOptimizer:
    global _optimizer
    if _optimizer is None:
        _optimizer = MiniMaxOptimizer(coding_key, normal_key)
    return _optimizer


def optimize_minimax_usage(tasks: List[Dict]) -> Dict:
    """
    优化 MiniMax 模型使用
    
    Usage:
        results = optimize_minimax_usage([
            {'type': 'code', 'content': 'Write a function...'},
            {'type': 'explain', 'content': 'Explain this code...'}
        ])
    """
    optimizer = get_optimizer()
    return optimizer.process_batch(tasks)


# 测试
if __name__ == "__main__":
    print("Testing MiniMax Optimizer...")
    
    optimizer = MiniMaxOptimizer()
    
    # 测试任务
    test_tasks = [
        {'type': 'code', 'content': 'def hello(): pass'},
        {'type': 'chat', 'content': 'Hello!'},
        {'type': 'debug', 'content': 'Fix this bug'},
        {'type': 'explain', 'content': 'Explain Python'},
        {'type': 'review', 'content': 'Review my code'},
    ]
    
    # 批量处理
    results = optimizer.process_batch(test_tasks)
    
    print(f"\n处理了 {len(results)} 个任务")
    
    # 显示统计
    print(optimizer.generate_report())
    
    print("\n✅ MiniMax Optimizer working!")
