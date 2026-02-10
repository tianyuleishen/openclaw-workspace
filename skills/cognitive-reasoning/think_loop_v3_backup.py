#!/usr/bin/env python3
"""
Cognitive Reasoning Framework v3 - Memory-Aware Intent Understanding
升级版：集成历史对话、用户记忆、经验学习
"""

import json
import os
from datetime import datetime
from pathlib import Path

class ThinkLoopV3:
    """
    认知推理框架v3
    核心能力：
    - 记忆集成：读取MEMORY.md、USER.md
    - 历史分析：分析最近对话
    - 经验学习：累积学习用户偏好
    - 多轮澄清：反复讨论直到明确
    """
    
    def __init__(self):
        self.threshold = 0.80  # 提高阈值
        self.memory_dir = Path.home() / ".openclaw/workspace/memory"
        self.memory_file = Path.home() / ".openclaw/workspace/MEMORY.md"
        self.user_file = Path.home() / ".openclaw/workspace/USER.md"
        self.learning_file = Path.home() / ".openclaw/workspace/.intent_learning.json"
        
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
    
    def _save_learning_data(self):
        """保存学习数据"""
        with open(self.learning_file, 'w') as f:
            json.dump(self.learning_data, f, ensure_ascii=False, indent=2)
    
    def read_memory(self):
        """读取长期记忆"""
        memory = {}
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r') as f:
                    content = f.read()
                    # 提取关键信息
                    if "用户:" in content:
                        memory["user_preferences"] = self._extract_section(content, "USER.md", "##")
                    if "项目" in content:
                        memory["projects"] = self._extract_section(content, "项目", "##")
                    if "技术" in content:
                        memory["technologies"] = self._extract_section(content, "技术", "##")
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
                    # 提取用户偏好
                    if "timezone" in content:
                        profile["timezone"] = content.split("timezone:")[1].strip().split("\n")[0]
                    if "Notes" in content:
                        profile["notes"] = content.split("Notes:")[1].strip()
            except:
                pass
        return profile
    
    def analyze_history(self, recent_messages):
        """分析历史对话"""
        analysis = {
            "topics": [],
            "patterns": [],
            "context": []
        }
        
        if not recent_messages:
            return analysis
            
        # 分析话题趋势
        keywords = []
        for msg in recent_messages[-5:]:  # 最近5条
            text = msg.get("content", "").lower()
            keywords.extend([w for w in ["测试", "生成", "视频", "认知", "框架"] if w in text])
        
        analysis["topics"] = list(set(keywords))
        
        # 分析用户说话模式
        short_requests = sum(1 for msg in recent_messages if len(msg.get("content", "")) < 10)
        if short_requests > 2:
            analysis["patterns"].append("用户倾向简短请求")
        
        # 分析上下文
        if recent_messages:
            last_msg = recent_messages[-1].get("content", "")
            if "升级" in last_msg or "优化" in last_msg:
                analysis["context"].append("用户正在进行系统优化")
        
        return analysis
    
    def learn_from_interaction(self, message, clarification, response):
        """从交互中学习"""
        # 学习用户偏好
        if "测试" in message:
            self.learning_data["user_patterns"]["test_preference"] = "用户经常测试系统"
        
        # 学习澄清效果
        if clarification:
            self.learning_data["clarification_count"] += 1
        
        self._save_learning_data()
    
    def think(self, message, history=None):
        """
        主思考流程v3 - 集成记忆、历史、经验
        """
        print("\n" + "🧠" * 35)
        print("🧠🧠🧠 COGNITIVE REASONING FRAMEWORK v3 🧠🧠🧠")
        print("🧠🧠🧠  集成记忆·历史·经验  🧠🧠🧠")
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
        analysis = self.analyze_history(history or [])
        
        print(f"   长期记忆: {'✅ 已加载' if memory else '❌ 空'}")
        print(f"   用户档案: {'✅ 已加载' if profile else '❌ 空'}")
        print(f"   历史分析: {len(analysis.get('topics', []))} 个话题")
        
        # Step 1: 意图分类（带记忆）
        print("\n" + "-" * 60)
        print("Step 1 🎯 意图分类（记忆增强）")
        print("-" * 60)
        intent = self.classify_intent_v3(message, memory, profile)
        print(f"   类型: {intent['type']}")
        print(f"   置信度: {intent['confidence']*100:.0f}%")
        print(f"   依据: {intent.get('reason', '基础分类')}")
        
        # Step 2: 歧义检测（带历史）
        print("\n" + "-" * 60)
        print("Step 2 🔍 歧义检测（历史增强）")
        print("-" * 60)
        ambiguities = self.detect_ambiguities_v3(message, intent, analysis)
        print(f"   发现 {len(ambiguities)} 个模糊点")
        
        # Step 3: 经验学习
        print("\n" + "-" * 60)
        print("Step 3 📈 经验学习")
        print("-" * 60)
        experience_bonus = self.apply_experience(message, intent, analysis)
        print(f"   经验加成: +{experience_bonus*100:.0f}%")
        
        # Step 4: 置信度计算
        print("\n" + "-" * 60)
        print("Step 4 📊 综合置信度")
        print("-" * 60)
        base_confidence = self.calculate_confidence(intent, ambiguities)
        final_confidence = min(0.98, base_confidence + experience_bonus)
        print(f"   基础置信度: {base_confidence*100:.0f}%")
        print(f"   最终置信度: {final_confidence*100:.0f}%")
        
        # Step 5: 决策（多轮澄清）
        print("\n" + "-" * 60)
        print("Step 5 " + ("✅ 可以执行" if final_confidence >= self.threshold else "🔄 反复讨论"))
        print("-" * 60)
        
        result = {
            "message": message,
            "timestamp": timestamp,
            "memory": memory,
            "history_analysis": analysis,
            "intent": intent,
            "ambiguities": ambiguities,
            "confidence": final_confidence,
            "experience_bonus": experience_bonus,
            "can_execute": final_confidence >= self.threshold,
            "rounds": 1
        }
        
        if final_confidence >= self.threshold:
            print(f"   置信度 {final_confidence*100:.0f}% ≥ {self.threshold*100:.0f}%")
            print(f"   ✅ 执行任务")
            
            # === 全主动模式：自动保存决策 ===
            try:
                from auto_save import AutoMemorySaver
                saver = AutoMemorySaver()
                saver.save_decision(
                    decision_type="DECISION",
                    content=f"执行: {intent['type']} - {message}",
                    confidence=final_confidence,
                    context=f"经验加成 +{experience_bonus*100:.0f}%"
                )
                print(f"   💾 决策已自动保存")
            except Exception as e:
                print(f"   ⚠️ 自动保存失败: {e}")
            # ====================================
        else:
            print(f"   置信度 {final_confidence*100:.0f}% < {self.threshold*100:.0f}%")
            print(f"   🔄 进入讨论模式")
        
        return result
    
    def classify_intent_v3(self, message, memory, profile):
        """记忆增强的意图分类"""
        msg = message.lower().strip()
        
        # 基于历史学习调整权重
        learned_patterns = self.learning_data.get("user_patterns", {})
        
        # 增强模式
        patterns = {
            "TEST_FRAMEWORK": {
                "keywords": ["测试", "test", "检测", "验证", "检查框架"],
                "base_confidence": 0.85,
                "reason": "用户经常测试系统"
            },
            "OPTIMIZE_SYSTEM": {
                "keywords": ["升级", "优化", "改进", "增强"],
                "base_confidence": 0.80,
                "reason": "用户关注系统优化"
            },
            "EXECUTE_TASK": {
                "keywords": ["生成", "创建", "执行", "运行"],
                "base_confidence": 0.75
            },
            "CHECK_STATUS": {
                "keywords": ["检查", "查看", "状态"],
                "base_confidence": 0.70
            },
            "LEARNING": {
                "keywords": ["学习", "了解", "看看"],
                "base_confidence": 0.65
            }
        }
        
        # 特殊模式："X框架" 或 "X系统"
        if any(word in msg for word in ["框架", "系统", "skill"]):
            for pname, pdata in patterns.items():
                if any(k in msg for k in pdata.get("keywords", [])):
                    return {
                        "type": pname,
                        "confidence": pdata["base_confidence"],
                        "reason": pdata.get("reason", "关键词匹配")
                    }
        
        # 简短请求特殊处理
        if len(msg) < 4:
            return {
                "type": "AMBIGUOUS_REQUEST",
                "confidence": 0.20,
                "reason": "请求过短，需要澄清",
                "needs_discussion": True
            }
        
        # 默认分类
        return {
            "type": "CONVERSATION",
            "confidence": 0.50,
            "reason": "默认分类"
        }
    
    def detect_ambiguities_v3(self, message, intent, history_analysis):
        """历史增强的歧义检测"""
        amb = []
        msg = message.lower().strip()
        
        # 1. 基于历史上下文调整
        topics = history_analysis.get("topics", [])
        
        # 2. 标准歧义检测
        if len(msg) < 4:
            amb.append({
                "type": "TOO_SHORT",
                "question": "您的请求太简短",
                "options": ["测试框架", "优化功能", "运行测试", "查看状态"],
                "weight": 1.0,
                "history_context": topics
            })
        
        # 3. 框架相关歧义
        if any(w in msg for w in ["框架", "系统", "skill"]):
            if "可用" in msg or "能用" in msg or "可以" in msg:
                amb.append({
                    "type": "FRAMEWORK_AVAILABILITY",
                    "question": "您想检测框架的哪方面?",
                    "options": ["启动测试", "功能测试", "压力测试", "集成测试"],
                    "weight": 0.9
                })
        
        # 4. "升级"歧义
        if "升级" in msg:
            amb.append({
                "type": "UPGRADE_SCOPE",
                "question": "升级什么?",
                "options": ["核心引擎", "测试用例", "文档", "全部"],
                "weight": 0.85
            })
        
        return amb
    
    def apply_experience(self, message, intent, history_analysis):
        """应用经验学习"""
        bonus = 0.0
        
        # 基于历史话题加分
        topics = history_analysis.get("topics", [])
        if "框架" in topics or "测试" in topics:
            bonus += 0.10  # 用户在讨论这个领域
        
        # 基于用户模式
        patterns = self.learning_data.get("user_patterns", {})
        if "test_preference" in patterns:
            if "测试" in message.lower():
                bonus += 0.05
        
        return bonus
    
    def calculate_confidence(self, intent, ambiguities):
        """计算置信度"""
        score = intent.get("confidence", 0.5)
        
        # 歧义惩罚
        for amb in ambiguities:
            score -= amb.get("weight", 0.5) * 0.15
        
        return max(0, min(1, score))
    
    def discuss(self, result):
        """生成讨论/澄清问题"""
        if result["can_execute"]:
            return None
        
        lines = ["**🔄 反复讨论，直到明确**\n"]
        lines.append(f"当前置信度: {result['confidence']*100:.0f}%")
        lines.append(f"意图: {result['intent']['type']}\n")
        
        if result["ambiguities"]:
            lines.append("请选择或详细说明:\n")
            for i, amb in enumerate(result["ambiguities"], 1):
                lines.append(f"{i}. {amb['question']}")
                lines.append(f"   选项: {' | '.join(amb['options'])}")
        
        # 添加历史上下文
        topics = result.get("history_analysis", {}).get("topics", [])
        if topics:
            lines.append(f"\n💡 上下文: 您最近在讨论 {', '.join(topics)}")
        
        return "\n".join(lines)
    
    def think_and_respond(self, message, history=None):
        """完整思考流程"""
        result = self.think(message, history)
        
        print("\n" + "=" * 60)
        
        discussion = self.discuss(result)
        
        if discussion:
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
                "message": f"开始执行: {result['intent']['type']}",
                "result": result
            }
    
    def record_learning(self, original_msg, clarified_msg, final_intent):
        """记录学习（用于持续优化）"""
        self.learning_data["user_patterns"][original_msg] = {
            "clarified_to": clarified_msg,
            "final_intent": final_intent,
            "timestamp": datetime.now().isoformat()
        }
        self._save_learning_data()


def demo():
    """演示"""
    thinker = ThinkLoopV3()
    
    # 模拟历史对话
    history = [
        {"content": "创建一个新的技能"},
        {"content": "测试一下视频生成"},
        {"content": "升级认知推理框架"}
    ]
    
    tests = [
        "检测一下你这个认知推理框架是否可用",
        "测试一下",
        "优化系统"
    ]
    
    for msg in tests:
        print("\n" + "=" * 70)
        print(f"测试: \"{msg}\"")
        print("=" * 70)
        
        response = thinker.think_and_respond(msg, history)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        thinker = ThinkLoopV3()
        response = thinker.think_and_respond(" ".join(sys.argv[1:]))
    else:
        demo()
