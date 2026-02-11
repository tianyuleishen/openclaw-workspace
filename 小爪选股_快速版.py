#!/usr/bin/env python3
"""
小爪智能选股模型 v1.0（精简版）
快速获取真实数据，选股演示
"""

import tushare as ts
from datetime import datetime, timedelta
from typing import List, Dict
import os

# 配置Token
TOKEN = "YOUR_TUSHARE_TOKEN"

# 初始化
ts.set_token(TOKEN)
pro = ts.pro_api()

# 评分参数
MIN_SCORE = 60
STRONG_SCORE = 75

def get_market_sentiment():
    """获取市场情绪"""
    today = datetime.now().strftime('%Y%m%d')
    
    try:
        # 涨停数据
        up_df = pro.limit_list(trade_date=today, limit_type='U')
        up_limit_count = len(up_df) if not up_df.empty else 0
        
        # 跌停数据
        down_df = pro.limit_list(trade_date=today, limit_type='D')
        down_limit_count = len(down_df) if not down_df.empty else 0
        
        # 大盘数据
        df = pro.daily(trade_date=today)
        up_count = len(df[df['pct_chg'] > 0]) if not df.empty else 2000
        down_count = len(df[df['pct_chg'] < 0]) if not df.empty else 2000
        
        # 判断周期
        if up_limit_count > 200 and up_count > 3500:
            phase = "高潮"
        elif up_limit_count > 100 and up_count > 3000:
            phase = "回暖"
        elif up_limit_count > 50 and up_count > 2500:
            phase = "复苏"
        elif down_limit_count > 50 and up_count < 1500:
            phase = "冰点"
        elif up_limit_count > 150 and up_count > 3200:
            phase = "过热"
        else:
            phase = "退潮"
        
        return phase, up_count, up_limit_count, down_count, down_limit_count
    
    except Exception as e:
        print(f"获取市场数据失败: {e}")
        return "回暖", 2500, 80, 1500, 20

def get_hot_stocks(count: int = 50) -> List[Dict]:
    """获取热门股票（涨幅榜）"""
    try:
        today = datetime.now().strftime('%Y%m%d')
        df = pro.daily(trade_date=today)
        
        if df.empty:
            # 如果今日数据为空，获取昨日数据
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
            df = pro.daily(trade_date=yesterday)
        
        # 排除ST和新股，按涨跌幅排序
        df = df[~df['ts_code'].str.contains('ST|N|')]
        df = df.sort_values('pct_chg', ascending=False)
        
        stocks = []
        for _, row in df.head(count).iterrows():
            code = row['ts_code'][:6]
            stocks.append({
                'code': code,
                'name': code  # 简化处理
            })
        
        return stocks
    
    except Exception as e:
        print(f"获取热门股票失败: {e}")
        return []

def get_stock_details(code: str) -> Dict:
    """获取股票详情"""
    try:
        # 获取日线数据
        df = pro.daily(
            ts_code=f"{code}.SZ" if code.startswith(('0','3')) else f"{code}.SH",
            start_date=(datetime.now() - timedelta(days=20)).strftime('%Y%m%d'),
            end_date=datetime.now().strftime('%Y%m%d')
        )
        
        if df.empty:
            return None
        
        latest = df.iloc[0]
        prev = df.iloc[1] if len(df) > 1 else latest
        
        # 计算均线
        closes = df['close'].tolist()
        ma5 = sum(closes[:5]) / 5 if len(closes) >= 5 else closes[0]
        ma10 = sum(closes[:10]) / 10 if len(closes) >= 10 else closes[0]
        ma20 = sum(closes[:20]) / 20 if len(closes) >= 20 else closes[0]
        ma60 = sum(closes[:60]) / 60 if len(closes) >= 60 else closes[0]
        
        # 计算量比
        avg_vol = df['vol'].iloc[1:6].mean() if len(df) > 5 else latest['vol']
        volume_ratio = latest['vol'] / avg_vol if avg_vol > 0 else 1.0
        
        # 趋势判断
        if ma5 > ma10 > ma20 > ma60:
            trend = "上升"
        elif ma5 < ma10 < ma20 < ma60:
            trend = "下降"
        else:
            trend = "震荡"
        
        # 均线多头
        ma_multi = ma5 > ma10 > ma20 > ma60
        
        return {
            'code': code,
            'close': latest['close'],
            'open': latest['open'],
            'high': latest['high'],
            'low': latest['low'],
            'pct_chg': latest['pct_chg'],
            'volume_ratio': volume_ratio,
            'turnover_rate': latest['turnover_rate'],
            'ma5': ma5,
            'ma10': ma10,
            'ma20': ma20,
            'ma60': ma60,
            'trend': trend,
            'ma_multi': ma_multi
        }
    
    except Exception as e:
        return None

