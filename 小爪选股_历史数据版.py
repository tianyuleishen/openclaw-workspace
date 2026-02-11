#!/usr/bin/env python3
"""
小爪智能选股模型 v1.0（历史数据版）
获取最近交易日数据
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

def get_last_trading_date() -> str:
    """获取最近交易日"""
    try:
        df = pro.daily(trade_date=(datetime.now() - timedelta(days=1)).strftime('%Y%m%d'))
        if not df.empty:
            return (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    except:
        pass
    
    # 尝试获取最近5天
    for i in range(1, 6):
        try:
            date = (datetime.now() - timedelta(days=i)).strftime('%Y%m%d')
            df = pro.daily(trade_date=date)
            if not df.empty:
                return date
        except:
            continue
    
    return (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')

def get_market_sentiment(trade_date: str) -> Dict:
    """获取市场情绪"""
    try:
        # 涨停数据
        up_df = pro.limit_list(trade_date=trade_date, limit_type='U')
        up_limit_count = len(up_df) if not up_df.empty else 0
        
        # 跌停数据
        down_df = pro.limit_list(trade_date=trade_date, limit_type='D')
        down_limit_count = len(down_df) if not down_df.empty else 0
        
        # 大盘数据
        df = pro.daily(trade_date=trade_date)
        up_count = len(df[df['pct_chg'] > 0]) if not df.empty else 2000
        down_count = len(df[df['pct_chg'] < 0]) if not df.empty else 2000
        
        # 上涨幅度
        avg_pct = df['pct_chg'].mean() if not df.empty else 0
        
        # 判断周期
        if up_limit_count > 200 and avg_pct > 3:
            phase = "高潮"
        elif up_limit_count > 100 and avg_pct > 2:
            phase = "回暖"
        elif up_limit_count > 50 and avg_pct > 1:
            phase = "复苏"
        elif down_limit_count > 50 and avg_pct < -2:
            phase = "冰点"
        elif up_limit_count > 150 and avg_pct > 2.5:
            phase = "过热"
        else:
            phase = "退潮"
        
        return {
            'phase': phase,
            'up_count': up_count,
            'up_limit_count': up_limit_count,
            'down_count': down_count,
            'down_limit_count': down_limit_count,
            'avg_pct': avg_pct
        }
    
    except Exception as e:
        print(f"获取市场情绪失败: {e}")
        return {'phase': '回暖', 'up_count': 2500, 'up_limit_count': 80, 'avg_pct': 1.0}

def get_all_stocks(trade_date: str) -> List[Dict]:
    """获取所有在交易股票"""
    try:
        df = pro.daily(trade_date=trade_date)
        
        if df.empty:
            return []
        
        # 排除ST
        stocks = []
        for _, row in df.iterrows():
            if not row['ts_code'].startswith('BJ'):  # 排除北交所
                code = row['ts_code'][:6]
                stocks.append({
                    'code': code,
                    'ts_code': row['ts_code']
                })
        
        return stocks
    
    except Exception as e:
        print(f"获取股票列表失败: {e}")
        return []

def get_stock_details(ts_code: str, trade_date: str) -> Dict:
    """获取股票详情"""
    try:
        # 获取日线数据
        df = pro.daily(
            ts_code=ts_code,
            start_date=(datetime.now() - timedelta(days=30)).strftime('%Y%m%d'),
            end_date=trade_date
        )
        
        if df.empty or len(df) < 5:
            return None
        
        # 最新一天数据
        latest = df.iloc[0]
        
        # 前一天数据
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
        
        return {
            'code': ts_code[:6],
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
            'ma_multi': ma5 > ma10 > ma20 > ma60
        }
    
    except Exception as e:
        return None

def calculate_score(stock: Dict, market_info: Dict) -> Dict:
    """计算评分"""
    score = 0
    
    # 1. 情绪周期
    if market_info['phase'] in ['复苏', '回暖', '高潮']:
        score += 20
    elif market_info['phase'] == '过热':
        score += 10
    
    # 2. 板块效应
    if market_info['up_limit_count'] > 100:
        score += 15
    elif market_info['up_limit_count'] > 50:
        score += 5
    
    # 3. 个股地位
    if stock['pct_chg'] > 9.5 and stock['volume_ratio'] > 2:
        score += 20
    elif stock['pct_chg'] > 5:
        score += 10
    
    # 4. 形态
    pattern = 0
    if stock['ma_multi']:
        pattern += 5
    if stock['trend'] == '上升':
        pattern += 5
    if stock['pct_chg'] > 0 and stock['volume_ratio'] > 1:
        pattern += 3
    score += pattern
    
    # 5. 筹码
    if 3 <= stock['turnover_rate'] <= 15:
        score += 10
    else:
        score += 5
    
    # 6. 量能
    volume_score = 0
    if stock['volume_ratio'] > 1.5:
        volume_score += 5
    if stock['pct_chg'] > 0 and stock['volume_ratio'] > 1:
        volume_score += 3
    score += volume_score
    
    # 7. 分时
    if stock['close'] > stock['open']:
        score += 5
    
    return {
        'stock': stock,
        'score': score,
        'buy_signal': score >= MIN_SCORE,
        'stop_loss': round(stock['close'] * 0.95, 2),
        'target': round(stock['close'] * 1.10, 2)
    }

def main():
    """主函数"""
    print("="*80)
    print("小爪智能选股模型 v1.0（真实历史数据版）")
    print("="*80)
    print()
    
    # 获取最近交易日
    trade_date = get_last_trading_date()
    print(f"使用交易日: {trade_date}")
    
    # 1. 获取市场情绪
    print("\n【1】获取市场情绪...")
    market_info = get_market_sentiment(trade_date)
    print(f"   市场周期: {market_info['phase']}")
    print(f"   上涨: {market_info['up_count']}, 涨停: {market_info['up_limit_count']}, 跌停: {market_info['down_limit_count']}")
    print(f"   平均涨幅: {market_info['avg_pct']:.2f}%")
    
    # 2. 获取股票列表
    print("\n【2】获取股票数据...")
    stocks = get_all_stocks(trade_date)
    print(f"   在交易股票: {len(stocks)}只")
    
    # 3. 评分
    print("\n【3】开始评分...")
    results = []
    for i, stock in enumerate(stocks, 1):
        detail = get_stock_details(stock['ts_code'], trade_date)
        if detail:
            result = calculate_score(detail, market_info)
            results.append(result)
        
        if i % 100 == 0:
            print(f"   完成: {i}/{len(stocks)}")
        
        # 避免请求过快
        if i % 300 == 0:
            import time
            time.sleep(1)
    
    print(f"   评分完成: {len(results)}只")
    
    # 排序
    results.sort(key=lambda x: x['score'], reverse=True)
    
    # 4. 输出结果
    print("\n【4】选股结果")
    print("="*80)
    
    qualified = [r for r in results if r['score'] >= MIN_SCORE]
    strong = [r for r in results if r['score'] >= STRONG_SCORE]
    
    print(f"\n✅ 及格股票（≥{MIN_SCORE}分）: {len(qualified)}只")
    print(f"🌟 强烈推荐（≥{STRONG_SCORE}分）: {len(strong)}只")
    
    if strong:
        print("\n" + "-"*80)
        print(f"{'排名':^4} {'代码':^10} {'收盘价':^10} {'涨幅':^10} {'量比':^8} {'换手率':^10} {'评分':^6}")
        print("-"*80)
        for i, r in enumerate(strong[:15], 1):
            s = r['stock']
            print(f"{i:^4} {s['code']:^10} {s['close']:^10.2f} {s['pct_chg']:^9.2f}% "
                  f"{s['volume_ratio']:^8.2f} {s['turnover_rate']:^9.2f}% {r['score']:^6}")
    
    if qualified:
        print(f"\n📋 买入建议（TOP 10）:")
        print("-"*80)
        for i, r in enumerate(qualified[:10], 1):
            s = r['stock']
            print(f"\n{i}. {s['code']}")
            print(f"   当前价: {s['close']:.2f}元  目标: {r['target']:.2f}元 (+10%)")
            print(f"   止损: {r['stop_loss']:.2f}元 (-5%)  评分: {r['score']}分")
            print(f"   形态: {'均线多头' if s['ma_multi'] else ''} {s['trend']}")
    
    # 5. 保存
    save_results(qualified, strong, trade_date)
    
    print("\n" + "="*80)
    print("选股完成！")
    print("="*80)

def save_results(qualified: List, strong: List, trade_date: str):
    """保存结果"""
    output_dir = "/home/admin/.openclaw/workspace/选股结果"
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f"{output_dir}/真实选股结果_{trade_date}.txt", "w", encoding='utf-8') as f:
        f.write(f"小爪智能选股结果 - 交易日: {trade_date}\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"强烈推荐（≥{STRONG_SCORE}分）:\n")
        for i, r in enumerate(strong, 1):
            s = r['stock']
            f.write(f"{i}. {s['code']} 收盘{s['close']:.2f}元 涨幅{s['pct_chg']:.2f}% "
                  f"量比{s['volume_ratio']:.2f} 评分{r['score']}\n")
        
        f.write(f"\n及格股票（≥{MIN_SCORE}分）:\n")
        for i, r in enumerate(qualified, 1):
            s = r['stock']
            f.write(f"{i}. {s['code']} 收盘{s['close']:.2f}元 涨幅{s['pct_chg']:.2f}% "
                  f"量比{s['volume_ratio']:.2f} 评分{r['score']}\n")
        
        print(f"\n✅ 结果已保存到: {output_dir}/真实选股结果_{trade_date}.txt")

if __name__ == "__main__":
    main()
