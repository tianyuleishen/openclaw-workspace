#!/usr/bin/env python3
"""
Cognitive Reasoning Framework v2 - Think First, Clarify, Then Execute
升级版：增强歧义检测和澄清循环
"""

import json
from datetime import datetime

class ThinkLoopV2:
    """增强版思考循环 - 真正理解用户意图"""
    
    def __init__(self):
        self.threshold = 0.75  # 提高阈值
        self.history = []
        
    def think(self, message):
        """
        主思考流程 - 4步结构化推理
        """
        print("\n" + "🧠" * 30)
        print("🧠🧠🧠 COGNITIVE REASONING FRAMEWORK v2 🧠🧠🧠")
        print("🧠" * 30)
        print(f"\n👤 用户: \"{message}\"")
        print(f"⏰ 时间: {datetime.now().strftime('%H:%M:%S')}")
        
        # Step 1: 意图分类
        print("\n" + "-" * 50)
        print("Step 1 🎯 意图分类")
        print("-" * 50)
        intent = self.classify_intent(message)
        print(f"  类型: {intent['type']}")
        print(f"  置信度: {intent['confidence']*100:.0f}%")
        
        # Step 2: 歧义检测（增强版）
        print("\n" + "-" * 50)
        print("Step 2 🔍 歧义检测")
        print("-" * 50)
        ambiguities = self.detect_ambiguities_v2(message, intent)
        print(f"  发现 {len(ambiguities)} 个模糊点")
        
        # Step 3: 置信度计算
        print("\n" + "-" * 50)
        print("Step 3 📊 计算置信度")
        print("-" * 50)
        confidence = self.calculate_confidence(intent, ambiguities)
        print(f"  综合置信度: {confidence*100:.0f}%")
        
        # Step 4: 决策
        print("\n" + "-" * 50)
        print("Step 4 " + ("✅ 可以执行" if confidence >= self.threshold else "⚠️ 需要澄清"))
        print("-" * 50)
        
        result = {
            "message": message,
            "intent": intent,
            "ambiguities": ambiguities,
            "confidence": confidence,
            "can_execute": confidence >= self.threshold
        }
        
        return result
    
    def classify_intent(self, message):
        """意图分类"""
        msg = message.lower().strip()
        
        # 增强的意图模式
        patterns = {
            "TEST_REQUEST": {
                "keywords": ["测试", "test", "检测", "验证", "check"],
                "desc": "测试/验证某个功能"
            },
            "EXECUTE_TASK": {
                "keywords": ["生成", "创建", "执行", "运行", "create", "make", "run"],
                "desc": "执行某个任务"
            },
            "SEARCH_INFO": {
                "keywords": ["搜索", "查找", "找", "搜索", "search"],
                "desc": "搜索信息"
            },
            "CHECK_STATUS": {
                "keywords": ["检查", "查看", "状态", "检查", "status"],
                "desc": "检查状态"
            },
            "LEARNING": {
                "keywords": ["学习", "了解", "看看", "研究", "learn"],
                "desc": "学习/了解"
            },
            "CONVERSATION": {
                "keywords": [],
                "desc": "对话/闲聊"
            }
        }
        
        # 特殊模式检测
        if msg in ["测试", "test", "试试", "试一下"]:
            return {
                "type": "AMBIGUOUS_REQUEST",
                "subtype": "TEST_REQUEST",
                "description": "这是一个模糊请求",
                "keywords": msg,
                "confidence": 0.3,  # 低置信度
                "reason": "请求过于简短，无法确定具体测试内容"
            }
        
        # 正常模式匹配
        for ptype, pdata in patterns.items():
            match_count = sum(1 for k in pdata["keywords"] if k in msg)
            if match_count > 0:
                return {
                    "type": ptype,
                    "subtype": pdata["desc"],
                    "keywords": [k for k in pdata["keywords"] if k in msg],
                    "confidence": min(0.9, 0.5 + match_count * 0.15),
                    "reason": f"检测到关键词: {', '.join([k for k in pdata['keywords'] if k in msg])}"
                }
        
        # 默认
        return {
            "type": "CONVERSATION",
            "subtype": "对话",
            "keywords": [],
            "confidence": 0.5,
            "reason": "未检测到特定关键词"
        }
    
    def detect_ambiguities_v2(self, message, intent):
        """增强版歧义检测"""
        amb = []
        msg = message.lower().strip()
        
        # 特殊歧义：过于简短
        if len(msg) < 4:
            amb.append({
                "type": "TOO_SHORT",
                "question": "您的请求太简短，我无法确定具体意图",
                "options": ["测试认知框架", "测试某个功能", "运行测试用例", "其他"],
                "weight": 1.0
            })
        
        # "测试一下"特定歧义
        if "测试" in msg and len(msg) < 10:
            amb.append({
                "type": "TEST_SCOPE_UNCLEAR",
                "question": "您想测试什么？",
                "options": [
                    "测试认知框架本身",
                    "测试某个具体功能",
                    "运行自动化测试",
                    "其他测试"
                ],
                "weight": 0.95
            })
        
        # 通用歧义
        common_ambiguities = [
            ("检查", "检查什么?", ["健康状态", "日志", "性能", "全部"]),
            ("生成", "生成什么内容?", ["图片", "视频", "文档", "其他"]),
            ("搜索", "搜索什么?", ["网络", "本地文件", "记忆", "全部"]),
            ("查看", "查看什么?", ["当前状态", "历史记录", "配置", "全部"]),
        ]
        
        for keyword, question, options in common_ambiguities:
            if keyword in msg and len(msg) < 15:
                amb.append({
                    "type": "INCOMPLETE_SPEC",
                    "question": question,
                    "options": options,
                    "weight": 0.7
                })
        
        return amb
    
    def calculate_confidence(self, intent, ambiguities):
        """计算置信度"""
        score = intent.get("confidence", 0.5)
        
        # 惩罚歧义
        for amb in ambiguities:
            score -= amb["weight"] * 0.2
        
        # 惩罚过于简短
        if len(intent.get("message", "")) < 4:
            score -= 0.3
        
        return max(0, min(1, score))
    
    def format_clarification(self, result):
        """生成澄清请求"""
        if result["can_execute"]:
            return None
        
        lines = ["**⚠️ 请求不够明确，需要澄清**\n"]
        
        lines.append(f"我理解您想: **{result['intent']['subtype']}**")
        lines.append(f"置信度: {result['confidence']*100:.0f}%")
        lines.append("\n请选择或详细说明:\n")
        
        for i, amb in enumerate(result["ambiguities"], 1):
            lines.append(f"{i}. {amb['question']}")
            lines.append(f"   选项: {' | '.join(amb['options'])}")
        
        return "\n".join(lines)
    
    def think_and_respond(self, message):
        """
        完整思考流程 - 返回澄清或执行确认
        """
        result = self.think(message)
        
        print("\n" + "=" * 50)
        
        clarification = self.format_clarification(result)
        
        if clarification:
            print(clarification)
            return {
                "action": "CLARIFY",
                "message": clarification,
                "result": result
            }
        else:
            print(f"✅ 高置信度 ({result['confidence']*100:.0f}%)，可以执行")
            return {
                "action": "EXECUTE",
                "message": f"开始执行: {result['intent']['type']}",
                "result": result
            }


def demo():
    """演示"""
    thinker = ThinkLoopV2()
    
    tests = [
        "测试一下",           # 模糊请求
        "检查服务器",         # 中等歧义
        "生成一个视频",       # 有歧义
        "查看今天的文件"      # 较明确
    ]
    
    for msg in tests:
        print("\n" + "=" * 60)
        print(f"测试: \"{msg}\"")
        print("=" * 60)
        
        response = thinker.think_and_respond(msg)
        
        print(f"\n📋 行动: {response['action']}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # 从命令行参数读取
        thinker = ThinkLoopV2()
        response = thinker.think_and_respond(" ".join(sys.argv[1:]))
    else:
        demo()
