#!/usr/bin/env python3
"""
Enhanced Auto Memory Loader - 集成错误处理和指令解析
"""

import json
from datetime import datetime
from structured_memory import StructuredMemory
from error_handler import get_error_handler
from instruction_parser import get_instruction_parser


class EnhancedAutoMemoryLoader:
    """
    增强版自动记忆加载器
    
    功能：
    - 自动加载JSON记忆
    - 错误处理和日志
    - 指令解析和验证
    """
    
    def __init__(self):
        self.memory = StructuredMemory()
        self.error_handler = get_error_handler()
        self.instruction_parser = get_instruction_parser()
        self.cache = {}
        self.loaded_at = None
    
    def load_all(self):
        """加载所有记忆"""
        try:
            self.cache["decisions"] = self.memory.query_decisions()
            self.cache["learnings"] = self.memory.query_learnings()
            self.cache["conversations"] = self.memory.query_conversations()
            self.cache["stats"] = self.memory.stats()
            self.loaded_at = datetime.now()
            return self.cache
        except Exception as e:
            self.error_handler.capture_error(e, "load_all")
            return {}
    
    def parse_instruction(self, instruction: str):
        """解析用户指令"""
        try:
            return self.instruction_parser.parse(instruction)
        except Exception as e:
            self.error_handler.capture_error(e, "parse_instruction")
            return None
    
    def validate_instruction(self, instruction: str):
        """验证指令完整性"""
        try:
            return self.instruction_parser.validate_instruction(instruction)
        except Exception as e:
            self.error_handler.capture_error(e, "validate_instruction")
            return None
    
    def get_decisions(self, min_confidence=None):
        """获取决策"""
        try:
            if "decisions" not in self.cache:
                self.load_all()
            if min_confidence:
                return [d for d in self.cache["decisions"] if d.get("confidence", 0) >= min_confidence]
            return self.cache.get("decisions", [])
        except Exception as e:
            self.error_handler.capture_error(e, "get_decisions")
            return []
    
    def get_learnings(self, topic=None):
        """获取学习"""
        try:
            if "learnings" not in self.cache:
                self.load_all()
            if topic:
                return [l for l in self.cache.get("learnings", []) if topic.lower() in l.get("topic", "").lower()]
            return self.cache.get("learnings", [])
        except Exception as e:
            self.error_handler.capture_error(e, "get_learnings")
            return []
    
    def get_stats(self):
        """获取统计"""
        try:
            if "stats" not in self.cache:
                self.load_all()
            return self.cache.get("stats", {})
        except Exception as e:
            self.error_handler.capture_error(e, "get_stats")
            return {}
    
    def get_recent_errors(self, limit=10):
        """获取最近错误"""
        return self.error_handler.get_recent_errors(limit)
    
    def analyze_errors(self):
        """分析错误模式"""
        return self.error_handler.analyze_errors()


# Global loader
_loader = None

def get_memory_loader():
    """获取全局增强记忆加载器"""
    global _loader
    if _loader is None:
        _loader = EnhancedAutoMemoryLoader()
        _loader.load_all()
    return _loader


# Convenience functions
def load_memory():
    """加载所有记忆"""
    return get_memory_loader().load_all()

def parse_instruction(instruction):
    """解析用户指令"""
    return get_memory_loader().parse_instruction(instruction)

def validate_instruction(instruction):
    """验证指令"""
    return get_memory_loader().validate_instruction(instruction)

def get_recent_decisions(min_confidence=0.8):
    """获取高置信度决策"""
    return get_memory_loader().get_decisions(min_confidence)

def get_learnings(topic=None):
    """获取学习"""
    return get_memory_loader().get_learnings(topic)

def get_errors(limit=10):
    """获取错误日志"""
    return get_memory_loader().get_recent_errors(limit)


if __name__ == "__main__":
    print("Enhanced Auto Memory Loader Test")
    print("=" * 50)
    
    loader = get_memory_loader()
    
    print("1. Load all memory...")
    cache = loader.load_all()
    print(f"   Decisions: {len(cache.get('decisions', []))}")
    print(f"   Learnings: {len(cache.get('learnings', []))}")
    
    print("\n2. Parse instruction...")
    result = loader.parse_instruction("创建视频")
    print(f"   Intent: {result['intent']}")
    print(f"   Context: {result['context']}")
    print(f"   Confidence: {result['confidence']*100:.0f}%")
    
    print("\n3. Validate instruction...")
    validation = loader.validate_instruction("创建视频")
    print(f"   Complete: {validation['validation']['complete']}")
    
    print("\n" + "=" * 50)
    print("Enhanced memory loader works!")
