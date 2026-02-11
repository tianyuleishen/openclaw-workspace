
# 讯飞语音识别配置

## 申请地址
https://www.xfyun.cn/services/lfasr

## 免费额度
- 每日 500 次调用
- 永久有效

## SDK 安装
```bash
pip install xfyun
```

## 使用示例
```python
import json
from xfyun import Speech

# 配置
appid = "YOUR_APPID"
api_key = "YOUR_API_KEY"
api_secret = "YOUR_API_SECRET"

# 初始化
speech = Speech(appid, api_key, api_secret)

# 识别音频
with open("audio.wav", "rb") as f:
    result = speech.recognize(f, format="wav", rate=16000)

print(result)
```
