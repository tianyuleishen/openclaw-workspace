/**
 * 优化版A股AI策略模拟交易系统
 * 
 * 改进交易策略，使其更符合实际市场情况
 */

const AStockSimulator = require('./stock_simulator');
const AdvancedStrategy = require('./advanced_strategy');

class OptimizedAStockSimulator extends AStockSimulator {
  constructor(initialCapital = 100000) {
    super(initialCapital);
    this.advancedStrategy = new AdvancedStrategy();
    this.positionHistory = {}; // 记录持仓历史
    this.profitTargets = {}; // 记录买入价格以计算止盈止损
  }

  /**
   * 优化的交易信号生成
   */
  generateOptimizedSignal(symbol) {
    if (!this.marketData[symbol] || this.marketData[symbol].length < 20) {
      return super.generateSignal(symbol); // 回退到基础策略
    }

    const stockData = this.marketData[symbol];
    const currentPrice = stockData[stockData.length - 1].close;
    const fundamentals = this.generateMockFundamentals(symbol);
    
    // 使用高级策略生成信号
    const signal = this.advancedStrategy.generateSignal(symbol, stockData, fundamentals);
    
    // 检查持仓情况和止盈止损条件
    const currentPosition = this.portfolio[symbol] ? this.portfolio[symbol].quantity : 0;
    
    // 检查是否触发止盈/止损
    if (currentPosition > 0 && this.portfolio[symbol]) {
      const avgBuyPrice = this.portfolio[symbol].avgPrice;
      const currentReturn = (currentPrice - avgBuyPrice) / avgBuyPrice;
      
      // 止盈条件：收益超过10%
      if (currentReturn >= this.strategyParams.takeProfit) {
        return { action: 'SELL', symbol, quantity: currentPosition, price: currentPrice };
      }
      // 止损条件：亏损超过5%
      else if (currentReturn <= -this.strategyParams.stopLoss) {
        return { action: 'SELL', symbol, quantity: currentPosition, price: currentPrice };
      }
    }
    
    // 如果没有持仓，检查买入条件
    if (currentPosition === 0) {
      if (signal.action.includes('BUY')) {
        const totalValue = this.getCurrentPortfolioValue();
        const riskAmount = totalValue * this.strategyParams.riskPerTrade;
        const quantity = Math.floor(riskAmount / currentPrice);
        
        // 检查是否达到最大持仓限制
        const positionCount = Object.keys(this.portfolio).length;
        if (positionCount >= this.strategyParams.maxPositions) {
          return { action: 'HOLD', symbol, quantity: 0, price: currentPrice };
        }
        
        // 检查资金是否足够
        const cost = quantity * currentPrice;
        if (cost > this.currentCapital) {
          // 按比例减少购买数量
          const affordableQty = Math.floor(this.currentCapital * 0.9 / currentPrice); // 保留10%现金
          if (affordableQty > 0) {
            return { action: 'BUY', symbol, quantity: affordableQty, price: currentPrice };
          } else {
            return { action: 'HOLD', symbol, quantity: 0, price: currentPrice };
          }
        }
        
        return { action: 'BUY', symbol, quantity, price: currentPrice };
      }
    }
    
    // 如果持有但不满足止盈止损条件，继续持有
    return { action: 'HOLD', symbol, quantity: currentPosition, price: currentPrice };
  }

  /**
   * 生成模拟基本面数据
   */
  generateMockFundamentals(symbol) {
    // 为不同股票生成不同的基本面特征
    const baseValues = {
      '000001.SZ': { pe: 8 + Math.random() * 4, pb: 0.8 + Math.random() * 0.5, roe: 0.12 + Math.random() * 0.05, debtToEquity: 0.4 + Math.random() * 0.2 },
      '600000.SH': { pe: 5 + Math.random() * 3, pb: 0.6 + Math.random() * 0.4, roe: 0.15 + Math.random() * 0.04, debtToEquity: 0.3 + Math.random() * 0.15 },
      '000858.SZ': { pe: 15 + Math.random() * 8, pb: 3 + Math.random() * 2, roe: 0.20 + Math.random() * 0.08, debtToEquity: 0.2 + Math.random() * 0.1 },
      '002594.SZ': { pe: 12 + Math.random() * 6, pb: 2 + Math.random() * 1.5, roe: 0.18 + Math.random() * 0.06, debtToEquity: 0.25 + Math.random() * 0.15 },
      '600519.SH': { pe: 25 + Math.random() * 10, pb: 8 + Math.random() * 4, roe: 0.25 + Math.random() * 0.05, debtToEquity: 0.1 + Math.random() * 0.05 }
    };

    // 如果符号不存在，生成随机基本面
    if (!baseValues[symbol]) {
      return {
        pe: 10 + Math.random() * 15,
        pb: 1 + Math.random() * 3,
        roe: 0.1 + Math.random() * 0.15,
        debtToEquity: 0.2 + Math.random() * 0.3
      };
    }

    return baseValues[symbol];
  }

