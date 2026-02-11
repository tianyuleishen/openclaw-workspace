#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国股市分析模块 v1.0
分析A股、港股、美股中概股
"""

from typing import Dict, List
from datetime import datetime


class ChinaStockAnalyzer:
    def __init__(self):
        self.version = "1.0"
        
        # 中国股市核心知识
        self.knowledge = {
            # 主要指数
            "index_shanghai": """上证指数 (SSE Composite Index):
代码: sh000001
范围: 上海交易所全部A股
特点: 反映上海市场整体表现
市盈率: 约13-15倍 (历史均值)

编制方法: 市值加权平均
权重股: 茅台、工商银行、中石油等""",
            
            "index_shenzhen": """深证成指 (SZSE Component Index):
代码: sz399001
范围: 深圳交易所500家大盘股
特点: 反映深圳市场大盘股表现
行业分布: 电子、医药、新能源为主""",
            
            "index_chi_next": """创业板指 (ChiNext Index):
代码: sz399006
范围: 创业板100家大盘股
特点: 反映创新型企业
市值: 较小但成长性高
风险: 波动较大""",
            
            "index_star": """科创50指数:
代码: sh000688
范围: 科创板前50大市值股
特点: 反映科技创新企业
行业: 半导体、生物医药、高端制造""",
            
            "index_hk": """恒生指数 (Hang Seng Index):
代码: hkHSI
范围: 香港交易所50家大盘股
特点: 反映香港市场整体表现
权重股: 腾讯、阿里巴巴、美团等""",
            
            "index_nasdaq_china": """纳斯达克中国概念股:
代码: NASDAQ: BABA, JD, PDD, BIDU
特点: 中国科技股在美上市
估值: 通常高于A股同类公司""",
            
            # A股特点
            "a_share_features": """A股市场特点:

1. 散户为主
   - 散户占比约60-70%
   - 交易量贡献80%+
   - 情绪波动大

2. T+1交易
   - 当日买入，次日才能卖出
   - 防止过度投机

3. 涨跌停板
   - 普通股: ±10%
   - ST股: ±5%
   - 新股上市首日: ±44%

4. 政策影响大
   - 证监会政策
   - 央行货币政策
   - 财政政策
   - 国家队干预""",
            
            "a_share_investors": """A股投资者结构:

1. 散户 (约60-70%)
   - 平均持股周期短
   - 追涨杀跌
   - 消息面敏感

2. 机构 (约30%)
   - 公募基金
   - 私募基金
   - 社保基金
   - 保险资金
   - 国家队

3. 外资 (约5%)
   - QFII/RQFII
   - 北向资金
   - 沪深港通""",
            
            "market_cycles": """A股牛熊周期:

1. 2007年大牛市
   - 背景: 经济高速增长+股权分置改革
   - 顶点: 6124点
   - 原因: 估值泡沫+政策调控

2. 2015年杠杆牛
   - 背景: 杠杆资金大量入市
   - 顶点: 5178点
   - 原因: 场外配资+清理杠杆

3. 2019-2021结构性牛
   - 背景: 外资流入+基金抱团
   - 特点: 核心资产大涨
   - 赛道: 消费、医药、新能源

4. 2024年复苏
   - 背景: 经济复苏预期
   - 政策: 新国九条+科技政策
   - 机会: AI、新质生产力""",
            
            "policy_analysis": """中国股市政策框架:

1. 证监会政策
   - IPO注册制改革
   - 退市制度完善
   - 信息披露监管

2. 货币政策
   - 利率水平
   - 存款准备金率
   - 流动性投放

3. 财政政策
   - 税收优惠
   - 产业补贴
   - 基建投资

4. 国家队干预
   - 社保基金
   - 证金公司
   - 外汇局投资

5. 国际政策
   - MSCI纳入因子
   - 沪深港通
   - QFII额度""",
            
            "sector_analysis": """A股热门板块分析:

1. 新能源
   - 宁德时代 (300750.SZ)
   - 比亚迪 (002594.SZ)
   - 隆基绿能 (601012.SH)
   - 逻辑: 碳中和+政策支持

2. 半导体
   - 中芯国际 (688981.SH)
   - 北方华创 (002371.SZ)
   - 海光信息 (688041.SH)
   - 逻辑: 国产替代+AI需求

3. 消费
   - 贵州茅台 (600519.SH)
   - 五粮液 (000858.SZ)
   - 海尔智家 (600690.SH)
   - 逻辑: 消费升级+品牌价值

4. 医药
   - 药明康德 (603259.SH)
   - 恒瑞医药 (600276.SH)
   - 创新药+老龄化逻辑

