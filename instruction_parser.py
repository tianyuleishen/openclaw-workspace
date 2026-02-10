#!/usr/bin/env python3
"""
Instruction Parser - 提高指令理解和解析
"""

import re
from datetime import datetime
from typing import Dict, List, Optional

class InstructionParser:
    """指令解析器"""
    
    def __init__(self):
        self.intent_patterns = {
            "create": ["创建", "生成", "制作", "write", "create", "generate"],
            "read": ["读取", "查看", "显示", "read", "show", "display"],
            "update": ["更新", "修改", "改进", "update", "modify", "improve"],
            "delete": ["删除", "移除", "delete", "remove"],
            "search": ["搜索", "查找", "查询", "search", "find", "query"],
            "learn": ["学习", "了解", "研究", "learn", "study", "research"],
            "execute": ["执行", "运行", "启动", "execute", "run", "start"],
            "save": ["保存", "记录", "记住", "save", "record", "remember"],
            "test": ["测试", "验证", "检查", "test", "verify", "check"],
        }
        
        self.context_patterns = {
            "memory": ["记忆", "memory", "保存", "学习"],
            "video": ["视频", "video", "生成", "创建"],
            "image": ["图片", "image", "图像", "生成"],
            "community": ["社区", "community", "Moltbook", "moltbook"],
            "file": ["文件", "file", "文档", "doc"],
        }
    
    def parse(self, instruction: str) -> Dict:
        """解析指令"""
        result = {
            "original": instruction,
            "intent": self._detect_intent(instruction),
            "context": self._detect_context(instruction),
            "entities": self._extract_entities(instruction),
            "confidence": 0.0,
            "parsed_at": datetime.now().isoformat()
        }
        
        # 计算置信度
        confidence = 0.5
        if result["intent"]:
            confidence += 0.3
        if result["context"]:
            confidence += 0.2
        result["confidence"] = min(1.0, confidence)
        
        return result
    
    def _detect_intent(self, instruction: str) -> Optional[str]:
        """检测意图"""
        instruction_lower = instruction.lower()
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if pattern.lower() in instruction_lower:
                    return intent
        
        return None
    
    def _detect_context(self, instruction: str) -> Optional[str]:
        """检测上下文"""
        instruction_lower = instruction.lower()
        
        for context, patterns in self.context_patterns.items():
            for pattern in patterns:
                if pattern.lower() in instruction_lower:
                    return context
        
        return None
    
    def _extract_entities(self, instruction: str) -> List[str]:
        """提取实体"""
        entities = []
        
        # 提取文件名
        file_pattern = r'[a-zA-Z_]+\.py|\.md|\.json|\.txt'
        entities.extend(re.findall(file_pattern, instruction))
        
        # 提取链接
        url_pattern = r'https?://[^\s]+'
        entities.extend(re.findall(url_pattern, instruction))
        
        return entities
    
    def validate_instruction(self, instruction: str) -> Dict:
        """验证指令完整性"""
        result = self.parse(instruction)
        
        validation = {
            "complete": False,
            "missing": [],
            "suggestions": []
        }
        
        if not result["intent"]:
            validation["missing"].append("intent (意图)")
            validation["suggestions"].append("请说明要做什么：创建/读取/更新/删除")
        
        if not result["entities"]:
            validation["suggestions"].append("请提供具体对象：文件名/链接等")
        
        validation["complete"] = len(validation["missing"]) == 0
        
        return {
            "parsed": result,
            "validation": validation
        }


# 全局解析器
_parser = None

def get_instruction_parser():
    """获取全局指令解析器"""
    global _parser
    if _parser is None:
        _parser = InstructionParser()
    return _parser


if __name__ == "__main__":
    print("Instruction Parser Test")
    print("=" * 50)
    
    parser = InstructionParser()
    
    # 测试
    tests = [
        "创建视频",
        "查看记忆",
        "保存学习",
        "搜索Moltbook"
    ]
    
    for test in tests:
        result = parser.parse(test)
        print(f"\nInput: {test}")
        print(f"  Intent: {result['intent']}")
        print(f"  Context: {result['context']}")
        print(f"  Confidence: {result['confidence']*100:.0f}%")
    
    print("\n" + "=" * 50)
    print("Instruction parser works!")
