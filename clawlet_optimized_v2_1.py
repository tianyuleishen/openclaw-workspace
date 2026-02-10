#!/usr/bin/env python3
"""
小爪系统优化版 v2.1 - 基于硬件条件的性能优化
支持: 批处理、多级缓存、内存优化、异步并发、性能监控
"""

import asyncio
import aiohttp
import time
import hashlib
import pickle
import os
import sys
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from collections import OrderedDict
from datetime import datetime
import json

# ==================== 优化配置 ====================

@dataclass
class OptimizationConfig:
    """优化配置"""
    # 批处理配置
    batch_size: int = 4
    batch_timeout: float = 0.05  # 50ms 超时
    
    # 缓存配置
    l1_cache_size: int = 100  # L1 内存缓存大小
    l2_cache_dir: str = "/tmp/clawlet_cache"  # L2 磁盘缓存目录
    cache_ttl: int = 3600  # 缓存有效期 (秒)
    
    # 内存配置
    max_memory_usage: float = 0.7  # 最大内存使用率
    gc_interval: int = 100  # GC 间隔
    
    # 并发配置
    max_concurrent: int = 2  # 最大并发数 (基于 2CPU 核)
    
    # 监控配置
    enable_metrics: bool = True
    metrics_interval: float = 10.0  # 指标收集间隔


# ==================== 内存优化 ====================

class MemoryOptimizer:
    """内存优化器"""
    
    def __init__(self, max_usage: float = 0.7):
        self.max_usage = max_usage
        self.gc_count = 0
        
    def get_memory_usage(self) -> float:
        """获取当前内存使用率"""
        try:
            with open('/proc/memory_info', 'r') as f:
                lines = f.readlines()
                
                total = 0
                available = 0
                
                for line in lines:
                    if line.startswith('MemTotal:'):
                        total = int(line.split()[1]) * 1024  # KB
                    elif line.startswith('MemAvailable:'):
                        available = int(line.split()[1]) * 1024  # KB
                
                if total > 0:
                    return (total - available) / total
        
        except:
            pass
        
        return 0.5  # 默认 50%
    
    def should_gc(self) -> bool:
        """判断是否需要 GC"""
        return self.get_memory_usage() > self.max_usage
    
    def optimize(self):
        """执行内存优化"""
        if self.should_gc():
            import gc
            gc.collect()
            self.gc_count += 1
            
            # 清理内存
            if hasattr(sys, 'set_int_max_str_digits'):
                pass  # Python 3.14+ 优化
            
            return True
        return False
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            'usage_percent': self.get_memory_usage() * 100,
            'gc_count': self.gc_count
        }


# ==================== LRU 缓存 ====================

class LRUCache:
    """LRU 缓存实现"""
    
    def __init__(self, max_size: int = 100, ttl: int = 3600):
        self.max_size = max_size
        self.ttl = ttl
        self.cache = OrderedDict()  # {key: (value, timestamp)}
    
    def _is_expired(self, timestamp: float) -> bool:
        """检查是否过期"""
        return time.time() - timestamp > self.ttl
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        if key in self.cache:
            value, timestamp = self.cache[key]
            
            # 检查过期
            if self._is_expired(timestamp):
                del self.cache[key]
                return None
            
            # 移动到末尾 (LRU)
            self.cache.move_to_end(key)
            return value
        
        return None
    
    def set(self, key: str, value: Any):
        """设置缓存"""
        # 移除过期项
        if key in self.cache:
            del self.cache[key]
        
        # 检查容量
        while len(self.cache) >= self.max_size:
            # 移除最早的
            self.cache.popitem(last=False)
        
        # 添加新项
        self.cache[key] = (value, time.time())
    
    def clear(self):
        """清空缓存"""
        self.cache.clear()
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'ttl': self.ttl
        }


# ==================== 多级缓存系统 ====================

