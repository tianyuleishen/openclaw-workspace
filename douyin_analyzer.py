#!/usr/bin/env python3
"""
抖音热门内容分析工具
功能：下载抖音视频，分析风格、素材、热门规律
"""

import os
import json
import requests
from datetime import datetime

class DouyinAnalyzer:
    """抖音内容分析器"""
    
    def __init__(self, download_dir="douyin_analysis"):
        self.download_dir = download_dir
        os.makedirs(download_dir, exist_ok=True)
        os.makedirs(f"{download_dir}/videos", exist_ok=True)
        os.makedirs(f"{download_dir}/analysis", exist_ok=True)
        
        # 热门内容分类模板
        self.categories = {
            "萌系可爱": ["可爱", "萌", "小动物", "宠物", "小朋友"],
            "搞笑幽默": ["搞笑", "幽默", "段子", "笑死", "哈哈哈"],
            "治愈系": ["治愈", "温暖", "舒压", "解压", " calm"],
            "技能展示": ["教程", "技巧", "教学", "教学", "学会"],
            "生活日常": ["日常", "生活", " vlog", "记录"],
            "美食": ["美食", "吃播", "做饭", "美食制作"]
        }
    
    def analyze_video_info(self, info):
        """分析视频信息"""
        analysis = {
            "发布时间": info.get("create_time", "未知"),
            "时长": info.get("duration", "未知"),
            "点赞数": info.get("statistics", {}).get("digg_count", 0),
            "评论数": info.get("statistics", {}).get("comment_count", 0),
            "分享数": info.get("statistics", {}).get("share_count", 0),
            "播放量估算": info.get("statistics", {}).get("play_count", "未知"),
            "音乐": info.get("music", {}).get("title", "未知"),
            "标签": [tag.get("tag_name") for tag in info.get("challenge", [])],
            "描述": info.get("desc", "无描述")
        }
        return analysis
    
    def generate_report(self, videos):
        """生成分析报告"""
        report = []
        report.append("# 抖音热门内容分析报告")
        report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append(f"分析视频数: {len(videos)}")
        report.append("")
        
        # 统计
        total_likes = sum(v.get("likes", 0) for v in videos)
        avg_likes = total_likes / len(videos) if videos else 0
        
        report.append("## 整体数据")
        report.append(f"- 总点赞: {total_likes:,}")
        report.append(f"- 平均点赞: {avg_likes:,.0f}")
        report.append("")
        
        # 风格分类
        style_count = {}
        for v in videos:
            style = v.get("style", "未分类")
            style_count[style] = style_count.get(style, 0) + 1
        
        report.append("## 内容风格分布")
        for style, count in sorted(style_count.items(), key=lambda x: -x[1]):
            pct = count / len(videos) * 100 if videos else 0
            report.append(f"- {style}: {count} ({pct:.0f}%)")
        report.append("")
        
        # 热门元素
        report.append("## 热门元素总结")
        all_tags = []
        for v in videos:
            all_tags.extend(v.get("tags", []))
        
        from collections import Counter
        top_tags = Counter(all_tags).most_common(20)
        for tag, count in top_tags:
            report.append(f"- #{tag}: {count}")
        
        return "\n".join(report)
    
    def save_analysis(self, report, filename="analysis_report.md"):
        """保存分析报告"""
        path = f"{self.download_dir}/analysis/{filename}"
        with open(path, 'w', encoding='utf-8') as f:
            f.write(report)
        return path

# 使用说明
USAGE = """
🦞 抖音热门内容分析器使用说明

使用方法：

1️⃣ 手动收集视频链接：
   - 在抖音App中找到热门视频
   - 点击分享 → 复制链接
   - 保存到文本文件（每行一个链接）

2️⃣ 使用在线工具下载：
   - 访问 https://douyin.wtf/
   - 粘贴链接下载视频
   - 保存到 douyin_analysis/videos/ 目录

3️⃣ 分析已下载的视频：
   python3 douyin_analyzer.py

4️⃣ 查看分析报告：
   cat douyin_analysis/analysis/analysis_report.md

---

收集素材建议：

🎵 背景音乐：
   - 记录热门视频使用的音乐
   - 保存音乐标题
   - 后续可下载使用

🎨 风格特点：
   - 拍摄手法（特写/远景/运镜）
   - 滤镜/特效
   - 色调（暖色/冷色/高饱和）

📝 文案结构：
   - 开场吸引力
   - 内容节奏
   - 结尾引导

---

热门内容规律：

✅ 黄金3秒：
   - 开头必须有吸引力
   - 使用强视觉/听觉冲击

✅ 内容节奏：
   - 15秒内完成故事
   - 每2-3秒一个转折点

✅ 情绪价值：
   - 提供情绪（搞笑/治愈/感动）
   - 让用户有情感共鸣

✅ 互动引导：
   - 提问/投票/挑战
   - 引导评论/分享

---

建议收集10-20个热门视频进行分析，
找出共性规律，指导我们的内容创作！
"""

if __name__ == "__main__":
    print(USAGE)
    
    analyzer = DouyinAnalyzer()
    print(f"\n📁 素材保存目录: {analyzer.download_dir}/")
    print(f"📹 视频存放: {analyzer.download_dir}/videos/")
    print(f"📊 分析报告: {analyzer.download_dir}/analysis/")
