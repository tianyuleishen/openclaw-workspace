/**
 * 高级AI策略模块
 * 
 * 包含更复杂的交易策略和风险管理
 */

class AdvancedStrategy {
  constructor() {
    // 多因子模型权重
    this.factorWeights = {
      momentum: 0.25,
      value: 0.20,
      quality: 0.20,
      volatility: 0.15,
      liquidity: 0.10,
      sentiment: 0.10
    };
    
    // 市场状态检测
    this.marketState = {
      trend: 'neutral',  // bullish, bearish, neutral
      volatility: 'normal', // low, normal, high
      momentum: 'normal' // weak, normal, strong
    };
  }

  /**
   * 多因子评分模型
   */
  multiFactorScore(stockData, fundamentals) {
    // 动量因子 (25%)
    const momentum = this.calculateMomentum(stockData);
    
    // 价值因子 (20%)
    const value = this.calculateValue(fundamentals);
    
    // 质量因子 (20%)
    const quality = this.calculateQuality(fundamentals);
    
    // 波动率因子 (15%)
    const vol = this.calculateVolatility(stockData);
    
    // 流动性因子 (10%)
    const liquidity = this.calculateLiquidity(stockData);
    
    // 情绪因子 (10%)
    const sentiment = this.calculateSentiment(stockData);
    
    // 加权得分
    const score = 
      momentum * this.factorWeights.momentum +
      value * this.factorWeights.value +
      quality * this.factorWeights.quality +
      vol * this.factorWeights.volatility +
      liquidity * this.factorWeights.liquidity +
      sentiment * this.factorWeights.sentiment;
    
    return {
      totalScore: score,
      factors: { momentum, value, quality, vol, liquidity, sentiment }
    };
  }

  /**
   * 计算动量因子
   */
  calculateMomentum(stockData) {
    if (stockData.length < 20) return 0.5;
    
    const recent = stockData.slice(-10);
    const past = stockData.slice(-20, -10);
    
    const recentAvg = recent.reduce((sum, d) => sum + d.close, 0) / recent.length;
    const pastAvg = past.reduce((sum, d) => sum + d.close, 0) / past.length;
    
    // 动量得分：正向动量为正值，负向动量为负值
    const momentum = (recentAvg - pastAvg) / pastAvg;
    
    // 归一化到0-1区间
    return Math.max(0, Math.min(1, (momentum + 0.2) * 2.5)); // 假设典型动量范围为-20%到+20%
  }

  /**
   * 计算价值因子
   */
  calculateValue(fundamentals) {
    // 简化的价值评分，基于PE、PB等指标
    const pe = fundamentals.pe || 20; // 默认市盈率
    const pb = fundamentals.pb || 2;  // 默认市净率
    
    // 价值得分：越低越好
    const peScore = Math.max(0, Math.min(1, (30 - pe) / 20)); // PE越低越好，假设30以下是合理
    const pbScore = Math.max(0, Math.min(1, (4 - pb) / 3));   // PB越低越好，假设4以下是合理
    
    return (peScore + pbScore) / 2;
  }

  /**
   * 计算质量因子
   */
  calculateQuality(fundamentals) {
    // 基于ROE、负债率等指标
    const roe = fundamentals.roe || 0.1; // 默认ROE 10%
    const debtToEquity = fundamentals.debtToEquity || 0.5; // 默认负债权益比50%
    
    const roeScore = Math.max(0, Math.min(1, roe / 0.2)); // 假设20% ROE为优秀
    const debtScore = Math.max(0, Math.min(1, (1 - debtToEquity) * 2)); // 负债越少越好
    
    return (roeScore + debtScore) / 2;
  }

  /**
   * 计算波动率因子
   */
  calculateVolatility(stockData) {
    if (stockData.length < 10) return 0.5;
    
    // 计算价格波动率
    const returns = [];
    for (let i = 1; i < stockData.length; i++) {
      const ret = (stockData[i].close - stockData[i-1].close) / stockData[i-1].close;
      returns.push(ret);
    }
    
    const avgReturn = returns.reduce((sum, r) => sum + r, 0) / returns.length;
    const variance = returns.reduce((sum, r) => sum + Math.pow(r - avgReturn, 2), 0) / returns.length;
    const volatility = Math.sqrt(variance);
    
    // 波动率适中为好（太高或太低都不理想）
    // 假设理想的日波动率为1-3%
    const idealLow = 0.01;
    const idealHigh = 0.03;
    
    if (volatility >= idealLow && volatility <= idealHigh) {
      return 1.0; // 理想波动率
    } else if (volatility < idealLow) {
      return 0.3; // 波动率太低
    } else {
      return Math.max(0, 1 - (volatility - idealHigh) / 0.02); // 波动率太高，递减
    }
  }

