#!/usr/bin/env python3
"""
Auto Conversation Saver - 自动保存所有对话
"""

import json
from datetime import datetime
from pathlib import Path
from structured_memory import StructuredMemory

class ConversationSaver:
    """
    自动保存所有对话内容
    """
    
    def __init__(self):
        self.saver = StructuredMemory()
        self.current_conversation = []
        self.session_start = datetime.now()
    
    def save_turn(self, user_message: str, assistant_response: str, intent: str = None, confidence: float = None):
        """
        保存一轮对话
        
        Args:
            user_message: 用户消息
            assistant_response: 助手响应
            intent: 意图
            confidence: 置信度
        """
        turn = {
            "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "assistant_response": assistant_response,
            "intent": intent,
            "confidence": confidence,
            "type": "CONVERSATION_TURN"
        }
        
        self.current_conversation.append(turn)
        
        # 保存到结构化记忆
        self.saver.save_conversation({
            "user": user_message[:100],
            "message": assistant_response[:200],
            "intent": intent or "UNKNOWN",
            "confidence": confidence or 0.0,
            "turn_id": turn["id"]
        })
        
        return turn
    
    def save_conversation(self, turns: list = None):
        """
        保存完整对话会话
        
        Args:
            turns: 对话轮次列表，如果为空则保存当前会话
        """
        conversation = {
            "id": self.session_start.strftime("%Y%m%d_%H%M%S"),
            "start_time": self.session_start.isoformat(),
            "end_time": datetime.now().isoformat(),
            "turn_count": len(self.current_conversation),
            "turns": self.current_conversation if turns is None else turns,
            "type": "CONVERSATION_SESSION"
        }
        
        # 保存到JSON文件
        conv_file = Path.home() / ".openclaw/workspace/.memory/conversations" / f"{conversation['id']}.json"
        conv_file.parent.mkdir(exist_ok=True, parents=True)
        
        with open(conv_file, 'w', encoding='utf-8') as f:
            json.dump(conversation, f, ensure_ascii=False, indent=2, default=str)
        
        return conversation
    
    def get_conversation_history(self, limit: int = 10) -> list:
        """
        获取对话历史
        
        Args:
            limit: 返回数量限制
        """
        conv_dir = Path.home() / ".openclaw/workspace/.memory/conversations"
        
        if not conv_dir.exists():
            return []
        
        conversations = []
        for f in sorted(conv_dir.glob("*.json"), reverse=True)[:limit]:
            with open(f, 'r', encoding='utf-8') as fp:
                try:
                    conv = json.load(fp)
                    conversations.append(conv)
                except:
                    pass
        
        return conversations
    
    def get_recent_turns(self, limit: int = 20) -> list:
        """
        获取最近的对话轮次
        """
        history = self.get_conversation_history(limit=5)
        
        turns = []
        for conv in history:
            turns.extend(conv.get("turns", [])[-limit:])
        
        return turns[-limit:]


# 全局保存器
_conversation_saver = None

def get_conversation_saver():
    """获取全局对话保存器"""
    global _conversation_saver
    if _conversation_saver is None:
        _conversation_saver = ConversationSaver()
    return _conversation_saver


# 便捷函数
def save_turn(user_message: str, assistant_response: str, intent: str = None, confidence: float = None):
    """
    保存一轮对话
    """
    saver = get_conversation_saver()
    return saver.save_turn(user_message, assistant_response, intent, confidence)


def save_session():
    """保存当前会话"""
    saver = get_conversation_saver()
    return saver.save_conversation()


def get_history(limit: int = 10):
    """获取对话历史"""
    saver = get_conversation_saver()
    return saver.get_conversation_history(limit)


def get_recent(limit: int = 20):
    """获取最近对话"""
    saver = get_conversation_saver()
    return saver.get_recent_turns(limit)


if __name__ == "__main__":
    print("Conversation Saver Test")
    print("=" * 50)
    
    # 测试保存
    saver = ConversationSaver()
    
    # 保存几轮对话
    saver.save_turn(
        user_message="测试对话1",
        assistant_response="这是响应1",
        intent="TEST",
        confidence=0.95
    )
    
    saver.save_turn(
        user_message="测试对话2",
        assistant_response="这是响应2",
        intent="TEST",
        confidence=0.90
    )
    
    # 保存会话
    conv = saver.save_session()
    
    print(f"Session ID: {conv['id']}")
    print(f"Turns: {conv['turn_count']}")
    
    # 获取历史
    history = saver.get_conversation_history(limit=5)
    print(f"History count: {len(history)}")
    
    print("\nConversation saving works!")
