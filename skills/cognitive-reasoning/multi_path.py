#!/usr/bin/env python3
"""
Multi-Path Understanding Generator - 思维树推理实践
多路径理解生成：从不同角度分析用户请求，提高意图识别准确率
"""

import json
import sys
from datetime import datetime
from pathlib import Path

class MultiPathUnderstanding:
    """
    多路径理解生成器
    
    核心功能：
    - 从多个角度理解用户请求
    - 评估每条路径的质量
    - 选择最优理解或返回候选
    """
    
    def __init__(self):
        self.workspace = Path.home() / ".openclaw/workspace"
        
    def understand(self, message, history=None, max_paths=3):
        """
        多路径理解
        
        Args:
            message: 用户消息
            history: 历史对话
            max_paths: 最大路径数
        
        Returns:
            dict: 包含主路径和候选路径
        """
        # Step 1: 生成多个理解角度
        paths = self._generate_paths(message, history, max_paths)
        
        # Step 2: 评估每个路径
        evaluated = self._evaluate_paths(paths, message, history)
        
        # Step 3: 选择最优路径
        best = evaluated[0]
        alternatives = evaluated[1:]
        
        return {
            "primary": best,
            "alternatives": alternatives,
            "path_count": len(evaluated),
            "timestamp": datetime.now().isoformat()
        }
    
    def _generate_paths(self, message, history, max_paths):
        """生成多个理解路径"""
        paths = []
        
        # 路径1: 执行任务视角
        paths.append({
            "id": "path_1",
            "angle": "执行任务",
            "perspective": "用户想让我执行某个具体任务",
            "interpretation": self._interpret_from_angle(message, "执行任务"),
            "keywords": self._extract_keywords(message)
        })
        
        # 路径2: 澄清确认视角
        if max_paths >= 2:
            paths.append({
                "id": "path_2",
                "angle": "澄清确认",
                "perspective": "用户想确认或澄清某个问题",
                "interpretation": self._interpret_from_angle(message, "澄清确认"),
                "keywords": self._extract_keywords(message)
            })
        
        # 路径3: 学习探索视角
        if max_paths >= 3:
            paths.append({
                "id": "path_3",
                "angle": "学习探索",
                "perspective": "用户想学习或了解某个主题",
                "interpretation": self._interpret_from_angle(message, "学习探索"),
                "keywords": self._extract_keywords(message)
            })
        
        # 路径4: 讨论交流视角
        if max_paths >= 4:
            paths.append({
                "id": "path_4",
                "angle": "讨论交流",
                "perspective": "用户想进行讨论或交流观点",
                "interpretation": self._interpret_from_angle(message, "讨论交流"),
                "keywords": self._extract_keywords(message)
            })
        
        # 路径5: 系统检查视角
        if max_paths >= 5:
            paths.append({
                "id": "path_5",
                "angle": "系统检查",
                "perspective": "用户想检查或测试系统功能",
                "interpretation": self._interpret_from_angle(message, "系统检查"),
                "keywords": self._extract_keywords(message)
            })
        
        return paths[:max_paths]
    
    def _interpret_from_angle(self, message, angle):
        """从特定角度解释用户意图"""
        msg_lower = message.lower()
        
        # 基于关键词的意图分类
        intent_patterns = {
            "创建": ("CREATE", 0.9),
            "生成": ("CREATE", 0.85),
            "执行": ("EXECUTE", 0.9),
            "运行": ("EXECUTE", 0.85),
            "测试": ("TEST", 0.95),
            "检查": ("CHECK", 0.9),
            "查看": ("CHECK", 0.8),
            "搜索": ("SEARCH", 0.9),
            "查找": ("SEARCH", 0.85),
            "学习": ("LEARN", 0.9),
            "了解": ("LEARN", 0.85),
            "优化": ("OPTIMIZE", 0.95),
            "升级": ("UPGRADE", 0.95),
            "配置": ("CONFIG", 0.9),
            "设置": ("CONFIG", 0.85),
            "讲解": ("EXPLAIN", 0.9),
            "详细": ("EXPLAIN", 0.8),
            "诊断": ("DIAGNOSE", 0.9),
            "问题": ("DIAGNOSE", 0.7),
        }
        
        # 检测意图
        detected_intent = "CONVERSATION"
        max_score = 0.5
        
        for keyword, (intent, score) in intent_patterns.items():
            if keyword in msg_lower:
                if score > max_score:
                    detected_intent = intent
                    max_score = score
        
        # 基于角度调整
        if angle == "执行任务":
            intent = detected_intent if max_score >= 0.8 else "EXECUTE_TASK"
            confidence = 0.7 if max_score < 0.8 else max_score
        
        elif angle == "澄清确认":
            intent = "CLARIFY" if len(message) < 20 else detected_intent
            confidence = 0.6 if len(message) < 20 else 0.5
        
        elif angle == "学习探索":
            intent = "LEARNING" if any(k in msg_lower for k in ["学习", "了解", "什么", "how"]) else detected_intent
            confidence = 0.7
        
        elif angle == "讨论交流":
            intent = "CONVERSATION"
            confidence = 0.6
        
        elif angle == "系统检查":
            intent = "TEST_SYSTEM" if any(k in msg_lower for k in ["测试", "检查", "诊断", "可用"]) else detected_intent
            confidence = 0.8 if any(k in msg_lower for k in ["测试", "检查", "诊断", "可用"]) else 0.5
        
        else:
            intent = detected_intent
            confidence = max_score
        
        return {
            "intent": intent,
            "confidence": confidence,
            "reason": f"从{angle}角度分析"
        }
    
    def _extract_keywords(self, message):
        """提取关键词"""
        keywords = []
        
        action_words = ["创建", "生成", "执行", "运行", "测试", "检查", "查看", 
                        "搜索", "查找", "学习", "了解", "优化", "升级", "配置",
                        "讲解", "详细", "诊断", "集成", "部署"]
        
        for word in action_words:
            if word in message:
                keywords.append(word)
        
        if not keywords:
            # 尝试提取名词
            if "框架" in message:
                keywords.append("框架")
            if "系统" in message:
                keywords.append("系统")
            if "功能" in message:
                keywords.append("功能")
            if "问题" in message:
                keywords.append("问题")
        
        return keywords[:5]  # 最多5个关键词
    
    def _evaluate_paths(self, paths, message, history):
        """评估每条路径的质量"""
        evaluated = []
        
        # 历史上下文分析
        topics = []
        if history:
            for h in history[-5:]:
                content = h.get("content", "").lower()
                if "框架" in content or "系统" in content:
                    topics.append("system")
                if "创建" in content or "生成" in content:
                    topics.append("creation")
                if "学习" in content or "了解" in content:
                    topics.append("learning")
        
        for path in paths:
            score = 0.0
            reasons = []
            
            # 1. 关键词匹配度 (40%)
            keywords = path.get("keywords", [])
            if keywords:
                score += 0.4
                reasons.append("包含有效关键词")
            
            # 2. 历史一致性 (30%)
            if topics:
                if path["angle"] == "系统检查" and "system" in topics:
                    score += 0.3
                    reasons.append("与历史话题一致")
                elif path["angle"] == "学习探索" and "learning" in topics:
                    score += 0.3
                    reasons.append("与历史话题一致")
                elif path["angle"] == "执行任务" and "creation" in topics:
                    score += 0.3
                    reasons.append("与历史话题一致")
            
            # 3. 置信度 (30%)
            interp = path["interpretation"]
            confidence = interp.get("confidence", 0.5)
            score += confidence * 0.3
            
            # 综合评分
            final_score = min(0.98, score)
            
            evaluated.append({
                **path,
                "score": final_score,
                "reasons": reasons,
                "analysis": {
                    "keyword_match": 0.4 if keywords else 0,
                    "history_consistency": 0.3 if topics else 0,
                    "confidence": confidence * 0.3
                }
            })
        
        # 按分数排序
        return sorted(evaluated, key=lambda x: x["score"], reverse=True)
    
    def format_result(self, result):
        """格式化输出结果"""
        lines = []
        
        lines.append("**🧠 多路径理解分析**\n")
        
        # 主路径
        primary = result["primary"]
        lines.append(f"**主路径 ({primary['angle']})**")
        lines.append(f"  意图: {primary['interpretation']['intent']}")
        lines.append(f"  置信度: {primary['interpretation']['confidence']*100:.0f}%")
        lines.append(f"  综合评分: {primary['score']*100:.0f}%")
        
        if primary.get("keywords"):
            lines.append(f"  关键词: {', '.join(primary['keywords'])}")
        
        # 候选路径
        if result["alternatives"]:
            lines.append(f"\n**候选路径 ({len(result['alternatives'])}个)**\n")
            
            for i, alt in enumerate(result["alternatives"], 1):
                lines.append(f"{i}. **{alt['angle']}**")
                lines.append(f"   意图: {alt['interpretation']['intent']}")
                lines.append(f"   评分: {alt['score']*100:.0f}%")
        
        # 建议
        if result["primary"]["score"] >= 0.8:
            lines.append(f"\n✅ **建议**: 采用主路径")
        elif result["primary"]["score"] >= 0.6:
            lines.append(f"\n⚠️ **建议**: 主路径置信度中等，可结合候选路径")
        else:
            lines.append(f"\n🔄 **建议**: 置信度较低，建议澄清确认")
        
        return "\n".join(lines)


def demo():
    """演示"""
    print("\n" + "=" * 60)
    print("🧠 多路径理解生成演示")
    print("=" * 60 + "\n")
    
    mpu = MultiPathUnderstanding()
    
    # 测试案例
    test_cases = [
        ("测试一下", []),
        ("创建认知框架", [{"content": "升级系统"}]),
        ("了解机器学习", [{"content": "学习AI技术"}]),
        ("检查系统可用性", [{"content": "配置框架"}]),
    ]
    
    for message, history in test_cases:
        print(f"📝 用户: \"{message}\"")
        print("-" * 40)
        
        result = mpu.understand(message, history, max_paths=3)
        output = mpu.format_result(result)
        print(output)
        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # 从命令行读取消息
        message = " ".join(sys.argv[1:])
        mpu = MultiPathUnderstanding()
        result = mpu.understand(message, [], max_paths=3)
        print(mpu.format_result(result))
    else:
        demo()
