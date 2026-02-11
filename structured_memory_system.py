#!/usr/bin/env python3
"""
小爪JSON结构化记忆系统
快速读取上下文内容，优化性能
"""

import json
import os
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

# ==================== 配置 ====================

class MemoryConfig:
    """记忆配置"""
    MEMORY_DIR = "/home/admin/.openclaw/workspace/memory/structured"
    CONTEXT_FILE = "context.json"
    ENTITIES_FILE = "entities.json"
    RELATIONS_FILE = "relations.json"
    EVENTS_FILE = "events.json"
    MAX_CONTEXT_SIZE = 50000  # 最大上下文50KB
    INDEX_FILE = "memory_index.json"


# ==================== 结构化记忆 ====================

class StructuredMemory:
    """JSON结构化记忆系统"""
    
    def __init__(self, config: MemoryConfig = None):
        self.config = config or MemoryConfig()
        self.memory_dir = Path(self.config.MEMORY_DIR)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化存储
        self.context = self._load_json(self.config.CONTEXT_FILE)
        self.entities = self._load_json(self.config.ENTITIES_FILE)
        self.relations = self._load_json(self.config.RELATIONS_FILE)
        self.events = self._load_json(self.config.EVENTS_FILE)
        self.index = self._load_json(self.config.INDEX_FILE)
        
        # 初始化结构
        if not self.context:
            self.context = {
                "session_id": None,
                "created_at": None,
                "updated_at": None,
                "user_info": {},
                "system_state": {},
                "current_task": None,
                "pending_actions": [],
                "completed_tasks": [],
                "notes": []
            }
        
        if not self.entities:
            self.entities = {
                "users": {},
                "projects": {},
                "systems": {},
                "documents": {}
            }
        
        if not self.relations:
            self.relations = {
                "project_docs": [],
                "user_projects": [],
                "system_tasks": []
            }
        
        if not self.events:
            self.events = {
                "today": [],
                "recent": []
            }
        
        if not self.index:
            self.index = {
                "last_update": None,
                "context_hash": None,
                "size_bytes": 0,
                "entries_count": 0
            }
    
    def _load_json(self, filename: str) -> dict:
        """加载JSON文件"""
        filepath = self.memory_dir / filename
        if filepath.exists():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_json(self, filename: str, data: dict):
        """保存JSON文件"""
        filepath = self.memory_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _update_index(self):
        """更新索引"""
        total_size = 0
        total_entries = 0
        
        for filename in [self.config.CONTEXT_FILE, self.config.ENTITIES_FILE, 
                        self.config.RELATIONS_FILE, self.config.EVENTS_FILE]:
            filepath = self.memory_dir / filename
            if filepath.exists():
                total_size += filepath.stat().st_size
                total_entries += len(self._load_json(filename))
        
        self.index = {
            "last_update": datetime.now().isoformat(),
            "context_hash": hashlib.md5(json.dumps(self.context).encode()).hexdigest()[:16],
            "size_bytes": total_size,
            "entries_count": total_entries
        }
        
        self._save_json(self.config.INDEX_FILE, self.index)
    
    # ==================== 核心API ====================
    
    def start_session(self, session_id: str):
        """开始新会话"""
        self.context["session_id"] = session_id
        self.context["created_at"] = datetime.now().isoformat()
        self.context["updated_at"] = datetime.now().isoformat()
        self._save_all()
    
    def update_context(self, key: str, value: Any):
        """更新上下文"""
        self.context[key] = value
        self.context["updated_at"] = datetime.now().isoformat()
        self._save_all()
    
    def get_context(self, key: str, default=None) -> Any:
        """快速读取上下文"""
        return self.context.get(key, default)
    
    def add_entity(self, entity_type: str, entity_id: str, data: Dict):
        """添加实体"""
        if entity_type not in self.entities:
            self.entities[entity_type] = {}
        
        self.entities[entity_type][entity_id] = {
            "data": data,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self._save_all()
    
    def get_entity(self, entity_type: str, entity_id: str) -> Optional[Dict]:
        """获取实体"""
        return self.entities.get(entity_type, {}).get(entity_id)
    
    def add_event(self, event_type: str, description: str, data: Dict = None):
        """添加事件"""
        event = {
            "type": event_type,
            "description": description,
            "data": data or {},
            "timestamp": datetime.now().isoformat()
        }
        
        self.events["today"].append(event)
        
        # 保持最近30条
        if len(self.events["today"]) > 30:
            self.events["today"] = self.events["today"][-30:]
        
        self._save_all()
    
    def add_relation(self, relation_type: str, source: str, target: str, data: Dict = None):
        """添加关系"""
        relation = {
            "type": relation_type,
            "source": source,
            "target": target,
            "data": data or {},
            "created_at": datetime.now().isoformat()
        }
        self.relations["project_docs"].append(relation)
        self._save_all()
    
    def _save_all(self):
        """保存所有数据"""
        self._save_json(self.config.CONTEXT_FILE, self.context)
        self._save_json(self.config.ENTITIES_FILE, self.entities)
        self._save_json(self.config.RELATIONS_FILE, self.relations)
        self._save_json(self.config.EVENTS_FILE, self.events)
        self._update_index()
    
    def get_summary(self) -> Dict:
        """获取摘要"""
        return {
            "session": self.context.get("session_id"),
            "created": self.context.get("created_at"),
            "updated": self.context.get("updated_at"),
            "user": self.context.get("user_info", {}).get("name"),
            "task": self.context.get("current_task"),
            "entities": {
                "users": len(self.entities.get("users", {})),
                "projects": len(self.entities.get("projects", {})),
                "systems": len(self.entities.get("systems", {}))
            },
            "events_today": len(self.events.get("today", [])),
            "index": self.index
        }
    
    def get_context_for_ai(self, max_size: int = None) -> str:
        """获取AI可读的上下文摘要"""
        if max_size is None:
            max_size = self.config.MAX_CONTEXT_SIZE
        
        summary = {
            "session_id": self.context.get("session_id"),
            "user": self.context.get("user_info", {}),
            "current_task": self.context.get("current_task"),
            "recent_events": self.events.get("today", [])[-5:],
            "entities_count": {
                "projects": len(self.entities.get("projects", {})),
                "systems": len(self.entities.get("systems", {}))
            },
            "pending_actions": self.context.get("pending_actions", [])[-3:]
        }
        
        context_str = json.dumps(summary, ensure_ascii=False, indent=2)
        
        if len(context_str) > max_size:
            # 截取关键信息
            summary["note"] = "上下文已截取，详细内容见文件"
            context_str = json.dumps(summary, ensure_ascii=False, indent=2)
        
        return context_str
    
    def clear_session(self):
        """清理会话"""
        self.context = {
            "session_id": None,
            "created_at": None,
            "updated_at": None,
            "user_info": self.context.get("user_info", {}),
            "system_state": {},
            "current_task": None,
            "pending_actions": [],
            "completed_tasks": [],
            "notes": []
        }
        self._save_all()


# ==================== 快速检索 ====================

class MemorySearch:
    """快速检索"""
    
    def __init__(self, memory: StructuredMemory):
        self.memory = memory
    
    def search_entities(self, query: str, entity_type: str = None) -> List[Dict]:
        """搜索实体"""
        results = []
        entities = self.memory.entities
        
        types_to_search = [entity_type] if entity_type else entities.keys()
        
        for etype in types_to_search:
            for entity_id, entity_data in entities.get(etype, {}).items():
                if query.lower() in entity_id.lower():
                    results.append({
                        "type": etype,
                        "id": entity_id,
                        "data": entity_data
                    })
        
        return results
    
    def search_events(self, query: str, limit: int = 10) -> List[Dict]:
        """搜索事件"""
        results = []
        for event in self.memory.events.get("today", []):
            if query.lower() in event.get("description", "").lower():
                results.append(event)
                if len(results) >= limit:
                    break
        return results


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 初始化
    memory = StructuredMemory()
    search = MemorySearch(memory)
    
    print("=== JSON结构化记忆系统 ===\n")
    
    # 开始会话
    memory.start_session("session_001")
    print(f"✅ 会话开始: {memory.context['session_id']}")
    
    # 更新上下文
    memory.update_context("current_task", "视频制作")
    memory.update_user_info("name", "雷哥")
    print(f"✅ 上下文更新: {memory.get_context('current_task')}")
    
    # 添加实体
    memory.add_entity("project", "元宵视频", {
        "status": "进行中",
        "frames": 4,
        "duration": "15秒"
    })
    print(f"✅ 实体添加: 元宵视频")
    
    # 添加事件
    memory.add_event("task", "完成视频脚本", {"file": "元宵节小爪.md"})
    memory.add_event("system", "系统优化", {"performance": "+7%"})
    print(f"✅ 事件添加: 2个")
    
    # 搜索
    results = search.search_entities("视频")
    print(f"🔍 搜索'视频': {len(results)} 个结果")
    
    # 获取摘要
    summary = memory.get_summary()
    print(f"\n📊 系统摘要:")
    print(f"   会话: {summary['session']}")
    print(f"   用户: {summary['user']}")
    print(f"   任务: {summary['task']}")
    print(f"   实体数: {summary['entities_count']}")
    print(f"   今日事件: {summary['events_today']}")
    print(f"   索引: {summary['index']}")
    
    # AI上下文
    ai_context = memory.get_context_for_ai()
    print(f"\n🤖 AI上下文 (JSON格式):")
    print(ai_context[:500] + "...")
    
    print("\n✅ 结构化记忆系统运行正常!")
