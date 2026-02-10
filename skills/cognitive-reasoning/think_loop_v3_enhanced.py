#!/usr/bin/env python3
"""
Cognitive Reasoning Framework v3 Enhanced - 集成多路径理解
增强版认知框架：结合记忆、历史、经验 + 多路径理解生成
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# 导入多路径理解
from multi_path import MultiPathUnderstanding


class ThinkLoopV3Enhanced:
    """
    增强版认知框架v3
    
    核心能力：
    - 记忆集成：读取MEMORY.md、USER.md
    - 历史分析：分析最近对话
    - 经验学习：累积学习用户偏好
    - 多路径理解：从多个角度分析用户意图
    - 反复讨论：反复讨论直到明确
    """
    
    def __init__(self):
        self.threshold = 0.75  # 阈值
        self.memory_dir = Path.home() / ".openclaw/workspace/memory"
        self.memory_file = Path.home() / ".openclaw/workspace/MEMORY.md"
        self.user_file = Path.home() / ".openclaw/workspace/USER.md"
        self.learning_file = Path.home() / ".openclaw/workspace/.intent_learning.json"
        
        # 多路径理解器
        self.mpu = MultiPathUnderstanding()
        
        # 加载学习数据
        self.learning_data = self._load_learning_data()
    
    def _load_learning_data(self):
        """加载学习数据"""
        if self.learning_file.exists():
            try:
                with open(self.learning_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"user_patterns": {}, "preferred_actions": {}, "clarification_count": 0}
    
    def think(self, message, history=None):
        """
        主思考流程v3增强版 - 集成多路径理解
        
        Returns:
            dict: 思考结果
        """
        print("\n" + "🧠" * 35)
        print("🧠🧠🧠 COGNITIVE REASONING FRAMEWORK v3 Enhanced 🧠🧠🧠")
        print("🧠🧠🧠  集成记忆·历史·经验·多路径理解  🧠🧠🧠")
        print("🧠" * 35)
        
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"\n👤 用户: \"{message}\"")
        print(f"⏰ 时间: {timestamp}")
        
        # Step 0: 加载记忆
        print("\n" + "-" * 60)
        print("Step 0 📚 加载记忆")
        print("-" * 60)
        memory = self.read_memory()
        profile = self.read_user_profile()
        print(f"   长期记忆: {'✅ 已加载' if memory else '❌ 空'}")
        print(f"   用户档案: {'✅ 已加载' if profile else '❌ 空'}")
        
        # Step 1: 多路径理解（新增）
        print("\n" + "-" * 60)
        print("Step 1 🎯 多路径理解生成")
        print("-" * 60)
        multi_path_result = self.mpu.understand(message, history or [], max_paths=3)
        
        primary = multi_path_result["primary"]
        alternatives = multi_path_result["alternatives"]
        
        print(f"   生成路径: {multi_path_result['path_count']}个")
        print(f"   主路径: {primary['angle']}")
        print(f"   主路径评分: {primary['score']*100:.0f}%")
        
        if alternatives:
            print(f"   候选路径: {', '.join([a['angle'] for a in alternatives])}")
        
        # Step 2: 歧义检测
        print("\n" + "-" * 60)
        print("Step 2 🔍 歧义检测（历史增强）")
        print("-" * 60)
        ambiguities = self.detect_ambiguities_v3(message, primary, history or [])
        print(f"   发现 {len(ambiguities)} 个模糊点")
        
        # Step 3: 经验学习
        print("\n" + "-" * 60)
        print("Step 3 📈 经验学习")
        print("-" * 60)
        experience_bonus = self.apply_experience(message, primary, history or [])
        print(f"   经验加成: +{experience_bonus*100:.0f}%")
        
        # Step 4: 综合置信度
        print("\n" + "-" * 60)
        print("Step 4 📊 综合置信度")
        print("-" * 60)
        
        # 多路径评分
        base_score = primary["score"]
        
        # 歧义惩罚
        for amb in ambiguities:
            base_score -= amb.get("weight", 0.3) * 0.1
        
        # 经验加成
        final_confidence = min(0.98, base_score + experience_bonus)
        
        print(f"   多路径基础分: {base_score*100:.0f}%")
        print(f"   歧义惩罚: -{sum([amb.get('weight', 0.3)*0.1 for amb in ambiguities])*100:.0f}%")
        print(f"   经验加成: +{experience_bonus*100:.0f}%")
        print(f"   最终置信度: {final_confidence*100:.0f}%")
        
        # Step 5: 决策
        print("\n" + "-" * 60)
        print("Step 5 " + ("✅ 可以执行" if final_confidence >= self.threshold else "🔄 反复讨论"))
        print("-" * 60)
        
        result = {
            "message": message,
            "timestamp": timestamp,
            "memory": memory,
            "history_analysis": self.analyze_history(history or []),
            "multi_path": multi_path_result,
            "primary_path": primary,
            "alternatives": alternatives,
            "ambiguities": ambiguities,
            "confidence": final_confidence,
            "experience_bonus": experience_bonus,
            "can_execute": final_confidence >= self.threshold,
            "rounds": 1
        }
        
        if final_confidence >= self.threshold:
            print(f"   置信度 {final_confidence*100:.0f}% ≥ {self.threshold*100:.0f}%")
            print(f"   ✅ 执行任务")
        else:
            print(f"   置信度 {final_confidence*100:.0f}% < {self.threshold*100:.0f}%")
            print(f"   🔄 进入讨论模式")
        
        return result
    
    def read_memory(self):
        """读取长期记忆"""
        memory = {}
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r') as f:
                    content = f.read()
                    if "用户:" in content:
                        memory["user"] = True
                    if "项目" in content or "技术" in content:
                        memory["projects"] = True
            except Exception as e:
                memory["error"] = str(e)
        return memory
    
    def read_user_profile(self):
        """读取用户档案"""
        profile = {}
        if self.user_file.exists():
            try:
                with open(self.user_file, 'r') as f:
                    content = f.read()
                    if "timezone" in content:
                        profile["timezone"] = content.split("timezone:")[1].strip().split("\n")[0]
            except:
                pass
        return profile
    
    def analyze_history(self, recent_messages):
        """分析历史对话"""
        analysis = {"topics": [], "patterns": [], "context": []}
        
        if not recent_messages:
            return analysis
        
        keywords = []
        for msg in recent_messages[-5:]:
            text = msg.get("content", "").lower()
            keywords.extend([w for w in ["框架", "系统", "测试", "学习", "创建"] if w in text])
        
        analysis["topics"] = list(set(keywords))
        
        short_requests = sum(1 for msg in recent_messages if len(msg.get("content", "")) < 10)
        if short_requests > 2:
            analysis["patterns"].append("用户倾向简短请求")
        
        return analysis
    
    def detect_ambiguities_v3(self, message, primary_path, history):
        """歧义检测"""
        amb = []
        msg = message.lower().strip()
        
        # 基于路径调整
        angle = primary_path.get("angle", "")
        
        # 简短请求
        if len(msg) < 4:
            amb.append({
                "type": "TOO_SHORT",
                "question": "您的请求太简短",
                "options": ["测试框架", "优化功能", "运行测试", "查看状态"],
                "weight": 1.0
            })
        
        # 路径特定歧义
        if angle == "执行任务" and len(msg) < 10:
            amb.append({
                "type": "INCOMPLETE_SPEC",
                "question": "请提供更多细节",
                "options": ["详细说明", "示例", "直接执行"],
                "weight": 0.7
            })
        
        if angle == "澄清确认":
            amb.append({
                "type": "CLARIFICATION_NEEDED",
                "question": "您想确认什么？",
                "options": ["系统状态", "功能详情", "使用方法"],
                "weight": 0.8
            })
        
        return amb
    
    def apply_experience(self, message, primary_path, history):
        """应用经验学习"""
        bonus = 0.0
        
        topics = primary_path.get("keywords", [])
        if topics:
            if any(w in topics for w in ["框架", "系统"]):
                bonus += 0.05
            if any(w in topics for w in ["测试", "检查"]):
                bonus += 0.05
        
        return bonus
    
    def discuss(self, result):
        """生成讨论问题"""
        lines = ["**🔄 反复讨论，直到明确**\n"]
        lines.append(f"当前置信度: {result['confidence']*100:.0f}%")
        lines.append(f"理解路径: {result['primary_path']['angle']}\n")
        
        if result['ambiguities']:
            lines.append("请选择或详细说明:\n")
            for i, amb in enumerate(result['ambiguities'], 1):
                lines.append(f"{i}. {amb['question']}")
                lines.append(f"   选项: {' | '.join(amb['options'])}\n")
        
        return "\n".join(lines)
    
    def think_and_respond(self, message, history=None):
        """完整思考流程"""
        result = self.think(message, history)
        
        print("\n" + "=" * 60)
        
        discussion = self.discuss(result)
        
        if discussion and not result['can_execute']:
            print(discussion)
            return {
                "action": "DISCUSS",
                "message": discussion,
                "result": result
            }
        else:
            print(f"✅ 置信度 {result['confidence']*100:.0f}% - 开始执行")
            return {
                "action": "EXECUTE",
                "message": f"开始执行: {result['primary_path']['interpretation']['intent']}",
                "result": result
            }


def demo():
    """演示"""
    print("\n" + "🧠" * 35)
    print("🧠🧠🧠🧠 COGNITIVE REASONING v3 Enhanced DEMO 🧠🧠🧠🧠")
    print("🧠🧠🧠🧠  集成多路径理解  🧠🧠🧠🧠")
    print("🧠" * 35 + "\n")
    
    thinker = ThinkLoopV3Enhanced()
    
    # 历史
    history = [
        {"content": "创建认知推理框架"},
        {"content": "升级到v2"},
        {"content": "配置全主动模式"}
    ]
    
    tests = [
        ("测试一下", history),
        ("创建新功能", history),
        ("了解机器学习", []),
        ("检查系统可用性", [{"content": "升级系统"}]),
    ]
    
    for message, hist in tests:
        print("=" * 70)
        print(f"测试: \"{message}\"")
        print("=" * 70)
        
        response = thinker.think_and_respond(message, hist)
        
        print(f"\n📋 行动: {response['action']}")
        print("-" * 70 + "\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
        thinker = ThinkLoopV3Enhanced()
        response = thinker.think_and_respond(message, [])
    else:
        demo()