class MultiLevelCache:
    """多级缓存系统 (L1 内存 + L2 磁盘)"""
    
    def __init__(self, config: OptimizationConfig):
        self.config = config
        
        # L1 缓存 (内存)
        self.l1_cache = LRUCache(
            max_size=config.l1_cache_size,
            ttl=config.cache_ttl
        )
        
        # L2 缓存 (磁盘)
        self.l2_cache_dir = config.l2_cache_dir
        os.makedirs(self.l2_cache_dir, exist_ok=True)
        
        # 统计
        self.l1_hits = 0
        self.l2_hits = 0
        self.misses = 0
    
    def _hash_key(self, key: str) -> str:
        """生成缓存键的哈希"""
        return hashlib.md5(key.encode()).hexdigest()
    
    async def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        # L1 检查
        value = self.l1_cache.get(key)
        if value is not None:
            self.l1_hits += 1
            return value
        
        # L2 检查
        l2_key = self._hash_key(key)
        l2_path = f"{self.l2_cache_dir}/{l2_key}.pkl"
        
        if os.path.exists(l2_path):
            try:
                with open(l2_path, 'rb') as f:
                    value = pickle.load(f)
                
                # 提升到 L1
                self.l1_cache.set(key, value)
                self.l2_hits += 1
                return value
            except:
                pass
        
        self.misses += 1
        return None
    
    async def set(self, key: str, value: Any):
        """设置缓存"""
        # 优先设置到 L1
        self.l1_cache.set(key, value)
        
        # L1 满时写入 L2
        l1_stats = self.l1_cache.get_stats()
        if l1_stats['size'] >= l1_stats['max_size'] * 0.9:  # L1 接近满
            # 获取最早的项
            if self.l1_cache.cache:
                oldest_key, (oldest_value, _) = self.l1_cache.cache.popitem(last=False)
                
                # 写入 L2
                l2_key = self._hash_key(oldest_key)
                l2_path = f"{self.l2_cache_dir}/{l2_key}.pkl"
                
                try:
                    with open(l2_path, 'wb') as f:
                        pickle.dump(oldest_value, f)
                except:
                    pass
    
    def get_stats(self) -> Dict:
        """获取统计"""
        total = self.l1_hits + self.l2_hits + self.misses
        l1_rate = (self.l1_hits / max(total, 1)) * 100
        l2_rate = (self.l2_hits / max(total, 1)) * 100
        miss_rate = (self.misses / max(total, 1)) * 100
        
        return {
            'l1_size': self.l1_cache.get_stats()['size'],
            'l1_hits': self.l1_hits,
            'l2_hits': self.l2_hits,
            'misses': self.misses,
            'l1_hit_rate': f"{l1_rate:.1f}%",
            'l2_hit_rate': f"{l2_rate:.1f}%",
            'miss_rate': f"{miss_rate:.1f}%"
        }


# ==================== 动态批处理器 ====================

class DynamicBatcher:
    """动态批处理器"""
    
    def __init__(self, config: OptimizationConfig):
        self.config = config
        self.queue = []
        self.last_batch_time = time.time()
        self.total_batches = 0
        self.total_requests = 0
        self.batch_times = []
    
    async def add_request(self, request: Dict) -> Optional[List[Dict]]:
        """添加请求，返回批量结果"""
        self.queue.append({
            'request': request,
            'timestamp': time.time()
        })
        self.total_requests += 1
        
        # 检查是否满足批处理条件
        if len(self.queue) >= self.config.batch_size:
            return await self._process_batch()
        
        # 检查超时
        elapsed = time.time() - self.last_batch_time
        if elapsed >= self.config.batch_timeout:
            if self.queue:  # 至少有一个请求
                return await self._process_batch()
        
        return None
    
    async def _process_batch(self) -> List[Dict]:
        """处理批量请求"""
        if not self.queue:
            return []
        
        batch_start = time.time()
        batch = self.queue
        self.queue = []
        self.last_batch_time = time.time()
        self.total_batches += 1
        
        # 模拟批处理 (实际应用中会调用模型)
        results = []
        for item in batch:
            results.append({
                'request_id': item['request'].get('id', 'unknown'),
                'result': f"Processed: {item['request'].get('text', 'N/A')[:50]}",
                'batch_index': len(results)
            })
        
        batch_time = time.time() - batch_start
        self.batch_times.append(batch_time)
        
        return results
    
    def get_stats(self) -> Dict:
        """获取统计"""
        avg_batch_time = sum(self.batch_times) / max(len(self.batch_times), 1)
        
        return {
            'total_batches': self.total_batches,
            'total_requests': self.total_requests,
            'queue_size': len(self.queue),
            'avg_batch_time': f"{avg_batch_time*1000:.2f}ms",
            'avg_batch_size': self.total_requests / max(self.total_batches, 1)
        }


