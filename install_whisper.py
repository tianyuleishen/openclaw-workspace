#!/usr/bin/env python3
"""
Whisper 语音识别配置脚本

使用方法:
1. 运行此脚本自动配置
2. 或者手动执行以下命令
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """运行命令"""
    print(f"\n📝 {description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ 成功")
        return True
    else:
        print(f"❌ 失败: {result.stderr}")
        return False

def install_whisper():
    """安装 Whisper"""
    
    print("=" * 60)
    print("🎤 Whisper 语音识别配置")
    print("=" * 60)
    
    # 检查 Python
    print("\n1. 检查 Python 环境...")
    try:
        version = subprocess.check_output("python3 --version", shell=True).decode().strip()
        print(f"✅ Python: {version}")
    except:
        print("❌ 未找到 Python")
        return False
    
    # 创建虚拟环境
    venv_path = "/home/admin/.openclaw/venv_whisper"
    if not os.path.exists(venv_path):
        print(f"\n2. 创建虚拟环境...")
        if not run_command(f"python3 -m venv {venv_path}", "创建虚拟环境"):
            return False
    else:
        print(f"\n2. 虚拟环境已存在")
    
    # 激活虚拟环境
    print(f"\n3. 激活虚拟环境...")
    activate_cmd = f"source {venv_path}/bin/activate"
    
    # 安装依赖
    print(f"\n4. 安装 Whisper 依赖...")
    
    # 安装 PyTorch (CPU 版本)
    cmds = [
        (f"{activate_cmd} && pip install --upgrade pip", "升级 pip"),
        (f"{activate_cmd} && pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu", "安装 PyTorch CPU 版本"),
        (f"{activate_cmd} && pip install openai-whisper", "安装 Whisper"),
        (f"{activate_cmd} && pip install ffmpeg-python", "安装 ffmpeg-python"),
    ]
    
    for cmd, desc in cmds:
        if not run_command(cmd, desc):
            print(f"\n⚠️ 安装失败，请手动执行:")
            print(cmd)
            return False
    
    # 安装系统依赖
    print(f"\n5. 安装系统依赖 (ffmpeg)...")
    run_command("sudo apt-get update && sudo apt-get install -y ffmpeg", "安装 ffmpeg")
    
    # 测试安装
    print(f"\n6. 测试 Whisper...")
    test_cmd = f'{activate_cmd} && python3 -c "import whisper; print(f"✅ Whisper 版本: {{whisper.__version__}}")"'
    run_command(test_cmd, "测试 Whisper")
    
    # 创建快捷脚本
    print(f"\n7. 创建快捷命令...")
    script_content = f'''#!/bin/bash
# Whisper 语音识别快捷脚本

# 使用方法:
# ./whisper_transcribe.sh <音频文件>

venv_path="/home/admin/.openclaw/venv_whisper"
audio_file="${{1:-/home/admin/.openclaw/media/inbound/latest.ogg}}"

if [ ! -f "$audio_file" ]; then
    echo "用法: $0 <音频文件>"
    exit 1
fi

source "$venv_path/bin/activate"

echo "🎤 正在识别语音: $audio_file"

whisper "$audio_file" \\
    --model small \\
    --language Chinese \\
    --output_dir /home/admin/.openclaw/media/outbound

echo "✅ 识别完成! 结果保存在: /home/admin/.openclaw/media/outbound/"
'''
    
    with open("/home/admin/.openclaw/whisper_transcribe.sh", "w") as f:
        f.write(script_content)
    
    os.chmod("/home/admin/.openclaw/whisper_transcribe.sh", 0o755)
    print("✅ 创建快捷脚本: /home/admin/.openclaw/whisper_transcribe.sh")
    
    print("\n" + "=" * 60)
    print("🎉 安装完成!")
    print("=" * 60)
    print("\n使用方法:")
    print("1. 手动执行:")
    print("   source /home/admin/.openclaw/venv_whisper/bin/activate")
    print("   whisper <音频文件> --model small --language Chinese")
    print("")
    print("2. 使用快捷脚本:")
    print("   /home/admin/.openclaw/whisper_transcribe.sh <音频文件>")
    print("")
    print("示例:")
    print("   /home/admin/.openclaw/whisper_transcribe.sh /home/admin/.openclaw/media/inbound/audio.ogg")
    
    return True

if __name__ == "__main__":
    install_whisper()
