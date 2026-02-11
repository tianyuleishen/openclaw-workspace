#!/usr/bin/env python3
"""
讯飞语音识别配置工具

使用方法:
python3 xunfei_asr_setup.py
"""

import os
import json
from datetime import datetime

def create_config_guide():
    """创建配置指南"""
    
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    guide = f'''# 讯飞语音识别配置指南

**日期**: {current_date}

---

## 🎤 讯飞语音识别

### 免费额度
- **每日**: 500 次调用
- **有效期**: 永久
- **适合**: 个人使用

---

## 📝 申请流程

### 1. 注册账号
1. 访问: https://www.xfyun.cn
2. 点击"免费注册"
3. 完成手机号验证

### 2. 开通服务
1. 登录讯飞开放平台
2. 进入"控制台"
3. 点击"创建新应用"
4. 填写应用信息:
   - 应用名称: 小爪语音助手
   - 应用类型: 工具类
   - 功能描述: 语音识别

### 3. 获取 API Key
创建完成后，在应用详情页获取:
- **APPID**: 
- **APIKey**: 
- **APISecret**: 

---

## 🔧 安装 SDK

```bash
# 方法1: 使用 pip (推荐)
pip install --user xfyun

# 方法2: 如果遇到问题
pip install --user RequestsToolbox
```

---

## 💻 使用示例

### 基础用法

```python
#!/usr/bin/env python3
import os
from xfyun import Speech

# 配置
APPID = "your_appid"
APIKey = "your_apikey"
APISecret = "your_apisecret"

# 初始化
speech = Speech(APPID, APIKey, APISecret)

# 音频文件路径
audio_path = "/home/admin/.openclaw/media/inbound/audio.ogg"

# 读取音频
with open(audio_path, "rb") as f:
    audio_data = f.read()

# 识别
result = speech.recognize(
    audio_data,
    format="ogg",  # ogg, wav, mp3
    rate=16000,     # 采样率
    channel=1,     # 单声道
    bie=1,         # 开启表情识别
    lang="zh_cn"   # 中文
)

# 解析结果
if result and "data" in result:
    text = result["data"]
    print(f"识别结果: {{text}}")
else:
    print(f"识别失败: {{result}}")
```

---

## 🔄 音频格式转换

如果音频格式不支持，可以使用 ffmpeg 转换:

```bash
# OGG 转 WAV
ffmpeg -i input.ogg -ar 16000 -ac 1 -acodec pcm_s16le output.wav

# MP3 转 WAV
ffmpeg -i input.mp3 -ar 16000 -ac 1 -acodec pcm_s16le output.wav

# FLAC 转 WAV
ffmpeg -i input.flac -ar 16000 -ac 1 -acodec pcm_s16le output.wav
```

---

## 🛠️ 创建快捷脚本

创建一个统一的语音识别脚本:

```bash
#!/bin/bash
# 文件: ~/voice_recognize.sh

AUDIO_FILE="$1"

if [ -z "$AUDIO_FILE" ]; then
    echo "用法: $0 <音频文件>"
    exit 1
fi

# 检查文件
if [ ! -f "$AUDIO_FILE" ]; then
    echo "文件不存在: $AUDIO_FILE"
    exit 1
fi

# 转换音频格式
TEMP_WAV="/tmp/voice_$(date +%s).wav"
ffmpeg -i "$AUDIO_FILE" -ar 16000 -ac 1 -acodec pcm_s16le "$TEMP_WAV" -y 2>/dev/null

# 调用讯飞 API
# (需要填写 API Key)

# 清理
rm -f "$TEMP_WAV"

echo "识别完成"
```

---

## 📊 常见问题

### Q: 识别准确率低?
A: 
- 确保音频清晰
- 说话语速适中
- 环境噪音小

### Q: 返回空结果?
A:
- 检查 API Key 是否正确
- 检查音频格式是否支持
- 查看返回的错误码

### Q: 提示"认证失败"?
A:
- 检查 APPID, APIKey, APISecret 是否匹配
- 确认服务已开通

---

## 🔗 相关链接

- **官网**: https://www.xfyun.cn
- **控制台**: https://www.xfyun.cn/console
- **文档**: https://www.xfyun.cn/doc/interface/asr.html
- **价格**: https://www.xfyun.cn/service/price

---

**创建时间**: {current_date}
'''

    with open("/home/admin/.openclaw/workspace/memory/xunfei_asr_config.md", "w") as f:
        f.write(guide)
    
    print("✅ 配置指南已保存: workspace/memory/xunfei_asr_config.md")

