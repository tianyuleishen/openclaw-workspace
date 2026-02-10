# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## A股分析工具箱 v2.0 (2026-02-09)

### 工具箱入口

**文件**: `stock_tools.py`

**使用方法**:
```bash
# 默认传媒板块
python3 stock_tools.py

# 查看帮助
python3 stock_tools.py help

# 财经新闻 ⭐NEW
python3 stock_tools.py news

# 股票查询
python3 stock_tools.py quote

# 涨停数据
python3 stock_tools.py limitup

# AI分析
python3 stock_tools.py analyze

# 全部查询
python3 stock_tools.py all
```

---

### 财经新闻查询 ⭐NEW

**文件**: `finance_news.py`

**功能**: 获取财经新闻

```bash
python3 stock_tools.py news
# 或
python3 finance_news.py
```

**获取内容**:
- 今日热点新闻
- 传媒板块相关
- 财经日历事件
- 市场动态

**数据来源**:
- 财联社
- 新浪财经
- 东方财富

---

### 腾讯财经实时行情

**文件**: `stock_query.py`

**使用方法**:
```bash
# 默认查询传媒板块
python3 stock_query.py

# 查询指定股票
python3 stock_query.py sh600519  # 贵州茅台
python3 stock_query.py sz300364  # 中文在线
python3 stock_query.py sh000001  # 上证指数
```

**支持的股票代码**:
- A股: `sh600519` (沪市), `sz000001` (深市)
- 创业板: `sz300xxx`
- 科创板: `sh688xxx`
- 指数: `sh000001` (上证), `sz399001` (深证)

---

### TuShare涨停分析

**文件**: `get_limit_up.py`

**功能**: 获取A股涨停股票列表

```bash
python3 get_limit_up.py  # 获取今日涨停
```

---

### 多因子分析

**文件**: `stock_analyzer.py`

**功能**: AI多因子评分分析

```bash
python3 stock_analyzer.py  # 生成分析报告
```

---

### 涨停原因分析

**文件**: `stock_rally_analyzer.py`

**功能**: 分析涨停原因

```bash
python3 stock_rally_analyzer.py
```

---

## 财经数据源

### TuShare (已配置)
- **Token**: 06dcd1581204b5fbf16a2d500fbba9b7fab80d38329b1e7cc2069f03
- **用途**: 获取A股行情数据
- **状态**: 已配置

### 腾讯财经API
- **URL**: https://qt.gtimg.cn
- **用途**: 实时股票价格
- **状态**: 可访问
- **限制**: 无需API Key

### 新浪财经
- **URL**: https://finance.sina.com.cn
- **用途**: 财经新闻
- **状态**: 可访问

### 财联社
- **URL**: https://m.cls.cn
- **用途**: 财经日历
- **状态**: 可访问

---

## 常用传媒股票

| 代码 | 名称 | 用途 |
|------|------|------|
| sz300364 | 中文在线 | 数字文学 |
| sz301231 | 荣信文化 | 数字内容 |
| sh603598 | 引力传媒 | 数字营销 |
| sh603103 | 横店影视 | 影视制作 |

**快速查询**:
```bash
python3 stock_query.py
```

---

## 快速使用指南

### 场景1: 查看传媒板块

```bash
python3 stock_tools.py
```

### 场景2: 获取财经新闻 ⭐

```bash
python3 stock_tools.py news
```

### 场景3: 分析涨停

```bash
python3 stock_tools.py all
```

### 场景4: 查询个股

```bash
python3 stock_query.py sh600519
```
