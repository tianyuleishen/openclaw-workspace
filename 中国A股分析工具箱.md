# 🇨🇳 中国A股分析工具箱

**创建时间**: 2026-02-09
**更新**: 2026-02-09 21:45

---

## 📦 已安装的相关工具

### 1. TuShare (已配置 ✅)

**用途**: 获取A股真实行情数据

**Token**: 06dcd1581204b5fbf16a2d500fbba9b7fab80d38329b1e7cc2069f03

**使用方法**:
```python
import tushare as ts
ts.set_token("06dcd1581...")
pro = ts.pro_api()
df = pro.daily(trade_date='20260209')
```

**已实现功能**:
- ✅ 获取涨停股票列表
- ✅ 行业分类统计
- ✅ 多因子评分分析

**文件**:
- `get_limit_up.py` - 获取涨停数据
- `stock_analyzer.py` - AI多因子分析
- `limit_up_analyzer.py` - 扩展分析

---

### 2. 腾讯财经API (已验证 ✅)

**状态**: 可访问 https://qt.gtimg.cn

**用途**: 实时股票价格查询

**支持的股票代码**:
- A股: `sh600519`, `sz000001`, `sz300364`
- 指数: `sh000001` (上证), `sz399001` (深证)
- 港股: `hk00700`, `hk09988`
- 美股: `AAPL`, `TSLA`, `NVDA`

**使用方法**:
```python
from china_stock_analyzer import ChinaStockAnalyzer
analyzer = ChinaStockAnalyzer()
data = analyzer.get_stock_price('sh600519')
```

**文件**:
- `china_stock_analyzer.py` - 腾讯财经API封装

---

### 3. 财联社 (部分可用 ⚠️)

**状态**: 
- ✅ 首页: 可访问
- ⚠️ API: 被WAF拦截

**用途**: 财经新闻日历

**访问方式**:
- 网页: https://m.cls.cn/
- 今日事件: 春节档、AI研讨会等

**问题**: API需要反爬虫策略

---

### 4. ClawHub技能 (已安装 2个)

#### news-summary
- ❌ 国际新闻 (BBC/Reuters)
- ❌ 无中国财经新闻

#### financial-market-analysis  
- ⚠️ 美股分析 (Yahoo Finance)
- ❌ 需要付费API (CRAFTED_API_KEY)

---

## 🎯 涨停分析工具

### 快速分析

```bash
# 获取涨停数据
python3 get_limit_up.py

# 分析涨停原因
python3 stock_rally_analyzer.py

# 生成分析报告
python3 limit_up_analyzer.py
```

### 传媒涨停分析

```bash
python3 stock_rally_analyzer.py
```

**输出**:
- 共同驱动因素
- 个股涨停原因
- 投资建议

---

## 📊 分析报告模板

### 1. 每日涨停分析

**文件**: `limit_up_analysis_20260209.md`

**内容**:
- TOP 20 评分排名
- 行业分布统计
- 热点板块分析
- 涨停梯队

### 2. 传媒板块分析

**文件**: `media_rally_reasons.md`

**内容**:
- 涨停股票列表
- 共同驱动因素
- 个股原因分析

### 3. 市场概览

**文件**: `stock_analysis_20260209.md`

**内容**:
- 全部涨停股票
- 多因子评分
- 投资建议

---

## 💡 使用场景

### 场景1: 获取今日涨停股票

```bash
python3 get_limit_up.py
```

**输出**: 121只涨停股票列表

---

### 场景2: 分析传媒为什么涨

```bash
python3 stock_rally_analyzer.py
```

**预测原因**:
1. 春节档预期
2. 影视复苏
3. AI赋能
4. 板块轮动

---

### 场景3: 获取实时价格

```python
from china_stock_analyzer import ChinaStockAnalyzer

analyzer = ChinaStockAnalyzer()
data = analyzer.get_stock_price('sh600519')
print(data)
```

---

## 🔧 后续优化方向

### 短期 (本周)
- [ ] 完善腾讯财经API解析
- [ ] 添加更多股票代码支持
- [ ] 优化涨停分析算法

### 中期 (本月)
- [ ] 绕过财联社API限制
- [ ] 集成更多财经数据源
- [ ] 实现新闻自动获取

### 长期 (可选)
- [ ] 开发专用财经新闻技能
- [ ] 集成情感分析
- [ ] 实现自动交易信号

---

## 📁 文件清单

```
/home/admin/.openclaw/workspace/
├── china_stock_analyzer.py      # 腾讯财经API
├── get_limit_up.py              # TuShare涨停数据
├── stock_analyzer.py            # AI多因子分析
├── limit_up_analyzer.py        # 扩展涨停分析
├── stock_rally_analyzer.py      # 涨停原因分析
├── finance_news_fetcher.py      # 财经新闻抓取
│
├── limit_up_stocks_20260209.json  # 涨停数据
├── limit_up_analysis_20260209.md  # 分析报告
└── media_rally_reasons.md         # 传媒分析
```

---

## ⚠️ 注意事项

1. **网络限制**: 部分API可能需要代理
2. **数据延迟**: 实时数据可能略有延迟
3. **投资风险**: 分析仅供参考，不构成投资建议

---

## 🎯 总结

**可用的分析工具**:
- ✅ TuShare: 获取涨停数据
- ✅ 腾讯财经: 实时价格
- ⚠️ 财联社: 部分可用
- ❌ 新闻API: 需要手动

**建议**:
1. 使用TuShare获取涨停数据 ✅
2. 使用腾讯财经获取实时价格 ✅
3. 手动访问财联社获取新闻 ⚠️

---

**文档创建**: 2026-02-09 21:45
