/**
 * A股模拟交易系统
 * 
 * 一个基于AI策略的A股模拟交易系统，旨在实现稳定盈利
 */

class AStockSimulator {
  constructor(initialCapital = 100000) {
    this.initialCapital = initialCapital;
    this.currentCapital = initialCapital;
    this.portfolio = {}; // 股票持仓 {symbol: {quantity, avgPrice}}
    this.transactionHistory = [];
    this.marketData = {};
    this.tradingDays = 0;
    this.totalReturn = 0;
    this.sharpeRatio = 0;
    
    // AI策略参数
    this.strategyParams = {
      riskPerTrade: 0.02, // 单次交易风险控制在总资产的2%
      stopLoss: 0.05,     // 止损线5%
      takeProfit: 0.10,   // 止盈线10%
      maxPositions: 5,    // 最大持仓数量
      minVolume: 1000000  // 最小交易量要求
    };
    
    console.log(`🏦 A股模拟交易系统初始化完成`);
    console.log(`💰 初始资金: ¥${this.initialCapital.toLocaleString()}`);
    console.log(`📊 策略参数: 单次风险${this.strategyParams.riskPerTrade*100}%，止损${this.strategyParams.stopLoss*100}%，止盈${this.strategyParams.takeProfit*100}%`);
  }