  /**
   * 执行交易 - 优化版
   */
  executeTransaction(action, symbol, quantity, price) {
    if (quantity <= 0) return false;
    
    // 计算交易成本（A股交易成本）
    let cost = quantity * price;
    let actualQuantity = quantity;
    
    if (action === 'BUY') {
      // A股买入成本：交易金额 * 0.0001 (过户费) + max(5, 交易金额 * 0.00025) (佣金)
      const commission = Math.max(5, cost * 0.00025);
      const transferFee = cost * 0.0001;
      cost += commission + transferFee;
      
      if (cost > this.currentCapital) {
        // 调整购买数量以适应可用资金
        const availableFunds = this.currentCapital * 0.99; // 保留少量现金
        actualQuantity = Math.floor(availableFunds / price);
        cost = actualQuantity * price;
        const adjustedCommission = Math.max(5, cost * 0.00025);
        const adjustedTransferFee = cost * 0.0001;
        cost = cost + adjustedCommission + adjustedTransferFee;
        
        if (cost > this.currentCapital) {
          console.log(`❌ 资金不足，无法买入 ${symbol}`);
          return false;
        }
      }
      
      // 执行买入
      if (!this.portfolio[symbol]) {
        this.portfolio[symbol] = { quantity: 0, avgPrice: 0 };
      }
      
      const oldTotal = this.portfolio[symbol].quantity * this.portfolio[symbol].avgPrice;
      const newTotal = oldTotal + cost;
      const newQuantity = this.portfolio[symbol].quantity + actualQuantity;
      
      this.portfolio[symbol].avgPrice = newTotal / newQuantity;
      this.portfolio[symbol].quantity = newQuantity;
      this.currentCapital -= cost;
      
      console.log(`✅ 买入 ${actualQuantity} 股 ${symbol} @ ¥${price.toFixed(2)}, 耗资 ¥${cost.toFixed(2)}`);
    } else if (action === 'SELL') {
      if (!this.portfolio[symbol] || this.portfolio[symbol].quantity < quantity) {
        console.log(`❌ 持仓不足，无法卖出 ${symbol}`);
        return false;
      }
      
      // A股卖出成本：交易金额 * 0.0001 (过户费) + max(5, 交易金额 * 0.00025) (佣金) + 交易金额 * 0.001 (印花税)
      const revenue = quantity * price;
      const commission = Math.max(5, revenue * 0.00025);
      const transferFee = revenue * 0.0001;
      const tax = revenue * 0.001; // 印花税
      const totalCost = commission + transferFee + tax;
      const netRevenue = revenue - totalCost;
      
      // 执行卖出
      this.portfolio[symbol].quantity -= quantity;
      
      if (this.portfolio[symbol].quantity === 0) {
        delete this.portfolio[symbol];
      }
      
      this.currentCapital += netRevenue;
      
      const profit = netRevenue - (quantity * this.portfolio[symbol]?.avgPrice || price);
      console.log(`✅ 卖出 ${quantity} 股 ${symbol} @ ¥${price.toFixed(2)}, 净收入 ¥${netRevenue.toFixed(2)}, 收益 ¥${profit.toFixed(2)}`);
    }
    
    // 记录交易历史
    this.transactionHistory.push({
      date: new Date().toISOString(),
      action,
      symbol,
      quantity: actualQuantity,
      price,
      value: action === 'BUY' ? -cost : (revenue - totalCost),
      capitalAfter: this.currentCapital,
      commission: action === 'BUY' ? (cost - quantity * price) : totalCost
    });
    
    return true;
  }

  /**
   * 运行优化版模拟交易
   */
  runOptimizedSimulation(symbols = ['000001.SZ', '600000.SH', '000858.SZ', '002594.SZ', '600519.SH'], days = 120) {
    console.log(`\n🚀 运行优化版A股AI策略模拟交易`);
    console.log(`📊 采用改进的多因子AI策略，包含动态止盈止损`);
    
    // 为每个股票生成模拟数据
    symbols.forEach(symbol => {
      this.generateMockData(symbol, days);
    });
    
    // 模拟每天的交易
    for (let day = 0; day < days; day++) {
      console.log(`\n📅 第 ${day + 1} 天`);
      
      // 更新市场状态
      this.advancedStrategy.updateMarketState(null);
      
      // 为每个股票生成交易信号并执行
      for (const symbol of symbols) {
        const signal = this.generateOptimizedSignal(symbol);
        if (signal && signal.action !== 'HOLD') {
          const executed = this.executeTransaction(signal.action, symbol, signal.quantity, signal.price);
          if (executed) {
            console.log(`   🤖 AI策略: ${signal.action} ${signal.symbol} ${signal.quantity}股 @ ¥${signal.price.toFixed(2)}`);
          }
        }
      }
      
      // 输出当日摘要
      const currentValue = this.getCurrentPortfolioValue();
      const dailyReturn = ((currentValue - this.initialCapital) / this.initialCapital * 100).toFixed(2);
      console.log(`   💰 当前总资产: ¥${currentValue.toFixed(2)} (累计收益: ${dailyReturn}%)`);
      
      this.tradingDays++;
    }
    
    this.calculateEnhancedMetrics();
    return this.getEnhancedPerformanceReport();
  }

