#!/usr/bin/env python3
"""
Enhanced Memory System - 借鉴 LightAgent 的 mem0 思想
增强版记忆系统，支持语义搜索和智能检索
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import re


@dataclass
class MemoryEntry:
    """记忆条目"""
    id: str
    timestamp: str
    type: str  # DECISION, LEARNING, CONVERSATION, USER_PREF
    content: str
    embedding: Optional[List[float]] = None
    metadata: Dict = None
    importance: float = 0.5
    access_count: int = 0
    last_accessed: str = None

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "type": self.type,
            "content": self.content,
            "embedding": self.embedding,
            "metadata": self.metadata or {},
            "importance": self.importance,
            "access_count": self.access_count,
            "last_accessed": self.last_accessed
        }


class EnhancedMemorySystem:
    """
    增强型记忆系统
    借鉴 LightAgent + mem0 设计理念
    """

    def __init__(self):
        self.wd = Path.home() / ".openclaw/workspace"
        self.md = self.wd / ".memory"
        self.enhanced_md = self.md / "enhanced"

        # 初始化目录
        for d in ["decisions", "learnings", "conversations", "users", "semantic"]:
            (self.enhanced_md / d).mkdir(exist_ok=True, parents=True)

        # 内存缓存
        self._cache = {
            "decisions": [],
            "learnings": [],
            "conversations": [],
            "users": []
        }

        # 统计信息
        self._stats = {
            "total_memories": 0,
            "by_type": {},
            "last_updated": None
        }

        # 加载现有记忆
        self._load_all()

    def _generate_id(self, content: str) -> str:
        """生成唯一ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        hash_val = hashlib.md5(f"{content}{timestamp}".encode()).hexdigest()[:8]
        return f"{timestamp}_{hash_val}"

    def _now(self) -> str:
        return datetime.now().isoformat()

    # ==================== 保存功能 ====================

    def save_decision(self, intent: str, action: str, confidence: float,
                      message: str, context: Dict = None,
                      importance: float = 0.8) -> Dict:
        """保存决策记忆"""
        entry = MemoryEntry(
            id=self._generate_id(message),
            timestamp=self._now(),
            type="DECISION",
            content=f"Intent: {intent}\nAction: {action}\nMessage: {message}",
            metadata={"intent": intent, "action": action, "context": context},
            importance=importance,
            last_accessed=self._now()
        )

        self._cache["decisions"].append(entry)
        self._save_to_file("decisions", entry.to_dict())
        self._update_stats("DECISION")

        return entry.to_dict()

    def save_learning(self, topic: str, insight: str, source: str,
                      importance: float = 0.7) -> Dict:
        """保存学习记忆"""
        entry = MemoryEntry(
            id=self._generate_id(insight),
            timestamp=self._now(),
            type="LEARNING",
            content=f"Topic: {topic}\nInsight: {insight}\nSource: {source}",
            metadata={"topic": topic, "source": source},
            importance=importance,
            last_accessed=self._now()
        )

        self._cache["learnings"].append(entry)
        self._save_to_file("learnings", entry.to_dict())
        self._update_stats("LEARNING")

        return entry.to_dict()

    def save_conversation(self, user_message: str, assistant_response: str,
                          intent: str = None, importance: float = 0.5) -> Dict:
        """保存对话记忆"""
        entry = MemoryEntry(
            id=self._generate_id(user_message),
            timestamp=self._now(),
            type="CONVERSATION",
            content=f"User: {user_message}\nAssistant: {assistant_response}",
            metadata={"intent": intent, "message_length": len(user_message)},
            importance=importance,
            last_accessed=self._now()
        )

        self._cache["conversations"].append(entry)
        self._save_to_file("conversations", entry.to_dict())
        self._update_stats("CONVERSATION")

        return entry.to_dict()

    def save_user_preference(self, user_id: str, preference_type: str,
                             value: Any, importance: float = 0.9) -> Dict:
        """保存用户偏好"""
        entry = MemoryEntry(
            id=self._generate_id(f"{user_id}{preference_type}"),
            timestamp=self._now(),
            type="USER_PREF",
            content=f"User: {user_id}\nPreference: {preference_type}\nValue: {value}",
            metadata={"user_id": user_id, "preference_type": preference_type},
            importance=importance,
            last_accessed=self._now()
        )

        self._cache["users"].append(entry)
        self._save_to_file("users", entry.to_dict())
        self._update_stats("USER_PREF")

        return entry.to_dict()

    # ==================== 检索功能 ====================

    def query_memories(self, query: str, memory_type: str = None,
                       min_importance: float = 0.3, limit: int = 10) -> List[Dict]:
        """
        智能检索记忆 (简化版语义搜索)

        借鉴 LightAgent 的 mem0 检索方式：
        - 关键词匹配
        - 类型过滤
        - 重要性排序
        - 访问频率加权
        """
        results = []
        query_lower = query.lower()
        query_keywords = set(re.findall(r'\w+', query_lower))

        # 选择搜索范围
        search_cache = []
        if memory_type:
            # 统一转换为小写并处理复数形式
            type_map = {
                "decision": "decisions",
                "learning": "learnings",
                "conversation": "conversations",
                "user_pref": "users",
                "user_preference": "users"
            }
            cache_key = type_map.get(memory_type.lower(), memory_type.lower())
            # 移除末尾的s以处理单复数
            if not cache_key.endswith('s'):
                cache_key = cache_key + 's'
            search_cache = self._cache.get(cache_key, [])
        else:
            for cache_list in self._cache.values():
                search_cache.extend(cache_list)

        for entry in search_cache:
            # 过滤重要性
            if entry.importance < min_importance:
                continue

            # 关键词匹配
            content_lower = entry.content.lower()
            keyword_matches = sum(1 for kw in query_keywords if kw in content_lower)

            if keyword_matches > 0:
                # 计算相关性分数
                relevance_score = (
                    keyword_matches * 0.4 +
                    entry.importance * 0.3 +
                    (entry.access_count / 10) * 0.2 +
                    (1.0 if query_type_matches(entry.type, query) else 0) * 0.1
                )

                # 更新访问计数
                entry.access_count += 1
                entry.last_accessed = self._now()

                results.append({
                    **entry.to_dict(),
                    "relevance_score": relevance_score
                })

        # 按相关性排序
        results.sort(key=lambda x: x["relevance_score"], reverse=True)

        return results[:limit]

    def get_recent_memories(self, memory_type: str = None, limit: int = 5) -> List[Dict]:
        """获取最近记忆"""
        search_cache = []
        if memory_type:
            cache_key = memory_type.lower().replace(" ", "_")
            search_cache = self._cache.get(cache_key, [])
        else:
            for cache_list in self._cache.values():
                search_cache.extend(cache_list)

        # 按时间排序
        sorted_memories = sorted(
            search_cache,
            key=lambda x: x.timestamp,
            reverse=True
        )

        return [m.to_dict() for m in sorted_memories[:limit]]

    def get_high_importance_memories(self, min_importance: float = 0.7,
                                      limit: int = 10) -> List[Dict]:
        """获取重要记忆"""
        all_memories = []
        for cache_list in self._cache.values():
            all_memories.extend(cache_list)

        important = [m for m in all_memories if m.importance >= min_importance]
        important.sort(key=lambda x: x.importance, reverse=True)

        return [m.to_dict() for m in important[:limit]]

    # ==================== 统计功能 ====================

    def stats(self) -> Dict:
        """获取统计信息"""
        total = sum(len(cache) for cache in self._cache.values())

        by_type = {}
        for mem_type, cache_list in self._cache.items():
            by_type[mem_type] = len(cache_list)

        return {
            "total_memories": total,
            "by_type": by_type,
            "cache_counts": {
                "decisions": len(self._cache["decisions"]),
                "learnings": len(self._cache["learnings"]),
                "conversations": len(self._cache["conversations"]),
                "users": len(self._cache["users"])
            },
            "last_updated": self._stats.get("last_updated")
        }

    def _update_stats(self, memory_type: str):
        """更新统计"""
        self._stats["total_memories"] += 1
        self._stats["last_updated"] = self._now()

        if memory_type not in self._stats.get("by_type", {}):
            self._stats["by_type"][memory_type] = 0
        self._stats["by_type"][memory_type] += 1

    # ==================== 文件操作 ====================

    def _save_to_file(self, category: str, data: Dict):
        """保存到文件"""
        f = self.enhanced_md / category / f"{data['id']}.json"
        with open(f, 'w', encoding='utf-8') as fp:
            json.dump(data, fp, ensure_ascii=False, indent=2)

    def _load_all(self):
        """加载所有记忆"""
        for category in ["decisions", "learnings", "conversations", "users"]:
            category_path = self.enhanced_md / category
            if category_path.exists():
                for f in category_path.glob("*.json"):
                    try:
                        with open(f, 'r', encoding='utf-8') as fp:
                            data = json.load(fp)
                            # 转换为 MemoryEntry
                            entry = MemoryEntry(**data)
                            self._cache[category].append(entry)
                    except Exception as e:
                        print(f"Warning: Failed to load {f}: {e}")

        self._update_stats_from_cache()

    def _update_stats_from_cache(self):
        """从缓存更新统计"""
        for category, entries in self._cache.items():
            self._stats["by_type"][category.upper()] = len(entries)
        self._stats["total_memories"] = sum(
            len(entries) for entries in self._cache.values()
        )


