#!/usr/bin/env python3
"""
Auto Learner - 自动触发学习保存
基于用户消息和AI响应自动检测学习点并保存
"""

import re
from datetime import datetime
from structured_memory import StructuredMemory


class AutoLearner:
    """
    自动学习器
    
    功能：
    - 分析对话自动检测学习点
    - 完成任务时自动保存学习
    - 高置信度决策自动记录
    """
    
    def __init__(self):
        self.memory = StructuredMemory()
        self.last_learning_time = None
        self.min_confidence = 0.85  # 触发阈值
    
    def analyze_for_learning(self, user_message: str, assistant_response: str, 
                            intent: str = None, confidence: float = None) -> list:
        """
        分析对话，检测学习点
        
        Args:
            user_message: 用户消息
            assistant_response: AI响应
            intent: 意图
            confidence: 置信度
            
        Returns:
            list of detected learnings
        """
        learnings = []
        
        # 1. 检测是否用户要求保存学习
        if self._is_save_request(user_message):
            learnings.append({
                "topic": "用户请求学习",
                "insight": f"用户要求保存: {user_message}",
                "source": "user_request"
            })
        
        # 2. 检测是否AI主动总结
        if self._is_summary(assistant_response):
            learnings.append({
                "topic": "AI主动总结",
                "insight": self._extract_summary(assistant_response),
                "source": "ai_initiated"
            })
        
        # 3. 高置信度决策自动记录
        if confidence and confidence >= self.min_confidence:
            learnings.append({
                "topic": f"高置信度决策 ({intent})",
                "insight": f"置信度 {confidence*100:.0f}% 完成任务",
                "source": "auto_decision"
            })
        
        # 4. 检测是否学习新技能
        if self._is_skill_learning(user_message, assistant_response):
            learnings.append({
                "topic": "学习新技能",
                "insight": assistant_response[:150],
                "source": "skill_learning"
            })
        
        # 5. 检测重要发现
        if self._is_discovery(user_message, assistant_response):
            learnings.append({
                "topic": "重要发现",
                "insight": assistant_response[:150],
                "source": "discovery"
            })
        
        return learnings
    
    def save_auto_learning(self, user_message: str, assistant_response: str,
                          intent: str = None, confidence: float = None) -> list:
        """
        自动检测并保存学习
        
        Returns:
            list of saved entries
        """
        learnings = self.analyze_for_learning(
            user_message, assistant_response, intent, confidence
        )
        
        saved = []
        for l in learnings:
            entry = self.memory.save_learning(
                topic=l["topic"],
                insight=l["insight"],
                source=l["source"]
            )
            saved.append(entry)
            self.last_learning_time = datetime.now()
        
        return saved
    
    def save_task_completion(self, task: str, result: str, confidence: float):
        """
        任务完成时自动保存学习
        
        Args:
            task: 任务描述
            result: 结果
            confidence: 置信度
        """
        if confidence >= self.min_confidence:
            return self.memory.save_learning(
                topic="任务成功完成",
                insight=f"任务: {task[:50]}... 结果: {result[:50]}",
                source="task_completion"
            )
        return None
    
    def save_research_result(self, topic: str, findings: str):
        """
        研究结果自动保存
        
        Args:
            topic: 研究主题
            findings: 发现
        """
        return self.memory.save_learning(
            topic=f"研究: {topic}",
            insight=findings[:200],
            source="research"
        )
    
    # ========== 检测方法 ==========
    
    def _is_save_request(self, message: str) -> bool:
        """检测是否用户要求保存"""
        keywords = [
            "保存", "记录", "学习", "记住",
            "把这个", "记下来", "存一下"
        ]
        return any(kw in message for kw in keywords)
    
    def _is_summary(self, response: str) -> bool:
        """检测是否AI主动总结"""
        keywords = [
            "总结", "学到", "发现", "已完成",
            "我注意到", "关键点是", "重要的是"
        ]
        return any(kw in response for kw in keywords) and len(response) > 50
    
    def _is_skill_learning(self, user: str, assistant: str) -> bool:
        """检测是否学习新技能"""
        keywords = [
            "如何", "怎么", "是什么", "学习",
            "创建", "实现", "配置", "编写"
        ]
        return any(kw in user.lower() for kw in keywords) and len(assistant) > 100
    
    def _is_discovery(self, user: str, assistant: str) -> bool:
        """检测是否重要发现"""
        keywords = [
            "发现", "原来", "竟然", "没想到",
            "原来如此", "原来是这样"
        ]
        return any(kw in assistant for kw in keywords) and len(assistant) > 50
    
    def _extract_summary(self, response: str) -> str:
        """提取总结内容"""
        # 取前150字符
        return response[:150].replace('\n', ' ')


# 全局自动学习器
_learner = None

def get_learner():
    """获取全局自动学习器"""
    global _learner
    if _learner is None:
        _learner = AutoLearner()
    return _learner


# 便捷函数
def auto_learn(user_message: str, assistant_response: str, 
              intent: str = None, confidence: float = None):
    """
    自动检测并保存学习
    
    Usage:
        auto_learn(user_msg, assistant_msg, intent, confidence)
    """
    learner = get_learner()
    return learner.save_auto_learning(user_message, assistant_response, intent, confidence)


def save_completion(task: str, result: str, confidence: float):
    """保存任务完成"""
    learner = get_learner()
    return learner.save_task_completion(task, result, confidence)


def save_research(topic: str, findings: str):
    """保存研究结果"""
    learner = get_learner()
    return learner.save_research_result(topic, findings)


if __name__ == "__main__":
    print("Auto Learner Test")
    print("=" * 50)
    
    learner = AutoLearner()
    
    # 测试1: 保存请求
    print("1. Test save request...")
    saved = auto_learn(
        user_message="保存这个学习",
        assistant_response="好的，已保存",
        intent="SAVE_LEARNING",
        confidence=0.95
    )
    print(f"   Saved: {len(saved)} entries")
    
    # 测试2: 任务完成
    print("2. Test task completion...")
    entry = save_completion("创建系统", "成功", 0.95)
    print(f"   Saved: {entry['id'] if entry else 'None'}")
    
    # 测试3: 研究结果
    print("3. Test research result...")
    entry = save_research("AI技术", "学到了新方法")
    print(f"   Saved: {entry['id'] if entry else 'None'}")
    
    print("\nAuto learning works!")
