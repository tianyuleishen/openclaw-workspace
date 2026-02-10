# 🦞 元宇宙虚拟办公室视频 - 全自动生成

## ⚠️ 当前状态

**问题**: API密钥权限不足或格式错误
**状态**: 已创建自动化脚本，等待有效密钥

---

## 📋 已完成的工作

### ✅ 创建的文件

1. **AUTO_VIDEO_GENERATOR.sh** - 一键生成脚本
2. **scripts/generate_cheap_video.py** - Python生成脚本
3. **scripts/generate_metaverse_clawlet.py** - 元宇宙场景库
4. **cheap_models.md** - 模型对比

### ✅ 已配置

| 项目 | 配置 |
|------|------|
| 场景 | 虚拟办公室 🏢 |
| 分辨率 | 720p (720×1280) |
| 比例 | 9:16 竖屏 |
| 时长 | 15秒 |
| 风格 | 动漫/卡通 |
| 文案 | "元宇宙搬砖第一天~" |
| 成本 | ¥0.30 |

---

## 🚀 快速开始

### 方法1：更新密钥后一键生成

```bash
# 1. 更新API密钥
export DASHSCOPE_API_KEY="sk-你的真实密钥"

# 2. 运行一键生成
bash /home/admin/.openclaw/workspace/AUTO_VIDEO_GENERATOR.sh
```

### 方法2：手动生成（当前可用）

1. 访问：https://tongyi.aliyun.com/wanxiang/
2. 选择「文生视频」
3. 输入提示词
4. 生成并下载

---

## 📝 提示词

```
Cute little red lobster AI mascot character '小爪' working 
in a futuristic virtual office with holographic computer screens 
floating around, neon lights, cyberpunk aesthetic, 
working on code, 9:16 vertical aspect ratio, 
high tech atmosphere, anime style, 15 seconds
```

---

## 💰 成本

| 方案 | 费用 |
|------|------|
| **推荐** | ¥0.30 (wan2.1-t2v-1.3b) |
| 高清 | ¥0.75 (wan2.6-i2v-flash) |

---

## 📥 下载服务器

**地址**: http://8.130.18.239:8080/

**上传命令**:
```bash
curl -F 'file=@video.mp4' http://8.130.18.239:8080/office_video.mp4
```

---

## 🎯 下一步

1. ✅ 创建所有脚本
2. ⏳ 等待有效API密钥
3. ⏳ 生成视频
4. ⏳ 测试效果

---

*更新时间: 2026-02-09*
*作者: 小爪 🦞*
