#!/usr/bin/env python3
"""
抖音视频制作 - 快速调用记忆
Usage: python douyin_helper.py
"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace')

from structured_memory import StructuredMemory

def main():
    print("=" * 70)
    print("                    🎬 抖音视频制作 - 快速调用")
    print("=" * 70)
    
    m = StructuredMemory()
    
    # 搜索抖音记忆
    learnings = m.query_learnings()
    douyin = [l for l in learnings if 'douyin' in l.get('source', '').lower() or '抖音' in l.get('topic', '')]
    
    print(f"\n📚 找到 {len(douyin)} 条抖音相关记忆:\n")
    
    for i, l in enumerate(douyin[-10:], 1):
        print(f"{i}. {l['topic']}")
        print(f"   来源: {l['source']}")
        print(f"   洞察: {l['insight'][:80]}...")
        print()
    
    print("=" * 70)
    print("                    💡 快速调用路径")
    print("=" * 70)
    print("""
📄 文件:
   • 抖音视频制作检查清单.md
   • 小爪抖音行动计划.md
   • 抖音运营研究报告.md

🔧 代码:
   from structured_memory import StructuredMemory
   m = StructuredMemory()
   learnings = m.query_learnings(topic='抖音')
""")

if __name__ == "__main__":
    main()
