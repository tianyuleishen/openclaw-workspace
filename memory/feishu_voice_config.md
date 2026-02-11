# 飞书语音消息发送配置指南

**日期**: 2026-02-10

---

## 🎤 飞书语音消息 vs 文件消息

### 区别

| 类型 | msg_type | 显示方式 | 用户体验 |
|------|---------|---------|---------|
| **语音消息** | `audio` | 🎵 语音播放按钮 | 一键播放，类似微信语音 |
| **文件消息** | `file` | 📎 文件下载 | 需要下载后播放 |

### 推荐

**使用语音消息 (audio)**:
- ✅ 更友好的用户体验
- ✅ 飞书内直接播放
- ✅ 节省用户操作

---

## 📝 配置步骤

### 步骤1: 创建飞书应用

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 登录账号
3. 点击"创建企业自建应用"
4. 填写应用信息:
   - 应用名称: 小爪语音助手
   - 应用描述: AI语音助手
   - 应用图标: (可选)

### 步骤2: 获取凭证

在应用详情页获取:
- **APP ID**: 应用 ID
- **App Secret**: 应用密钥

### 步骤3: 配置权限

在"权限管理"中添加:
```
im:message:send_as_bot  - 发送消息权限
```

### 步骤4: 配置环境变量

```bash
export FEISHU_APP_ID="your_app_id"
export FEISHU_APP_SECRET="your_app_secret"

# 保存到文件
echo 'export FEISHU_APP_ID="your_app_id"' >> ~/.bashrc
echo 'export FEISHU_APP_SECRET="your_app_secret"' >> ~/.bashrc

# 立即生效
source ~/.bashrc
```

### 步骤5: 获取用户 ID

发送消息需要接收者的 `open_id`:
- 用户详情页可查看
- 通过 API 获取用户列表

---

## 🔧 使用方法

### 基本用法

```bash
# 设置环境变量
export FEISHU_APP_ID="your_app_id"
export FEISHU_APP_SECRET="your_app_secret"

# 发送语音消息
python3 /home/admin/.openclaw/workspace/feishu_voice_send.py <音频文件> <open_id>

# 示例
python3 /home/admin/.openclaw/workspace/feishu_voice_send.py voice.ogg ou_abc123
```

### 支持的音频格式

| 格式 | 支持 | 推荐 |
|------|------|------|
| OGG | ✅ | 🎯 推荐 |
| MP3 | ✅ | ✅ |
| WAV | ✅ | ✅ |
| M4A | ✅ | ✅ |

### 高级用法

```python
from feishu_voice_send import FeishuVoiceSender

# 初始化
sender = FeishuVoiceSender()

# 发送语音
sender.send("voice.ogg", "ou_user123")
```

---

## 💻 集成到 OpenClaw

### 方法1: 使用 message 工具（推荐）

OpenClaw 的 message 工具已经支持发送语音:

```python
# 在 OpenClaw 中使用
message.send(
    media="/path/to/voice.mp3",
    message="语音消息内容",
    target="user:open_id"
)
```

### 方法2: 使用 TTS 集成

```python
# 1. 文字转语音
tts = TTS()
audio_path = tts.synthesize("Hello!", output_path="/tmp/voice.ogg")

# 2. 发送语音消息
sender = FeishuVoiceSender()
sender.send(audio_path, "ou_user123")
```

---

## 📊 API 参考

### 上传文件 API

```
POST https://open.feishu.cn/open-apis/im/v1/files

参数:
- file_type: voice (语音)
- file_name: 文件名
- file: 文件内容

返回:
{
  "code": 0,
  "data": {
    "file_token": "xxx"
  }
}
```

### 发送消息 API

```
POST https://open.feishu.cn/open-apis/im/v1/messages

参数:
- receive_id_type: open_id
- receive_id: 用户 open_id
- msg_type: audio
- content: {"file_token": "xxx"}

返回:
{
  "code": 0,
  "data": {
    "message_id": "xxx"
  }
}
```

---

## 🛠️ 故障排除

### 问题1: 权限不足

**错误**: `Permission denied`
**解决**: 
1. 在飞书开放平台添加 `im:message:send_as_bot` 权限
2. 重新发布应用

### 问题2: Token 无效

**错误**: `invalid tenant_access_token`
**解决**:
1. 检查 APP_ID 和 APP_SECRET 是否正确
2. 确认应用已激活

### 问题3: 用户不存在

**错误**: `receive_id not found`
**解决**:
1. 检查 open_id 是否正确
2. 确认用户已在应用中

---

## 🔗 相关链接

- **飞书开放平台**: https://open.feishu.cn/
- **创建应用**: https://open.feishu.cn/application
- **消息 API 文档**: https://open.feishu.cn/document/server-docs/im-v1/message/create
- **文件上传文档**: https://open.feishu.cn/document/server-docs/im-v1/file/create

---

## 📁 相关文件

| 文件 | 说明 |
|------|------|
| `workspace/feishu_voice_send.py` | 语音消息发送脚本 |
| `workspace/.feishu_env.example` | 环境变量模板 |
| `workspace/memory/feishu_voice_config.md` | 本配置指南 |

---

**创建时间**: 2026-02-10 21:22