# ==================== 异步并发控制器 ====================

class ConcurrencyController:
    """并发控制器"""
    
    def __init__(self, max_concurrent: int = 2):
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.active_tasks = 0
        self.total_tasks = 0
        self.completed_tasks = 0
        self.total_latency = 0.0
    
    async def execute(self, coro) -> Any:
        """执行异步任务 (带并发控制)"""
        async with self.semaphore:
            start = time.time()
            self.active_tasks += 1
            self.total_tasks += 1
            
            try:
                result = await coro
                self.completed_tasks += 1
                latency = time.time() - start
                self.total_latency += latency
                return result
            except Exception as e:
                self.completed_tasks += 1
                raise e
            finally:
                self.active_tasks -= 1
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            'active': self.active_tasks,
            'total': self.total_tasks,
            'completed': self.completed_tasks,
            'avg_latency': f"{self.total_latency / max(self.completed_tasks, 1)*1000:.2f}ms",
            'throughput': self.completed_tasks / max(self.total_latency, 0.001)
        }


# ==================== API 连接池 ====================

class ConnectionPool:
    """API 连接池"""
    
    def __init__(self, max_connections: int = 5, max_per_host: int = 2):
        self.connector = aiohttp.TCPConnector(
            limit=max_connections,
            limit_per_host=max_per_host,
            ttl_dns_cache=300,
            keepalive_timeout=30
        )
        self.session = None
        self.request_count = 0
        self.error_count = 0
    
    async def get_session(self) -> aiohttp.ClientSession:
        """获取会话"""
        if not self.session or self.session.closed:
            self.session = aiohttp.ClientSession(
                connector=self.connector,
                timeout=aiohttp.ClientTimeout(total=30)
            )
        return self.session
    
    async def request(self, method: str, url: str, **kwargs) -> Dict:
        """发起请求"""
        try:
            session = await self.get_session()
            async with session.request(method, url, **kwargs) as response:
                self.request_count += 1
                return {
                    'status': response.status,
                    'data': await response.json() if response.headers.get('content-type', '').startswith('application/json') else await response.text()
                }
        except Exception as e:
            self.error_count += 1
            return {'error': str(e)}
    
    async def close(self):
        """关闭连接池"""
        if self.session and not self.session.closed:
            await self.session.close()
    
    def get_stats(self) -> Dict:
        """获取统计"""
        total = self.request_count + self.error_count
        error_rate = (self.error_count / max(total, 1)) * 100
        
        return {
            'requests': self.request_count,
            'errors': self.error_count,
            'error_rate': f"{error_rate:.1f}%"
        }


# ==================== 性能监控器 ====================

class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        self.start_time = time.time()
        self.metrics = {
            'requests': 0,
            'successful': 0,
            'failed': 0,
            'total_latency': 0.0,
            'min_latency': float('inf'),
            'max_latency': 0.0,
            'batch_count': 0,
            'cache_hits': 0,
            'cache_misses': 0
        }
        self.latencies = []
    
    def record(self, success: bool, latency: float, cached: bool = False, batched: bool = False):
        """记录指标"""
        self.metrics['requests'] += 1
        
        if success:
            self.metrics['successful'] += 1
        else:
            self.metrics['failed'] += 1
        
        self.metrics['total_latency'] += latency
        self.latencies.append(latency)
        
        if latency < self.metrics['min_latency']:
            self.metrics['min_latency'] = latency
        
        if latency > self.metrics['max_latency']:
            self.metrics['max_latency'] = latency
        
        if cached:
            self.metrics['cache_hits'] += 1
        else:
            self.metrics['cache_misses'] += 1
    
    def get_stats(self) -> Dict:
        """获取统计"""
        uptime = time.time() - self.start_time
        total = self.metrics['requests']
        successful = self.metrics['successful']
        
        # 计算 P50, P90, P99
        sorted_latencies = sorted(self.latencies) if self.latencies else [0]
        p50 = sorted_latencies[int(len(sorted_latencies) * 0.50)]
        p90 = sorted_latencies[int(len(sorted_latencies) * 0.90)]
        p99 = sorted_latencies[int(len(sorted_latencies) * 0.99)]
        
        return {
            'uptime': f"{uptime:.1f}s",
            'total_requests': total,
            'successful': successful,
            'failed': self.metrics['failed'],
            'success_rate': f"{(successful / max(total, 1)) * 100:.1f}%",
            'latency': {
                'avg': f"{(self.metrics['total_latency'] / max(total, 1)) * 1000:.2f}ms",
                'min': f"{self.metrics['min_latency'] * 1000:.2f}ms",
                'max': f"{self.metrics['max_latency'] * 1000:.2f}ms",
                'p50': f"{p50 * 1000:.2f}ms",
                'p90': f"{p90 * 1000:.2f}ms",
                'p99': f"{p99 * 1000:.2f}ms"
            },
            'cache': {
                'hits': self.metrics['cache_hits'],
                'misses': self.metrics['cache_misses'],
                'hit_rate': f"{(self.metrics['cache_hits'] / max(self.metrics['cache_hits'] + self.metrics['cache_misses'], 1)) * 100:.1f}%"
            },
            'throughput': f"{total / max(uptime, 0.001):.2f} req/s"
        }


