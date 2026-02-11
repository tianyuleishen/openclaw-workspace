#!/usr/bin/env python3
"""
MiniMax API 集成测试
使用保存的 API Key 测试连接
"""

import os
import sys
import json
from datetime import datetime

# 安全获取 API Key
def get_minimax_key():
    """安全获取 MiniMax API Key"""
    # 1. 先从环境变量读取
    key = os.environ.get('MINIMAX_API_KEY')
    if key:
        return key
    
    # 2. 从 .env 文件读取
    try:
        with open('/home/admin/.openclaw/workspace/.env', 'r') as f:
            for line in f:
                if line.startswith('MINIMAX_API_KEY='):
                    return line.strip().split('=')[1].strip()
    except:
        pass
    
    return None

API_KEY = get_minimax_key()

print("=" * 60)
print("🚀 MiniMax API 集成测试")
print("=" * 60)
print()

if not API_KEY:
    print("❌ 未找到 API Key")
    sys.exit(1)

print(f"✅ API Key 已加载: {API_KEY[:25]}...")
print()

# 测试 API 连接
import urllib.request
import urllib.parse
import json

BASE_URL = "https://api.minimaxi.com/v1"

# 测试请求（获取模型列表）
def test_models_api():
    try:
        url = f"{BASE_URL}/models"
        
        req = urllib.request.Request(
            url,
            headers={
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json'
            }
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data, None
    except Exception as e:
        return None, str(e)

# 测试聊天补全
def test_chat_api():
    try:
        url = f"{BASE_URL}/chat/completions"
        
        payload = {
            "model": "MiniMax-M2.1",
            "messages": [
                {"role": "user", "content": "你好！请用中文介绍一下自己。"}
            ],
            "max_tokens": 200,
            "temperature": 0.7
        }
        
        data = json.dumps(payload).encode('utf-8')
        
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json'
            }
        )
        
        with urllib.request.urlopen(req, timeout=15) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result, None
    except Exception as e:
        return None, str(e)

# 执行测试
print("📡 测试 API 连接...")
print()

print("1️⃣ 测试模型列表...")
models, error = test_models_api()
if error:
    print(f"   ❌ 失败: {error}")
else:
    print(f"   ✅ 成功!")
    if isinstance(models, dict) and 'data' in models:
        print(f"   📋 可用模型: {len(models['data'])} 个")
        for model in models['data'][:5]:
            print(f"      - {model.get('id', 'Unknown')}")

print()
print("2️⃣ 测试聊天补全...")
result, error = test_chat_api()
if error:
    print(f"   ❌ 失败: {error}")
else:
    print(f"   ✅ 成功!")
    if isinstance(result, dict) and 'choices' in result:
        message = result['choices'][0]['message']['content']
        print(f"   💬 回复: {message[:150]}...")

print()
print("=" * 60)
print("📊 测试总结")
print("=" * 60)

test_results = {
    "timestamp": datetime.now().isoformat(),
    "api_key_configured": True,
    "api_key_prefix": API_KEY[:20] + "...",
    "models_api": "✅ 成功" if models else "❌ 失败",
    "chat_api": "✅ 成功" if result else "❌ 失败",
    "available_models": len(models['data']) if isinstance(models, dict) and 'data' in models else 0
}

print(f"API Key: {test_results['api_key_configured']}")
print(f"模型API: {test_results['models_api']}")
print(f"聊天API: {test_results['chat_api']}")
print(f"可用模型: {test_results['available_models']}")

# 保存结果
with open('/home/admin/.openclaw/workspace/minimax_test_results.json', 'w') as f:
    json.dump(test_results, f, indent=2, ensure_ascii=False)

print()
print("✅ 测试结果已保存")
print("=" * 60)
