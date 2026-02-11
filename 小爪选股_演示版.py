#!/usr/bin/env python3
"""
小爪智能选股模型 - 演示版
使用Tushare获取真实数据
"""

import tushare as ts
from datetime import datetime, timedelta
import sys

# 配置Token
TOKEN = "YOUR_TUSHARE_TOKEN"

# 初始化
ts.set_token(TOKEN)
pro = ts.pro_api()

# 评分参数
MIN_SCORE = 60
STRONG_SCORE = 75

def main():
    print("="*80)
    print("小爪智能选股模型 v1.0")
    print("="*80)
    
    # 获取最近交易日
    try:
        # 尝试获取今日数据
        today = datetime.now().strftime('%Y%m%d')
        df = pro.daily(trade_date=today)
        
        if df.empty:
            # 尝试昨日数据
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
            df = pro.daily(trade_date=yesterday)
            trade_date = yesterday
        else:
            trade_date = today
        
        if df.empty:
            print("❌ 无法获取交易日数据")
            print("可能原因：非交易时间、数据未更新")
            return
        
        print(f"📅 交易日: {trade_date}")
        print(f"📊 总股票数: {len(df)}")
        
        # 排除北交所
        df = df[~df['ts_code'].str.startswith('BJ')]
        print(f"📊 排除北交后: {len(df)}")
        
        # 计算市场情绪
        up_count = len(df[df['pct_chg'] > 0])
        down_count = len(df[df['pct_chg'] < 0])
        up_limit = len(df[df['pct_chg'] >= 9.5])
        avg_pct = df['pct_chg'].mean()
        
        print(f"\n🌡️ 市场情绪:")
        print(f"   上涨: {up_count} 下跌: {down_count}")
        print(f"   涨停: {up_limit} 平均涨幅: {avg_pct:.2f}%")
        
        # 判断周期
        if up_limit > 200 and avg_pct > 3:
            phase = "高潮"
        elif up_limit > 100 and avg_pct > 2:
            phase = "回暖"
        elif up_limit > 50 and avg_pct > 1:
            phase = "复苏"
        else:
            phase = "退潮"
        print(f"   周期: {phase}")
        
        # 评分并排序
        print(f"\n🔍 开始评分...")
        results = []
        
        for i, (_, row) in enumerate(df.iterrows(), 1):
            code = row['ts_code'][:6]
            pct_chg = row['pct_chg']
            vol = row['vol']
            turnover = row['turnover_rate']
            close = row['close']
            high = row['high']
            low = row['low']
            
            # 简单评分
            score = 0
            
            # 情绪周期
            if phase in ['复苏', '回暖', '高潮']:
                score += 20
            
            # 个股涨幅
            if pct_chg >= 9.5:
                score += 20
            elif pct_chg >= 5:
                score += 10
            
            # 趋势（简化）
            if pct_chg > 0:
                score += 10
            
            # 量能
            if turnover >= 3 and turnover <= 15:
                score += 10
            
            # 分时
            if close >= row['open']:
                score += 5
            
            if score >= MIN_SCORE:
                results.append({
                    'code': code,
                    'close': close,
                    'pct_chg': pct_chg,
                    'turnover': turnover,
                    'score': score
                })
            
            if i % 500 == 0:
                print(f"   已处理: {i}/{len(df)}")
        
        print(f"   完成: 共{len(results)}只股票达到{MIN_SCORE}分")
        
        # 排序
        results.sort(key=lambda x: x['score'], reverse=True)
        strong = [r for r in results if r['score'] >= STRONG_SCORE]
        
        print(f"\n✅ 选股结果:")
        print(f"   及格（≥{MIN_SCORE}分）: {len(results)}只")
        print(f"   强烈（≥{STRONG_SCORE}分）: {len(strong)}只")
        
        if strong:
            print(f"\n🌟 强烈推荐 TOP 10:")
            print("-"*60)
            print(f"{'排名':^4} {'代码':^10} {'收盘价':^10} {'涨幅':^10} {'换手率':^10} {'评分':^6}")
            print("-"*60)
            for i, r in enumerate(strong[:10], 1):
                print(f"{i:^4} {r['code']:^10} {r['close']:^10.2f} "
                      f"{r['pct_chg']:^9.2f}% {r['turnover']:^9.2f}% {r['score']:^6}")
            
            print(f"\n📋 买入建议:")
            for i, r in enumerate(strong[:3], 1):
                print(f"   {i}. {r['code']} - 收盘{r['close']:.2f}元 目标{r['close']*1.1:.2f}元 (+10%)")
        
        # 保存结果
        save_results(strong, results, trade_date)
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*80)

def save_results(strong: list, all_q: list, trade_date: str):
    """保存结果"""
    import os
    output_dir = "/home/admin/.openclaw/workspace/选股结果"
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f"{output_dir}/选股结果_{trade_date}.txt", "w", encoding='utf-8') as f:
        f.write(f"小爪智能选股结果 - {trade_date}\n")
        f.write("="*60 + "\n\n")
        
        f.write("强烈推荐:\n")
        for i, r in enumerate(strong, 1):
            f.write(f"{i}. {r['code']} 收盘{r['close']:.2f} 涨幅{r['pct_chg']:.2f}% 评分{r['score']}\n")
        
        f.write(f"\n及格:\n")
        for i, r in enumerate(all_q, 1):
            f.write(f"{i}. {r['code']} 收盘{r['close']:.2f} 涨幅{r['pct_chg']:.2f}% 评分{r['score']}\n")
        
        print(f"\n✅ 结果已保存到: {output_dir}/选股结果_{trade_date}.txt")

if __name__ == "__main__":
    main()
