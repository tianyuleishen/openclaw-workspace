#!/usr/bin/env python3
"""
小爪智能选股模型 v1.0
真实数据版
"""

import tushare as ts
import datetime
import os

TOKEN = "YOUR_TUSHARE_TOKEN"
ts.set_token(TOKEN)
pro = ts.pro_api()

MIN_SCORE = 60
STRONG_SCORE = 75

def main():
    print("="*80)
    print("小爪智能选股模型 v1.0")
    print("="*80)
    
    # 获取昨日数据
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y%m%d')
    
    print(f"\n📡 获取 {yesterday} 数据...")
    
    try:
        df = pro.daily(trade_date=yesterday)
        
        if df.empty or len(df) == 0:
            print("❌ 无数据")
            return
        
        # 排除北交所
        df = df[~df['ts_code'].str.startswith('BJ')]
        print(f"📊 股票数: {len(df)}")
        
        # 统计
        up = len(df[df['pct_chg'] > 0])
        limit = len(df[df['pct_chg'] >= 9.5])
        avg = df['pct_chg'].mean()
        
        print(f"🌡️ 上涨: {up} 涨停: {limit} 均涨幅: {avg:.2f}%")
        
        # 评分
        print(f"\n🔍 评分...")
        results = []
        
        for _, r in df.iterrows():
            score = 0
            pct = r['pct_chg']
            tr = r.get('turnover', r.get('turnover_rate', 0))
            
            # 情绪
            if avg > 1: score += 20
            elif avg > 0: score += 10
            
            # 涨幅
            if pct >= 9.5: score += 20
            elif pct >= 5: score += 10
            elif pct > 0: score += 10
            
            # 换手
            if 3 <= tr <= 15: score += 10
            
            # 分时
            if r['close'] > r['open']: score += 5
            if pct >= 9.5: score += 5
            
            if score >= MIN_SCORE:
                results.append({
                    'code': r['ts_code'][:6],
                    'close': r['close'],
                    'pct': pct,
                    'turnover': tr,
                    'score': score
                })
        
        # 排序
        results.sort(key=lambda x: x['score'], reverse=True)
        strong = [r for r in results if r['score'] >= STRONG_SCORE]
        
        print(f"✅ 及格: {len(results)} 强烈: {len(strong)}")
        
        if strong:
            print(f"\n🌟 强烈推荐 TOP 15:")
            print("-"*60)
            print(f"{'排名':^4} {'代码':^10} {'收盘':^10} {'涨幅':^10} {'换手':^8} {'评分':^6}")
            print("-"*60)
            for i, r in enumerate(strong[:15], 1):
                print(f"{i:^4} {r['code']:^10} {r['close']:^10.2f} "
                      f"{r['pct']:^9.2f}% {r['turnover']:^7.2f}% {r['score']:^6}")
            
            print(f"\n📋 买入建议（TOP 5）:")
            for i, r in enumerate(strong[:5], 1):
                print(f"   {i}. {r['code']} 收盘{r['close']:.2f} → 目标{r['close']*1.1:.2f} 止损{r['close']*0.95:.2f}")
        
        # 保存
        save(strong, results, yesterday)
        
    except Exception as e:
        print(f"❌ 错误: {e}")
    
    print("\n" + "="*80)

def save(strong, all_q, date):
    d = f"/home/admin/.openclaw/workspace/选股结果"
    os.makedirs(d, exist_ok=True)
    
    with open(f"{d}/选股结果_{date}.txt", "w", encoding='utf-8') as f:
        f.write(f"小爪智能选股 - {date}\n")
        f.write("="*50 + "\n\n")
        f.write(f"强烈推荐:\n")
        for i, r in enumerate(strong, 1):
            f.write(f"{i}. {r['code']} 收盘{r['close']:.2f} 涨幅{r['pct']:.2f}% 评分{r['score']}\n")
        f.write(f"\n及格({MIN_SCORE}分以上):\n")
        for i, r in enumerate(all_q, 1):
            f.write(f"{i}. {r['code']} 收盘{r['close']:.2f} 涨幅{r['pct']:.2f}%\n")
        print(f"\n✅ 结果已保存到: {d}/选股结果_{date}.txt")

if __name__ == "__main__":
    main()
