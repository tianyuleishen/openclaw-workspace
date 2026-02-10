#!/usr/bin/env python3
"""
A股涨停股票获取器 - 使用TuShare真实数据
"""

import tushare as ts
from datetime import datetime
import json

# TuShare Token配置
TOKEN = "06dcd1581204b5fbf16a2d500fbba9b7fab80d38329b1e7cc2069f03"

def setup_tushare():
    """配置TuShare"""
    ts.set_token(TOKEN)
    pro = ts.pro_api()
    return pro

def get_stock_names():
    """获取股票名称映射"""
    pro = setup_tushare()
    
    try:
        # 获取所有上市股票
        stocks = pro.stock_basic(
            exchange='',
            list_status='L',
            fields='ts_code,name'
        )
        
        # 创建字典: ts_code -> name
        name_map = {}
        for _, row in stocks.iterrows():
            code = row['ts_code']
            name = row['name']
            # 去掉交易所后缀
            code_short = code.split('.')[0]
            name_map[code_short] = name
        
        return name_map
        
    except Exception as e:
        print(f"❌ 获取股票名称失败: {e}")
        return {}

def get_today_limit_up():
    """获取今日涨停股票"""
    pro = setup_tushare()
    
    today = datetime.now().strftime("%Y%m%d")
    
    print("=" * 80)
    print(f"📈 获取 {today} 涨停股票数据...")
    print("=" * 80)
    print()
    
    try:
        # 获取全部A股数据
        df = pro.daily(trade_date=today)
        
        if df is None or df.empty:
            print("⚠️ 未获取到数据")
            return None
        
        # 获取股票名称映射
        name_map = get_stock_names()
        
        # 筛选涨停股票
        limit_up = df[
            (df['pct_chg'] >= 9.9) |  # 普通A股涨停
            ((df['pct_chg'] >= 4.9) & (df['ts_code'].str.contains('ST|SZT', na=False)))  # ST股
        ]
        
        # 添加股票名称
        limit_up = limit_up.copy()
        limit_up['code'] = limit_up['ts_code'].str.split('.').str[0]
        limit_up['name'] = limit_up['code'].map(name_map).fillna('N/A')
        
        # 按涨跌幅排序
        limit_up = limit_up.sort_values('pct_chg', ascending=False)
        
        print(f"✅ 找到 {len(limit_up)} 只涨停股票")
        print()
        
        return limit_up
        
    except Exception as e:
        print(f"❌ 获取数据失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def save_limit_up_data(limit_up_df):
    """保存涨停数据"""
    if limit_up_df is None:
        return None
    
    today = datetime.now().strftime("%Y%m%d")
    filename = f"limit_up_stocks_{today}.json"
    
    # 转换为字典列表
    stocks_list = limit_up_df.to_dict('records')
    
    # 简化数据
    simplified = []
    for stock in stocks_list:
        simplified.append({
            "code": stock.get('code', ''),
            "name": stock.get('name', ''),
            "pct_chg": round(stock.get('pct_chg', 0), 2),
            "turnover": round(stock.get('vol', 0) / 1000000, 2),  # 估算换手率
            "industry": "待分析"
        })
    
    # 保存到文件
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(simplified, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 数据已保存: {filename}")
    print(f"   共 {len(simplified)} 只股票")
    
    return simplified

def display_stocks(stocks_list):
    """显示股票列表"""
    if not stocks_list:
        print("❌ 无数据可显示")
        return
    
    print()
    print("涨停股票列表:")
    print("-" * 80)
    print(f"{'序号':^4} {'代码':^10} {'名称':^10} {'涨跌幅':^10}")
    print("-" * 80)
    
    for i, stock in enumerate(stocks_list, 1):
        code = stock.get('code', 'N/A')
        name = stock.get('name', 'N/A')[:8]
        pct = stock.get('pct_chg', 0)
        
        print(f"{i:^4} {code:^10} {name:^10} {pct:>8.2f}%")
    
    print()
    print(f"💡 共 {len(stocks_list)} 只涨停股票")

def main():
    print("=" * 80)
    print("              🇨🇳 TuShare A股涨停数据获取")
    print("=" * 80)
    print()
    
    # 获取涨停数据
    limit_up_df = get_today_limit_up()
    
    if limit_up_df is not None:
        # 保存数据
        stocks_list = save_limit_up_data(limit_up_df)
        
        # 显示列表
        display_stocks(stocks_list)
        
        # 返回数据供后续分析
        return stocks_list
    else:
        print("❌ 无法获取涨停数据")
        return None

if __name__ == "__main__":
    main()
