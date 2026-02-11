#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦞 自动推理集成 - 会话默认启用
==================================
集成到OpenClaw会话流程中

功能:
1. 自动检测用户意图
2. 自动调用推理引擎
3. 自动生成推理报告
4. 无需手动调用

使用方法:
# 在会话开始时初始化
from auto_reasoning_integration import AutoReasoning
reasoning = AutoReasoning()

# 用户每条消息自动处理
result = reasoning.process(user_message)
print(result["answer"])
print(result["reasoning_report"])

Version: 1.0
Date: 2026-02-11
"""

from unified_reasoning_engine import UnifiedReasoningEngine, ReasoningResult


class AutoReasoning:
    """
    自动推理集成器
    
    特点:
    - 自动检测是否需要推理
    - 自动选择推理模式
    - 自动生成推理报告
    - 无需手动调用
    """
    
    def __init__(self, auto_enable: bool = True):
        """
        Args:
            auto_enable: 是否自动启用推理
        """
        self.auto_enable = auto_enable
        self.engine = UnifiedReasoningEngine()
        self.session_history = []
        self.enabled = True
        
    def process(self, user_message: str) -> dict:
        """
        处理用户消息
        
        Args:
            user_message: 用户的消息
            
        Returns:
            包含答案和推理报告的字典
        """
        # 检查是否启用
        if not self.enabled:
            return {
                "answer": user_message,
                "reasoning_report": "推理引擎未启用",
                "auto_enabled": False
            }
        
        # 检测是否需要推理
        needs_reasoning = self._needs_reasoning(user_message)
        
        if needs_reasoning:
            # 调用推理引擎
            result = self.engine.solve(user_message)
            
            # 生成推理报告
            report = self._generate_report(user_message, result)
            
            # 记录历史
            self.session_history.append({
                "message": user_message,
                "result": result
            })
            
            return {
                "answer": result.answer,
                "reasoning_report": report,
                "auto_enabled": True,
                "confidence": result.confidence,
                "mode_used": result.mode_used,
                "key_insight": result.key_insight,
                "steps": result.steps
            }
        else:
            # 一般对话，直接返回
            return {
                "answer": self._general_response(user_message),
                "reasoning_report": "一般对话，无需推理",
                "auto_enabled": True,
                "confidence": 0.5,
                "mode_used": "chat"
            }
    
    def _needs_reasoning(self, message: str) -> bool:
        """检测是否需要推理"""
        reasoning_keywords = [
            # 逻辑推理
            "真话", "假话", "如果", "真假", "谁会", "谁是",
            # 数学计算
            "计算", "等于", "解", "直角三角形",
            # 几何问题
            "厘米", "体积", "面积", "水位", "放入",
            # 智商测试
            "为什么", "测试", "推理",
            # 伦理分析
            "应该", "能否", "道德",
            # 实际问题
            "开车", "走路", "洗车", "去还是"
        ]
        
        message_lower = message.lower()
        for keyword in reasoning_keywords:
            if keyword in message or keyword in message_lower:
                return True
        
        # 检测是否包含数字（可能是数学题）
        import re
        numbers = re.findall(r'\d+', message)
        if len(numbers) >= 2 and any(kw in message for kw in ["多少", "是几", "等于", "计算"]):
            return True
        
        return False
    
    def _generate_report(self, message: str, result: ReasoningResult) -> str:
        """生成推理报告"""
        report = f"""
╔═══════════════════════════════════════════════════════════════╗
║ 🦞 推理引擎分析报告                                      ║
╠═══════════════════════════════════════════════════════════════╣
║
║ 问题: {message[:50]}...
║
║ 📊 分析结果:
║    答案: {result.answer}
║    置信度: {result.confidence:.0%}
║    推理模式: {result.mode_used}
║
║ 💡 关键洞察:
║    {result.key_insight}
║
║ 🔄 推理步骤:
"""
        
        for i, step in enumerate(result.steps, 1):
            report += f"║    {i}. {step}\n"
        
        report += """║
╚═══════════════════════════════════════════════════════════════╝"""
        
        return report
    
    def _general_response(self, message: str) -> str:
        """一般对话回复"""
        # 简单的问候和闲聊
        greetings = ["你好", "在吗", "早上好", "晚安"]
        for greet in greetings:
            if greet in message:
                return f"你好！有什么我可以帮助你的吗？🦞"
        
        # 感谢
        if "谢谢" in message:
            "不客气！🦞"
        
        # 默认回复
        return "我理解了，请继续。"
    
    def enable(self):
        """启用推理"""
        self.enabled = True
        return "✅ 推理引擎已启用"
    
    def disable(self):
        """禁用推理"""
        self.enabled = False
        return "✅ 推理引擎已禁用"
    
    def status(self) -> dict:
        """获取状态"""
        return {
            "enabled": self.enabled,
            "total_messages": len(self.session_history),
            "engine_status": "运行中"
        }
    
    def get_session_summary(self) -> str:
        """获取会话总结"""
        if not self.session_history:
            return "暂无推理记录"
        
        lines = ["\n📊 本次会话推理记录:\n"]
        for i, record in enumerate(self.session_history, 1):
            lines.append(f"{i}. {record['result'].answer} ({record['result'].confidence:.0%})")
        
        return "\n".join(lines)


# 便捷函数
_reasoning_instance = None

def get_reasoning():
    """获取推理实例（单例模式）"""
    global _reasoning_instance
    if _reasoning_instance is None:
        _reasoning_instance = AutoReasoning()
    return _reasoning_instance

def process(message: str) -> dict:
    """一键处理用户消息"""
    return get_reasoning().process(message)


def demo():
    """演示"""
    print("="*70)
    print("🦞 自动推理集成 - 会话默认启用演示")
    print("="*70)
    
    # 创建实例
    reasoning = AutoReasoning()
    
    # 测试各种问题
    tests = [
        "甲乙丙三人谁会游泳？",
        "直角三角形面积等于周长有哪些？",
        "棱长30厘米的水位问题放入2500平方厘米盛水20厘米的容器",
        "洗车应该开车还是走路？",
        "你好！"  # 一般对话
    ]
    
    for test in tests:
        print(f"\n{'='*70}")
        print(f"用户: {test}")
        print("-"*70)
        result = reasoning.process(test)
        print(result["reasoning_report"])
    
    print("\n" + "="*70)
    print("状态:", reasoning.status())
    print("="*70)


if __name__ == "__main__":
    demo()
