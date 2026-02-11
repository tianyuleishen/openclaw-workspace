#!/usr/bin/env python3
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
        param = "{"aue":"raw","auf":"audio/L16;rate=16000","channel":1,"rate":16000,"token":"","ver":"0.0.0.1","flac":"false"}"
        
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