5. AI/科技
   - 科大讯飞 (002230.SZ)
   - 海康威视 (002415.SZ)
   - 逻辑: 政策支持+技术突破""",
            
            "valuation_methods": """A股估值方法:

1. PE (市盈率)
   - 历史均值: 13-15倍
   - 当前区间: 10-20倍
   - 低估: <10倍
   - 高估: >20倍

2. PB (市净率)
   - 历史均值: 1.5-2倍
   - 银行股: 0.5-1倍 (破净)
   - 成长股: 3-5倍

3. 股息率
   - 银行股: 5-7%
   - 公用事业: 3-4%
   - 高分红策略有效

4. 估值指标
   - 股债性价比 (ERP)
   - 风险溢价
   - 市场情绪指标""",
            
            "trading_tips": """A股投资策略:

1. 长期投资
   - 持有优质白马股
   - 享受分红+成长
   - 忽略短期波动

2. 价值投资
   - 低PE/PB买入
   - 高分红股票
   - 逆向投资

3. 趋势投资
   - 跟随主力资金
   - 关注板块轮动
   - 设置止损

4. 政策套利
   - 关注政策方向
   - 提前布局受益行业
   - 政策出台后获利了结

5. 风险控制
   - 分散投资
   - 设置止损
   - 控制仓位
   - 避免杠杆""",
            
            "hong_kong": """港股市场特点:

1. 成熟市场
   - 机构为主
   - 估值偏低
   - 流动性一般

2. 独特优势
   - 接轨国际
   - 汇率优势
   - 科技股回归

3. 风险因素
   - 流动性折价
   - 地缘政治
   - 汇率波动

4. 主要指数
   - 恒生指数 (HSI)
   - 恒生科技指数
   - 国企指数 (H股)""",
            
            "us_china_concepts": """中概股分析:

1. 主要公司
   - 阿里巴巴 (BABA)
   - 京东 (JD)
   - 拼多多 (PDD)
   - 百度 (BIDU)
   - 蔚来 (NIO)
   - 小鹏 (XPEV)

2. 投资逻辑
   - 业务在中国
   - 估值受政策影响
   - ADR交易便捷

