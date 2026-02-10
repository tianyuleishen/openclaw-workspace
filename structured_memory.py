#!/usr/bin/env python3
"""Structured Memory System - JSON格式存储记忆"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# 添加路径
WORKSPACE = Path.home() / ".openclaw/workspace"
if str(WORKSPACE) not in sys.path:
    sys.path.insert(0, str(WORKSPACE))

class StructuredMemory:
    """结构化记忆管理器"""
    
    def __init__(self):
        self.wd = WORKSPACE
        self.md = self.wd / ".memory"
        
        # 初始化目录
        for d in ["decisions", "learnings", "configs", "conversations", "users"]:
            (self.md / d).mkdir(exist_ok=True, parents=True)
    
    def _save_json(self, path: Path, data: Any):
        """保存JSON"""
        path.parent.mkdir(exist_ok=True, parents=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    
    def _load_json(self, path: Path) -> Any:
        """加载JSON"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None
    
    # ==================== 保存功能 ====================
    
    def save_decision(self, intent: str, action: str, confidence: float, 
                      message: str, context: Dict = None) -> Dict:
        """保存决策"""
        entry = {
            "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "timestamp": datetime.now().isoformat(),
            "type": "DECISION",
            "intent": intent,
            "action": action,
            "confidence": confidence,
            "message": message,
            "context": context or {}
        }
        
        f = self.md / "decisions" / "index.json"
        data = self._load_json(f) or {"entries": []}
        data["entries"].append(entry)
        data["last_updated"] = datetime.now().isoformat()
        self._save_json(f, data)
        
        return entry
    
    def save_learning(self, topic: str, insight: str, source: str) -> Dict:
        """保存学习"""
        entry = {
            "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "timestamp": datetime.now().isoformat(),
            "type": "LEARNING",
            "topic": topic,
            "insight": insight,
            "source": source
        }
        
        f = self.md / "learnings" / "index.json"
        data = self._load_json(f) or {"entries": []}
        data["entries"].append(entry)
        data["last_updated"] = datetime.now().isoformat()
        self._save_json(f, data)
        
        return entry
    
    def save_config(self, name: str, old_value: str, new_value: str, reason: str) -> Dict:
        """保存配置"""
        entry = {
            "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "timestamp": datetime.now().isoformat(),
            "type": "CONFIG",
            "name": name,
            "old_value": old_value,
            "new_value": new_value,
            "reason": reason
        }
        
        f = self.md / "configs" / "index.json"
        data = self._load_json(f) or {"entries": []}
        data["entries"].append(entry)
        self._save_json(f, data)
        
        return entry
    
    def save_conversation(self, conversation: Dict) -> Dict:
        """保存对话记录"""
        entry = {
            "id": conversation.get("id", datetime.now().strftime("%Y%m%d_%H%M%S")),
            "timestamp": datetime.now().isoformat(),
            **conversation
        }
        
        f = self.md / "conversations" / "index.json"
        data = self._load_json(f) or {"entries": []}
        data["entries"].append(entry)
        self._save_json(f, data)
        
        return entry
    
    def query_conversations(self, limit: int = 10) -> List[Dict]:
        """查询对话"""
        f = self.md / "conversations" / "index.json"
        data = self._load_json(f) or {"entries": []}
        return data.get("entries", [])[-limit:]
    
    # ==================== 查询功能 ====================
    
    def query_decisions(self, since: str = None, min_confidence: float = None) -> List[Dict]:
        """查询决策"""
        f = self.md / "decisions" / "index.json"
        data = self._load_json(f) or {"entries": []}
        results = data.get("entries", [])
        
        if since:
            results = [e for e in results if e["timestamp"] >= since]
        
        if min_confidence is not None:
            results = [e for e in results if e.get("confidence", 0) >= min_confidence]
        
        return results
    
    def query_learnings(self, topic: str = None) -> List[Dict]:
        """查询学习"""
        f = self.md / "learnings" / "index.json"
        data = self._load_json(f) or {"entries": []}
        results = data.get("entries", [])
        
        if topic:
            results = [e for e in results if topic.lower() in e.get("topic", "").lower()]
        
        return results
    
    # ==================== 统计功能 ====================
    
    def stats(self) -> Dict:
        """获取统计"""
        stats = {}
        
        for mem_type in ["decisions", "learnings", "configs"]:
            f = self.md / mem_type / "index.json"
            data = self._load_json(f) or {"entries": []}
            stats[mem_type] = len(data.get("entries", []))
        
        return stats
    
    def get_today_entries(self) -> List[Dict]:
        """获取今天的记录"""
        today = datetime.now().strftime("%Y-%m-%d")
        results = []
        
        for mem_type in ["decisions", "learnings", "configs"]:
            f = self.md / mem_type / "index.json"
            data = self._load_json(f) or {"entries": []}
            
            for e in data.get("entries", []):
                if today in e.get("timestamp", ""):
                    results.append(e)
        
        return results


# ==================== 便捷函数 ====================

def save_decision(intent: str, action: str, confidence: float, 
                 message: str, context: Dict = None) -> Dict:
    """保存决策"""
    m = StructuredMemory()
    return m.save_decision(intent, action, confidence, message, context)

def query_decisions(since: str = None, min_confidence: float = None) -> List[Dict]:
    """查询决策"""
    m = StructuredMemory()
    return m.query_decisions(since, min_confidence)

def get_stats() -> Dict:
    """获取统计"""
    m = StructuredMemory()
    return m.stats()


if __name__ == "__main__":
    print("\n🧠 结构化记忆系统测试")
    print("=" * 50)
    
    m = StructuredMemory()
    
    # 保存测试
    print("\n1. 保存测试决策...")
    e = m.save_decision(
        intent="TEST",
        action="EXECUTE", 
        confidence=0.97,
        message="测试结构化记忆系统",
        context={"user": "熊雷"}
    )
    print(f"   ✅ 已保存: {e['id']}")
    
    # 查询测试
    print("\n2. 查询决策...")
    decisions = m.query_decisions()
    print(f"   📊 决策数: {len(decisions)}")
    
    # 统计
    print("\n3. 记忆统计...")
    stats = m.stats()
    for k, v in stats.items():
        print(f"   {k}: {v}")
    
    print("\n✅ 结构化记忆系统工作正常!")
