# 📚 OpenClaw 社交媒体管理平台 - 完整部署教程

## 📅 创建日期: 2026-02-08
## 👨‍💻 作者: Clawlet 🦞
## 🎯 目标: 帮助个人和企业快速部署 OpenClaw，实现多平台社交媒体自动化管理

---

## 📋 目录

1. [简介](#1-简介)
2. [环境准备](#2-环境准备)
3. [本地部署 (个人用户)](#3-本地部署-个人用户)
4. [服务器部署 (企业用户)](#4-服务器部署-企业用户)
5. [平台集成配置](#5-平台集成配置)
6. [AI 功能配置](#6-ai-功能配置)
7. [常见问题](#7-常见问题)
8. [高级功能](#8-高级功能)

---

## 1. 简介

### 1.1 什么是 OpenClaw？

OpenClaw 是一个开源的 AI Agent 框架，专注于：
- 🤖 **多平台社交媒体管理**
- ✍️ **AI 驱动的内容创作**
- 💬 **自动化评论和私信回复**
- 📊 **数据分析和报表**
- 🔄 **定时任务和自动化**

### 1.2 能做什么？

| 功能 | 说明 |
|------|------|
| **多平台发布** | 一键发布到抖音、小红书、微信、微博等 |
| **AI 创作** | 自动生成文案、图片、视频脚本 |
| **自动回复** | AI 智能回复评论和私信 |
| **定时发布** | 预设时间自动发布内容 |
| **数据分析** | 追踪数据，生成报表 |
| **团队协作** | 多账号管理，权限控制 |

### 1.3 适用人群

- 📝 **个人博主** - 节省运营时间
- 🏢 **MCN 机构** - 批量管理多个账号
- 🏬 **中小企业** - 低成本自动化运营
- 🏢 **大企业** - 品牌一致性管理

---

## 2. 环境准备

### 2.1 硬件要求

#### 本地部署 (Mac/Windows/Ubuntu)

**最低配置**
- CPU: 4 核心
- 内存: 8GB
- 存储: 50GB 可用空间

**推荐配置**
- CPU: 8 核心
- 内存: 16GB
- 存储: 100GB SSD

#### 服务器部署

**入门配置** (1-10 账号)
- CPU: 2 核心
- 内存: 4GB
- 带宽: 5Mbps
- 价格: ¥50-100/月

**标准配置** (10-100 账号)
- CPU: 4 核心
- 内存: 8GB
- 带宽: 10Mbps
- 价格: ¥200-400/月

### 2.2 软件要求

#### 必须安装

1. **Docker Desktop** (必装)
   - macOS: [下载链接](https://www.docker.com/products/docker-desktop)
   - Windows: [下载链接](https://www.docker.com/products/docker-desktop)
   - Ubuntu: `sudo apt install docker.io`

2. **Node.js 22+** (可选，本教程不使用)
   - 本教程使用 Docker 部署，无需本地 Node.js

3. **Git** (可选)
   - 用于克隆项目源码

#### 验证安装

```bash
# 检查 Docker 是否安装成功
docker --version
# 期望输出: Docker version 24.0.x 或更高

# 检查 Docker Compose
docker-compose --version
# 期望输出: Docker Compose version v2.x.x 或更高

# 启动 Docker Desktop (macOS/Windows)
# 在应用列表中找到 Docker Desktop 并启动

# 验证 Docker 运行状态
docker ps
# 应该看到类似这样的输出:
# CONTAINER ID   IMAGE   COMMAND   CREATED   STATUS   PORTS   NAMES
```

### 2.3 账号准备

在开始之前，你需要准备以下平台的开发者账号：

| 平台 | 申请链接 | 用途 |
|------|---------|------|
| **抖音** | [抖音开放平台](https://developer.douyin.com/) | 内容发布、数据分析 |
| **小红书** | [小红书开放平台](https://developer.xiaohongshu.com/) | 内容发布 |
| **微信** | [微信开放平台](https://open.weixin.qq.com/) | 公众号/视频号发布 |
| **企业微信** | [企业微信后台](https://work.weixin.qq.com/) | 客户管理、消息推送 |
| **飞书** | [飞书开放平台](https://open.feishu.cn/) | 消息推送、文档集成 |
| **微博** [微博开放平台](https://open.weibo.com/) | 内容发布、数据分析 |

**注意**: 部分平台需要企业资质才能申请开发者账号，个人用户可能无法申请。

---

## 3. 本地部署 (个人用户)

### 3.1 克隆项目

```bash
# 创建项目目录
mkdir -p ~/openclaw-social
cd ~/openclaw-social

# 克隆项目 (如果已有源码)
git clone https://github.com/your-org/openclaw-social.git .

# 或者下载 release 包并解压
# wget https://github.com/your-org/openclaw-social/releases/latest/download/openclaw-social.tar.gz
# tar -xzf openclaw-social.tar.gz
```

### 3.2 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑配置文件
nano .env
```

**完整配置示例 (.env)**

```bash
# ===========================================
# 应用配置
# ===========================================
APP_ENV=development
APP_DEBUG=true
APP_URL=http://localhost:3000
API_URL=http://localhost:3000/api

# ===========================================
# 数据库配置 (使用 Docker PostgreSQL)
# ===========================================
DB_CONNECTION=postgres
DB_HOST=postgres
DB_PORT=5432
DB_DATABASE=openclaw_social
DB_USERNAME=postgres
DB_PASSWORD=your_strong_password_here

# ===========================================
# Redis 配置 (使用 Docker Redis)
# ===========================================
REDIS_HOST=redis
REDIS_PASSWORD=null
REDIS_PORT=6379

# ===========================================
# JWT 安全配置
# ===========================================
JWT_SECRET=生成一个随机的256位密钥
JWT_EXPIRE=24h

# ===========================================
# AI 功能配置 (Claude API)
# ===========================================
AI_PROVIDER=claude
CLAUDE_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxx
CLAUDE_MODEL=claude-sonnet-4-20250514

# ===========================================
# 存储配置
# ===========================================
STORAGE_DRIVER=local
STORAGE_PATH=./storage

# ===========================================
# 邮件配置 (可选)
# ===========================================
MAIL_MAILER=smtp
MAIL_HOST=smtp.example.com
MAIL_PORT=587
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-email-password
```

**生成随机 JWT 密钥**

```bash
# 方法 1: 使用 openssl
openssl rand -base64 32
# 输出类似: dGhpcyBpcyBhIHJhbmRvbSBzZWNyZXQga2V5IGZvciBKd1QgdG9rZW4=

# 方法 2: 使用 Python
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# 方法 3: 在线生成
# 访问 https://acte.ltd/utils/randomkey
```

### 3.3 Docker Compose 配置

**创建 docker-compose.yml**

```yaml
version: '3.8'

services:
  # OpenClaw 主应用
  openclaw:
    image: openclaw/social:latest
    container_name: openclaw-social
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - APP_ENV=${APP_ENV:-development}
      - APP_DEBUG=${APP_DEBUG:-true}
      - DB_CONNECTION=postgres
      - DB_HOST=postgres
      - DB_PORT=5432
      - DB_DATABASE=${DB_DATABASE:-openclaw_social}
      - DB_USERNAME=${DB_USERNAME:-postgres}
      - DB_PASSWORD=${DB_PASSWORD}
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - JWT_SECRET=${JWT_SECRET}
      - JWT_EXPIRE=24h
      - AI_PROVIDER=${AI_PROVIDER:-claude}
      - CLAUDE_API_KEY=${CLAUDE_API_KEY}
      - CLAUDE_MODEL=${CLAUDE_MODEL:-claude-sonnet-4-20250514}
    volumes:
      - ./storage:/app/storage
      - ./logs:/app/storage/logs
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - openclaw-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

  # PostgreSQL 数据库
  postgres:
    image: postgres:15-alpine
    container_name: openclaw-postgres
    restart: unless-stopped
    environment:
      - POSTGRES_DB=${DB_DATABASE:-openclaw_social}
      - POSTGRES_USER=${DB_USERNAME:-postgres}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - openclaw-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USERNAME:-postgres}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s

  # Redis 缓存
  redis:
    image: redis:7-alpine
    container_name: openclaw-redis
    restart: unless-stopped
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    networks:
      - openclaw-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

networks:
  openclaw-network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
```

### 3.4 启动服务

```bash
# 在项目目录下执行
cd ~/openclaw-social

# 首次启动 (会自动创建数据库表)
docker-compose up -d

# 查看启动日志
docker-compose logs -f

# 或者只查看应用日志
docker-compose logs -f openclaw
```

**正常启动日志示例**

```
openclaw-social | [Info] Application starting...
openclaw-social | [Info] Connecting to database...
openclaw-social | [Info] Database connected successfully!
openclaw-social | [Info] Connecting to Redis...
openclaw-social | [Info] Redis connected successfully!
openclaw-social | [Info] Starting HTTP server on port 3000...
openclaw-social | [Info] Server started successfully!
openclaw-social | [Info] Health check available at http://localhost:3000/api/health
```

### 3.5 验证安装

```bash
# 1. 检查容器状态
docker-compose ps
# 应该看到三个容器都是 "Up" 状态

# 2. 健康检查
curl http://localhost:3000/api/health
# 期望输出:
# {
#   "status": "healthy",
#   "timestamp": "2026-02-08T07:30:00Z",
#   "version": "1.0.0"
# }

# 3. 访问管理界面
# 打开浏览器访问: http://localhost:3000
# 应该看到 OpenClaw 登录/注册页面
```

### 3.6 初始化账号

1. **打开浏览器**
   - 访问: http://localhost:3000

2. **注册账号**
   - 点击"注册"按钮
   - 填写邮箱、密码
   - 接收验证邮件（如果配置了邮件服务）
   - 或使用测试模式直接登录

3. **初始设置**
   - 设置用户名
   - 选择使用场景（个人/团队/企业）
   - 同意服务条款

---

## 4. 服务器部署 (企业用户)

### 4.1 选择云服务器

**推荐服务商**

| 服务商 | 入门配置 | 标准配置 | 链接 |
|--------|---------|---------|------|
| **阿里云** | ¥84/月 | ¥267/月 | [阿里云服务器](https://www.aliyun.com/) |
| **腾讯云** | ¥79/月 | ¥249/月 | [腾讯云服务器](https://cloud.tencent.com/) |
| **华为云** | ¥75/月 | ¥239/月 | [华为云服务器](https://www.huaweicloud.com/) |

**推荐配置选择**

```bash
# 对于 1-50 个社交账号
推荐: 4核心 CPU + 8GB 内存 + 100GB SSD
价格: ¥200-400/月
```

### 4.2 购买和配置服务器

#### 步骤 1: 购买服务器

1. 选择云服务商（推荐阿里云）
2. 选择地域（选择离你最近的地域）
3. 选择实例规格（推荐: ecs.c6.large - 2核心4GB，或 ecs.c6.xlarge - 4核心8GB）
4. 选择操作系统: Ubuntu 22.04 LTS
5. 设置安全组: 开放 80, 443, 22 端口
6. 设置登录密码或 SSH 密钥

#### 步骤 2: 连接到服务器

```bash
# macOS/Linux 使用终端
ssh root@你的服务器IP

# Windows 使用 PuTTY 或 Windows Terminal
# 连接信息:
# 主机: 你的服务器IP
# 端口: 22
# 用户名: root
# 密码: 你设置的密码
```

#### 步骤 3: 系统初始化

```bash
# 更新系统
apt update && apt upgrade -y

# 设置时区
timedatectl set-timezone Asia/Shanghai

# 安装基础工具
apt install -y curl wget git vim htop unzip

# 创建用户 (可选，推荐)
adduser openclaw
usermod -aG docker openclaw
```

### 4.3 安装 Docker

```bash
# 安装 Docker
curl -fsSL https://get.docker.com | sh

# 安装 Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# 启动 Docker
systemctl start docker
systemctl enable docker

# 验证安装
docker --version
docker-compose --version
```

### 4.4 部署 OpenClaw

```bash
# 切换到用户目录
cd /home/openclaw

# 克隆项目
git clone https://github.com/your-org/openclaw-social.git openclaw-social
cd openclaw-social

# 配置环境变量
cp .env.example .env.production
nano .env.production
```

**生产环境配置 (.env.production)**

```bash
# ===========================================
# 应用配置 (生产环境)
# ===========================================
APP_ENV=production
APP_DEBUG=false
APP_URL=https://your-domain.com
API_URL=https://your-domain.com/api

# ===========================================
# 数据库配置
# ===========================================
DB_CONNECTION=postgres
DB_HOST=postgres
DB_PORT=5432
DB_DATABASE=openclaw_social
DB_USERNAME=postgres
DB_PASSWORD=生成一个强密码

# ===========================================
# Redis 配置
# ===========================================
REDIS_HOST=redis
REDIS_PORT=6379

# ===========================================
# JWT 配置
# ===========================================
JWT_SECRET=生成一个随机256位密钥
JWT_EXPIRE=24h

# ===========================================
# AI 功能配置
# ===========================================
AI_PROVIDER=claude
CLAUDE_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxx
CLAUDE_MODEL=claude-sonnet-4-20250514

# ===========================================
# 存储配置
# ===========================================
STORAGE_DRIVER=local
STORAGE_PATH=./storage
```

### 4.5 配置 Nginx 和 SSL

```bash
# 安装 Nginx
apt install -y nginx

# 创建 Nginx 配置
cat > /etc/nginx/sites-available/openclaw-social << 'EOF'
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    # 重定向到 HTTPS
    return 301 https://$server_name$request_uri;
}
EOF

# 启用配置
ln -s /etc/nginx/sites-available/openclaw-social /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

### 4.6 配置 SSL 证书

**使用 Certbot (Let's Encrypt 免费证书)**

```bash
# 安装 Certbot
apt install -y certbot python3-certbot-nginx

# 获取 SSL 证书
certbot --nginx -d your-domain.com -d www.your-domain.com

# 按照提示操作:
# 1. 输入邮箱地址
# 2. 同意服务条款
# 3. 选择是否接收邮件
# 4. 选择是否重定向 HTTP 到 HTTPS (推荐选择 2)
```

**SSL 证书续期**

```bash
# 测试续期
certbot renew --dry-run

# 添加定时任务
crontab -e
# 添加:
# 0 0,12 * * * certbot renew --quiet
```

### 4.7 启动生产环境

```bash
# 在项目目录
cd /home/openclaw/openclaw-social

# 使用生产环境配置启动
docker-compose -f docker-compose.prod.yml up -d

# 检查状态
docker-compose -f docker-compose.prod.yml ps

# 查看日志
docker-compose -f docker-compose.prod.yml logs -f
```

**docker-compose.prod.yml**

```yaml
version: '3.8'

services:
  openclaw:
    image: openclaw/social:latest
    container_name: openclaw-social
    restart: always
    ports:
      - "127.0.0.1:3000:3000"
    environment:
      - APP_ENV=production
      - APP_DEBUG=false
    env_file:
      - .env.production
    volumes:
      - ./storage:/app/storage
      - ./logs:/app/storage/logs
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - openclaw-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  postgres:
    image: postgres:15-alpine
    restart: always
    environment:
      - POSTGRES_DB=openclaw_social
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - openclaw-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    restart: always
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    networks:
      - openclaw-network

networks:
  openclaw-network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
```

### 4.8 配置防火墙

```bash
# 检查防火墙状态
ufw status

# 开放必要端口
ufw allow 22
ufw allow 80
ufw allow 443

# 启用防火墙
ufw enable
```

### 4.9 验证生产环境

```bash
# 1. 检查服务状态
curl http://localhost:3000/api/health

# 2. 检查 HTTPS 访问
curl https://your-domain.com/api/health

# 3. 访问管理界面
# 打开浏览器访问: https://your-domain.com
```

---

## 5. 平台集成配置

### 5.1 抖音配置

#### 步骤 1: 创建应用

1. 访问 [抖音开放平台](https://developer.douyin.com/)
2. 注册开发者账号
3. 创建应用，获取:
   - App Key
   - App Secret
4. 配置回调地址: `https://your-domain.com/api/callback/douyin`

#### 步骤 2: 配置环境变量

```bash
# 编辑 .env 或 .env.production
nano .env.production

# 添加抖音配置
DOUYIN_APP_KEY=your-douyin-app-key
DOUYIN_APP_SECRET=your-douyin-app-secret
DOUYIN_ACCESS_TOKEN=
DOUYIN_REFRESH_TOKEN=
```

#### 步骤 3: OAuth 授权

1. 在管理界面点击"添加账号"
2. 选择"抖音"
3. 点击"授权"按钮
4. 使用抖音账号扫描二维码
5. 授权成功后会显示账号信息

### 5.2 小红书配置

#### 步骤 1: 创建应用

1. 访问 [小红书开放平台](https://developer.xiaohongshu.com/)
2. 注册开发者账号
3. 创建应用，获取:
   - App Key
   - App Secret
4. 配置回调地址

#### 步骤 2: 配置环境变量

```bash
# 添加小红书配置
XIAOHONGSHU_APP_KEY=your-xiaohongshu-app-key
XIAOHONGSHU_APP_SECRET=your-xiaohongshu-app-secret
XIAOHONGSHU_ACCESS_TOKEN=
XIAOHONGSHU_REFRESH_TOKEN=
```

### 5.3 微信配置

#### 步骤 1: 创建应用

1. 访问 [微信开放平台](https://open.weixin.qq.com/)
2. 注册开发者账号
3. 创建网站/应用，获取:
   - App ID
   - App Secret
4. 配置授权回调域

#### 步骤 2: 配置环境变量

```bash
# 添加微信配置
WECHAT_APP_ID=your-wechat-app-id
WECHAT_APP_SECRET=your-wechat-app-secret
WECHAT_ACCESS_TOKEN=
WECHAT_REFRESH_TOKEN=
```

### 5.4 企业微信配置

#### 步骤 1: 创建应用

1. 登录 [企业微信后台](https://work.weixin.qq.com/)
2. 进入"应用管理"
3. 创建应用，获取:
   - CorpID
   - AgentId
   - AgentSecret
4. 配置应用权限

#### 步骤 2: 配置环境变量

```bash
# 添加企业微信配置
WECOM_CORP_ID=your-wecom-corp-id
WECOM_AGENT_ID=your-wecom-agent-id
WECOM_APP_SECRET=your-wecom-app-secret
WECOM_ACCESS_TOKEN=
```

### 5.5 飞书配置

#### 步骤 1: 创建应用

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 创建应用
3. 获取:
   - App ID
   - App Secret
4. 配置应用权限:
   - im:message
   - im:message:send_as_bot
   - contact:user.base:readonly

#### 步骤 2: 配置环境变量

```bash
# 添加飞书配置
FEISHU_APP_ID=your-feishu-app-id
FEISHU_APP_SECRET=your-feishu-app-secret
FEISHU_APP_TOKEN=
FEISHU_REFRESH_TOKEN=
```

### 5.6 微博配置

#### 步骤 1: 创建应用

1. 访问 [微博开放平台](https://open.weibo.com/)
2. 创建应用
3. 获取:
   - App Key
   - App Secret
4. 配置授权回调页

#### 步骤 2: 配置环境变量

```bash
# 添加微博配置
WEIBO_APP_KEY=your-weibo-app-key
WEIBO_APP_SECRET=your-weibo-app-secret
WEIBO_ACCESS_TOKEN=
WEIBO_REFRESH_TOKEN=
```

### 5.7 平台配置汇总

```bash
# .env 完整配置示例

# ===========================================
# 抖音
# ===========================================
DOUYIN_APP_KEY=your-key
DOUYIN_APP_SECRET=your-secret

# ===========================================
# 小红书
# ===========================================
XIAOHONGSHU_APP_KEY=your-key
XIAOHONGSHU_APP_SECRET=your-secret

# ===========================================
# 微信
# ===========================================
WECHAT_APP_ID=your-app-id
WECHAT_APP_SECRET=your-secret

# ===========================================
# 企业微信
# ===========================================
WECOM_CORP_ID=your-corp-id
WECOM_AGENT_ID=your-agent-id
WECOM_APP_SECRET=your-secret

# ===========================================
# 飞书
# ===========================================
FEISHU_APP_ID=your-app-id
FEISHU_APP_SECRET=your-secret

# ===========================================
# 微博
# ===========================================
WEIBO_APP_KEY=your-key
WEIBO_APP_SECRET=your-secret
```

---

## 6. AI 功能配置

### 6.1 Claude API 配置

#### 申请 Claude API

1. 访问 [Claude 官网](https://www.anthropic.com/)
2. 注册账号并申请 API 访问
3. 获取 API Key

#### 配置环境变量

```bash
# 添加 Claude 配置
AI_PROVIDER=claude
CLAUDE_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxx
CLAUDE_MODEL=claude-sonnet-4-20250514
```

### 6.2 AI 功能使用

#### 文案生成

```bash
# API 调用示例
curl -X POST https://your-domain.com/api/ai/generate \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "social_post",
    "platform": "douyin",
    "topic": "推荐一款好用的咖啡",
    "style": "亲和、活泼",
    "length": "短文案"
  }'
```

#### 图片生成

```bash
# AI 配图生成
curl -X POST https://your-domain.com/api/ai/image \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "一杯精美的拿铁咖啡，配上拉花",
    "size": "1024x1024",
    "style": "写实"
  }'
```

#### 自动回复

```bash
# 配置自动回复规则
curl -X POST https://your-domain.com/api/automation/reply-rules \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "douyin",
    "trigger": "keyword",
    "keywords": ["价格", "多少钱", "怎么买"],
    "response_style": "专业、简洁",
    "enabled": true
  }'
```

---

## 7. 常见问题

### Q1: Docker 启动失败？

**解决方法:**

```bash
# 1. 检查 Docker 状态
docker ps

# 2. 查看详细错误日志
docker-compose logs openclaw

# 3. 检查端口占用
lsof -i :3000

# 4. 重启 Docker
sudo systemctl restart docker
```

### Q2: 数据库连接失败？

**解决方法:**

```bash
# 1. 检查 PostgreSQL 容器状态
docker-compose ps postgres

# 2. 查看 PostgreSQL 日志
docker-compose logs postgres

# 3. 检查连接配置
# 确认 .env 文件中的数据库配置正确

# 4. 重启数据库容器
docker-compose restart postgres
```

### Q3: AI 功能无法使用？

**解决方法:**

```bash
# 1. 检查 API Key 配置
# 确认 CLAUDE_API_KEY 正确设置

# 2. 检查 API 调用日志
docker-compose logs openclaw | grep -i claude

# 3. 测试 API 连通性
curl -X POST https://api.anthropic.com/v1/messages \
  -H "x-api-key: YOUR_CLAUDE_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"claude-sonnet-4-20250514","max_tokens":100,"messages":[{"role":"user","content":"hi"}]}'
```

### Q4: 平台授权失败？

**解决方法:**

```bash
# 1. 检查回调地址配置
# 确保平台后台的回调地址与配置一致

# 2. 检查 App Key/Secret
# 确认没有多余的空格或特殊字符

# 3. 检查网络连通性
curl -I https://api.douyin.com

# 4. 查看授权日志
docker-compose logs openclaw | grep -i oauth
```

### Q5: 如何升级版本？

```bash
# 1. 备份数据
docker-compose exec postgres pg_dump -U postgres openclaw_social > backup.sql

# 2. 拉取最新镜像
docker-compose pull

# 3. 重启服务
docker-compose down
docker-compose up -d

# 4. 运行迁移（如果有）
docker-compose exec openclaw php artisan migrate
```

### Q6: 如何备份数据？

```bash
# 备份数据库
docker-compose exec postgres pg_dump -U postgres openclaw_social > backups/openclaw_social_$(date +%Y%m%d).sql

# 备份文件
tar -czf backups/storage_$(date +%Y%m%d).tar.gz storage/

# 备份配置
cp .env backups/.env.$(date +%Y%m%d)
```

---

## 8. 高级功能

### 8.1 定时任务配置

```bash
# 配置定时发布任务
curl -X POST https://your-domain.com/api/scheduler/posts \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "这是一条定时发布的动态",
    "platforms": ["douyin", "xiaohongshu", "weibo"],
    "publish_time": "2026-02-09T10:00:00Z",
    "timezone": "Asia/Shanghai"
  }'
```

### 8.2 团队协作

```bash
# 创建团队
curl -X POST https://your-domain.com/api/teams \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "我的运营团队",
    "members": ["user1@example.com", "user2@example.com"]
  }'

# 设置权限
curl -X POST https://your-domain.com/api/teams/1/roles \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 2,
    "role": "editor",
    "permissions": ["posts:create", "posts:edit", "analytics:view"]
  }'
```

### 8.3 API 接口

**获取账号列表**

```bash
curl https://your-domain.com/api/accounts \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**发布内容**

```bash
curl -X POST https://your-domain.com/api/posts \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "这是一条测试动态",
    "platforms": ["douyin", "xiaohongshu"],
    "media": {
      "type": "image",
      "urls": ["https://example.com/image.jpg"]
    }
  }'
```

**获取数据统计**

```bash
curl https://your-domain.com/api/analytics/douyin \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## 📞 技术支持

**遇到问题？**

1. 查看[常见问题](#7-常见问题)
2. 查看日志: `docker-compose logs`
3. 联系客服: support@example.com

---

## 📝 附录

### A. 命令速查表

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看日志
docker-compose logs -f

# 查看状态
docker-compose ps

# 更新代码
git pull
docker-compose down
docker-compose up -d

# 备份数据
docker-compose exec postgres pg_dump -U postgres openclaw_social > backup.sql
```

### B. 端口说明

| 端口 | 用途 |
|------|------|
| 80 | HTTP (开发环境) |
| 443 | HTTPS (生产环境) |
| 3000 | OpenClaw 应用端口 |
| 5432 | PostgreSQL 数据库端口 |
| 6379 | Redis 缓存端口 |

### C. 目录结构

```
openclaw-social/
├── docker-compose.yml          # Docker Compose 配置
├── .env                        # 环境变量文件
├── storage/                   # 文件存储目录
│   ├── uploads/               # 上传文件
│   ├── logs/                  # 日志文件
│   └── cache/                 # 缓存文件
├── nginx/                     # Nginx 配置
├── backups/                   # 备份文件
└── README.md                  # 项目说明
```

---

**🎉 恭喜！你已经完成了 OpenClaw 的部署！**

如果有任何问题，请随时联系技术支持。

---

*本教程由 Clawlet 🦞 编写*
*最后更新: 2026-02-08*
