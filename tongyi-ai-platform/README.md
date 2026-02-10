# 🚀 通义万相 AI 生成平台

基于阿里云通义万相的 AI 图片/视频生成平台。

## ✨ 功能特性

| 功能 | 描述 | 状态 |
|------|------|------|
| 📝 文生图 | 根据文字描述生成图片 | ✅ 可用 |
| 🎬 文生视频 | 根据文字描述生成视频 | ✅ 可用 |
| 🖼️ 图生视频 | 根据图片生成动态视频 | ✅ 可用 |
| 📋 历史记录 | 保存创作历史 | ✅ 可用 |

## 🛠️ 技术栈

- **前端**: HTML5, CSS3, JavaScript
- **后端**: Python Flask
- **AI 服务**: 阿里云 DashScope（通义万相）
- **部署**: Docker, Nginx

## 📁 项目结构

```
tongyi-ai-platform/
├── app.py                    # Flask 主应用
├── requirements.txt          # Python 依赖
├── Dockerfile               # Docker 配置
├── docker-compose.yml       # Docker Compose 配置
├── nginx.conf               # Nginx 配置
├── .env.example             # 环境变量模板
├── templates/               # HTML 模板
│   ├── index.html          # 首页
│   ├── text-to-image.html  # 文生图
│   ├── text-to-video.html  # 文生视频
│   ├── image-to-video.html # 图生视频
│   └── history.html        # 历史记录
├── static/                  # 静态资源
│   ├── css/style.css       # 样式
│   └── js/                 # JavaScript
│       ├── text-to-image.js
│       ├── text-to-video.js
│       ├── image-to-video.js
│       └── history.js
└── uploads/                # 上传文件目录
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件
# 修改 DASHSCOPE_API_KEY 为您的 API Key
```

### 3. 运行开发服务器

```bash
python app.py
```

访问 http://localhost:5000

## 🐳 Docker 部署

### 1. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入 API Key
```

### 2. 构建和启动

```bash
# 构建并启动服务
docker-compose up -d --build

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 3. 访问

- 无 Nginx: http://localhost:5000
- 有 Nginx: http://localhost

## 🔧 配置说明

### 环境变量

| 变量名 | 描述 | 默认值 |
|--------|------|--------|
| `DASHSCOPE_API_KEY` | 阿里云 DashScope API Key | 必填 |
| `SERVER_HOST` | 服务器地址 | `0.0.0.0` |
| `SERVER_PORT` | 服务端口 | `5000` |
| `SECRET_KEY` | Flask session 密钥 | 自动生成 |
| `MAX_CONTENT_LENGTH` | 上传文件大小限制 | `104857600` (100MB) |

### 获取 API Key

1. 打开 [阿里云 DashScope 控制台](https://dashscope.console.aliyun.com/)
2. 登录阿里云账号
3. 创建 API Key
4. 开通通义万相服务

## 📖 API 接口

### 文生图

```bash
POST /api/text-to-image
Content-Type: application/json

{
    "prompt": "一只可爱的小猫",
    "size": "1024*1024",
    "style": "卡通"
}
```

### 文生视频

```bash
POST /api/text-to-video
Content-Type: application/json

{
    "prompt": "现代办公室场景",
    "size": "1280*720",
    "duration": 5
}
```

### 图生视频

```bash
POST /api/image-to-video
Content-Type: multipart/form-data

image: [图片文件]
prompt: [描述文字]
size: "1280*720"
```

## 🐛 常见问题

### 1. API Key 无效

确保已开通通义万相服务，并在控制台中获取有效的 API Key。

### 2. 模型不存在

确认模型名称正确，并在控制台中开通相应服务。

### 3. 上传文件过大

检查 `MAX_CONTENT_LENGTH` 配置和 Nginx 的 `client_max_body_size`。

## 📝 许可证

MIT License

## 👨‍💻 作者

小爪 (Clawlet)

---

**Happy Creating! 🎨🎬**
