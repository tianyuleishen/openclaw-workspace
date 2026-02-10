#!/usr/bin/env python3
"""
Proactive Learner - 主动学习系统
实现：
1. 根据用户指导完成任务并记录
2. 自动保存学习记忆方便下次独立完成
3. 从书籍、文档自动提取学习
4. 基于历史学习独立完成任务
"""

import json
import re
from datetime import datetime
from pathlib import Path
from structured_memory import StructuredMemory


class ProactiveLearner:
    """
    主动学习器
    
    功能：
    1. 捕获用户指导 - 记录如何完成任务
    2. 任务模式学习 - 学习完成任务的方法
    3. 文档学习 - 从阅读中提取知识
    4. 独立完成 - 基于历史学习执行任务
    """
    
    def __init__(self):
        self.memory = StructuredMemory()
        self.task_patterns = {}  # 任务模式库
        self.guidance_cache = {}  # 用户指导缓存
        self.min_confidence = 0.8
    
    # ========== 1. 用户指导捕获 ==========
    
    def capture_guidance(self, task: str, guidance: str, result: str = None) -> dict:
        """
        捕获用户指导
        
        Usage:
            learner.capture_guidance(
                task="创建自动学习器",
                guidance="用户说：要检测关键词、创建模块、保存学习",
                result="成功创建"
            )
        """
        entry = {
            "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "timestamp": datetime.now().isoformat(),
            "type": "GUIDANCE",
            "task": task,
            "guidance": guidance,
            "result": result,
            "steps": self._extract_steps(guidance)
        }
        
        # 保存到记忆
        self.memory.save_learning(
            topic=f"用户指导: {task}",
            insight=f"指导: {guidance[:100]}... 步骤: {len(entry['steps'])}步",
            source="user_guidance"
        )
        
        # 保存任务模式
        self._save_task_pattern(task, entry["steps"])
        
        # 缓存指导
        self.guidance_cache[task] = entry
        
        return entry
    
    def _extract_steps(self, guidance: str) -> list:
        """从指导中提取步骤"""
        steps = []
        
        # 匹配步骤模式
        patterns = [
            r'(\d+)[\.、：:]\s*(.+)',
            r'第一步[：:]\s*(.+)',
            r'第二步[：:]\s*(.+)',
            r'第三步[：:]\s*(.+)',
            r'首先[，,]\s*(.+)',
            r'然后[，,]\s*(.+)',
            r'最后[，,]\s*(.+)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, guidance)
            steps.extend(matches)
        
        # 如果没匹配到，尝试按句号分割
        if not steps:
            steps = [s.strip() for s in guidance.split('。') if len(s.strip()) > 5]
        
        return steps[:10]  # 最多10步
    
    # ========== 2. 任务模式学习 ==========
    
    def _save_task_pattern(self, task: str, steps: list):
        """保存任务模式"""
        pattern_id = task.lower().replace(' ', '_')
        
        self.task_patterns[pattern_id] = {
            "task": task,
            "steps": steps,
            "learned_at": datetime.now().isoformat(),
            "usage_count": 0
        }
    
    def get_task_pattern(self, task: str) -> dict:
        """
        获取任务模式
        
        Returns:
            {
                "task": "xxx",
                "steps": ["xxx", "xxx"],
                "learned_at": "xxx",
                "usage_count": 5
            }
        """
        pattern_id = task.lower().replace(' ', '_')
        
        if pattern_id in self.task_patterns:
            self.task_patterns[pattern_id]["usage_count"] += 1
            return self.task_patterns[pattern_id]
        
        # 尝试模糊匹配
        for pid, pattern in self.task_patterns.items():
            if task.lower() in pattern["task"].lower():
                pattern["usage_count"] += 1
                return pattern
        
        return None
    
    # ========== 3. 文档学习 ==========
    
    def learn_from_document(self, doc_content: str, doc_name: str, 
                           doc_type: str = "document") -> list:
        """
        从文档中学习
        
        Usage:
            learner.learn_from_document(
                doc_content="文档内容...",
                doc_name="通义万相指南",
                doc_type="guide"
            )
        """
        learnings = []
        
        # 提取关键概念
        concepts = self._extract_concepts(doc_content)
        
        # 提取代码示例
        examples = self._extract_code_examples(doc_content)
        
        # 提取重要信息
        facts = self._extract_facts(doc_content)
        
        # 保存每个概念
        for concept in concepts[:5]:  # 最多5个
            entry = self.memory.save_learning(
                topic=f"概念: {concept['name']}",
                insight=concept['definition'][:150],
                source=f"doc_{doc_type}"
            )
            learnings.append(entry)
        
        # 保存重要事实
        for fact in facts[:3]:  # 最多3个
            entry = self.memory.save_learning(
                topic=f"事实: {doc_name}",
                insight=fact[:150],
                source=f"doc_{doc_type}"
            )
            learnings.append(entry)
        
        return learnings
    
    def _extract_concepts(self, content: str) -> list:
        """提取概念"""
        concepts = []
        
        # 匹配概念定义模式
        patterns = [
            r'([A-Z][a-zA-Z\s]+?)\s*[:：-]\s*(.+)',
            r'所谓\s*(.+?)[，,]\s*(.+)',
            r'(.+?)\s*是指\s*(.+)',
            r'(.+?)\s*就是\s*(.+)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if len(match[0]) < 50 and len(match[1]) < 100:
                    concepts.append({
                        "name": match[0].strip(),
                        "definition": match[1].strip()
                    })
        
        return concepts[:10]
    
    def _extract_code_examples(self, content: str) -> list:
        """提取代码示例"""
        examples = []
        
        # 匹配代码块
        pattern = r'```[\w]*\n([\s\S]*?)```'
        matches = re.findall(pattern, content)
        
        for match in matches[:3]:
            lines = match.strip().split('\n')[:5]
            summary = lines[0] if lines else ""
            examples.append({
                "code": match.strip(),
                "summary": summary
            })
        
        return examples
    
    def _extract_facts(self, content: str) -> list:
        """提取重要事实"""
        facts = []
        
        # 匹配重要信息
        patterns = [
            r'(必须|需要|应该|一定要)\s*(.+)',
            r'(重要|关键|核心|主要)\s*[:：-]?\s*(.+)',
            r'(优点|优势|特点)\s*[:：-]?\s*(.+)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if len(match[-1]) < 100:
                    facts.append(match[-1].strip())
        
        return facts[:10]
    
    # ========== 4. 独立完成任务 ==========
    
    def execute_task(self, task: str, context: dict = None) -> dict:
        """
        基于历史学习独立完成任务
        
        Usage:
            result = learner.execute_task(
                task="创建自动学习器",
                context={"files": ["auto_learner.py"]}
            )
            
            Returns:
                {
                    "success": True,
                    "confidence": 0.85,
                    "steps_used": ["检测关键词", "创建模块", "保存学习"],
                    "pattern_source": "用户指导: 创建自动学习器"
                }
        """
        pattern = self.get_task_pattern(task)
        
        result = {
            "task": task,
            "success": False,
            "confidence": 0.0,
            "steps_used": [],
            "pattern_source": None,
            "message": ""
        }
        
        if pattern:
            result["success"] = True
            result["confidence"] = min(0.95, 0.5 + (pattern["usage_count"] * 0.1))
            result["steps_used"] = pattern["steps"]
            result["pattern_source"] = pattern["task"]
            result["message"] = f"基于历史学习执行任务 (使用{len(pattern['steps'])}个步骤)"
            
            # 记录执行
            self.memory.save_learning(
                topic=f"独立执行: {task}",
                insight=f"置信度: {result['confidence']*100:.0f}% 使用模式: {pattern['task']}",
                source="independent_execution"
            )
        
        else:
            result["message"] = "未找到任务模式，需要用户指导"
        
        return result
    
    # ========== 5. 综合自动学习 ==========
    
    def learn_from_interaction(self, user_message: str, assistant_response: str,
                               task: str = None, guidance: str = None,
                               intent: str = None, confidence: float = None) -> list:
        """
        综合学习：从一次交互中全面学习
        
        Usage:
            learner.learn_from_interaction(
                user_message="创建自动学习器",
                assistant_response="好的，我来...",
                task="创建自动学习器",
                guidance="用户说：要检测关键词...",
                intent="CREATE_AUTO_LEARNER",
                confidence=0.95
            )
        """
        learnings = []
        
        # 1. 如果有用户指导，捕获
        if guidance:
            self.capture_guidance(task, guidance, assistant_response[:100])
        
        # 2. 如果是高置信度决策，记录
        if confidence and confidence >= self.min_confidence:
            self.memory.save_learning(
                topic=f"高置信度任务: {intent or task}",
                insight=f"置信度 {confidence*100:.0f}% 完成",
                source="task_completion"
            )
        
        # 3. 如果识别到新概念，从响应中学习
        concepts = self._extract_concepts(assistant_response)
        for concept in concepts[:2]:
            self.memory.save_learning(
                topic=f"概念: {concept['name']}",
                insight=concept['definition'][:150],
                source="interaction"
            )
        
        return learnings


# 全局主动学习器
_learner = None

def get_proactive_learner():
    """获取全局主动学习器"""
    global _learner
    if _learner is None:
        _learner = ProactiveLearner()
    return _learner


# 便捷函数
def capture_guidance(task: str, guidance: str, result: str = None):
    """捕获用户指导"""
    return get_proactive_learner().capture_guidance(task, guidance, result)

def learn_from_document(content: str, name: str, type: str = "document"):
    """从文档学习"""
    return get_proactive_learner().learn_from_document(content, name, type)

def execute_task(task: str, context: dict = None):
    """独立完成任务"""
    return get_proactive_learner().execute_task(task, context)

def learn_from_interaction(user_msg: str, assistant_msg: str,
                           task: str = None, guidance: str = None,
                           intent: str = None, confidence: float = None):
    """综合学习"""
    return get_proactive_learner().learn_from_interaction(
        user_msg, assistant_msg, task, guidance, intent, confidence
    )


if __name__ == "__main__":
    print("=" * 70)
    print("Proactive Learner Test")
    print("=" * 70)
    
    learner = ProactiveLearner()
    
    # 1. 捕获用户指导
    print("\n1. Capture user guidance...")
    entry = learner.capture_guidance(
        task="创建自动学习器",
        guidance="1.检测关键词 2.创建模块 3.保存学习",
        result="成功"
    )
    print(f"   ✅ Captured: {entry['id']}")
    print(f"   Steps: {entry['steps']}")
    
    # 2. 独立执行任务
    print("\n2. Execute task independently...")
    result = learner.execute_task("创建自动学习器")
    print(f"   Success: {result['success']}")
    print(f"   Confidence: {result['confidence']*100:.0f}%")
    print(f"   Steps: {len(result['steps_used'])}")
    
    # 3. 从文档学习
    print("\n3. Learn from document...")
    doc = """
    结构化记忆系统使用JSON格式存储数据。
    核心功能包括：保存决策、保存学习、查询记录。
    使用方法：from structured_memory import StructuredMemory
    关键优势：比纯文本快10倍以上。
    """
    learnings = learner.learn_from_document(doc, "记忆系统指南", "guide")
    print(f"   ✅ Learned: {len(learnings)} entries")
    
    # 4. 综合学习
    print("\n4. Learn from interaction...")
    learner.learn_from_interaction(
        user_message="学习如何创建模块",
        assistant_response="创建模块需要：1.定义类 2.实现方法 3.添加测试",
        task="创建模块",
        guidance="用户说：要定义类、实现方法、添加测试",
        intent="LEARN_CREATE_MODULE",
        confidence=0.90
    )
    print("   ✅ Learned from interaction")
    
    print("\n" + "=" * 70)
    print("Proactive learning works!")
    print("=" * 70)
