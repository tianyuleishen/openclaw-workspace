#!/usr/bin/env python3
"""
认知推理测试 - 思考后执行
"""

import json
from datetime import datetime

class ThinkLoop:
    """简化版思考循环"""
    
    def __init__(self):
        self.threshold = 0.7
        
    def classify_intent(self, message):
        """意图分类"""
        msg = message.lower()
        
        patterns = [
            ("EXECUTE_TASK", ["生成", "create", "make", "做", "执行"], 0.9),
            ("CHECK_STATUS", ["检查", "查看", "check", "看", "状态"], 0.85),
            ("SEARCH_INFO", ["搜索", "查找", "search", "找"], 0.8),
            ("LEARNING", ["学习", "了解", "看看", "研究"], 0.75),
        ]
        
        for p_type, keywords, base in patterns:
            if any(k in msg for k in keywords):
                return {"type": p_type, "confidence": base}
        
        return {"type": "CONVERSATION", "confidence": 0.6}
    
    def detect_ambiguities(self, message):
        """检测歧义"""
        amb = []
        msg = message.lower()
        
        if "检查" in msg or "check" in msg:
            amb.append({
                "type": "INCOMPLETE_SPEC",
                "question": "具体检查什么?",
                "options": ["健康状态", "日志", "性能", "全部"]
            })
        
        if "生成" in msg or "create" in msg:
            amb.append({
                "type": "FORMAT_UNCLEAR",
                "question": "输出格式是什么?",
                "options": ["文件", "链接", "仅显示"]
            })
        
        if "视频" in msg or "video" in msg:
            amb.append({
                "type": "SPEC_UNCLEAR",
                "question": "时长和分辨率?",
                "options": ["5秒/720P", "10秒/720P", "15秒/1080P"]
            })
        
        return amb
    
    def calculate_confidence(self, intent, ambiguities):
        """计算置信度"""
        score = intent["confidence"]
        for amb in ambiguities:
            score -= 0.2
        return max(0, min(1, score))
    
    def think(self, message):
        """主思考流程"""
        print("\n" + "🧠" * 25)
        print("🧠 COGNITIVE REASONING - THINK LOOP")
        print("🧠" * 25)
        print("")
        print(f"👤 用户: \"{message}\"")
        print("")
        
        # Step 1: 意图分类
        print("Step 1: 🎯 意图分类...")
        intent = self.classify_intent(message)
        print(f"       意图: {intent['type']} ({intent['confidence']*100:.0f}%)")
        print("")
        
        # Step 2: 歧义检测
        print("Step 2: 🔍 歧义检测...")
        ambiguities = self.detect_ambiguities(message)
        print(f"       发现 {len(ambiguities)} 个模糊点")
        print("")
        
        # Step 3: 置信度
        print("Step 3: 📊 计算置信度...")
        confidence = self.calculate_confidence(intent, ambiguities)
        print(f"       置信度: {confidence*100:.0f}%")
        print("")
        
        # Step 4: 决策
        print("Step 4: " + ("✅ 高置信度 - 可以执行" if confidence >= self.threshold else "⚠️ 低置信度 - 需要澄清"))
        print("")
        
        return {
            "intent": intent,
            "ambiguities": ambiguities,
            "confidence": confidence,
            "can_execute": confidence >= self.threshold
        }


def run_tests():
    """运行测试"""
    thinker = ThinkLoop()
    
    tests = [
        "检查服务器",
        "生成一个视频要快又要便宜",
        "查看今天的所有文件",
        "检查8080端口是否运行"
    ]
    
    for i, msg in enumerate(tests, 1):
        print("=" * 60)
        print(f"测试 {i}: {msg}")
        print("=" * 60)
        
        result = thinker.think(msg)
        
        print("\n📊 结果:")
        print(f"   意图: {result['intent']['type']}")
        print(f"   置信度: {result['confidence']*100:.0f}%")
        print(f"   可以执行: {'✅ 是' if result['can_execute'] else '⚠️ 否，需要澄清'}")
        
        if not result['can_execute'] and result['ambiguities']:
            print("\n💬 澄清问题:")
            for q in result['ambiguities']:
                print(f"   • {q['question']}")
                print(f"     选项: {' | '.join(q['options'])}")
        
        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    run_tests()