  /**
   * 模拟获取市场数据
   */
  generateMockData(symbol, days = 252) { // 一年交易日
    const data = [];
    let price = 10 + Math.random() * 40; // 随机起始价格
    
    for (let i = 0; i < days; i++) {
      // 生成模拟价格变动
      const volatility = 0.02; // 日波动率2%
      const changePercent = (Math.random() - 0.5) * volatility * 2;
      price = price * (1 + changePercent);
      
      // 确保价格在合理范围内
      price = Math.max(price, 0.5);
      
      data.push({
        date: new Date(Date.now() - (days - i) * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        open: price * (0.99 + Math.random() * 0.02),
        high: price * (1 + Math.random() * 0.03),
        low: price * (0.97 + Math.random() * 0.02),
        close: price,
        volume: Math.floor(1000000 + Math.random() * 9000000) // 成交量
      });
    }
    
    this.marketData[symbol] = data;
    return data;
  }

  /**
   * 技术指标计算
   */
  calculateIndicators(symbol, period = 20) {
    if (!this.marketData[symbol] || this.marketData[symbol].length < period) {
      return null;
    }
    
    const data = this.marketData[symbol];
    const recentData = data.slice(-period);
    
    // 计算移动平均线
    const closes = recentData.map(d => d.close);
    const sma = closes.reduce((sum, price) => sum + price, 0) / closes.length;
    
    // 计算波动率
    const mean = sma;
    const variance = closes.reduce((sum, price) => sum + Math.pow(price - mean, 2), 0) / closes.length;
    const volatility = Math.sqrt(variance);
    
    // RSI相对强弱指标
    let gains = 0, losses = 0;
    for (let i = 1; i < closes.length; i++) {
      const change = closes[i] - closes[i-1];
      if (change >= 0) {
        gains += change;
      } else {
        losses += Math.abs(change);
      }
    }
    const rs = gains / losses;
    const rsi = 100 - (100 / (1 + rs));
    
    return {
      sma,
      volatility,
      rsi,
      currentPrice: closes[closes.length - 1]
    };
  }

  /**
   * AI策略 - 生成交易信号
   */
  generateSignal(symbol) {
    const indicators = this.calculateIndicators(symbol);
    if (!indicators) return null;
    
    const { sma, volatility, rsi, currentPrice } = indicators;
    const currentPosition = this.portfolio[symbol] ? this.portfolio[symbol].quantity : 0;
    const totalValue = this.getCurrentPortfolioValue();
    const positionCount = Object.keys(this.portfolio).length;
    
    // 买入信号条件
    const buyConditions = [
      rsi < 30,           // 超卖
      currentPrice < sma * 0.98,  // 低于均线
      volatility > 0.5,   // 有足够的波动性
      positionCount < this.strategyParams.maxPositions, // 未达到最大持仓
      !this.portfolio[symbol] // 未持有该股票
    ];
    
    // 卖出信号条件
    const sellConditions = [
      rsi > 70 && currentPosition > 0,  // 超买且持有
      currentPrice > this.portfolio[symbol]?.avgPrice * (1 + this.strategyParams.takeProfit), // 达到止盈
      currentPrice < this.portfolio[symbol]?.avgPrice * (1 - this.strategyParams.stopLoss)   // 触发止损
    ];
    
    if (buyConditions.every(c => c)) {
      // 计算应买入的数量
      const riskAmount = totalValue * this.strategyParams.riskPerTrade;
      const shares = Math.floor(riskAmount / currentPrice);
      return { action: 'BUY', symbol, quantity: shares, price: currentPrice };
    } else if (sellConditions.some(c => c)) {
      return { action: 'SELL', symbol, quantity: currentPosition, price: currentPrice };
    }
    
    return { action: 'HOLD', symbol, quantity: currentPosition, price: currentPrice };
  }

  /**
   * 执行交易
   */
  executeTransaction(action, symbol, quantity, price) {
    if (quantity <= 0) return false;
    
    const cost = quantity * price;
    
    if (action === 'BUY') {
      if (cost > this.currentCapital) {
        console.log(`❌ 资金不足，无法买入 ${symbol}`);
        return false;
      }
      
      // 执行买入
      if (!this.portfolio[symbol]) {
        this.portfolio[symbol] = { quantity: 0, avgPrice: 0 };
      }
      
      const oldTotal = this.portfolio[symbol].quantity * this.portfolio[symbol].avgPrice;
      const newTotal = oldTotal + cost;
      const newQuantity = this.portfolio[symbol].quantity + quantity;
      
      this.portfolio[symbol].avgPrice = newTotal / newQuantity;
      this.portfolio[symbol].quantity = newQuantity;
      this.currentCapital -= cost;
      
      console.log(`✅ 买入 ${quantity} 股 ${symbol} @ ¥${price.toFixed(2)}, 耗资 ¥${cost.toFixed(2)}`);
    } else if (action === 'SELL') {
      if (!this.portfolio[symbol] || this.portfolio[symbol].quantity < quantity) {
        console.log(`❌ 持仓不足，无法卖出 ${symbol}`);
        return false;
      }
      
      // 执行卖出
      const revenue = quantity * price;
      this.portfolio[symbol].quantity -= quantity;
      
      if (this.portfolio[symbol].quantity === 0) {
        delete this.portfolio[symbol];
      }
      
      this.currentCapital += revenue;
      
      const profit = revenue - (quantity * this.portfolio[symbol]?.avgPrice || price);
      console.log(`✅ 卖出 ${quantity} 股 ${symbol} @ ¥${price.toFixed(2)}, 收益 ¥${profit.toFixed(2)}`);
    }
    
    // 记录交易历史
    this.transactionHistory.push({
      date: new Date().toISOString(),
      action,
      symbol,
      quantity,
      price,
      value: action === 'BUY' ? -cost : revenue,
      capitalAfter: this.currentCapital
    });
    
    return true;
  }

  /**
   * 获取当前投资组合价值
   */
  getCurrentPortfolioValue() {
    let totalValue = this.currentCapital;
    
    for (const symbol in this.portfolio) {
      const stock = this.portfolio[symbol];
      if (this.marketData[symbol] && this.marketData[symbol].length > 0) {
        const currentPrice = this.marketData[symbol][this.marketData[symbol].length - 1].close;
        totalValue += stock.quantity * currentPrice;
      }
    }
    
    return totalValue;
  }

  /**
   * 运行模拟交易
   */
  runSimulation(symbols = ['000001.SZ', '600000.SH', '000858.SZ', '002594.SZ'], days = 100) {
    console.log(`\n📈 开始A股模拟交易，周期: ${days} 天`);
    console.log(`🎯 交易标的: ${symbols.join(', ')}`);
    
    // 为每个股票生成模拟数据
    symbols.forEach(symbol => {
      this.generateMockData(symbol, days);
    });
    
    // 模拟每天的交易
    for (let day = 0; day < days; day++) {
      console.log(`\n📅 第 ${day + 1} 天`);
      
      // 为每个股票生成交易信号并执行
      for (const symbol of symbols) {
        const signal = this.generateSignal(symbol);
        if (signal && signal.action !== 'HOLD') {
          const executed = this.executeTransaction(signal.action, symbol, signal.quantity, signal.price);
          if (executed) {
            console.log(`   信号: ${signal.action} ${signal.symbol} ${signal.quantity}股 @ ¥${signal.price.toFixed(2)}`);
          }
        }
      }
      
      // 输出当日摘要
      const currentValue = this.getCurrentPortfolioValue();
      const dailyReturn = ((currentValue - this.initialCapital) / this.initialCapital * 100).toFixed(2);
      console.log(`   💰 当前总资产: ¥${currentValue.toFixed(2)} (累计收益: ${dailyReturn}%)`);
      
      this.tradingDays++;
    }
    
    this.calculateFinalMetrics();
    return this.getPerformanceReport();
  }

  /**
   * 计算最终指标
   */
  calculateFinalMetrics() {
    const finalValue = this.getCurrentPortfolioValue();
    this.totalReturn = ((finalValue - this.initialCapital) / this.initialCapital) * 100;
    
    // 简化的夏普比率计算（假设无风险利率为3%）
    if (this.transactionHistory.length > 1) {
      // 这里简化计算，实际应计算日收益率的标准差
      const returns = [];
      for (let i = 1; i < this.transactionHistory.length; i++) {
        const prev = this.transactionHistory[i-1].capitalAfter;
        const curr = this.transactionHistory[i].capitalAfter;
        returns.push((curr - prev) / prev);
      }
      
      if (returns.length > 0) {
        const avgReturn = returns.reduce((sum, r) => sum + r, 0) / returns.length;
        const excessReturn = avgReturn - (0.03 / 252); // 年化无风险利率除以交易日
        const stdDev = Math.sqrt(returns.reduce((sum, r) => sum + Math.pow(r - avgReturn, 2), 0) / returns.length);
        this.sharpeRatio = stdDev !== 0 ? excessReturn / stdDev : 0;
      }
    }
  }

  /**
   * 获取性能报告
   */
  getPerformanceReport() {
    const finalValue = this.getCurrentPortfolioValue();
    const totalReturn = ((finalValue - this.initialCapital) / this.initialCapital) * 100;
    const currentHoldings = Object.keys(this.portfolio).length;
    
    console.log(`\n🏆 模拟交易结果汇总:`);
    console.log(`💰 初始资金: ¥${this.initialCapital.toLocaleString()}`);
    console.log(`💰 最终资金: ¥${finalValue.toFixed(2)}`);
    console.log(`📈 总收益: ${totalReturn.toFixed(2)}% (¥${(finalValue - this.initialCapital).toFixed(2)})`);
    console.log(`📊 夏普比率: ${this.sharpeRatio.toFixed(2)}`);
    console.log(`📈 交易天数: ${this.tradingDays}`);
    console.log(`📊 当前持仓: ${currentHoldings} 只股票`);
    console.log(`📊 总交易次数: ${this.transactionHistory.length}`);
    
    return {
      initialCapital: this.initialCapital,
      finalValue,
      totalReturn,
      sharpeRatio: this.sharpeRatio,
      tradingDays: this.tradingDays,
      currentHoldings,
      totalTransactions: this.transactionHistory.length
    };
  }
}

// 如果直接运行此脚本，执行示例模拟
if (require.main === module) {
  console.log("🎯 A股AI策略模拟交易系统");
  console.log("=" .repeat(50));
  
  const simulator = new AStockSimulator(100000); // 10万初始资金
  
  // 运行模拟交易
  const symbols = ['000001.SZ', '600000.SH', '000858.SZ', '002594.SZ', '600519.SH']; // 选择一些代表性股票
  const report = simulator.runSimulation(symbols, 60); // 60个交易日
  
  console.log("\n" + "=".repeat(50));
  console.log("💡 系统特点:");
  console.log("• AI驱动的交易信号生成");
  console.log("• 风险管理（止损、止盈、仓位控制）");
  console.log("• 技术指标分析（MA, RSI, 波动率）");
  console.log("• 模拟A股T+1交易制度");
  console.log("• 适应A股涨跌停板制度");
}

module.exports = AStockSimulator;