# ==================== 优化后的小爪系统 ====================

class ClawletOptimized:
    """优化后的小爪系统"""
    
    def __init__(self, config: OptimizationConfig = None):
        self.config = config or OptimizationConfig()
        
        # 初始化各优化组件
        self.memory_optimizer = MemoryOptimizer(max_usage=self.config.max_memory_usage)
        self.cache = MultiLevelCache(self.config)
        self.batcher = DynamicBatcher(self.config)
        self.concurrency = ConcurrencyController(self.config.max_concurrent)
        self.connection_pool = ConnectionPool()
        self.monitor = PerformanceMonitor()
        
        # 版本
        self.version = "v2.1"
        
        # 初始化
        self._init_system()
    
    def _init_system(self):
        """初始化系统"""
        print(f"\n{'='*80}")
        print(f"🦞 小爪系统优化版 {self.version}")
        print(f"{'='*80}")
        print("\n✅ 初始化优化组件:")
        print(f"   • 批处理器 (batch_size={self.config.batch_size})")
        print(f"   • 多级缓存 (L1={self.config.l1_cache_size}, L2={self.config.l2_cache_dir})")
        print(f"   • 内存优化 (max_usage={self.config.max_memory_usage*100}%)")
        print(f"   • 并发控制 (max_concurrent={self.config.max_concurrent})")
        print(f"   • 性能监控 (interval={self.config.metrics_interval}s)")
        print(f"\n{'='*80}\n")
    
    async def process_request(self, request: Dict) -> Dict:
        """
        处理请求 (优化版)
        
        流程: 缓存检查 → 批处理 → 并发执行 → 缓存存储 → 监控记录
        """
        start_time = time.time()
        request_text = request.get('text', '')
        
        # 1. 缓存检查
        cache_key = hashlib.md5(request_text.encode()).hexdigest()
        cached_result = await self.cache.get(cache_key)
        
        if cached_result:
            latency = time.time() - start_time
            self.monitor.record(
                success=True,
                latency=latency,
                cached=True,
                batched=False
            )
            
            return {
                'result': cached_result,
                'cached': True,
                'latency': latency
            }
        
        # 2. 批处理
        batch_results = await self.batcher.add_request(request)
        
        if batch_results:
            # 批量处理完成
            batch_latency = time.time() - start_time
            
            # 存储第一批结果到缓存
            for item in batch_results:
                result_text = item.get('result', '')
                if result_text:
                    result_key = hashlib.md5(result_text.encode()).hexdigest()
                    await self.cache.set(result_key, result_text)
            
            self.monitor.record(
                success=True,
                latency=batch_latency,
                cached=False,
                batched=True
            )
            
            return {
                'batch_results': batch_results,
                'batch_size': len(batch_results),
                'cached': False,
                'batched': True,
                'latency': batch_latency
            }
        
        # 3. 并发执行 (单个请求)
        async def single_infer():
            # 模拟推理
            await asyncio.sleep(0.01)  # 10ms 模拟延迟
            return f"Processed: {request_text[:100]}"
        
        result = await self.concurrency.execute(single_infer())
        
        # 4. 存储到缓存
        await self.cache.set(cache_key, result)
        
        latency = time.time() - start_time
        self.monitor.record(
            success=True,
            latency=latency,
            cached=False,
            batched=False
        )
        
        return {
            'result': result,
            'cached': False,
            'batched': False,
            'latency': latency
        }
    
    def get_system_stats(self) -> Dict:
        """获取系统状态"""
        return {
            'version': self.version,
            'memory': self.memory_optimizer.get_stats(),
            'cache': self.cache.get_stats(),
            'batcher': self.batcher.get_stats(),
            'concurrency': self.concurrency.get_stats(),
            'connection_pool': self.connection_pool.get_stats(),
            'performance': self.monitor.get_stats()
        }
    
    async def health_check(self) -> Dict:
        """健康检查"""
        memory_stats = self.memory_optimizer.get_stats()
        
        return {
            'status': 'healthy' if memory_stats['usage_percent'] < 90 else 'warning',
            'memory_usage': f"{memory_stats['usage_percent']:.1f}%",
            'uptime': self.monitor.get_stats()['uptime'],
            'cache_status': self.cache.get_stats()['l1_size'] > 0
        }