def create_asr_script():
    """创建 ASR 主脚本"""
    
    script = '''#!/usr/bin/env python3
"""
讯飞语音识别脚本

支持:
- 音频文件识别
- 批量识别
- 结果保存

使用方法:
python3 xunfei_asr.py <音频文件> [--api KEY] [--format json|text]
"""

import os
import sys
import json
import base64
import hashlib
import hmac
import time
import requests
from urllib.parse import urlencode
from datetime import datetime

class XunfeiASR:
    """讯飞语音识别"""
    
    def __init__(self, appid, api_key, api_secret):
        self.appid = appid
        self.api_key = api_key
        self.api_secret = api_secret
        self.host = "iat.xfyun.cn"
        self.api = "/v2/iat"
    
    def get_header(self):
        """生成请求头"""
        cur_time = str(int(time.time()))
        param = "{\"aue\":\"raw\",\"auf\":\"audio/L16;rate=16000\",\"channel\":1,\"rate\":16000,\"token\":\"\",\
\"ver\":\"0.0.0.1\",\"flac\":\"false\"}"
        
        param_base64 = base64.b64encode(param.encode('utf-8')).decode('utf-8')
        
        m2 = hashlib.md5()
        m2.update((self.api_key + cur_time + param_base64).encode('utf-8'))
        check_sum = m2.hexdigest()
        
        header = {
            'X-CurTime': cur_time,
            'X-Param': param_base64,
            'X-Appid': self.appid,
            'X-CheckSum': check_sum,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        return header
    
    def get_body(self, audio_path):
        """生成请求体"""
        with open(audio_path, 'rb') as f:
            audio_data = f.read()
        
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        body = {
            'audio': audio_base64
        }
        return body
    
    def recognize(self, audio_path):
        """识别音频"""
        url = f"https://{self.host}{self.api}"
        header = self.get_header()
        body = self.get_body(audio_path)
        
        try:
            response = requests.post(url, headers=header, data=body, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    # 成功
                    data = result.get("data", "")
                    if data:
                        return base64.b64decode(data).decode('utf-8')
                else:
                    print(f"识别失败: {result.get('desc', '未知错误')}")
                    return None
            else:
                print(f"请求失败: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"异常: {e}")
            return None
    
    def recognize_text(self, audio_path):
        """识别并返回纯文本"""
        result = self.recognize(audio_path)
        if result:
            try:
                data = json.loads(result)
                if "si" in data:
                    return data["si"]
            except:
                pass
        return None


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python3 xunfei_asr.py <音频文件>")
        print("示例: python3 xunfei_asr.py audio.ogg")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    
    if not os.path.exists(audio_path):
        print(f"文件不存在: {audio_path}")
        sys.exit(1)
    
    # 检查是否配置
    appid = os.environ.get('XUNFEI_APPID', '')
    api_key = os.environ.get('XUNFEI_API_KEY', '')
    api_secret = os.environ.get('XUNFEI_API_SECRET', '')
    
    if not appid or not api_key or not api_secret:
        print("❌ 未配置 API Key")
        print("请设置环境变量:")
        print('  export XUNFEI_APPID="your_appid"')
        print('  export XUNFEI_API_KEY="your_apikey"')
        print('  export XUNFEI_API_SECRET="your_apisecret"')
        sys.exit(1)
    
    print(f"🎤 正在识别: {audio_path}")
    
    asr = XunfeiASR(appid, api_key, api_secret)
    result = asr.recognize_text(audio_path)
    
    if result:
        print(f"✅ 识别结果: {result}")
        return result
    else:
        print("❌ 识别失败")
        return None


if __name__ == "__main__":
    main()
'''
    
    with open("/home/admin/.openclaw/workspace/xunfei_asr.py", "w") as f:
        f.write(script)
    
    os.chmod("/home/admin/.openclaw/workspace/xunfei_asr.py", 0o755)
    print("✅ ASR 脚本已创建: workspace/xunfei_asr.py")

def create_env_template():
    """创建环境变量模板"""
    
    template = '''# 讯飞语音识别 API Key

# 请填入您在讯飞开放平台申请的 API Key

XUNFEI_APPID="your_appid_here"
XUNFEI_API_KEY="your_api_key_here"
XUNFEI_API_SECRET="your_api_secret_here"

# 保存为: ~/.xunfei_asr_env

# 使用方法:
# source ~/.xunfei_asr_env
'''
    
    with open("/home/admin/.openclaw/workspace/.xunfei_asr_env.example", "w") as f:
        f.write(template)
    
    print("✅ 环境变量模板已创建: workspace/.xunfei_asr_env.example")

def show_summary():
    """显示总结"""
    
    print("\n" + "=" * 60)
    print("🎤 讯飞语音识别配置")
    print("=" * 60)
    
    print("\n✅ 已创建:")
    print("   1. workspace/memory/xunfei_asr_config.md - 配置指南")
    print("   2. workspace/xunfei_asr.py - ASR 脚本")
    print("   3. workspace/.xunfei_asr_env.example - 环境变量模板")
    
    print("\n📝 下一步:")
    print("   1. 访问 https://www.xfyun.cn")
    print("   2. 注册账号并创建应用")
    print("   3. 获取 API Key")
    print("   4. 配置环境变量")
    print("   5. 运行测试")
    
    print("\n💡 使用方法:")
    print("   # 1. 配置 API Key")
    print('   export XUNFEI_APPID="your_appid"')
    print('   export XUNFEI_API_KEY="your_apikey"')
    print('   export XUNFEI_API_SECRET="your_apisecret"')
    print("")
    print("   # 2. 运行识别")
    print("   python3 workspace/xunfei_asr.py <音频文件>")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    create_config_guide()
    create_asr_script()
    create_env_template()
    show_summary()
