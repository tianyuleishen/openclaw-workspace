
# 阿里云语音识别配置

## 申请地址
https://www.aliyun.com/product/nls

## 免费额度
- 每月 1000 次调用
- 新用户更多优惠

## 安装 SDK
```bash
pip install aliyun-python-sdk-core-nls
```

## 使用示例
```python
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

# 配置
access_key_id = "YOUR_ACCESS_KEY_ID"
access_key_secret = "YOUR_ACCESS_KEY_SECRET"
region_id = "cn-shanghai"

client = AcsClient(access_key_id, access_key_secret, region_id)

# 创建请求
request = CommonRequest()
request.set_method('POST')
request.set_domain('filetrans.cn-shanghai.aliyuncs.com')
request.set_version('2018-08-17')
request.set_action_name('SubmitTask')

# 提交音频转写任务
task_config = {
    "file_link": "https://your-audio-url/audio.wav",
    "enable_words": True,
    "enable_sample_rate_adaptive": True
}

request.add_body_params('Task', json.dumps(task_config))
response = client.do_action_with_exception(request)
print(response)
```
