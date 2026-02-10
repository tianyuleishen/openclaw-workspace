# 通义万相 AI 生成平台开发文档

## 📋 目录

1. [项目概述](#项目概述)
2. [技术架构](#技术架构)
3. [环境准备](#环境准备)
4. [快速开始](#快速开始)
5. [前端开发](#前端开发)
6. [后端开发](#后端开发)
7. [API 接口文档](#api-接口文档)
8. [部署指南](#部署指南)
9. [常见问题](#常见问题)

---

## 项目概述

### 功能特性

| 功能 | 描述 | 模型 |
|------|------|------|
| 文生图 | 根据文字描述生成图片 | wanx-image-generation |
| 文生视频 | 根据文字描述生成视频 | wanx-video-01 |
| 图生视频 | 根据图片生成视频 | wanx-video-01 |

### 技术栈

- **前端**: HTML5, CSS3, JavaScript, Axios
- **后端**: Python, Flask, Flask-CORS
- **AI 服务**: 阿里云 DashScope（通义万相）
- **部署**: Docker, Nginx, Gunicorn

---

## 环境准备

### 1. 安装 Python 依赖

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install flask flask-cors dashscope requests
```

### 2. 配置环境变量

创建 `.env` 文件：

```bash
# 阿里云 DashScope API Key
DASHSCOPE_API_KEY=sk-您的APIKey

# 服务器配置
SERVER_HOST=0.0.0.0
SERVER_PORT=5000

# 上传文件配置
UPLOAD_FOLDER=./uploads
MAX_CONTENT_LENGTH=104857600  # 100MB
```

### 3. 安装 Docker（可选）

```bash
# Ubuntu
sudo apt-get update
sudo apt-get install docker.io docker-compose

# 启动 Docker
sudo systemctl start docker
sudo systemctl enable docker
```

---

## 快速开始

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd tongyi-ai-platform
```

### 2. 配置环境

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入您的 API Key
nano .env
```

### 3. 运行开发服务器

```bash
# 启动后端服务
python app.py

# 服务运行在 http://localhost:5000
```

### 4. 访问页面

打开浏览器访问：`http://localhost:5000`

---

## 前端开发

### 项目结构

```
templates/
├── index.html          # 主页面
├── text-to-image.html  # 文生图页面
├── text-to-video.html  # 文生视频页面
├── image-to-video.html # 图生视频页面
└── history.html        # 历史记录

static/
├── css/
│   └── style.css       # 样式文件
├── js/
│   ├── main.js         # 主逻辑
│   ├── text-to-image.js
│   ├── text-to-video.js
│   └── image-to-video.js
└── images/
    └── logo.png
```

### 1. 主页面 (index.html)

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>通义万相 AI 生成平台</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <h1>🎨 通义万相 AI 生成平台</h1>
            <ul>
                <li><a href="/">首页</a></li>
                <li><a href="/text-to-image">文生图</a></li>
                <li><a href="/text-to-video">文生视频</a></li>
                <li><a href="/image-to-video">图生视频</a></li>
                <li><a href="/history">历史记录</a></li>
            </ul>
        </div>
    </nav>

    <main class="container">
        <section class="hero">
            <h2>AI 创作，从这里开始</h2>
            <p>基于阿里云通义万相，一键生成高质量图片和视频</p>
            
            <div class="feature-cards">
                <div class="card" onclick="location.href='/text-to-image'">
                    <div class="card-icon">📝</div>
                    <h3>文生图</h3>
                    <p>输入文字描述，AI 自动生成图片</p>
                </div>
                
                <div class="card" onclick="location.href='/text-to-video'">
                    <div class="card-icon">🎬</div>
                    <h3>文生视频</h3>
                    <p>输入文字描述，AI 自动生成视频</p>
                </div>
                
                <div class="card" onclick="location.href='/image-to-video'">
                    <div class="card-icon">🖼️</div>
                    <h3>图生视频</h3>
                    <p>上传图片，AI 生成动态视频</p>
                </div>
            </div>
        </section>
    </main>

    <footer>
        <p>Powered by 阿里云通义万相 & DashScope</p>
    </footer>
</body>
</html>
```

### 2. 文生图页面 (text-to-image.html)

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文生图 - 通义万相</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <h1>📝 文生图</h1>
            <ul>
                <li><a href="/">首页</a></li>
                <li><a href="/text-to-image" class="active">文生图</a></li>
                <li><a href="/text-to-video">文生视频</a></li>
                <li><a href="/image-to-video">图生视频</a></li>
            </ul>
        </div>
    </nav>

    <main class="container">
        <div class="generate-box">
            <form id="generate-form">
                <div class="form-group">
                    <label for="prompt">输入描述：</label>
                    <textarea 
                        id="prompt" 
                        name="prompt" 
                        placeholder="请描述您想要的图片，例如：一只可爱的小猫在花园里玩耍"
                        required
                    ></textarea>
                </div>

                <div class="form-group">
                    <label for="size">图片尺寸：</label>
                    <select id="size" name="size">
                        <option value="1024*1024">1024 × 1024 (正方形)</option>
                        <option value="720*1280">720 × 1280 (竖版)</option>
                        <option value="1280*720" selected>1280 × 720 (横版)</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="style">风格：</label>
                    <select id="style" name="style">
                        <option value="通用">通用</option>
                        <option value="卡通">卡通</option>
                        <option value="写实">写实</option>
                        <option value="油画">油画</option>
                        <option value="水彩">水彩</option>
                    </select>
                </div>

                <button type="submit" class="btn-primary">
                    <span class="btn-text">生成图片</span>
                    <span class="btn-loading" style="display: none;">生成中...</span>
                </button>
            </form>

            <div id="result" class="result-box" style="display: none;">
                <h3>生成结果</h3>
                <div class="image-container">
                    <img id="generated-image" src="" alt="生成的图片">
                </div>
                <div class="actions">
                    <a id="download-link" href="" download="generated-image.png" class="btn-secondary">
                        下载图片
                    </a>
                    <button onclick="location.reload()" class="btn-secondary">
                        继续生成
                    </button>
                </div>
            </div>
        </div>
    </main>

    <script src="/static/js/text-to-image.js"></script>
</body>
</html>
```

### 3. 前端 JavaScript (text-to-image.js)

```javascript
document.getElementById('generate-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const btn = this.querySelector('button[type="submit"]');
    const btnText = btn.querySelector('.btn-text');
    const btnLoading = btn.querySelector('.btn-loading');
    
    // 显示加载状态
    btn.disabled = true;
    btnText.style.display = 'none';
    btnLoading.style.display = 'inline';
    
    const formData = {
        prompt: document.getElementById('prompt').value,
        size: document.getElementById('size').value,
        style: document.getElementById('style').value
    };
    
    try {
        const response = await fetch('/api/text-to-image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            // 显示结果
            const resultBox = document.getElementById('result');
            resultBox.style.display = 'block';
            
            document.getElementById('generated-image').src = result.image_url;
            document.getElementById('download-link').href = result.image_url;
            
            // 滚动到结果区域
            resultBox.scrollIntoView({ behavior: 'smooth' });
        } else {
            alert('生成失败：' + result.message);
        }
    } catch (error) {
        alert('请求失败：' + error.message);
    } finally {
        // 恢复按钮状态
        btn.disabled = false;
        btnText.style.display = 'inline';
        btnLoading.style.display = 'none';
    }
});
```

### 4. CSS 样式 (style.css)

```css
/* 全局样式 */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

/* 导航栏 */
.navbar {
    background: rgba(255, 255, 255, 0.95);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 15px 0;
    position: sticky;
    top: 0;
    z-index: 1000;
}

.navbar .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.navbar h1 {
    color: #333;
    font-size: 24px;
}

.navbar ul {
    display: flex;
    list-style: none;
    gap: 30px;
}

.navbar a {
    text-decoration: none;
    color: #666;
    font-weight: 500;
    transition: color 0.3s;
}

.navbar a:hover,
.navbar a.active {
    color: #667eea;
}

/* 主要内容区 */
main {
    padding: 40px 20px;
}

.hero {
    text-align: center;
    color: white;
    margin-bottom: 40px;
}

.hero h2 {
    font-size: 48px;
    margin-bottom: 20px;
}

.hero p {
    font-size: 20px;
    opacity: 0.9;
}

/* 功能卡片 */
.feature-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 30px;
    margin-top: 40px;
}

.card {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 16px;
    padding: 40px;
    text-align: center;
    cursor: pointer;
    transition: transform 0.3s, box-shadow 0.3s;
}

.card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

.card-icon {
    font-size: 64px;
    margin-bottom: 20px;
}

.card h3 {
    color: #333;
    margin-bottom: 10px;
}

.card p {
    color: #666;
}

/* 生成框 */
.generate-box {
    background: white;
    border-radius: 16px;
    padding: 40px;
    max-width: 800px;
    margin: 0 auto;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.form-group {
    margin-bottom: 25px;
}

.form-group label {
    display: block;
    margin-bottom: 10px;
    font-weight: 600;
    color: #333;
}

.form-group textarea {
    width: 100%;
    height: 120px;
    padding: 15px;
    border: 2px solid #e0e0e0;
    border-radius: 10px;
    font-size: 16px;
    resize: vertical;
    transition: border-color 0.3s;
}

.form-group textarea:focus {
    outline: none;
    border-color: #667eea;
}

.form-group select {
    width: 100%;
    padding: 12px;
    border: 2px solid #e0e0e0;
    border-radius: 10px;
    font-size: 16px;
    background: white;
    cursor: pointer;
}

/* 按钮 */
.btn-primary {
    width: 100%;
    padding: 15px 30px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 18px;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.3s, box-shadow 0.3s;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled {
    opacity: 0.7;
    cursor: not-allowed;
}

.btn-secondary {
    display: inline-block;
    padding: 12px 24px;
    background: #f0f0f0;
    color: #333;
    text-decoration: none;
    border-radius: 8px;
    font-weight: 500;
    cursor: pointer;
    border: none;
    transition: background 0.3s;
}

.btn-secondary:hover {
    background: #e0e0e0;
}

/* 结果展示 */
.result-box {
    margin-top: 40px;
    padding-top: 40px;
    border-top: 2px solid #f0f0f0;
}

.result-box h3 {
    margin-bottom: 20px;
    color: #333;
}

.image-container {
    background: #f8f8f8;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
}

.image-container img {
    max-width: 100%;
    border-radius: 8px;
}

.actions {
    display: flex;
    gap: 15px;
    justify-content: center;
}

/* 页脚 */
footer {
    text-align: center;
    padding: 30px;
    color: white;
    opacity: 0.8;
}
```

---

## 后端开发

### 1. 主应用 (app.py)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通义万相 AI 生成平台后端
"""

import os
import time
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import dashscope
from dashscope import ImageSynthesis, VideoSynthesis

# 配置
app = Flask(__name__)
CORS(app)

# 设置 API Key
dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY', 'sk-1d3af48425824e41981816390583d437')

# 配置上传文件夹
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB

# 历史记录存储
history = []


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
        
        # 调用 API
        response = ImageSynthesis.call(
            model='wanx-image-generation',
            prompt=prompt,
            size=size,
            style=style
        )
        
        if response.status_code == 200:
            image_url = response.output['image_url']
            
            # 保存到历史记录
            record = {
                'id': str(uuid.uuid4()),
                'type': 'text-to-image',
                'prompt': prompt,
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
        
        # 调用 API
        response = VideoSynthesis.call(
            model='wanx-video-01',  # 需要替换为正确的模型名称
            prompt=prompt,
            size=size,
            duration=duration
        )
        
        if response.status_code == 200:
            video_url = response.output.get('video_url', '')
            task_id = response.output.get('task_id', '')
            
            # 保存到历史记录
            record = {
                'id': str(uuid.uuid4()),
                'type': 'text-to-video',
                'prompt': prompt,
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
        
        # 调用 API
        response = VideoSynthesis.call(
            model='wanx-video-01',  # 需要替换为正确的模型名称
            prompt=prompt,
            img_url=f'file://{filepath}',
            size=size
        )
        
        if response.status_code == 200:
            video_url = response.output.get('video_url', '')
            task_id = response.output.get('task_id', '')
            
            # 保存到历史记录
            record = {
                'id': str(uuid.uuid4()),
                'type': 'image-to-video',
                'prompt': prompt,
                'image': filename,
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


if __name__ == '__main__':
    port = int(os.environ.get('SERVER_PORT', 5000))
    host = os.environ.get('SERVER_HOST', '0.0.0.0')
    
    print(f"""
    🚀 通义万相 AI 生成平台
    ======================
    服务地址: http://{host}:{port}
    
    功能页面:
    - 首页: http://{host}:{port}/
    - 文生图: http://{host}:{port}/text-to-image
    - 文生视频: http://{host}:{port}/text-to-video
    - 图生视频: http://{host}:{port}/image-to-video
    - 历史记录: http://{host}:{port}/history
    """)
    
    app.run(host=host, port=port, debug=True)
```

---

## API 接口文档

### 1. 文生图

**接口**: `POST /api/text-to-image`

**请求参数**:
```json
{
    "prompt": "一只可爱的小猫在花园里玩耍",
    "size": "1024*1024",
    "style": "卡通"
}
```

**响应成功**:
```json
{
    "status": "success",
    "image_url": "https://xxx.com/image.png",
    "task_id": "task_123456"
}
```

**响应失败**:
```json
{
    "status": "error",
    "message": "生成失败，请重试"
}
```

### 2. 文生视频

**接口**: `POST /api/text-to-video`

**请求参数**:
```json
{
    "prompt": "现代办公室场景，年轻白领使用AI工具工作",
    "size": "1280*720",
    "duration": 5
}
```

**响应**:
```json
{
    "status": "success",
    "video_url": "https://xxx.com/video.mp4",
    "task_id": "task_123456"
}
```

### 3. 图生视频

**接口**: `POST /api/image-to-video`

**Content-Type**: `multipart/form-data`

**表单参数**:
- `image`: 图片文件
- `prompt`: 描述（可选）
- `size`: 尺寸（可选）

**响应**:
```json
{
    "status": "success",
    "video_url": "https://xxx.com/video.mp4",
    "task_id": "task_123456"
}
```

---

## 部署指南

### 方案一：Docker 部署

#### 1. 创建 Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建上传目录
RUN mkdir -p uploads

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["python", "app.py"]
```

#### 2. 创建 docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DASHSCOPE_API_KEY=${DASHSCOPE_API_KEY}
      - SERVER_HOST=0.0.0.0
      - SERVER_PORT=5000
    volumes:
      - ./uploads:/app/uploads
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./uploads:/var/www/html/uploads
    depends_on:
      - web
    restart: unless-stopped
```

#### 3. 创建 nginx.conf

```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    
    server {
        listen 80;
        server_name localhost;
        
        location / {
            proxy_pass http://web:5000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
        
        location /uploads {
            alias /var/www/html/uploads;
        }
    }
}
```

#### 4. 部署命令

```bash
# 构建并启动
docker-compose up -d --build

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

---

### 方案二：手动部署

#### 1. 安装依赖

```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx
```

#### 2. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate
pip install flask flask-cors dashscope gunicorn
```

#### 3. 配置 Systemd 服务

创建 `/etc/systemd/system/ai-platform.service`:

```ini
[Unit]
Description=Tongyi AI Platform
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/ai-platform
Environment="PATH=/var/www/ai-platform/venv/bin"
Environment="DASHSCOPE_API_KEY=sk-您的APIKey"
ExecStart=/var/www/ai-platform/venv/bin/gunicorn \
    --workers 4 \
    --bind 127.0.0.1:5000 \
    app:app

Restart=always

[Install]
WantedBy=multi-user.target
```

#### 4. 配置 Nginx

创建 `/etc/nginx/sites-available/ai-platform`:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    location /uploads {
        alias /var/www/ai-platform/uploads;
    }
}
```

#### 5. 启动服务

```bash
# 启用服务
sudo systemctl enable ai-platform
sudo systemctl start ai-platform

# 配置 Nginx
sudo ln -s /etc/nginx/sites-available/ai-platform /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

### 方案三：云服务器部署

#### 使用阿里云服务器

1. **购买服务器**
   - 推荐配置：2核 4G
   - 操作系统：Ubuntu 20.04

2. **安全组配置**
   - 开放 80 端口（HTTP）
   - 开放 443 端口（HTTPS）
   - 开放 5000 端口（应用）

3. **安装 Docker**
   ```bash
   curl -fsSL https://get.docker.com | sh
   sudo usermod -aG docker $USER
   ```

4. **部署应用**
   按照 Docker 部署方案执行

---

## 常见问题

### 1. API Key 无效

**错误**: `Invalid API Key`

**解决方案**:
- 检查 API Key 是否正确
- 确认 API Key 是否有对应服务的调用权限
- 在控制台中开通相应服务

### 2. 模型不存在

**错误**: `Model not exist`

**解决方案**:
- 确认模型名称是否正确
- 在控制台中查看已开通的模型列表
- 开通相应的服务

### 3. 上传文件过大

**错误**: `413 Payload Too Large`

**解决方案**:
- 调整 `MAX_CONTENT_LENGTH` 配置
- Nginx 配置 `client_max_body_size`

### 4. 跨域问题

**错误**: CORS 错误

**解决方案**:
- 确保已安装 `flask-cors`
- 确保 `CORS(app)` 已添加

---

## 更新日志

### v1.0.0 (2026-02-08)
- ✨ 初始版本
- ✨ 文生图功能
- ✨ 文生视频功能
- ✨ 图生视频功能
- ✨ 历史记录功能
- ✨ Docker 部署支持

---

## 联系作者

如有问题，请联系：
- 作者：小爪 (Clawlet)
- 邮箱：support@example.com

---

**Happy Coding! 🚀**
