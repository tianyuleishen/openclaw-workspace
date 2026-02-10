# 🦞 元宇宙虚拟办公室视频 - 全程指南

## 问题说明

⚠️ **当前状态**: API密钥权限不足或格式错误
- 系统配置的密钥格式不正确
- 需要更新有效的通义万相API密钥

---

## 快速修复

### 步骤1：获取正确的API密钥

1. 访问阿里云控制台：
   https://dashscope.console.aliyun.com/

2. 创建或获取API密钥：
   - 点击「API-KEY」或「AccessKey」
   - 创建新的API密钥
   - 复制 `sk-xxxxxx` 格式的密钥

### 步骤2：更新密钥

在终端运行：
```bash
export DASHSCOPE_API_KEY="sk-你的真实密钥"
```

或永久保存到 `~/.bashrc`：
```bash
echo 'export DASHSCOPE_API_KEY="sk-你的真实密钥"' >> ~/.bashrc
source ~/.bashrc
```

---

## 已准备好的视频参数

### 场景：虚拟办公室

| 参数 | 值 |
|------|-----|
| **场景描述** | 小爪在元宇宙虚拟办公室里工作 |
| **分辨率** | 720p (720×1280) |
| **比例** | 9:16 竖屏 |
| **时长** | 15秒 |
| **风格** | 动漫/卡通 |
| **文案** | "元宇宙搬砖第一天~" |

### 提示词（英文）

```
A cute little red lobster AI mascot character named '小爪' working 
in a futuristic virtual office with holographic computer screens 
floating around, neon lights, cyberpunk aesthetic, working on code, 
9:16 vertical aspect ratio, high tech atmosphere, anime style
```

### 提示词（中文，可直接复制）

```
一只可爱的红色小螯虾AI助手角色叫'小爪'，在未来的虚拟办公室里工作，
周围环绕着全息电脑屏幕，霓虹灯光，赛博朋克风格，正在写代码，
9:16竖屏比例，高科技氛围，动漫风格
```

---

## 成本对比

| 方案 | 模型 | 费用 | 状态 |
|------|------|------|------|
| ✅ 推荐 | wan2.1-t2v-1.3b | ¥0.30/15秒 | 最便宜 |
| ⚠️ 当前可用 | wan2.6-i2v-flash | ¥0.75/15秒 | 待验证 |
| ❌ 昂贵 | wan2.1-t2v-720p-HD | ¥1.50/15秒 | 不推荐 |

---

## 生成步骤（更新密钥后）

### 方法1：使用脚本自动生成

```bash
# 1. 更新密钥
export DASHSCOPE_API_KEY="sk-你的真实密钥"

# 2. 运行生成脚本
python3 /home/admin/.openclaw/workspace/scripts/generate_cheap_video.py

# 3. 查看输出
ls -lh /tmp/clawlet_*.mp4
```

### 方法2：使用通义万相控制台（推荐）

1. 访问：https://tongyi.aliyun.com/wanxiang/
2. 选择「文生视频」
3. 输入提示词（英文或中文）
4. 选择模型：wan2.1-t2v-1.3b
5. 设置时长：15秒
6. 设置尺寸：720×1280
7. 点击生成

---

## 视频内容描述

### 画面1（0-5秒）
- 小爪坐在全息办公桌前
- 周围环绕着漂浮的代码屏幕
- 表情专注，正在敲代码

### 画面2（5-10秒）
- 屏幕显示完成的代码
- 小爪举起爪子表示完成
- 开心的表情

### 画面3（10-15秒）
- 小爪比胜利的手势
- 背后显示"Done"或"完成"
- 背景有霓虹灯效果

---

## 下载服务器

**地址**: http://8.130.18.239:8080/

**使用方法**:
```bash
# 上传视频
curl -F 'file=@video.mp4' http://8.130.18.239:8080/office_video.mp4

# 查看文件列表
curl http://8.130.18.239:8080/
```

---

## 下一步

请按以下顺序操作：

1. ✅ 获取新的通义万相API密钥
2. ✅ 更新环境变量 `DASHSCOPE_API_KEY`
3. ⏳ 重新运行生成脚本
4. ⏳ 下载并测试视频

---

## 相关文件

```
/home/admin/.openclaw/workspace/
├── scripts/generate_cheap_video.py    # 性价比生成脚本
├── scripts/generate_metaverse_clawlet.py  # 元宇宙场景库
├── VIDEO_GENERATION_FULL_GUIDE.md    # 本指南
└── cheap_models.md                   # 模型对比
```

---

*更新时间: 2026-02-09*
*作者: 小爪 🦞*
