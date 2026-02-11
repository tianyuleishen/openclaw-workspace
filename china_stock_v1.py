#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国股市分析模块 v1.0
"""

class ChinaStockAnalyzer:
    def __init__(self):
        self.version = "1.0"
        self.knowledge = {
            # 市场特点
            "a_share_features": """A股市场特点:
1. 散户为主：占比60-70%，交易量80%+
2. T+1交易：当日买入，次日才能卖出
3. 涨跌停板：普通股±10%，ST股±5%
4. 政策影响大：证监会、央行、国家队干预""",
            
            # 投资者结构
            "investors": """A股投资者结构:
1. 散户(60-70%): 追涨杀跌，消息面敏感
2. 机构(30%): 公募、私募、社保、保险
3. 外资(5%): QFII、北向资金""",
            
            # 主要指数
            "shanghai": """上证指数 (sh000001):
- 上海交易所全部A股
- 市盈率: 13-15倍
- 权重股: 茅台、工商银行、中石油""",
            
            "shenzhen": """深证成指 (sz399001):
- 深圳500家大盘股
- 行业: 电子、医药、新能源""",
            
            "chi_next": """创业板指 (sz399006):
- 创新型企业
- 风险: 波动较大""",
            
            "star_50": """科创50 (sh000688):
- 科创板前50大市值股
- 行业: 半导体、生物医药、高端制造""",
            
            "hang_seng": """恒生指数 (hkHSI):
- 香港50家大盘股
- 腾讯、阿里巴巴、美团""",
            
            # 热门板块
            "new_energy": """新能源板块:
龙头股: 宁德时代、比亚迪、隆基绿能
投资逻辑: 碳中和+政策支持
风险: 产能过剩、价格战""",
            
            "semiconductor": """半导体板块:
龙头股: 中芯国际、北方华创、海光信息
投资逻辑: 国产替代+AI需求
风险: 技术封锁""",
            
            "consumer": """消费板块:
龙头股: 茅台、五粮液、海尔智家
投资逻辑: 消费升级+品牌价值
风险: 经济下行、消费降级""",
            
            "pharma": """医药板块:
龙头股: 药明康德、恒瑞医药、百济神州
投资逻辑: 老龄化+创新驱动
风险: 集采政策""",
            
            # 估值
            "valuation": """A股估值水平:
上证PE: 13.2倍 (历史均值13-15倍)
恒生PE: 9.8倍 (全球最低估值市场之一)
PB: 银行股破净 (0.5-1倍)
股息率: 银行股5-7%""",
            
            # 投资策略
            "strategy": """A股投资策略:
1. 长期投资: 持有优质白马股，享受分红+成长
2. 价值投资: 低PE/PB买入，高分红策略
3. 趋势投资: 跟随主力资金，关注板块轮动
4. 政策套利: 关注政策方向，提前布局""",
            
            # 风险提示
            "risks": """投资风险:
1. 市场波动大: 散户主导，情绪化严重
2. 政策风险: 监管政策变化
3. 结构风险: 板块轮动快
4. 流动性风险: 港股流动性折价
5. 地缘政治: 中美关系影响""",
        }
    
    def analyze(self, question: str) -> dict:
        q = question.lower()
        
        # A股市场
        if "a股" in q or "a_share" in q or "a股市场" in q:
            return {"type": "market", "answer": self.knowledge["a_share_features"] + "\n\n" + self.knowledge["investors"], "confidence": 0.85}
        
        # 指数
        if "上证" in q:
            return {"type": "index", "answer": self.knowledge["shanghai"], "confidence": 0.85}
        if "深证" in q:
            return {"type": "index", "answer": self.knowledge["shenzhen"], "confidence": 0.85}
        if "创业板" in q:
            return {"type": "index", "answer": self.knowledge["chi_next"], "confidence": 0.85}
        if "科创" in q:
            return {"type": "index", "answer": self.knowledge["star_50"], "confidence": 0.85}
        if "恒生" in q or "港股" in q:
            return {"type": "index", "answer": self.knowledge["hang_seng"], "confidence": 0.85}
        
        # 板块
        if "新能源" in q or "光伏" in q or "锂电" in q or "电动车" in q:
            return {"type": "sector", "answer": self.knowledge["new_energy"], "confidence": 0.85}
        if "半导体" in q or "芯片" in q or "ai" in q:
            return {"type": "sector", "answer": self.knowledge["semiconductor"], "confidence": 0.85}
        if "消费" in q or "白酒" in q:
            return {"type": "sector", "answer": self.knowledge["consumer"], "confidence": 0.85}
        if "医药" in q or "医疗" in q:
            return {"type": "sector", "answer": self.knowledge["pharma"], "confidence": 0.85}
        
        # 估值
        if "估值" in q or "pe" in q or "市盈率" in q:
            return {"type": "valuation", "answer": self.knowledge["valuation"], "confidence": 0.85}
        
        # 投资策略
        if "投资策略" in q or "怎么投资" in q or "如何选股" in q:
            return {"type": "strategy", "answer": self.knowledge["strategy"] + "\n\n" + self.knowledge["risks"], "confidence": 0.85}
        
        # 默认返回A股概述
        return {"type": "market", "answer": self.knowledge["a_share_features"], "confidence": 0.80}


if __name__ == "__main__":
    analyzer = ChinaStockAnalyzer()
    
    print("="*80)
    print("中国股市分析模块 v1.0")
    print("="*80)
    
    questions = [
        "A股市场有什么特点？",
        "上证指数现在多少点？",
        "新能源板块怎么样？",
        "当前估值水平如何？",
        "如何投资A股？",
    ]
    
    for q in questions:
        print(f"\n问题: {q}")
        result = analyzer.analyze(q)
        print(f"类型: {result['type']}")
        print(f"置信度: {result['confidence']*100:.0f}%")
        print(f"回答: {result['answer'][:100]}...")
    
    print("\n" + "="*80)
