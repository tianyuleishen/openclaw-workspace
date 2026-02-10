#!/usr/bin/env python3
"""
A股常用工具箱 - 快速调用
Usage: python3 stock_tools.py [command]

Commands:
  media     - 查询传媒板块
  quote     - 查询指定股票
  news      - 财经新闻查询
  limitup   - 获取涨停数据
  analyze   - AI多因子分析
  reason    - 分析涨停原因
  all       - 全部查询
  help      - 显示帮助
"""

import sys
import subprocess

def run_script(script):
    """运行脚本"""
    try:
        subprocess.run([sys.executable, script], cwd='/home/admin/.openclaw/workspace')
    except Exception as e:
        print(f"Error: {e}")

def main():
    if len(sys.argv) < 2:
        # 默认查询传媒板块
        run_script('stock_query.py')
        return
    
    cmd = sys.argv[1].lower()
    
    commands = {
        'media': ('传媒板块', 'stock_query.py'),
        'quote': ('股票查询', 'stock_query.py'),
        'news': ('财经新闻', 'finance_news.py'),
        'limitup': ('涨停数据', 'get_limit_up.py'),
        'limit_up': ('涨停数据', 'get_limit_up.py'),
        'analyze': ('AI分析', 'stock_analyzer.py'),
        'reason': ('原因分析', 'stock_rally_analyzer.py'),
        'all': ('全部查询', None),
        'help': ('帮助', None),
    }
    
    if cmd == 'help':
        print("""
📦 A股常用工具箱 v2.0

Commands:
  python3 stock_tools.py           # 默认传媒板块
  python3 stock_tools.py quote    # 股票查询
  python3 stock_tools.py news     # ⭐ 财经新闻
  python3 stock_tools.py limitup  # 涨停数据
  python3 stock_tools.py analyze  # AI分析
  python3 stock_tools.py reason   # 原因分析
  python3 stock_tools.py all      # 全部查询
  python3 stock_tools.py help    # 显示帮助

Stock Examples:
  python3 stock_query.py sh600519  # 贵州茅台
  python3 stock_query.py sz300364  # 中文在线
  python3 stock_query.py sh000001  # 上证指数

News Examples:
  python3 finance_news.py  # 财经新闻
""")
        return
    
    if cmd == 'all':
        print("\n" + "="*60)
        print("  📊 全部查询")
        print("="*60 + "\n")
        
        print("1️⃣ 传媒板块行情...")
        run_script('stock_query.py')
        
        print("\n2️⃣ 财经新闻...")
        run_script('finance_news.py')
        
        return
    
    if cmd in commands:
        title, script = commands[cmd]
        print("\n" + "="*60)
        print(f"  📊 {title}")
        print("="*60 + "\n")
        
        if script:
            run_script(script)
    else:
        print(f"Unknown command: {cmd}")
        print("Use: python3 stock_tools.py help")

if __name__ == "__main__":
    main()