  /**
   * 计算增强版指标
   */
  calculateEnhancedMetrics() {
    super.calculateFinalMetrics(); // 基础指标
    
    // 计算最大回撤
    let peak = this.initialCapital;
    let maxDrawdown = 0;
    
    // 计算胜率
    let wins = 0;
    let totalTrades = 0;
    
    for (const tx of this.transactionHistory) {
      if (tx.action === 'SELL') {
        totalTrades++;
        // 这里简化计算胜率，实际需要跟踪具体买入成本
        if (tx.value > 0) wins++; 
      }
    }
    
    this.riskMetrics.winningRate = totalTrades > 0 ? (wins / totalTrades) * 100 : 0;
    
    // 简化的最大回撤计算
    this.riskMetrics.maxDrawdown = Math.abs(((this.initialCapital - this.getCurrentPortfolioValue()) / this.initialCapital) * 100);
  }

  /**
   * 获取增强版性能报告
   */
  getEnhancedPerformanceReport() {
    const finalValue = this.getCurrentPortfolioValue();
    const totalReturn = ((finalValue - this.initialCapital) / this.initialCapital) * 100;
    const currentHoldings = Object.keys(this.portfolio).length;
    
    console.log(`\n🏆 优化版AI策略模拟交易结果:`);
    console.log(`💰 初始资金: ¥${this.initialCapital.toLocaleString()}`);
    console.log(`💰 最终资金: ¥${finalValue.toFixed(2)}`);
    console.log(`📈 总收益: ${totalReturn.toFixed(2)}% (¥${(finalValue - this.initialCapital).toFixed(2)})`);
    
    if (this.tradingDays > 0) {
      const annualizedReturn = (Math.pow(finalValue / this.initialCapital, 252 / this.tradingDays) - 1) * 100;
      console.log(`📊 年化收益率: ${annualizedReturn.toFixed(2)}%`);
    }
    
    console.log(`📊 夏普比率: ${this.sharpeRatio.toFixed(2)}`);
    console.log(`📉 最大回撤: ${this.riskMetrics.maxDrawdown.toFixed(2)}%`);
    console.log(`🎯 胜率: ${this.riskMetrics.winningRate.toFixed(2)}%`);
    console.log(`📈 交易天数: ${this.tradingDays}`);
    console.log(`📊 当前持仓: ${currentHoldings} 只股票`);
    console.log(`📊 总交易次数: ${this.transactionHistory.length}`);
    
    // 计算相对于基准的超额收益
    // 假设沪深300年化收益为5%
    const daysToYears = this.tradingDays / 252;
    const benchmarkReturn = 5 * daysToYears;
    const alpha = (this.tradingDays > 0) ? 
      (Math.pow(finalValue / this.initialCapital, 252 / this.tradingDays) - 1) * 100 - 5 : 
      totalReturn - benchmarkReturn;
    console.log(`⭐ Alpha (超额收益): ${alpha.toFixed(2)}%`);
    
    return {
      initialCapital: this.initialCapital,
      finalValue,
      totalReturn,
      annualizedReturn: (this.tradingDays > 0) ? (Math.pow(finalValue / this.initialCapital, 252 / this.tradingDays) - 1) * 100 : totalReturn,
      sharpeRatio: this.sharpeRatio,
      maxDrawdown: this.riskMetrics.maxDrawdown,
      winningRate: this.riskMetrics.winningRate,
      tradingDays: this.tradingDays,
      currentHoldings,
      totalTransactions: this.transactionHistory.length,
      alpha
    };
  }
}

// 如果直接运行此脚本，执行示例模拟
if (require.main === module) {
  console.log("🎯 优化版A股AI策略模拟交易系统");
  console.log("=" .repeat(60));
  
  const simulator = new OptimizedAStockSimulator(100000); // 10万初始资金
  
  // 运行优化版模拟交易
  const symbols = ['000001.SZ', '600000.SH', '000858.SZ', '002594.SZ', '600519.SH'];
  const report = simulator.runOptimizedSimulation(symbols, 60); // 60个交易日
  
  console.log("\n" + "=".repeat(60));
  console.log("💡 优化版系统特性:");
  console.log("• 动态止盈止损机制");
  console.log("• 更真实的A股交易成本模型");
  console.log("• 资金管理优化");
  console.log("• 改进的风险控制");
  console.log("• 实时持仓跟踪");
  
  console.log("\n⚠️  风险提示:");
  console.log("• 此为模拟系统，不构成投资建议");
  console.log("• 实际投资存在市场风险");
  console.log("• 过往业绩不代表未来表现");
}

module.exports = OptimizedAStockSimulator;