def calculate_score(stock: Dict, market_info: Dict) -> Dict:
    """计算评分"""
    score = 0
    breakdown = {}
    
    # 1. 情绪周期
    if market_info['phase'] in ['复苏', '回暖', '高潮']:
        score += 20
    elif market_info['phase'] == '过热':
        score += 10
    breakdown['情绪'] = 20 if market_info['phase'] in ['复苏', '回暖', '高潮'] else 10 if market_info['phase'] == '过热' else 0
    
    # 2. 板块效应
    if market_info['up_limit_count'] > 100:
        score += 15
    elif market_info['up_limit_count'] > 50:
        score += 5
    breakdown['板块'] = 15 if market_info['up_limit_count'] > 100 else 5 if market_info['up_limit_count'] > 50 else 0
    
    # 3. 个股地位
    if stock['pct_chg'] > 9.5 and stock['volume_ratio'] > 2:
        score += 20
    elif stock['pct_chg'] > 5:
        score += 10
    breakdown['地位'] = 20 if stock['pct_chg'] > 9.5 and stock['volume_ratio'] > 2 else 10 if stock['pct_chg'] > 5 else 0
    
    # 4. 形态
    pattern = 0
    if stock['ma_multi']:
        pattern += 5
    if stock['trend'] == '上升':
        pattern += 5
    if stock['pct_chg'] > 0 and stock['volume_ratio'] > 1:
        pattern += 3
    score += pattern
    breakdown['形态'] = pattern
    
    # 5. 筹码
    if 3 <= stock['turnover_rate'] <= 15:
        score += 10
    else:
        score += 5
    breakdown['筹码'] = 10 if 3 <= stock['turnover_rate'] <= 15 else 5
    
    # 6. 量能
    volume_score = 0
    if stock['volume_ratio'] > 1.5:
        volume_score += 5
    if stock['pct_chg'] > 0 and stock['volume_ratio'] > 1:
        volume_score += 3
    score += volume_score
    breakdown['量能'] = volume_score
    
    # 7. 分时
    if stock['close'] > stock['open']:
        score += 5
    breakdown['分时'] = 5 if stock['close'] > stock['open'] else 0
    
    return {
        'stock': stock,
        'score': score,
        'breakdown': breakdown,
        'buy_signal': score >= MIN_SCORE,
        'stop_loss': round(stock['close'] * 0.95, 2),
        'target': round(stock['close'] * 1.10, 2)
    }

def main():
    """主函数"""
    print("="*80)
    print("小爪智能选股模型 v1.0（真实数据版）")
    print("="*80)
    print()
    
    # 1. 获取市场情绪
    print("【1】获取市场情绪...")
    phase, up_count, up_limit, down_count, down_limit = get_market_sentiment()
    market_info = {
        'phase': phase,
        'up_count': up_count,
        'up_limit_count': up_limit
    }
    print(f"   市场周期: {phase}")
    print(f"   上涨: {up_count}, 涨停: {up_limit}, 跌停: {down_limit}")
    print()
    
    # 2. 获取热门股票
    print("【2】获取热门股票...")
    stocks = get_hot_stocks(50)
    print(f"   热门股票: {len(stocks)}只")
    print()
    
    # 3. 评分
    print("【3】开始评分...")
    results = []
    for i, stock in enumerate(stocks, 1):
        detail = get_stock_details(stock['code'])
        if detail:
            result = calculate_score(detail, market_info)
            results.append(result)
        if i % 10 == 0:
            print(f"   完成: {i}/{len(stocks)}")
    
    # 排序
    results.sort(key=lambda x: x['score'], reverse=True)
    print(f"   评分完成: {len(results)}只")
    print()
    
    # 4. 输出结果
    print("【4】选股结果")
    print("="*80)
    
    qualified = [r for r in results if r['score'] >= MIN_SCORE]
    strong = [r for r in results if r['score'] >= STRONG_SCORE]
    
    print(f"\n✅ 及格股票（≥{MIN_SCORE}分）: {len(qualified)}只")
    print(f"🌟 强烈推荐（≥{STRONG_SCORE}分）: {len(strong)}只")
    
    if strong:
        print("\n" + "-"*80)
        print(f"{'排名':^4} {'代码':^10} {'收盘价':^10} {'涨幅':^10} {'量比':^8} {'评分':^6}")
        print("-"*80)
        for i, r in enumerate(strong[:10], 1):
            s = r['stock']
            print(f"{i:^4} {s['code']:^10} {s['close']:^10.2f} {s['pct_chg']:^9.2f}% {s['volume_ratio']:^8.2f} {r['score']:^6}")
    
    if qualified:
        print(f"\n📋 买入建议（TOP 5）:")
        print("-"*80)
        for i, r in enumerate(qualified[:5], 1):
            s = r['stock']
            print(f"\n{i}. {s['code']}")
            print(f"   当前价: {s['close']:.2f}元")
            print(f"   目标价: {r['target']:.2f}元 (+10%)")
            print(f"   止损价: {r['stop_loss']:.2f}元 (-5%)")
            print(f"   评分: {r['score']}分")
            print(f"   形态: {'均线多头' if s['ma_multi'] else ''} {s['trend']}")
    
    # 5. 保存结果
    save_results(qualified, strong)
    
    print("\n" + "="*80)
    print("选股完成！")
    print("="*80)

def save_results(qualified: List, strong: List):
    """保存结果"""
    import os
    output_dir = "/home/admin/.openclaw/workspace/选股结果"
    os.makedirs(output_dir, exist_ok=True)
    
    today = datetime.now().strftime('%Y%m%d')
    
    with open(f"{output_dir}/真实选股结果_{today}.txt", "w", encoding='utf-8') as f:
        f.write(f"小爪智能选股结果 - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"强烈推荐（≥{STRONG_SCORE}分）:\n")
        for i, r in enumerate(strong, 1):
            s = r['stock']
            f.write(f"{i}. {s['code']} - 评分{r['score']}分 - 收盘{s['close']:.2f}元 - 涨幅{s['pct_chg']:.2f}%\n")
        
        f.write(f"\n及格股票（≥{MIN_SCORE}分）:\n")
        for i, r in enumerate(qualified, 1):
            s = r['stock']
            f.write(f"{i}. {s['code']} - 评分{r['score']}分 - 收盘{s['close']:.2f}元 - 涨幅{s['pct_chg']:.2f}%\n")
        
        print(f"\n✅ 结果已保存到: {output_dir}/真实选股结果_{today}.txt")

if __name__ == "__main__":
    main()
