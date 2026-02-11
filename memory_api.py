#!/usr/bin/env python3
"""
OpenClaw快速记忆访问API
集成JSON结构化记忆系统
"""

from structured_memory_system import StructuredMemory, MemorySearch

# 全局实例
_memory = None
_search = None

def get_memory() -> StructuredMemory:
    """获取记忆实例"""
    global _memory
    if _memory is None:
        _memory = StructuredMemory()
    return _memory

def get_search() -> MemorySearch:
    """获取搜索实例"""
    global _search
    if _search is None:
        _search = MemorySearch(get_memory())
    return _search

# 便捷函数
def update_context(key: str, value):
    """更新上下文"""
    get_memory().update_context(key, value)

def get_context(key: str, default=None):
    """获取上下文"""
    return get_memory().get_context(key, default)

def add_event(type: str, description: str, data: dict = None):
    """添加事件"""
    get_memory().add_event(type, description, data)

def add_entity(entity_type: str, entity_id: str, data: dict):
    """添加实体"""
    get_memory().add_entity(entity_type, entity_id, data)

def get_ai_context() -> str:
    """获取AI上下文"""
    return get_memory().get_context_for_ai()

def get_system_status() -> dict:
    """获取系统状态"""
    memory = get_memory()
    return {
        "session_id": memory.context.get("session_id"),
        "current_task": memory.context.get("current_task"),
        "entities_count": len(memory.entities),
        "events_count": len(memory.events.get("today", [])),
        "memory_size": memory.index.get("size_bytes", 0)
    }

if __name__ == "__main__":
    # 测试
    status = get_system_status()
    print("系统状态:", status)
