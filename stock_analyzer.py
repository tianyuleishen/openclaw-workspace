#!/usr/bin/env python3
"""
A股涨停股票分析器
使用AI多因子模型分析涨停股票
"""

import json
from datetime import datetime
from typing import Dict, List

class StockAnalyzer:
    """股票分析器"""
    
    def __init__(self):
        self.factors = {
            "momentum": "动量因子",
            "value": "价值因子",
            "quality": "质量因子",
            "volatility": "波动率因子",
            "liquidity": "流动性因子",
            "sentiment": "情绪因子"
        }
        
        # 模拟今日涨停股票数据（扩展版）
        self.limit_up_stocks = [
            # 大盘蓝筹
            {"code": "000001", "name": "平安银行", "pct_chg": 10.05, "industry": "银行", "turnover": 2.5},
            {"code": "600519", "name": "贵州茅台", "pct_chg": 5.23, "industry": "白酒", "turnover": 1.8},
            {"code": "000002", "name": "万  科Ａ", "pct_chg": 9.87, "industry": "房地产", "turnover": 3.2},
            {"code": "600036", "name": "招商银行", "pct_chg": 6.54, "industry": "银行", "turnover": 2.1},
            {"code": "600050", "name": "中国联通", "pct_chg": 8.65, "industry": "通信", "turnover": 3.8},
            {"code": "600900", "name": "长江电力", "pct_chg": 3.21, "industry": "电力", "turnover": 1.2},
            {"code": "000009", "name": "中国石化", "pct_chg": 7.89, "industry": "石油石化", "turnover": 1.5},
            
            # 涨停板（按行业分类）
            {"code": "000012", "name": "南  玻Ａ", "pct_chg": 10.02, "industry": "玻璃", "turnover": 4.5},
            {"code": "600884", "name": "杉杉股份", "pct_chg": 9.98, "industry": "新能源", "turnover": 3.8},
            {"code": "002594", "name": "比亚迪", "pct_chg": 5.65, "industry": "汽车", "turnover": 2.3},
            {"code": "000725", "name": "京东方A", "pct_chg": 10.11, "industry": "电子", "turnover": 5.2},
            {"code": "600703", "name": "三安光电", "pct_chg": 8.92, "industry": "半导体", "turnover": 3.1},
            {"code": "002475", "name": "立讯精密", "pct_chg": 7.45, "industry": "电子", "turnover": 2.8},
            {"code": "000063", "name": "中兴通讯", "pct_chg": 9.23, "industry": "通信", "turnover": 4.1},
            {"code": "600522", "name": "中天科技", "pct_chg": 10.05, "industry": "通信", "turnover": 3.6},
            
            # 创业板/科创板
            {"code": "300750", "name": "宁德时代", "pct_chg": 4.89, "industry": "新能源", "turnover": 1.5},
            {"code": "300498", "name": "温氏股份", "pct_chg": 8.76, "industry": "农业", "turnover": 2.9},
            {"code": "300015", "name": "爱尔眼科", "pct_chg": 6.54, "industry": "医疗", "turnover": 1.8},
            {"code": "688981", "name": "中芯国际", "pct_chg": 7.89, "industry": "半导体", "turnover": 4.5},
            {"code": "688349", "name": "国巨航发", "pct_chg": 10.15, "industry": "军工", "turnover": 6.2},
            
            # 题材热点
            {"code": "600839", "name": "四川长虹", "pct_chg": 9.45, "industry": "家电", "turnover": 3.2},
            {"code": "000158", "name": "常山北明", "pct_chg": 10.08, "industry": "软件", "turnover": 5.8},
            {"code": "002410", "name": "广联达", "pct_chg": 8.32, "industry": "软件", "turnover": 2.1},
            {"code": "300059", "name": "东方财富", "pct_chg": 7.65, "industry": "金融", "turnover": 3.4},
            {"code": "002230", "name": "科大讯飞", "pct_chg": 9.12, "industry": "AI", "turnover": 4.2},
            {"code": "000977", "name": "浪潮信息", "pct_chg": 8.76, "industry": "AI", "turnover": 3.8},
            {"code": "600850", "name": "华东医药", "pct_chg": 6.54, "industry": "医药", "turnover": 1.9},
            {"code": "000538", "name": "云南白药", "pct_chg": 5.89, "industry": "医药", "turnover": 1.5},
            {"code": "600809", "name": "山西汾酒", "pct_chg": 7.23, "industry": "白酒", "turnover": 2.2},
            {"code": "000799", "name": "酒鬼酒", "pct_chg": 10.05, "industry": "白酒", "turnover": 4.5},
            
            #ST板块（警示）
            {"code": "000666", "name": "中工国际", "pct_chg": 10.18, "industry": "建筑", "turnover": 7.5},
        ]
    
    def analyze_stock(self, stock: Dict) -> Dict:
        """分析单只股票"""
        code = stock.get("code", "")
        name = stock.get("name", "")
        
        # 模拟AI多因子评分
        scores = {
            "momentum": min(100, max(0, 70 + (stock.get("pct_chg", 0) * 2))),
            "value": min(100, max(0, 75 - stock.get("turnover", 0))),
            "quality": min(100, max(0, 80 - abs(stock.get("pct_chg", 0) - 5) * 3)),
            "volatility": min(100, max(0, 90 - stock.get("turnover", 0) * 5)),
            "liquidity": min(100, max(0, stock.get("turnover", 0) * 30)),
            "sentiment": min(100, max(0, 85 + stock.get("pct_chg", 0))),
        }
        
        # 综合评分
        total_score = sum(scores.values()) / len(scores)
        
        # 风险评估
        risk_level = "低"
        if stock.get("turnover", 0) > 4:
            risk_level = "高"
        elif stock.get("turnover", 0) > 2:
            risk_level = "中"
        
        return {
            "code": code,
            "name": name,
            "scores": scores,
            "total_score": round(total_score, 2),
            "risk_level": risk_level,
            "recommendation": self._get_recommendation(total_score, risk_level),
            "analysis_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def _get_recommendation(self, score: float, risk: str) -> str:
        """获取推荐"""
        if score >= 80 and risk == "低":
            return "⭐⭐⭐ 强烈推荐"
        elif score >= 70:
            return "⭐⭐ 建议关注"
        elif score >= 60:
            return "⭐ 谨慎关注"
        else:
            return "⚠️ 建议观望"
    
    def analyze_all(self) -> List[Dict]:
        """分析所有涨停股票"""
        results = []
        for stock in self.limit_up_stocks:
            analysis = self.analyze_stock(stock)
            results.append(analysis)
        return results
    
    def generate_report(self) -> str:
        """生成分析报告"""
        results = self.analyze_all()
        
        report = []
        report.append("=" * 80)
        report.append("📈 A股涨停股票AI分析报告")
        report.append(f"📅 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append(f"📊 涨停数量: {len(results)} 只")
        report.append("=" * 80)
        report.append("")
        
        # 按综合评分排序
        sorted_results = sorted(results, key=lambda x: x["total_score"], reverse=True)
        
        for i, stock in enumerate(sorted_results, 1):
            report.append(f"【{i}】{stock['name']} ({stock['code']})")
            report.append(f"    涨跌幅: +{stock.get('pct_chg', 0):.2f}%")
            report.append(f"    综合评分: {stock['total_score']} 分")
            report.append(f"    风险等级: {stock['risk_level']}")
            report.append(f"    推荐: {stock['recommendation']}")
            report.append("")
            report.append("    因子得分:")
            for factor, name in self.factors.items():
                score = stock["scores"].get(factor, 0)
                bar = "█" * int(score / 10) + "░" * (10 - int(score / 10))
                report.append(f"      {name}: {bar} {score:.1f}")
            report.append("")
            report.append("-" * 80)
            report.append("")
        
        # 总结
        report.append("📋 分析总结:")
        top3 = sorted_results[:3]
        report.append(f"  推荐关注 TOP3:")
        for i, stock in enumerate(top3, 1):
            report.append(f"    {i}. {stock['name']} ({stock['code']}) - {stock['total_score']}分")
        
        report.append("")
        report.append("💡 风险提示:")
        high_risk = [s for s in results if s["risk_level"] == "高"]
        if high_risk:
            report.append(f"  警示股票: {[s['name'] for s in high_risk]}")
        report.append("  ⚠️ 仅供参考，不构成投资建议")
        
        return "\n".join(report)


def main():
    print("=" * 80)
    print("                📈 A股涨停股票AI分析")
    print("=" * 80)
    print()
    
    analyzer = StockAnalyzer()
    
    # 生成报告
    report = analyzer.generate_report()
    print(report)
    
    # 保存报告
    filename = f"stock_analysis_{datetime.now().strftime('%Y%m%d')}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ 报告已保存: {filename}")


if __name__ == "__main__":
    main()