def query_type_matches(memory_type: str, query: str) -> bool:
    """检查类型是否匹配"""
    type_keywords = {
        "DECISION": ["decision", "选择", "决定", "choose", "decide"],
        "LEARNING": ["learn", "学习", "研究", "study", "research"],
        "CONVERSATION": ["talk", "对话", "聊天", "conversation", "chat"],
        "USER_PREF": ["prefer", "偏好", "喜欢", "设置", "setting"]
    }

    query_lower = query.lower()
    keywords = type_keywords.get(memory_type, [])
    return any(kw in query_lower for kw in keywords)


# 测试代码
if __name__ == "__main__":
    print("Testing Enhanced Memory System...")

    memory = EnhancedMemorySystem()

    # 保存测试记忆
    memory.save_decision(
        intent="test_decision",
        action="save_test_memory",
        confidence=0.9,
        message="测试决策保存功能"
    )

    memory.save_learning(
        topic="Python",
        insight="Python是一种解释型语言",
        source="Python官方文档"
    )

    # 查询测试
    results = memory.query_memories("Python 学习", min_importance=0.3)
    print(f"\nQuery results: {len(results)} memories found")

    # 统计
    stats = memory.stats()
    print(f"\nStats: {stats}")

    print("\n✅ Enhanced Memory System working!")