# ==================== 性能测试 ====================

async def run_performance_test():
    """运行性能测试"""
    print("\n" + "="*80)
    print("🚀 性能测试")
    print("="*80 + "\n")
    
    # 初始化系统
    clawlet = ClawletOptimized()
    
    # 测试请求
    test_requests = [
        {'id': f'req_{i}', 'text': f'Test request number {i}'}
        for i in range(20)
    ]
    
    print(f"📤 发送 {len(test_requests)} 个测试请求...\n")
    
    # 并发发送请求
    start_time = time.time()
    
    results = []
    for request in test_requests:
        result = await clawlet.process_request(request)
        results.append(result)
        
        # 显示进度
        if len(results) % 5 == 0:
            print(f"  已完成: {len(results)}/{len(test_requests)}")
    
    total_time = time.time() - start_time
    
    # 统计结果
    cached_count = sum(1 for r in results if r.get('cached'))
    batched_count = sum(1 for r in results if r.get('batched'))
    total_latency = sum(r.get('latency', 0) for r in results)
    
    print("\n" + "="*80)
    print("📊 测试结果")
    print("="*80)
    
    print(f"\n✅ 成功处理: {len(results)}/{len(test_requests)}")
    print(f"⏱️  总耗时: {total_time:.2f}s")
    print(f"📈 平均延迟: {total_latency/len(results)*1000:.2f}ms")
    print(f"🚀 吞吐量: {len(test_requests)/max(total_time, 0.001):.2f} req/s")
    print(f"\n💾 缓存命中: {cached_count}")
    print(f"📦 批处理: {batched_count}")
    
    # 显示系统状态
    print("\n" + "="*80)
    print("📊 系统状态")
    print("="*80)
    
    stats = clawlet.get_system_stats()
    
    print(f"\n🦞 小爪系统 {stats['version']}")
    print(f"\n💾 内存:")
    print(f"   • 使用率: {stats['memory']['usage_percent']:.1f}%")
    print(f"   • GC次数: {stats['memory']['gc_count']}")
    
    print(f"\n💾 缓存:")
    print(f"   • L1 大小: {stats['cache']['l1_size']}")
    print(f"   • L1 命中: {stats['cache']['l1_hits']}")
    print(f"   • L2 命中: {stats['cache']['l2_hits']}")
    print(f"   • 命中率: {stats['cache']['l1_hit_rate']}")
    
    print(f"\n📦 批处理:")
    print(f"   • 批次数: {stats['batcher']['total_batches']}")
    print(f"   • 平均大小: {stats['batcher']['avg_batch_size']:.1f}")
    
    print(f"\n⚡ 并发:")
    print(f"   • 完成任务: {stats['concurrency']['completed']}")
    print(f"   • 平均延迟: {stats['concurrency']['avg_latency']}")
    
    print(f"\n📈 性能:")
    perf = stats['performance']
    print(f"   • 吞吐量: {perf['throughput']}")
    print(f"   • 成功率: {perf['success_rate']}")
    print(f"   • P50延迟: {perf['latency']['p50']}")
    print(f"   • P99延迟: {perf['latency']['p99']}")
    
    print("\n" + "="*80)
    print("✅ 性能测试完成！")
    print("="*80 + "\n")
    
    return clawlet


# ==================== 主函数 ====================

if __name__ == "__main__":
    import asyncio
    
    # 运行性能测试
    asyncio.run(run_performance_test())
