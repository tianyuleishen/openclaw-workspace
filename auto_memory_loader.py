#!/usr/bin/env python3
"""
Auto Memory Loader - 每次会话自动加载JSON记忆 + 自动学习
"""

import json
from datetime import datetime
from structured_memory import StructuredMemory
from auto_learner import AutoLearner

class AutoMemoryLoader:
    """
    自动记忆加载器 + 自动学习触发器
    """
    
    def __init__(self):
        self.memory = StructuredMemory()
        self.learner = AutoLearner()
        self.cache = {}
        self.loaded_at = None
    
    def load_all(self):
        """加载所有记忆"""
        self.cache["decisions"] = self.memory.query_decisions()
        self.cache["learnings"] = self.memory.query_learnings()
        self.cache["stats"] = self.memory.stats()
        self.loaded_at = datetime.now()
        return self.cache
    
    def get_decisions(self, min_confidence=None):
        if "decisions" not in self.cache:
            self.load_all()
        if min_confidence:
            return [d for d in self.cache["decisions"] if d.get("confidence", 0) >= min_confidence]
        return self.cache.get("decisions", [])
    
    def get_learnings(self, topic=None):
        if "learnings" not in self.cache:
            self.load_all()
        if topic:
            return [l for l in self.cache.get("learnings", []) if topic.lower() in l.get("topic", "").lower()]
        return self.cache.get("learnings", [])
    
    def get_stats(self):
        if "stats" not in self.cache:
            self.load_all()
        return self.cache.get("stats", {})
    
    def auto_learn(self, user_message: str, assistant_response: str,
                   intent: str = None, confidence: float = None):
        """
        自动检测并保存学习
        
        Usage:
            loader.auto_learn(user_msg, assistant_msg, intent, confidence)
        """
        return self.learner.save_auto_learning(
            user_message, assistant_response, intent, confidence
        )
    
    def save_completion(self, task: str, result: str, confidence: float):
        """保存任务完成"""
        return self.learner.save_task_completion(task, result, confidence)
    
    def save_research(self, topic: str, findings: str):
        """保存研究结果"""
        return self.learner.save_research_result(topic, findings)


# Global loader
_loader = None

def get_memory_loader():
    global _loader
    if _loader is None:
        _loader = AutoMemoryLoader()
        _loader.load_all()
    return _loader


# Convenience functions
def load_memory():
    return get_memory_loader().load_all()

def get_recent_decisions(min_confidence=0.8):
    return get_memory_loader().get_decisions(min_confidence)

def get_learnings(topic=None):
    return get_memory_loader().get_learnings(topic)

def auto_learn(user_message: str, assistant_response: str,
              intent: str = None, confidence: float = None):
    """
    自动检测并保存学习
    
    Usage:
        auto_learn(user_msg, assistant_msg, intent, confidence)
    """
    return get_memory_loader().auto_learn(user_message, assistant_response, intent, confidence)


if __name__ == "__main__":
    print("Auto Memory Loader with Auto-Learn")
    print("=" * 50)
    
    loader = get_memory_loader()
    print(f"Decisions: {len(loader.get_decisions())}")
    print(f"Learnings: {len(loader.get_learnings())}")
    print(f"Stats: {loader.get_stats()}")
    
    print("\nAuto memory with auto-learning works!")
