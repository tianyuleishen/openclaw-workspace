# 🦞 元宇宙虚拟办公室视频 - 生成指南

## 方案A：在线生成（推荐）

### 步骤1：访问通义万相
打开浏览器访问：https://tongyi.aliyun.com/wanxiang/

### 步骤2：生成首帧图片
1. 点击「文生图」
2. 输入以下提示词：
```
Cute little lobster AI mascot character '小爪' in a futuristic virtual office, holographic computer screens floating around, neon lights, cyberpunk aesthetic, working on AI code, 9:16 vertical aspect ratio, high tech atmosphere, front view, cute style
```
3. 设置尺寸：720×1280
4. 选择风格：动漫
5. 点击生成，下载保存为 `office_start.png`

### 步骤3：生成末帧图片
1. 点击「文生图」
2. 输入以下提示词：
```
Cute little lobster AI mascot character '小爪' in a futuristic virtual office, holographic screens showing completed code, neon lights, cyberpunk aesthetic, raising claw in victory, happy expression, high tech atmosphere, 9:16 vertical aspect ratio, cute style
```
3. 设置尺寸：720×1280
4. 选择风格：动漫
5. 点击生成，下载保存为 `office_end.png`

### 步骤4：生成视频
1. 点击「图生视频」
2. 选择「首尾帧」模式
3. 上传 `office_start.png` 作为首帧
4. 上传 `office_end.png` 作为末帧
5. 设置时长：15秒
6. 设置分辨率：720p
7. 点击生成，下载视频

### 步骤5：上传视频
将生成的视频上传到下载服务器：
```
http://8.130.18.239:8080/upload
```

---

## 方案B：本地生成脚本

如果想在本地运行，需要：

1. 安装Python 3.8+
2. 安装依赖：
```bash
pip install requests
```

3. 下载并运行脚本：
```bash
curl -O https://raw.main/server/generate_video.py
python3 generate_video.py
```

---

## 成本

| 项目 | 价格 |
|------|------|
| 首帧图片 | ¥0.02 |
| 末帧图片 | ¥0.02 |
| 视频生成 | ¥0.02 |
| **总计** | **¥0.06** |

---

## 下载链接

视频生成后，请上传到：

**服务器地址**: `http://8.130.18.239:8080`

**上传方式**:
- FTP: 8.130.18.239
- SSH: scp video.mp4 admin@8.130.18.239:/tmp/
- 或者使用下载服务器的上传页面

---

## 参考

- 通义万相：https://tongyi.aliyun.com/wanxiang/
- 下载服务器：http://8.130.18.239:8080

---

*创建时间: 2026-02-09*
