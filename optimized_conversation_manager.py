#!/usr/bin/env python3
"""
小爪优化对话管理器
集成JSON结构化记忆，快速上下文读取
"""

import json
import time
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
from structured_memory_system import StructuredMemory, MemorySearch, MemoryConfig

# ==================== 优化对话管理器 ====================

class OptimizedConversationManager:
    """优化版对话管理器"""
    
    def __init__(self):
        self.memory = StructuredMemory()
        self.search = MemorySearch(self.memory)
        
        # 配置
        self.max_context_size = 50000
        self.compression_threshold = 0.7
        
        # 统计
        self.stats = {
            "queries": 0,
            "cache_hits": 0,
            "avg_response_time": 0
        }
        
        # 初始化
        self._init_session()
    
    def _init_session(self):
        """初始化会话"""
        session_id = f"session_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.memory.start_session(session_id)
        self.memory.update_context("mode", "optimized")
        self.memory.add_event("system", "优化对话管理器启动", {"mode": "JSON结构化"})
    
    # ==================== 核心功能 ====================
    
    def process_message(self, message: str) -> Dict[str, Any]:
        """处理消息"""
        start_time = time.time()
        self.stats["queries"] += 1
        
        # 1. 快速检索上下文
        context = self._get_context(message)
        
        # 2. 提取关键信息
        entities = self._extract_entities(message)
        
        # 3. 生成响应
        response = self._generate_response(message, context, entities)
        
        # 4. 记录事件
        self.memory.add_event("message", message[:50], {
            "entities_found": len(entities),
            "response_length": len(response)
        })
        
        # 5. 更新统计
        response_time = time.time() - start_time
        self.stats["avg_response_time"] = (
            (self.stats["avg_response_time"] * (self.stats["queries"] - 1) + response_time)
            / self.stats["queries"]
        )
        
        return {
            "response": response,
            "context_used": context is not None,
            "entities_found": len(entities),
            "response_time": response_time
        }
    
    def _get_context(self, message: str) -> Optional[str]:
        """快速获取上下文"""
        # 搜索相关事件
        events = self.search.search_events(message)
        
        if events:
            self.stats["cache_hits"] += 1
            return json.dumps({"events": events}, ensure_ascii=False)
        
        # 返回AI上下文摘要
        return self.memory.get_context_for_ai(self.max_context_size)
    
    def _extract_entities(self, message: str) -> List[Dict]:
        """提取实体"""
        entities = []
        
        # 搜索项目
        for entity_type in ["projects", "systems", "documents"]:
            results = self.search.search_entities(message, entity_type)
            entities.extend(results)
        
        return entities
    
    def _generate_response(self, message: str, context: str, entities: List) -> str:
        """生成响应（集成到实际系统时替换为AI调用）"""
        # 这里返回结构化信息，实际使用时调用AI
        response_parts = []
        
        # 添加相关实体
        if entities:
            response_parts.append(f"📁 相关项目: {len(entities)} 个")
        
        # 添加上下文提示
        if context:
            response_parts.append("✅ 已加载上下文")
        
        # 生成响应
        if not response_parts:
            response_parts = ["收到消息，正在处理..."]
        
        return " | ".join(response_parts)
    
    # ==================== 快捷API ====================
    
    def set_task(self, task: str):
        """设置当前任务"""
        self.memory.update_context("current_task", task)
        self.memory.add_event("task", "设置当前任务", {"task": task})
    
    def complete_task(self, task: str, result: str):
        """完成任务"""
        self.memory.context["current_task"] = None
        completed = self.memory.get_context("completed_tasks", [])
        completed.append({
            "task": task,
            "result": result,
            "completed_at": datetime.now().isoformat()
        })
        self.memory.update_context("completed_tasks", completed)
        self.memory.add_event("task", "完成任务", {"task": task})
    
    def add_note(self, note: str):
        """添加笔记"""
        notes = self.memory.get_context("notes", [])
        notes.append({
            "note": note,
            "created_at": datetime.now().isoformat()
        })
        self.memory.update_context("notes", notes)
    
    def get_system_status(self) -> Dict:
        """获取系统状态"""
        return {
            "session_id": self.memory.context.get("session_id"),
            "current_task": self.memory.context.get("current_task"),
            "performance": {
                "total_queries": self.stats["queries"],
                "cache_hits": self.stats["cache_hits"],
                "hit_rate": f"{self.stats['cache_hits']/max(self.stats['queries'],1)*100:.1f}%",
                "avg_response_time": f"{self.stats['avg_response_time']*1000:.2f}ms"
            },
            "memory": self.memory.index,
            "entities": {
                "projects": len(self.memory.entities.get("projects", {})),
                "systems": len(self.memory.entities.get("systems", {}))
            },
            "recent_events": len(self.memory.events.get("today", []))
        }
    
    def clear_context(self):
        """清理上下文"""
        self.memory.clear_session()
        self._init_session()
        self.stats = {
            "queries": 0,
            "cache_hits": 0,
            "avg_response_time": 0
        }


# ==================== 性能测试 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 优化对话管理器测试")
    print("=" * 60)
    
    # 初始化
    manager = OptimizedConversationManager()
    
    print("\n📊 初始状态:")
    status = manager.get_system_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    # 性能测试
    print("\n⚡ 性能测试:")
    
    # 10次消息处理
    start = time.time()
    for i in range(10):
        result = manager.process_message(f"测试消息 {i}")
    total_time = time.time() - start
    
    print(f"   10次处理: {total_time*1000:.2f}ms")
    print(f"   平均响应: {total_time/10*1000:.2f}ms/次")
    
    # 上下文操作
    print("\n📝 上下文操作:")
    
    start = time.time()
    manager.set_task("视频制作")
    print(f"   设置任务: {(time.time()-start)*1000:.2f}ms")
    
    start = time.time()
    manager.add_note("测试笔记")
    print(f"   添加笔记: {(time.time()-start)*1000:.2f}ms")
    
    start = time.time()
    status = manager.get_system_status()
    print(f"   获取状态: {(time.time()-start)*1000:.2f}ms")
    
    print("\n📈 最终统计:")
    for key, value in manager.stats.items():
        print(f"   {key}: {value}")
    
    print("\n" + "=" * 60)
    print("✅ 优化对话管理器测试完成!")
    print("=" * 60)
