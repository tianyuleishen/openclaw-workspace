#!/usr/bin/env python3
"""
从文件学习便捷工具
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path.home() / ".openclaw/workspace"))

from proactive_learner import learn_from_document


def main():
    parser = argparse.ArgumentParser(description="从文件学习")
    parser.add_argument("filepath", help="文件路径")
    parser.add_argument("--name", "-n", default="文档", help="文档名称")
    parser.add_argument("--type", "-t", default="document", help="文档类型")
    
    args = parser.parse_args()
    
    path = Path(args.filepath)
    if not path.exists():
        print(f"❌ 文件不存在: {args.filepath}")
        return
    
    content = path.read_text(encoding='utf-8')
    
    print(f"📖 从 {args.name} 学习...")
    learnings = learn_from_document(content, args.name, args.type)
    print(f"   ✅ 学习: {len(learnings)} 条")


if __name__ == "__main__":
    main()
