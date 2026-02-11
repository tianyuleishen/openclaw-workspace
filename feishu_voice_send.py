#!/usr/bin/env python3
"""
飞书语音消息发送工具

支持发送语音消息（audio）而非文件（file）

使用方法:
python3 feishu_voice_send.py <音频文件> <接收者ID>
"""

import os
import sys
import json
import time
import base64
import hmac
import hashlib
import requests
from pathlib import Path

class FeishuVoiceSender:
    """飞书语音消息发送器"""
    
    def __init__(self):
        # 从环境变量读取配置
        self.app_id = os.environ.get('FEISHU_APP_ID', '')
        self.app_secret = os.environ.get('FEISHU_APP_SECRET', '')
        self.tenant_access_token = None
        self.token_expire_time = 0
    
    def get_tenant_access_token(self):
        """获取 tenant_access_token"""
        # 检查 token 是否过期
        if self.tenant_access_token and time.time() < self.token_expire_time:
            return self.tenant_access_token
        
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json; charset=utf-8"}
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            result = response.json()
            
            if result.get("code") == 0:
                self.tenant_access_token = result.get("tenant_access_token")
                # 提前5分钟刷新 token
                self.token_expire_time = time.time() + result.get("expire", 7200) - 300
                return self.tenant_access_token
            else:
                print(f"❌ 获取 token 失败: {result}")
                return None
        except Exception as e:
            print(f"❌ 请求异常: {e}")
            return None
    
    def upload_audio(self, audio_path):
        """上传音频文件"""
        token = self.get_tenant_access_token()
        if not token:
            return None
        
        # 确定文件类型
        file_ext = Path(audio_path).suffix.lower()
        file_type_map = {
            '.ogg': 'voice',
            '.mp3': 'audio/mp3', 
            '.wav': 'audio/wav',
            '.m4a': 'audio/mp4',
        }
        
        file_type = file_type_map.get(file_ext, 'voice')
        
        # 上传文件
        url = "https://open.feishu.cn/open-apis/im/v1/files"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        
        form = {
            "file_type": file_type,
            "file_name": Path(audio_path).name,
            "file": open(audio_path, "rb"),
        }
        
        try:
            response = requests.post(url, headers=headers, files=form, timeout=30)
            result = response.json()
            
            if result.get("code") == 0:
                file_token = result.get("data", {}).get("file_token")
                print(f"✅ 文件上传成功: {file_token}")
                return file_token
            else:
                print(f"❌ 上传失败: {result}")
                return None
        except Exception as e:
            print(f"❌ 上传异常: {e}")
            return None
        finally:
            form["file"].close()
    
    def send_voice_message(self, receive_id, file_token):
        """发送语音消息"""
        token = self.get_tenant_access_token()
        if not token:
            return False
        
        url = "https://open.feishu.cn/open-apis/im/v1/messages"
        params = {
            "receive_id_type": "open_id"
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        
        payload = {
            "receive_id": receive_id,
            "msg_type": "audio",
            "content": json.dumps({"file_token": file_token})
        }
        
        try:
            response = requests.post(url, params=params, headers=headers, 
                                   json=payload, timeout=10)
            result = response.json()
            
            if result.get("code") == 0:
                print("✅ 语音消息发送成功！")
                return True
            else:
                print(f"❌ 发送失败: {result}")
                return False
        except Exception as e:
            print(f"❌ 发送异常: {e}")
            return False
    
    def send(self, audio_path, receive_id):
        """发送语音消息（主函数）"""
        if not os.path.exists(audio_path):
            print(f"❌ 文件不存在: {audio_path}")
            return False
        
        if not self.app_id or not self.app_secret:
            print("❌ 未配置飞书 API Key")
            print("请设置环境变量:")
            print('  export FEISHU_APP_ID="your_app_id"')
            print('  export FEISHU_APP_SECRET="your_app_secret"')
            return False
        
        print(f"📤 发送语音: {audio_path}")
        print(f"📨 接收者: {receive_id}")
        
        # 1. 上传文件
        file_token = self.upload_audio(audio_path)
        if not file_token:
            return False
        
        # 2. 发送语音消息
        return self.send_voice_message(receive_id, file_token)


def main():
    """主函数"""
    if len(sys.argv) < 3:
        print("=" * 60)
        print("🎤 飞书语音消息发送")
        print("=" * 60)
        print("\n使用方法:")
        print("  python3 feishu_voice_send.py <音频文件> <接收者open_id>")
        print("\n示例:")
        print("  python3 feishu_voice_send.py voice.ogg ou_abc123")
        print("\n前提:")
        print("  需要配置飞书应用凭证")
        print('  export FEISHU_APP_ID="your_app_id"')
        print('  export FEISHU_APP_SECRET="your_app_secret"')
        print("\n注意:")
        print("  - 音频会被作为语音消息发送（不是文件）")
        print("  - 接收者需要是飞书用户")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    receive_id = sys.argv[2]
    
    sender = FeishuVoiceSender()
    
    if sender.send(audio_path, receive_id):
        print("\n✅ 发送完成！")
    else:
        print("\n❌ 发送失败！")


if __name__ == "__main__":
    main()
