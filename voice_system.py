#!/usr/bin/env python3
"""
完整语音识别系统

功能:
1. 自动转换音频格式
2. 调用讯飞 API 识别
3. 支持多种音频格式
4. 结果保存和展示

使用方法:
python3 voice_system.py <音频文件> [--api xunfei]
"""

import os
import sys
import json
import base64
import hashlib
import hmac
import time
import wave
import subprocess
from pathlib import Path

class VoiceRecognitionSystem:
    """语音识别系统"""
    
    def __init__(self):
        self.temp_files = []
        self.appid = os.environ.get('XUNFEI_APPID', '')
        self.api_key = os.environ.get('XUNFEI_API_KEY', '')
        self.api_secret = os.environ.get('XUNFEI_API_SECRET', '')
    
    def cleanup(self):
        """清理临时文件"""
        for f in self.temp_files:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except:
                pass
    
    def convert_audio(self, audio_path):
        """转换音频格式"""
        print(f"🔄 转换音频格式: {audio_path}")
        
        # 生成输出文件名
        output_path = f"/tmp/voice_converted_{int(time.time())}.wav"
        self.temp_files.append(output_path)
        
        # 使用 ffmpeg 转换
        cmd = [
            "ffmpeg", "-i", audio_path,
            "-ar", "16000",      # 16kHz 采样率
            "-ac", "1",          # 单声道
            "-acodec", "pcm_s16le",  # 16位 PCM
            output_path,
            "-y"                 # 覆盖已存在的文件
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ 转换成功: {output_path}")
                return output_path
            else:
                print(f"❌ 转换失败: {result.stderr}")
                return None
        except Exception as e:
            print(f"❌ 异常: {e}")
            return None
    
    def check_audio_format(self, audio_path):
        """检查音频格式"""
        try:
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-select_streams", "a:0",
                 "-show_entries", "stream=codec_name,sample_rate,channels",
                 "-of", "json", audio_path],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                info = json.loads(result.stdout)
                if "streams" in info and len(info["streams"]) > 0:
                    stream = info["streams"][0]
                    return {
                        "codec": stream.get("codec_name", "unknown"),
                        "sample_rate": int(stream.get("sample_rate", 16000)),
                        "channels": int(stream.get("channels", 1))
                    }
            return None
        except Exception as e:
            print(f"⚠️ 检查格式异常: {e}")
            return None
    
    def recognize_with_xunfei(self, audio_path):
        """使用讯飞识别"""
        if not self.appid or not self.api_key or not self.api_secret:
            print("❌ 未配置讯飞 API Key")
            print("请设置环境变量:")
            print('  export XUNFEI_APPID="your_appid"')
            print('  export XUNFEI_API_KEY="your_apikey"')
            print('  export XUNFEI_API_SECRET="your_apisecret"')
            return None
        
        print(f"🎤 使用讯飞识别: {audio_path}")
        
        # 读取音频文件
        with open(audio_path, 'rb') as f:
            audio_data = f.read()
        
        # 生成签名
        cur_time = str(int(time.time()))
        param = "{\"aue\":\"raw\",\"auf\":\"audio/L16;rate=16000\",\"channel\":1,\"rate\":16000}"
        param_base64 = base64.b64encode(param.encode('utf-8')).decode('utf-8')
        
        m2 = hashlib.md5()
        m2.update((self.api_key + cur_time + param_base64).encode('utf-8'))
        check_sum = m2.hexdigest()
        
        # 构建请求头
        header = {
            'X-CurTime': cur_time,
            'X-Param': param_base64,
            'X-Appid': self.appid,
            'X-CheckSum': check_sum,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        # 构建请求体
        body = {'audio': base64.b64encode(audio_data).decode('utf-8')}
        
        # 发送请求
        url = "https://iat.xfyun.cn/v2/iat"
        
        try:
            import requests
            response = requests.post(url, headers=header, data=body, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    # 解析结果
                    data = result.get("data", "")
                    if data:
                        text_data = base64.b64decode(data).decode('utf-8')
                        text_json = json.loads(text_data)
                        if "si" in text_json:
                            return text_json["si"]
                else:
                    print(f"❌ 识别失败: {result.get('desc', '未知错误')}")
            else:
                print(f"❌ 请求失败: {response.status_code}")
            
            return None
            
        except ImportError:
            print("❌ 未安装 requests 库")
            print("请运行: pip install requests")
            return None
        except Exception as e:
            print(f"❌ 异常: {e}")
            return None
    
    def recognize(self, audio_path, api="xunfei"):
        """识别音频"""
        if not os.path.exists(audio_path):
            print(f"❌ 文件不存在: {audio_path}")
            return None
        
        # 检查音频格式
        format_info = self.check_audio_format(audio_path)
        if format_info:
            print(f"📊 音频格式: {format_info}")
        
        # 如果格式不匹配，转换音频
        if format_info:
            needs_conversion = (
                format_info.get("sample_rate", 16000) != 16000 or
                format_info.get("channels", 1) != 1 or
                format_info.get("codec") not in ["pcm_s16le", "wav"]
            )
        else:
            needs_conversion = True
        
        if needs_conversion:
            converted_path = self.convert_audio(audio_path)
            if converted_path:
                audio_path = converted_path
        
        # 调用识别
        if api == "xunfei":
            return self.recognize_with_xunfei(audio_path)
        else:
            print(f"❌ 不支持的 API: {api}")
            return None
    
    def process_audio_folder(self, folder_path):
        """处理音频文件夹"""
        audio_files = []
        for ext in ['*.ogg', '*.mp3', '*.wav', '*.flac', '*.m4a', '*.aac']:
            audio_files.extend(Path(folder_path).glob(ext))
            audio_files.extend(Path(folder_path).glob(ext.upper()))
        
        print(f"📁 发现 {len(audio_files)} 个音频文件")
        
        results = []
        for audio_path in sorted(audio_files):
            print(f"\n处理: {audio_path.name}")
            text = self.recognize(str(audio_path))
            if text:
                results.append({
                    "file": audio_path.name,
                    "text": text
                })
        
        return results


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("=" * 60)
        print("🎤 语音识别系统")
        print("=" * 60)
        print("\n使用方法:")
        print("  python3 voice_system.py <音频文件>")
        print("  python3 voice_system.py <文件夹>")
        print("  python3 voice_system.py --api xunfei <音频文件>")
        print("\n示例:")
        print("  python3 voice_system.py audio.ogg")
        print("  python3 voice_system.py /home/admin/.openclaw/media/inbound/")
        print("\n前提:")
        print("  需要配置讯飞 API Key")
        print('  export XUNFEI_APPID="your_appid"')
        print('  export XUNFEI_API_KEY="your_apikey"')
        print('  export XUNFEI_API_SECRET="your_apisecret"')
        sys.exit(1)
    
    audio_path = sys.argv[1]
    api = "xunfei"
    
    # 检查参数
    if "--api" in sys.argv:
        idx = sys.argv.index("--api")
        if len(sys.argv) > idx + 1:
            api = sys.argv[idx + 1]
    
    # 初始化系统
    system = VoiceRecognitionSystem()
    
    try:
        if os.path.isdir(audio_path):
            # 处理文件夹
            results = system.process_audio_folder(audio_path)
            print("\n" + "=" * 60)
            print("📊 识别结果汇总")
            print("=" * 60)
            for result in results:
                print(f"\n{result['file']}:")
                print(f"  {result['text']}")
        else:
            # 处理单个文件
            result = system.recognize(audio_path, api)
            if result:
                print("\n" + "=" * 60)
                print("✅ 识别结果")
                print("=" * 60)
                print(f"\n{result}")
            else:
                print("\n❌ 识别失败")
    finally:
        # 清理
        system.cleanup()


if __name__ == "__main__":
    main()
