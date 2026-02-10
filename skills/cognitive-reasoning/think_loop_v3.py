#!/usr/bin/env python3
"""
Cognitive Reasoning Framework v3 - Auto Multi-Path Understanding
主动集成多路径理解的认知框架

核心能力：
- 主动集成多路径理解 (Multi-Path Understanding)
- 记忆集成：读取MEMORY.md、USER.md
- 历史分析：分析最近对话
- 经验学习：累积学习用户偏好
- 思维树推理：多路径探索，选择最优
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# 导入多路径理解
from multi_path import MultiPathUnderstanding


class ThinkLoopV3:
    """
    认知推理框架v3 - 主动多路径理解版
    
    使用模式：主动使用
    - 每次用户请求自动触发多路径理解
    - 无需手动调用，透明运行
    """
    
    def __init__(self):
        self.threshold = 0.75  # 阈值
        self.memory_dir = Path.home() / ".openclaw/workspace/memory"
        self.memory_file = Path.home() / ".openclaw/workspace/MEMORY.md"
        self.user_file = Path.home() / ".openclaw/workspace/USER.md"
        self.learning_file = Path.home() / ".openclaw/workspace/.intent_learning.json"
        
        # 多路径理解器 (主动集成)
        self.mpu = MultiPathUnderstanding()
        
        # 加载学习数据
        self.learning_data = self._load_learning_data()
        
        print("\n🧠 认知框架v3 - 主动多路径理解模式已启动")
        print(f"   阈值: {self.threshold*100:.0f}%")
        print(f"   多路径理解: ✅ 主动集成")
    
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
    
    def think(self, message, history=None):
        """
        主思考流程v3 - 主动多路径理解版
        
        Returns:
            dict: 思考结果
        """
        print("\n" + "🧠" * 35)
        print("🧠🧠🧠 COGNITIVE REASONING FRAMEWORK v3 🧠🧠🧠")
        print("🧠🧠🧠  主动多路径理解模式  🧠🧠🧠")
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
        history_analysis = self.analyze_history(history or [])
        
        print(f"   长期记忆: {'✅ 已加载' if memory else '❌ 空'}")
        print(f"   用户档案: {'✅ 已加载' if profile else '❌ 空'}")
        print(f"   历史分析: {len(history_analysis.get('topics', []))} 个话题")
        
        # Step 1: 主动多路径理解 (核心升级)
        print("\n" + "-" * 60)
        print("Step 1 🎯 主动多路径理解 (Tree of Thoughts)")
        print("-" * 60)
        
        # 主动调用多路径理解
        multi_path_result = self.mpu.understand(message, history or [], max_paths=3)
        
        primary = multi_path_result["primary"]
        alternatives = multi_path_result["alternatives"]
        
        print(f"   ✅ 主动触发多路径理解")
        print(f"   📊 生成路径: {multi_path_result['path_count']}个")
        print(f"   🎯 主路径: {primary['angle']} ({primary['score']*100:.0f}%)")
        
        if alternatives:
            print(f"   📋 候选路径:")
            for i, alt in enumerate(alternatives[:2], 1):
                print(f"      {i}. {alt['angle']} ({alt['score']*100:.0f}%)")
        
        # Step 2: 歧义检测（历史增强）
        print("\n" + "-" * 60)
        print("Step 2 🔍 歧义检测（历史增强）")
        print("-" * 60)
        ambiguities = self.detect_ambiguities(message, primary, history_analysis)
        print(f"   发现 {len(ambiguities)} 个模糊点")
        
        # Step 3: 经验学习
        print("\n" + "-" * 60)
        print("Step 3 📈 经验学习")
        print("-" * 60)
        experience_bonus = self.apply_experience(message, primary, history_analysis)
        print(f"   经验加成: +{experience_bonus*100:.0f}%")
        
        # Step 4: 综合置信度
        print("\n" + "-" * 60)
        print("Step 4 📊 综合置信度")
        print("-" * 60)
        
        # 综合评分 = 多路径评分 + 经验 - 歧义惩罚
        base_score = primary["score"]
        
        # 歧义惩罚
        for amb in ambiguities:
            base_score -= amb.get("weight", 0.3) * 0.1
        
        # 最终置信度
        final_confidence = min(0.98, base_score + experience_bonus)
        
        print(f"   多路径基础分: {base_score*100:.0f}%")
        print(f"   歧义惩罚: -{sum([amb.get('weight', 0.3)*0.1 for amb in ambiguities])*100:.0f}%")
        print(f"   经验加成: +{experience_bonus*100:.0f}%")
        print(f"   📈 最终置信度: {final_confidence*100:.0f}%")
        
        # Step 5: 决策
        print("\n" + "-" * 60)
        print("Step 5 " + ("✅ 可以执行" if final_confidence >= self.threshold else "🔄 反复讨论"))
        print("-" * 60)
        
        result = {
            "message": message,
            "timestamp": timestamp,
            "memory": memory,
            "history_analysis": history_analysis,
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
            print(f"   ✅ 置信度 {final_confidence*100:.0f}% ≥ {self.threshold*100:.0f}%")
            print(f"   🎯 执行意图: {primary['interpretation']['intent']}")
            
            # 自动保存决策
            self._auto_save_decision(result)
        else:
            print(f"   ⚠️ 置信度 {final_confidence*100:.0f}% < {self.threshold*100:.0f}%")
            print(f"   🔄 进入澄清模式")
        
        return result
    
    def _auto_save_decision(self, result):
        """自动保存决策到记忆"""
        try:
            daily_file = Path.home() / ".openclaw/workspace/memory" / f"{datetime.now().strftime('%Y-%m-%d')}.md"
            daily_file.parent.mkdir(exist_ok=True)
            
            entry = f"""