3. 风险因素
   - 退市风险
   - 审计问题
   - 中美关系""",
        }
        
        # 量化指标库
        self.metrics = {
            "shpe": "上证PE: 13.2倍 (截至2024)",
            "hkpe": "恒生PE: 9.8倍 (全球最低)",
            "a_shares": "A股总市值: 约80万亿人民币",
            "hk_market": "港股总市值: 约30万亿港币",
            "north_money": "北向资金: 单日流入100亿+",
            "margin_trading": "两融余额: 约1.5万亿",
        }
    
    def analyze_market(self, market: str = "a_share") -> Dict:
        """分析市场"""
        if market in ["a_share", "a股", "A股"]:
            return {
                "type": "market_analysis",
                "market": "A股",
                "summary": self.knowledge["a_share_features"],
                "investors": self.knowledge["a_share_investors"],
                "cycles": self.knowledge["market_cycles"],
                "confidence": 0.85
            }
        elif market in ["hk", "港股", "恒生"]:
            return {
                "type": "market_analysis", 
                "market": "港股",
                "summary": self.knowledge["hong_kong"],
                "confidence": 0.85
            }
        elif market in ["us_china", "中概股", "ADR"]:
            return {
                "type": "market_analysis",
                "market": "中概股", 
                "summary": self.knowledge["us_china_concepts"],
                "confidence": 0.85
            }
        else:
            return {
                "type": "market_analysis",
                "market": "A股/港股/中概股",
                "features": self.knowledge["a_share_features"],
                "confidence": 0.80
            }
    
    def analyze_sector(self, sector: str) -> Dict:
        """分析板块"""
        if sector in ["新能源", "光伏", "锂电"]:
            return {
                "type": "sector_analysis",
                "sector": sector,
                "key_stocks": ["宁德时代", "比亚迪", "隆基绿能"],
                "logic": "碳中和+政策支持",
                "confidence": 0.85
            }
        elif sector in ["半导体", "芯片", "AI"]:
            return {
                "type": "sector_analysis",
                "sector": sector,
                "key_stocks": ["中芯国际", "北方华创", "海光信息"],
                "logic": "国产替代+AI需求",
                "confidence": 0.85
            }
        elif sector in ["消费", "白酒", "食品"]:
            return {
                "type": "sector_analysis",
                "sector": sector,
                "key_stocks": ["茅台", "五粮液", "海天味业"],
                "logic": "消费升级+品牌价值",
                "confidence": 0.85
            }
        elif sector in ["医药", "医疗", "创新药"]:
            return {
                "type": "sector_analysis", 
                "sector": sector,
                "key_stocks": ["药明康德", "恒瑞医药", "百济神州"],
                "logic": "老龄化+创新驱动",
                "confidence": 0.85
            }
        else:
            return {
                "type": "sector_analysis",
                "sector": sector,
                "info": self.knowledge.get("sector_analysis", "请指定具体板块"),
                "confidence": 0.70
            }
    
    def get_market_metrics(self) -> Dict:
        """获取市场指标"""
        return {
            "metrics": self.metrics,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "note": "数据仅供参考，不构成投资建议"
        }
    
    def answer_question(self, question: str) -> Dict:
        """回答问题"""
        q = question.lower()
        
        # 市场分析
        if any(kw in q for kw in ["a股", "a_share", "a股市场", "上证", "深证", "创业板"]):
            return self.analyze_market("a_share")
        
        if any(kw in q for kw in ["港股", "恒生", "hk"]):
            return self.analyze_market("hk")
        
        if any(kw in q for kw in ["中概股", "adr", "美股中国"]):
            return self.analyze_market("us_china")
        
        # 板块分析
        if any(kw in q for kw in ["新能源", "光伏", "锂电", "电动车"]):
            return self.analyze_sector("新能源")
        
        if any(kw in q for kw in ["半导体", "芯片", "ai", "人工智能"]):
            return self.analyze_sector("半导体")
        
        if any(kw in q for kw in ["消费", "白酒", "食品"]):
            return self.analyze_sector("消费")
        
        if any(kw in q for kw in ["医药", "医疗", "创新药"]):
            return self.analyze_sector("医药")
        
        # 估值
        if any(kw in q for kw in ["估值", "pe", "市盈率", "pb"]):
            return {
                "type": "valuation",
                "info": self.knowledge["valuation_methods"],
                "metrics": self.metrics,
                "confidence": 0.85
            }
        
        # 政策
        if any(kw in q for kw in ["政策", "证监会", "国家队"]):
            return {
                "type": "policy",
                "info": self.knowledge["policy_analysis"],
                "confidence": 0.85
            }
        
        # 投资策略
        if any(kw in q for kw in ["投资策略", "怎么投资", "如何选股"]):
            return {
                "type": "strategy",
                "info": self.knowledge["trading_tips"],
                "confidence": 0.85
            }
        
        # 指数
        if any(kw in q for kw in ["上证指数", "深证成指", "创业板指", "科创50", "恒生指数"]):
            return self.analyze_index(q)
        
        # 默认返回A股概述
        return self.analyze_market("a_share")
    
    def analyze_index(self, question: str) -> Dict:
        """分析指数"""
        q = question.lower()
        
        if "上证" in q:
            return {
                "type": "index_analysis",
                "index": "上证指数",
                "info": self.knowledge["index_shanghai"],
                "confidence": 0.85
            }
        elif "深证" in q:
            return {
                "type": "index_analysis",
                "index": "深证成指", 
                "info": self.knowledge["index_shenzhen"],
                "confidence": 0.85
            elif "创业板" in q:
            return {
                "type": "index_analysis",
                "index": "创业板指",
                "info": self.knowledge["index_chi_next"],
                "confidence": 0.85
            }
        elif "科创" in q:
            return {
                "type": "index_analysis",
                "index": "科创50",
                "info": self.knowledge["index_star"],
                "confidence": 0.85
            }
        elif "恒生" in q:
            return {
                "type": "index_analysis",
                "index": "恒生指数",
                "info": self.knowledge["index_hk"],
                "confidence": 0.85
            }
        else:
            return {
                "type": "index_analysis",
                "index": "主要指数",
                "info": "请指定具体指数",
                "confidence": 0.50
            }


if __name__ == "__main__":
    analyzer = ChinaStockAnalyzer()
    
    print("="*80)
    print("中国股市分析模块 v1.0")
    print("="*80)
    
    questions = [
        "分析A股市场",
        "港股有什么特点？",
        "新能源板块怎么样？",
        "当前估值水平如何？",
        "上证指数现在多少点？",
    ]
    
    for q in questions:
        print(f"\n问题: {q}")
        result = analyzer.answer_question(q)
        print(f"类型: {result['type']}")
        print(f"置信度: {result['confidence']*100:.0f}%")
    
    print("\n" + "="*80)
    print("市场指标:")
    print(analyzer.get_market_metrics()["metrics"])
    print("="*80)
