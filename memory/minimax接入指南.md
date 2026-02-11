# MiniMax 模型接入指南

**日期**: 2026-02-10  
**主题**: Claude Code 接入 MiniMax 模型

---

## 📊 现状分析

### MiniMax MCP vs API

| 方式 | 用途 | 当前状态 |
|------|------|---------|
| **MCP (Model Context Protocol)** | 搜索 MiniMax 文档 | ✅ 可用，但仅文档搜索 |
| **API** | 调用 MiniMax 模型 | ✅ 完全支持 |

---

## 🛠️ 方案1: 使用 MiniMax API (推荐)

### 步骤

#### 1. 获取 API Key

访问: https://platform.minimaxi.com

1. 注册/登录账号
2. 进入"API Keys"页面
3. 创建新的 API Key
4. 复制保存 (格式: mapi_xxxxx)

#### 2. 安装依赖

```bash
pip install requests
```

#### 3. Python 示例

```python
#!/usr/bin/env python3
"""
MiniMax API 调用示例
"""

import requests

# 配置
API_KEY = "your-api-key-here"
MODEL = "MiniMax-M2.1"  # 或 MiniMax-M2.1-flash
BASE_URL = "https://api.minimaxi.com/v1"

# 请求头
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 请求体
data = {
    "model": MODEL,
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user", 
            "content": "你好，请介绍一下自己。"
        }
    ],
    "temperature": 0.7,
    "max_tokens": 1000
}

# 发送请求
response = requests.post(
    f"{BASE_URL}/chat/completions",
    headers=headers,
    json=data,
    timeout=30
)

# 解析响应
result = response.json()

if response.status_code == 200:
    content = result["choices"][0]["message"]["content"]
    print("回复:", content)
else:
    print("错误:", result)
```

#### 4. 高级配置

```python
# 流式输出
data["stream"] = True

# 响应格式
response = requests.post(
    f"{BASE_URL}/chat/completions",
    headers=headers,
    json=data,
    stream=True,
    timeout=30
)

for line in response.iter_lines():
    if line:
        print(line)
```

---

## 🛠️ 方案2: 使用 Claude Code MCP

### 前提

Claude Code 是 Anthropic 的 AI 编程工具，与 OpenClaw 是独立的。

### 安装步骤

```bash
# 1. 安装 Claude Code
# 下载地址: https://claude.com/claude-code

# 2. 安装 MiniMax MCP Server
npm install -g @minimax/mcp-server

# 3. 配置 Claude Code
claude code add-server minimax-mcp
```

### 使用限制

```json
{
  "mcpServers": {
    "minimax": {
      "command": "npx",
      "args": ["-y", "@minimax/mcp-server"],
      "env": {
        "MINIMAX_API_KEY": "your-key"
      }
    }
  }
}
```

**注意**: 当前 MCP 仅支持搜索文档，不支持模型调用。

---

## 🔄 OpenClaw 集成情况

### 当前状态

| 项目 | 状态 | 说明 |
|------|------|------|
| **模型** | ✅ 已集成 | MiniMax-M2.1 |
| **API** | ✅ 可用 | minimax_integration.py |
| **测试** | ✅ 通过 | test_minimax_api.py |

### 配置文件

```python
# minimax_config.py
class MiniMaxConfig:
    API_KEY = "mapi_xxxxx"  # 从环境变量或 .env 加载
    MODEL = "MiniMax-M2.1"
    BASE_URL = "https://api.minimaxi.com/v1"
```

---

## 📝 完整示例代码

```python
#!/usr/bin/env python3
"""
MiniMax 完整集成示例
"""

import requests
import json
from datetime import datetime

class MiniMaxClient:
    def __init__(self, api_key: str, model: str = "MiniMax-M2.1"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.minimaxi.com/v1"
        self.history = []
    
    def chat(self, message: str, system_prompt: str = None) -> str:
        """发送消息并获取回复"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": message})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            reply = result["choices"][0]["message"]["content"]
            
            # 保存到历史
            self.history.append({
                "user": message,
                "assistant": reply,
                "timestamp": datetime.now().isoformat()
            })
            
            return reply
        else:
            raise Exception(f"API Error: {response.text}")
    
    def get_history(self) -> list:
        """获取对话历史"""
        return self.history


# 使用示例
if __name__ == "__main__":
    client = MiniMaxClient(api_key="your-api-key")
    
    # 对话
    while True:
        user_input = input("你: ")
        if user_input.lower() in ["quit", "exit"]:
            break
        
        reply = client.chat(user_input)
        print(f"小爪: {reply}")
```

---

## 💡 最佳实践

### 1. API Key 管理

```bash
# 环境变量 (推荐)
export MINIMAX_API_KEY="your-api-key"

# 或 .env 文件
echo "MINIMAX_API_KEY=your-api-key" > .env
```

### 2. 错误处理

```python
try:
    response = requests.post(url, headers=headers, json=data, timeout=30)
    response.raise_for_status()  # 检查 HTTP 错误
    return response.json()
except requests.exceptions.Timeout:
    print("请求超时，请重试")
except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")
```

### 3. 速率限制

```python
import time

# 简单的速率限制
last_request = 0
MIN_INTERVAL = 1.0  # 最小间隔1秒

def safe_request():
    global last_request
    elapsed = time.time() - last_request
    if elapsed < MIN_INTERVAL:
        time.sleep(MIN_INTERVAL - elapsed)
    last_request = time.time()
    # 发送请求...
```

---

## 📚 常用模型

| 模型 | 特点 | 适用场景 |
|------|------|---------|
| **MiniMax-M2.1** | 最新旗舰模型 | 复杂推理、长文本 |
| **MiniMax-M2.1-flash** | 快速响应 | 简单对话、实时应用 |
| **MiniMax-M2** | 稳定可靠 | 通用场景 |

---

## 🔧 故障排除

### 常见错误

1. **401 Unauthorized**
   - 检查 API Key 是否正确
   - 确认 Key 已激活

2. **429 Rate Limit**
   - 降低请求频率
   - 检查配额使用情况

3. **500 Internal Error**
   - 重试请求
   - 检查参数是否正确

### 调试技巧

```python
# 开启详细日志
import requests
import logging

logging.basicConfig(level=logging.DEBUG)
requests.logging.getLogger().setLevel(logging.DEBUG)
```

---

## 📖 参考资源

- API 文档: https://platform.minimaxi.com/docs
- MCP 文档: https://platform.minimaxi.com/docs/mcp
- OpenClaw 集成: /home/admin/.openclaw/workspace/minimax_integration.py

---

**创建时间**: 2026-02-10  
**版本**: v1.0
