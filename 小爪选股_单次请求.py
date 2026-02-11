#!/usr/bin/env python3
"""
小爪智能选股模型 - 单次请求版
只调用一次API，获取全部数据
"""

import tushare as ts
from datetime import datetime, timedelta
import sys

# Token
TOKEN = "YOUR_TUSHARE_TOKEN"
ts.set_token(TOKEN)
pro = ts.pro_api()

# 评分参数
MIN_SCORE = 60
STRONG_SCORE = 75

def main():
    print("="*80)
    print("小爪智能选股模型 v1.0")
    print("="*80)
    
    try:
        # 获取最近交易日
        trade_date = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
        
        # 单次API调用获取所有数据
        print(f"\n📡 获取 {trade_date} 的市场数据...")
        df = pro.daily(trade_date=trade_date)
        
        if df.empty:
            print("❌ 无法获取数据")
            return
        
        # 排除北交所
        df = df[~df['ts_code'].str.startswith('BJ')]
        total = len(df)
        print(f"📊 总股票数: {total}")
        
        # 市场情绪
        up_count = len(df[df['pct_chg'] > 0])
        up_limit = len(df[df['pct_chg'] >= 9.5])
        avg_pct = df['pct_chg'].mean()
        
        print(f"\n🌡️ 市场情绪:")
        print(f"   上涨: {up_count} 涨停: {up_limit} 平均: {avg_pct:.2f}%")
        
        # 评分
        print(f"\n🔍 评分分析...")
        
        results = []
        phase_score = 20 if avg_pct > 1 else (10 if avg_pct > 0 else 0)
        
        for _, row in df.iterrows():
            pct = row['pct_chg']
            turnover = row['turnover']
            
            score = phase_score
            
            if pct >= 9.5:
                score += 20
            elif pct >= 5:
                score += 10
            elif pct > 0:
                score += 10
            
            if 3 <= turnover <= 15:
                score += 10
            
            if pct > 0:
                score += 5
            
            if pct >= 9.5:
                score += 5
            
            if score >= MIN_SCORE:
                results.append({
                    'code': row['ts_code'][:6],
                    'close': row['close'],
                    'pct_chg': pct,
                    'turnover': turnover,
                    'score': score
                })
        
        # 排序
        results.sort(key=lambda x: x['score'], reverse=True)
        strong = [r for r in results if r['score'] >= STRONG_SCORE]
        
        print(f"   评分完成: {len(results)}只及格, {len(strong)}只强烈推荐")
        
        print(f"\n✅ 选股结果:")
        print(f"   及格（≥{MIN_SCORE}分）: {len(results)}")
        print(f"   强烈（≥{STRONG_SCORE}分）: {len(strong)}")
        
        if strong:
            print(f"\n🌟 强烈推荐 TOP 15:")
            print("-"*70)
            print(f"{'排名':^4} {'代码':^10} {'收盘价':^10} {'涨幅':^10} {'换手率':^10} {'评分':^6}")
            print("-"*70)
            for i, r in enumerate(strong[:15], 1):
                print(f"{i:^4} {r['code']:^10} {r['close']:^10.2f} "
                      f"{r['pct_chg']:^9.2f}% {r['turnover']:^9.2f}% {r['score']:^6}")
            
            print(f"\n📋 买入建议（TOP 5）:")
            for i, r in enumerate(strong[:5], 1):
                print(f"   {i}. {r['code']} - 收盘{r['close']:.2f}元 "
                      f"目标{r['close']*1.1:.2f}元(+10%) 止损{r['close']*0.95:.2f}元(-5%)")
        
        # 保存
        save_results(strong, results, trade_date)
        
    except Exception as e:
        print(f"❌ 错误: {e}")
    
    print("\n" + "="*80)

def save_results(strong, all_q, trade_date):
    import os
    d = f"/home/admin/.openclaw/workspace/选股结果"
    os.makedirs(d, exist_ok=True)
    
    with open(f"{d}/选股结果_{trade_date}.txt", "w", encoding='utf-8') as f:
        f.write(f"小爪智能选股 - {trade_date}\n")
        f.write("="*50 + "\n\n")
        f.write("强烈推荐:\n")
        for i, r in enumerate(strong, 1):
            f.write(f"{i}. {r['code']} 收盘{r['close']:.2f} 涨幅{r['pct_chg']:.2f}% 评分{r['score']}\n")
        f.write(f"\n及格({MIN_SCORE}分以上):\n")
        for i, r in enumerate(all_q, 1):
            f.write(f"{i}. {r['code']} 收盘{r['close']:.2f} 涨幅{r['pct_chg']:.2f}%\n")
        print(f"\n✅ 结果已保存到: {d}/选股结果_{trade_date}.txt")

if __name__ == "__main__":
    main()
