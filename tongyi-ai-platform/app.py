#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通义万相 AI 生成平台
功能：文生图、文生视频、图生视频
"""

import os
import time
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import dashscope
from dashscope import ImageSynthesis, VideoSynthesis

# ==================== 配置 ====================

app = Flask(__name__)
CORS(app)

# 设置 API Key（优先使用环境变量）
dashscope.api_key = os.environ.get(
    'DASHSCOPE_API_KEY', 
    'sk-1d3af48425824e41981816390583d437'
)

# 配置
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

# 创建上传目录
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 历史记录存储（内存，生产环境建议使用数据库）
history = []


# ==================== 页面路由 ====================

@app.route('/')
def index():
    """首页"""
    return render_template('index.html')


@app.route('/text-to-image')
def text_to_image():
    """文生图页面"""
    return render_template('text-to-image.html')


@app.route('/text-to-video')
def text_to_video():
    """文生视频页面"""
    return render_template('text-to-video.html')


@app.route('/image-to-video')
def image_to_video():
    """图生视频页面"""
    return render_template('image-to-video.html')


@app.route('/history')
def history_page():
    """历史记录页面"""
    return render_template('history.html', history=history)


# ==================== API 接口 ====================

@app.route('/api/text-to-image', methods=['POST'])
def api_text_to_image():
    """文生图 API"""
    try:
        data = request.json
        
        prompt = data.get('prompt', '')
        size = data.get('size', '1024*1024')
        style = data.get('style', '通用')
        
        if not prompt:
            return jsonify({
                'status': 'error',
                'message': '请输入描述文字'
            }), 400
        
        print(f"🎨 文生图请求: {prompt[:50]}...")
        
        # 调用 API
        response = ImageSynthesis.call(
            model='wanx-image-generation',
            prompt=prompt,
            size=size,
            style=style
        )
        
        print(f"   状态码: {response.status_code}")
        
        if response.status_code == 200:
            image_url = response.output['image_url']
            
            # 保存到历史记录
            record = {
                'id': str(uuid.uuid4()),
                'type': 'text-to-image',
                'prompt': prompt,
                'size': size,
                'style': style,
                'result': image_url,
                'created_at': datetime.now().isoformat()
            }
            history.insert(0, record)
            
            return jsonify({
                'status': 'success',
                'image_url': image_url,
                'task_id': response.output.get('task_id')
            })
        else:
            return jsonify({
                'status': 'error',
                'message': response.message
            }), 400
            
    except Exception as e:
        print(f"❌ 文生图错误: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/text-to-video', methods=['POST'])
def api_text_to_video():
    """文生视频 API"""
    try:
        data = request.json
        
        prompt = data.get('prompt', '')
        size = data.get('size', '1280*720')
        duration = data.get('duration', 5)
        
        if not prompt:
            return jsonify({
                'status': 'error',
                'message': '请输入描述文字'
            }), 400
        
        print(f"🎬 文生视频请求: {prompt[:50]}...")
        
        # 调用 API（需要替换为正确的模型名称）
        response = VideoSynthesis.call(
            model='wanx-video-01',  # TODO: 替换为正确的模型
            prompt=prompt,
            size=size,
            duration=duration
        )
        
        print(f"   状态码: {response.status_code}")
        
        if response.status_code == 200:
            video_url = response.output.get('video_url', '')
            task_id = response.output.get('task_id', '')
            
            # 保存到历史记录
            record = {
                'id': str(uuid.uuid4()),
                'type': 'text-to-video',
                'prompt': prompt,
                'size': size,
                'duration': duration,
                'result': video_url,
                'task_id': task_id,
                'created_at': datetime.now().isoformat()
            }
            history.insert(0, record)
            
            return jsonify({
                'status': 'success',
                'video_url': video_url,
                'task_id': task_id
            })
        else:
            return jsonify({
                'status': 'error',
                'message': response.message
            }), 400
            
    except Exception as e:
        print(f"❌ 文生视频错误: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/image-to-video', methods=['POST'])
def api_image_to_video():
    """图生视频 API"""
    try:
        # 检查是否有文件上传
        if 'image' not in request.files:
            return jsonify({
                'status': 'error',
                'message': '请上传图片'
            }), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({
                'status': 'error',
                'message': '未选择文件'
            }), 400
        
        # 保存上传的图片
        filename = f"{uuid.uuid4()}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        prompt = request.form.get('prompt', '')
        size = request.form.get('size', '1280*720')
        
        print(f"🖼️ 图生视频请求: {filename}")
        
        # 调用 API（需要替换为正确的模型名称）
        response = VideoSynthesis.call(
            model='wanx-video-01',  # TODO: 替换为正确的模型
            prompt=prompt,
            img_url=f'file://{filepath}',
            size=size
        )
        
        print(f"   状态码: {response.status_code}")
        
        if response.status_code == 200:
            video_url = response.output.get('video_url', '')
            task_id = response.output.get('task_id', '')
            
            # 保存到历史记录
            record = {
                'id': str(uuid.uuid4()),
                'type': 'image-to-video',
                'prompt': prompt,
                'image': filename,
                'size': size,
                'result': video_url,
                'task_id': task_id,
                'created_at': datetime.now().isoformat()
            }
            history.insert(0, record)
            
            return jsonify({
                'status': 'success',
                'video_url': video_url,
                'task_id': task_id
            })
        else:
            return jsonify({
                'status': 'error',
                'message': response.message
            }), 400
            
    except Exception as e:
        print(f"❌ 图生视频错误: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/history', methods=['GET'])
def api_history():
    """获取历史记录"""
    return jsonify({
        'status': 'success',
        'data': history[:50]  # 返回最近50条
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat()
    })


# ==================== 启动入口 ====================

if __name__ == '__main__':
    port = int(os.environ.get('SERVER_PORT', 5000))
    host = os.environ.get('SERVER_HOST', '0.0.0.0')
    
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║     🚀 通义万相 AI 生成平台                                    ║
    ║     ═════════════════════════════════════════════════════    ║
    ║                                                               ║
    ║     服务地址: http://{host}:{port}                             ║
    ║                                                               ║
    ║     功能页面:                                                  ║
    ║     • 首页:           http://{host}:{port}/                    ║
    ║     • 文生图:         http://{host}:{port}/text-to-image       ║
    ║     • 文生视频:       http://{host}:{port}/text-to-video       ║
    ║     • 图生视频:       http://{host}:{port}/image-to-video      ║
    ║     • 历史记录:       http://{host}:{port}/history             ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """.format(host=host, port=port))
    
    app.run(host=host, port=port, debug=True)