  /**
   * 计算流动性因子
   */
  calculateLiquidity(stockData) {
    // 基于成交量评分
    if (stockData.length < 5) return 0.5;
    
    const recentVolumes = stockData.slice(-5).map(d => d.volume);
    const avgVolume = recentVolumes.reduce((sum, v) => sum + v, 0) / recentVolumes.length;
    
    // 假设平均成交量大于100万股/天为高流动性
    if (avgVolume > 1000000) return 1.0;
    if (avgVolume > 500000) return 0.8;
    if (avgVolume > 200000) return 0.6;
    if (avgVolume > 100000) return 0.4;
    return 0.2;
  }

  /**
   * 计算情绪因子
   */
  calculateSentiment(stockData) {
    // 基于价格行为的情绪指标
    if (stockData.length < 5) return 0.5;
    
    const latest = stockData[stockData.length - 1];
    const prev = stockData[stockData.length - 2];
    
    // 根据当日价格行为判断情绪
    const bodySize = Math.abs(latest.close - latest.open);
    const totalRange = latest.high - latest.low;
    const bodyRatio = totalRange > 0 ? bodySize / totalRange : 0;
    
    // 上涨且实体较大，情绪偏向积极
    if (latest.close > latest.open && bodyRatio > 0.7) return 0.8;
    if (latest.close > latest.open) return 0.7;
    
    // 下跌且实体较大，情绪偏向消极
    if (latest.close < latest.open && bodyRatio > 0.7) return 0.2;
    if (latest.close < latest.open) return 0.3;
    
    // 盘整，中性情绪
    return 0.5;
  }

  /**
   * 基于市场状态调整策略
   */
  adjustForMarketState(score, marketState) {
    // 根据市场状态调整得分
    switch(marketState.trend) {
      case 'bullish':
        // 牛市中适当提高买入倾向
        return score > 0.6 ? score * 1.1 : score;
      case 'bearish':
        // 熊市中更加谨慎
        return score > 0.7 ? score : score * 0.9;
      default:
        return score;
    }
  }

  /**
   * 生成交易信号
   */
  generateSignal(stockSymbol, stockData, fundamentals = {}) {
    // 计算多因子得分
    const factorResult = this.multiFactorScore(stockData, fundamentals);
    const adjustedScore = this.adjustForMarketState(factorResult.totalScore, this.marketState);
    
    // 生成交易信号
    if (adjustedScore > 0.7) {
      // 强买入信号
      return {
        action: 'BUY_STRONG',
        symbol: stockSymbol,
        score: adjustedScore,
        recommendation: '强烈建议买入',
        factors: factorResult.factors
      };
    } else if (adjustedScore > 0.6) {
      // 一般买入信号
      return {
        action: 'BUY',
        symbol: stockSymbol,
        score: adjustedScore,
        recommendation: '建议买入',
        factors: factorResult.factors
      };
    } else if (adjustedScore < 0.3) {
      // 强卖出信号
      return {
        action: 'SELL_STRONG',
        symbol: stockSymbol,
        score: adjustedScore,
        recommendation: '强烈建议卖出',
        factors: factorResult.factors
      };
    } else if (adjustedScore < 0.4) {
      // 一般卖出信号
      return {
        action: 'SELL',
        symbol: stockSymbol,
        score: adjustedScore,
        recommendation: '建议卖出',
        factors: factorResult.factors
      };
    } else {
      // 持有或观望
      return {
        action: 'HOLD',
        symbol: stockSymbol,
        score: adjustedScore,
        recommendation: '持有或观望',
        factors: factorResult.factors
      };
    }
  }

  /**
   * 更新市场状态
   */
  updateMarketState(indexData) {
    // 这里可以根据大盘指数数据更新市场状态
    // 简化实现，随机更新
    this.marketState.trend = ['bullish', 'bearish', 'neutral'][Math.floor(Math.random() * 3)];
    this.marketState.volatility = ['low', 'normal', 'high'][Math.floor(Math.random() * 3)];
    this.marketState.momentum = ['weak', 'normal', 'strong'][Math.floor(Math.random() * 3)];
  }
}

module.exports = AdvancedStrategy;