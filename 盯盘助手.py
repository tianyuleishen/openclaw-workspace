#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小爪盯盘助手 v1.0
手动输入价格，帮你分析

使用方法:
python3 盯盘助手.py

然后根据提示输入股票代码和当前价格
"""

from datetime import datetime


def analyze_position(stock_code: str, stock_name: str, 
                    buy_price: float, current_price: float) -> str:
    """分析持仓"""
    
    # 计算浮动盈亏
    pnl = current_price - buy_price
    pnl_pct = pnl / buy_price * 100
    
    # 止盈止损
    stop_loss = buy_price * 0.92
    take_profit = buy_price * 1.15
    
    # 距离止盈止损的距离
    to_stop = (current_price - stop_loss) / stop_loss * 100
    to_profit = (take_profit - current_price) / current_price * 100
    
    # 判断状态
    if pnl_pct >= 15:
        status = "🎯 达到止盈！"
        action = "建议：卖出止盈一半"
    elif pnl_pct <= -8:
        status = "⚠️ 触发止损！"
        action = "建议：立即止损卖出"
    elif pnl_pct >= 8:
        status = "📈 大幅盈利"
        action = "建议：移动止损到成本价"
    elif pnl_pct >= 0:
        status = "📉 小幅盈利"
        action = "建议：继续持有"
    else:
        status = "📉 亏损"
        action = "建议：设置止损，耐心等待"
    
    return f"""
{'='*60}
【{stock_name}】({stock_code})
{'='*60}
📊 持仓分析:
  买入价: ¥{buy_price:.2f}
  当前价: ¥{current_price:.2f}
  浮动盈亏: {pnl:+.2f} ({pnl_pct:+.2f}%)
  
🎯 止盈止损:
  止盈价: ¥{take_profit:.2f} (+15%)  还差 {to_profit:.1f}%
  止损价: ¥{stop_loss:.2f} (-8%)   还差 {to_stop:.1f}%
  
📌 当前状态: {status}
💡 操作建议: {action}
{'='*60}
"""


def main():
    """主函数"""
    print("\n" + "="*60)
    print("🦞 小爪盯盘助手 v1.0")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*60)
    print("\n请输入以下信息:")
    
    # 输入股票信息
    try:
        stock_code = input("  股票代码 (如 600589): ").strip()
        stock_name = input("  股票名称 (如 大位科技): ").strip()
        buy_price = float(input("  买入价格 (如 11.45): ").strip())
        current_price = float(input("  当前价格 (如 12.00): ").strip())
        
        # 分析
        result = analyze_position(stock_code, stock_name, buy_price, current_price)
        print(result)
        
        # 保存
        filename = f"/home/admin/.openclaw/workspace/选股结果/盯盘_{stock_code}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(result)
        
        print(f"\n✅ 分析已保存: {filename}")
        
    except KeyboardInterrupt:
        print("\n\n已退出")
    except Exception as e:
        print(f"\n❌ 错误: {e}")


if __name__ == '__main__':
    main()
