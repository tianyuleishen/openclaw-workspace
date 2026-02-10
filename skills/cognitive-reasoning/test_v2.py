#!/usr/bin/env python3
"""
Cognitive Reasoning Framework v2 - Test Suite
增强版认知推理框架测试
"""

from think_loop_v2 import ThinkLoopV2

def test_case(message, expected_action):
    """测试用例"""
    print("\n" + "=" * 60)
    print(f"📝 测试: \"{message}\"")
    print("=" * 60)
    
    thinker = ThinkLoopV2()
    response = thinker.think_and_respond(message)
    
    print(f"\n🎯 结果:")
    print(f"   行动: {response['action']}")
    print(f"   置信度: {response['result']['confidence']*100:.0f}%")
    print(f"   预期: {expected_action}")
    print(f"   实际: {response['action']}")
    
    # 验证结果
    if response['action'] == expected_action:
        print(f"   ✅ 通过")
        return True
    else:
        print(f"   ❌ 失败")
        return False


def main():
    """运行测试套件"""
    print("\n" + "🧠" * 30)
    print("🧠🧠🧠 COGNITIVE REASONING v2 TEST SUITE 🧠🧠🧠")
    print("🧠" * 30)
    
    tests = [
        # 模糊请求 - 应该需要澄清
        ("测试一下", "CLARIFY"),
        ("试试", "CLARIFY"),
        ("check", "CLARIFY"),
        
        # 较明确请求 - 可以执行
        ("检查服务器8080端口", "EXECUTE"),
        ("查看今天的文件列表", "EXECUTE"),
        ("生成一个5秒的视频", "CLARIFY"),  # 仍有歧义
        
        # 中等模糊
        ("检查服务器", "CLARIFY"),
        ("生成视频", "CLARIFY"),
    ]
    
    passed = 0
    failed = 0
    
    for msg, expected in tests:
        if test_case(msg, expected):
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 60)
    print("📊 测试结果")
    print("=" * 60)
    print(f"  通过: {passed}")
    print(f"  失败: {failed}")
    print(f"  总计: {passed + failed}")
    
    # 特别演示：用户的原话
    print("\n" + "=" * 60)
    print("🎯 特别演示: 用户原话 \"测试一下\"")
    print("=" * 60)
    
    thinker = ThinkLoopV2()
    response = thinker.think_and_respond("测试一下")
    
    print(response['message'])


if __name__ == "__main__":
    main()