### AUTO_SAVE - {result['timestamp']}

**执行决策**

- 意图: {result['primary_path']['interpretation']['intent']}
- 置信度: {result['confidence']*100:.0f}%
- 理解路径: {result['primary_path']['angle']}

"""
            with open(daily_file, 'a', encoding='utf-8') as f:
                f.write(entry)
            
            print(f"   💾 决策已自动保存")
        except Exception as e:
            print(f"   ⚠️ 自动保存失败: {e}")
    
    def read_memory(self):
        """读取长期记忆"""
        memory = {}
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
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
                with open(self.user_file, 'r', encoding='utf-8') as f:
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
    
    def detect_ambiguities(self, message, primary_path, history_analysis):
        """歧义检测"""
        amb = []
        msg = message.lower().strip()
        angle = primary_path.get("angle", "")
        
        # 简短请求
        if len(msg) < 4:
            amb.append({
                "type": "TOO_SHORT",
                "question": "您的请求太简短",
                "options": ["测试框架", "优化功能", "运行测试", "查看状态"],
                "weight": 1.0
            })
        
        # 执行任务特定歧义
        if angle == "执行任务" and len(msg) < 15:
            amb.append({
                "type": "INCOMPLETE_SPEC",
                "question": "需要更多细节",
                "options": ["详细说明", "直接执行"],
                "weight": 0.6
            })
        
        return amb
    
    def apply_experience(self, message, primary_path, history_analysis):
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
        """生成澄清问题"""
        lines = ["**🔄 反复讨论，直到明确**\n"]
        lines.append(f"置信度: {result['confidence']*100:.0f}%")
        lines.append(f"理解路径: {result['primary_path']['angle']}\n")
        
        if result['ambiguities']:
            lines.append("请选择:\n")
            for i, amb in enumerate(result['ambiguities'], 1):
                lines.append(f"{i}. {amb['question']}")
                lines.append(f"   选项: {' | '.join(amb['options'])}\n")
        
        # 显示候选路径
        if result['alternatives']:
            lines.append("其他理解方式:")
            for i, alt in enumerate(result['alternatives'][:2], 1):
                lines.append(f"   {i}. {alt['angle']}: {alt['interpretation']['intent']}")
        
        return "\n".join(lines)
    
    def think_and_respond(self, message, history=None):
        """
        完整思考流程
        
        使用方法（主动模式）:
            result = thinker.think("用户消息")
        无需手动调用think()，框架自动运行完整流程
        """
        result = self.think(message, history)
        
        print("\n" + "=" * 60)
        
        discussion = self.discuss(result)
        
        if not result['can_execute']:
            print(discussion)
            return {
                "action": "DISCUSS",
                "message": discussion,
                "result": result
            }
        else:
            print(f"✅ 开始执行: {result['primary_path']['interpretation']['intent']}")
            return {
                "action": "EXECUTE",
                "message": f"执行: {result['primary_path']['interpretation']['intent']}",
                "result": result
            }


def demo():
    """演示"""
    print("\n" + "🧠" * 35)
    print("🧠🧠🧠🧠 COGNITIVE REASONING v3 DEMO 🧠🧠🧠🧠")
    print("🧠🧠🧠🧠  主动多路径理解  🧠🧠🧠🧠")
    print("🧠" * 35 + "\n")
    
    thinker = ThinkLoopV3()
    
    history = [
        {"content": "创建认知推理框架"},
        {"content": "升级到v2"},
        {"content": "配置全主动模式"}
    ]
    
    tests = [
        "测试一下",
        "创建新功能",
        "了解机器学习",
        "检查系统可用性"
    ]
    
    for msg in tests:
        print("\n" + "=" * 70)
        print(f"测试: \"{msg}\"")
        print("=" * 70)
        
        response = thinker.think_and_respond(msg, history)
        
        print(f"\n📊 结果: {response['action']}")
        print("-" * 70 + "\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
        thinker = ThinkLoopV3()
        response = thinker.think_and_respond(message, [])
    else:
        demo()
