#!/usr/bin/env python3
"""
Cognitive Reasoning Auto-Integrator - Full Auto Mode
全主动模式：每次对话自动调用认知框架分析
"""

import sys
import json
from datetime import datetime
from pathlib import Path

# 导入认知框架
sys.path.insert(0, str(Path(__file__).parent))
from think_loop_v3 import ThinkLoopV3


class AutoCognitiveIntegrator:
    """自动认知集成器"""
    
    def __init__(self):
        self.thinker = ThinkLoopV3()
        self.enabled = True
        self.threshold = 0.80
        self.history_file = Path.home() / ".openclaw/workspace/.conversation_history.json"
        self._load_history()
    
    def _load_history(self):
        """加载对话历史"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
            except:
                self.history = []
        else:
            self.history = []
    
    def _save_history(self, message):
        """保存对话历史"""
        self.history.append({
            "content": message,
            "timestamp": datetime.now().isoformat()
        })
        # 只保留最近10条
        self.history = self.history[-10:]
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def process(self, message):
        """
        处理用户消息 - 全主动模式
        返回: (action, confidence, response)
        """
        if not self.enabled:
            return ("EXECUTE", 1.0, message)
        
        # 分析消息
        result = self.thinker.think(message, self.history)
        
        # 保存历史
        self._save_history(message)
        
        # 决策
        if result['confidence'] >= self.threshold:
            return ("EXECUTE", result['confidence'], 
                   f"✅ 置信度 {result['confidence']*100:.0f}% - 开始执行")
        else:
            clarification = self._generate_clarification(result)
            return ("CLARIFY", result['confidence'], clarification)
    
    def _generate_clarification(self, result):
        """生成澄清问题"""
        lines = [f"**⚠️ 置信度 {result['confidence']*100:.0f}% < 80%**\n"]
        lines.append(f"意图: {result['intent']['type']}\n")
        
        if result['ambiguities']:
            lines.append("请选择或说明:\n")
            for i, amb in enumerate(result['ambiguities'], 1):
                lines.append(f"{i}. {amb['question']}")
                lines.append(f"   选项: {' | '.join(amb['options'])}\n")
        
        return "\n".join(lines)
    
    def run_interactive(self):
        """交互模式"""
        print("\n🧠 认知推理框架 - 全主动模式")
        print("=" * 50)
        print("每次输入都会自动分析")
        print("输入 'quit' 退出\n")
        
        while True:
            try:
                msg = input("👤 你: ").strip()
                if not msg:
                    continue
                if msg.lower() == 'quit':
                    print("👋 再见!")
                    break
                
                action, confidence, response = self.process(msg)
                
                print(f"\n🧠 分析:")
                print(f"   置信度: {confidence*100:.0f}%")
                print(f"   行动: {action}")
                
                if action == "CLARIFY":
                    print(f"\n{response}")
                else:
                    print(f"\n{response}")
                
                print()
                
            except KeyboardInterrupt:
                print("\n👋 再见!")
                break
            except Exception as e:
                print(f"\n❌ 错误: {e}")


def main():
    """主入口"""
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        # 交互模式
        integrator = AutoCognitiveIntegrator()
        integrator.run_interactive()
    else:
        # 单次调用模式
        if len(sys.argv) < 2:
            print("用法: python3 auto_integrator.py \"用户消息\" [--interactive]")
            sys.exit(1)
        
        message = " ".join(sys.argv[1:])
        if "--interactive" in sys.argv:
            sys.argv.remove("--interactive")
            message = " ".join(sys.argv[1:])
        
        integrator = AutoCognitiveIntegrator()
        action, confidence, response = integrator.process(message)
        
        print(f"\n🧠 分析结果:")
        print(f"   置信度: {confidence*100:.0f}%")
        print(f"   行动: {action}")
        print(f"\n{response}")


if __name__ == "__main__":
    main()
