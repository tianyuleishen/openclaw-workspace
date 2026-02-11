#!/usr/bin/env python3
"""
飞书语音消息发送器 v2
修复版 - 使用正确的 API 参数
"""

import os
import sys
import json
import time
import base64
import requests
from pathlib import Path

class FeishuVoiceSenderV2:
    """飞书语音消息发送器 v2"""
    
    def __init__(self):
        self.app_id = os.environ.get('FEISHU_APP_ID', '')
        self.app_secret = os.environ.get('FEISHU_APP_SECRET', '')
        self.tenant_access_token = None
        self.token_expire_time = 0
    
    def get_tenant_access_token(self):
        """获取 tenant_access_token"""
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
                self.token_expire_time = time.time() + result.get("expire", 7200) - 300
                return self.tenant_access_token
            else:
                print(f"❌ 获取 token 失败: {result}")
                return None
        except Exception as e:
            print(f"❌ 请求异常: {e}")
            return None
    
    def upload_file(self, file_path):
        """上传文件（使用 multipart/form-data）"""
        token = self.get_tenant_access_token()
        if not token:
            return None
        
        # 确定文件类型
        file_ext = Path(file_path).suffix.lower()
        file_type = "voice"  # 语音文件使用 voice 类型
        
        print(f"📤 上传文件: {file_path}")
        print(f"   文件类型: {file_type}")
        
        # 使用 multipart/form-data 上传
        url = "https://open.feishu.cn/open-apis/im/v1/files"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        
        # 文件名需要包含扩展名
        file_name = Path(file_path).name
        
        files = {
            "file_type": (None, file_type),
            "file_name": (None, file_name),
            "file": (file_name, open(file_path, "rb"), "audio/ogg")
        }
        
        try:
            response = requests.post(url, headers=headers, files=files, timeout=30)
            result = response.json()
            
            print(f"   上传响应: {result}")
            
            if result.get("code") == 0:
                file_token = result.get("data", {}).get("file_token")
                print(f"   ✅ 文件 token: {file_token}")
                return file_token
            else:
                print(f"❌ 上传失败: {result.get('msg', '未知错误')}")
                return None
        except Exception as e:
            print(f"❌ 上传异常: {e}")
            import traceback
            traceback.print_exc()
            return None
        finally:
            files["file"][1].close()
    
    def send_voice_message(self, receive_id, file_token):
        """发送语音消息"""
        token = self.get_tenant_access_token()
        if not token:
            return False
        
        print(f"\n📨 发送语音消息...")
        print(f"   接收者: {receive_id}")
        print(f"   文件 token: {file_token}")
        
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
            
            print(f"   发送响应: {result}")
            
            if result.get("code") == 0:
                print("✅ 语音消息发送成功！")
                return True
            else:
                print(f"❌ 发送失败: {result.get('msg', '未知错误')}")
                return False
        except Exception as e:
            print(f"❌ 发送异常: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def send(self, audio_path, receive_id):
        """发送语音消息（主函数）"""
        if not os.path.exists(audio_path):
            print(f"❌ 文件不存在: {audio_path}")
            return False
        
        if not self.app_id or not self.app_secret:
            print("❌ 未配置飞书 API Key")
            return False
        
        print("="*60)
        print("🎤 飞书语音消息发送")
        print("="*60)
        
        # 1. 上传文件
        file_token = self.upload_file(audio_path)
        if not file_token:
            return False
        
        # 2. 发送语音消息
        return self.send_voice_message(receive_id, file_token)


def main():
    if len(sys.argv) < 3:
        print("用法: python3 feishu_voice_send_v2.py <音频文件> <open_id>")
        print("示例: python3 feishu_voice_send_v2.py voice.ogg ou_abc123")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    receive_id = sys.argv[2]
    
    sender = FeishuVoiceSenderV2()
    
    if sender.send(audio_path, receive_id):
        print("\n🎉 完成！")
    else:
        print("\n❌ 失败！")


if __name__ == "__main__":
    main()
