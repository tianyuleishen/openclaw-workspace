/**
 * A股AI策略模拟交易调度器
 * 
 * 负责每日自动执行模拟交易
 */

const EnhancedAStockSimulator = require('./enhanced_simulator_with_tushare');
const fs = require('fs').promises;
const path = require('path');

class TradingScheduler {
  constructor(initialCapital = 100000, token = null) {
    this.simulator = new EnhancedAStockSimulator(initialCapital, token);
    this.isRunning = false;
    this.scheduleInterval = null;
    this.tradingSymbols = ['000001.SZ', '600000.SH', '000858.SZ', '002594.SZ', '600519.SH', '000651.SZ', '600036.SH', '601398.SH'];
    this.tradeLogPath = path.join(__dirname, 'trading_logs');
  }

  /**
   * 初始化交易日志目录
   */
  async initializeLogs() {
    try {
      await fs.mkdir(this.tradeLogPath, { recursive: true });
      console.log(`📁 交易日志目录已创建: ${this.tradeLogPath}`);
    } catch (error) {
      console.error(`❌ 创建日志目录失败:`, error.message);
    }
  }

  /**
   * 执行单日模拟交易
   */
  async executeDailyTrade() {
    if (this.isRunning) {
      console.log('⏰ 模拟交易已在运行中，跳过本次执行');
      return;
    }

    try {
      this.isRunning = true;
      console.log(`\n🔔 开始执行每日模拟交易: ${new Date().toLocaleString('zh-CN')}`);

      // 执行每日模拟
      const result = await this.simulator.dailySimulation(this.tradingSymbols);

      // 保存交易日志
      await this.saveTradeLog(result);

      // 保存系统状态
      await this.saveSystemState();

      console.log(`✅ 每日模拟交易执行完成`);
    } catch (error) {
      console.error(`❌ 每日模拟交易执行失败:`, error);
    } finally {
      this.isRunning = false;
    }
  }

  /**
   * 保存交易日志
   */
  async saveTradeLog(tradeResult) {
    try {
      const logFileName = `trade_log_${new Date().toISOString().split('T')[0]}.json`;
      const logFilePath = path.join(this.tradeLogPath, logFileName);

      const logData = {
        timestamp: new Date().toISOString(),
        ...tradeResult,
        portfolio: { ...this.simulator.portfolio },
        cash: this.simulator.currentCapital,
        totalValue: this.simulator.getCurrentPortfolioValue()
      };

      await fs.writeFile(logFilePath, JSON.stringify(logData, null, 2), 'utf8');
      console.log(`💾 交易日志已保存: ${logFilePath}`);
    } catch (error) {
      console.error(`❌ 保存交易日志失败:`, error.message);
    }
  }

  /**
   * 保存系统状态
   */
  async saveSystemState() {
    try {
      const state = {
        timestamp: new Date().toISOString(),
        portfolio: { ...this.simulator.portfolio },
        cash: this.simulator.currentCapital,
        tradingDays: this.simulator.tradingDays,
        transactionHistory: this.simulator.transactionHistory.slice(-50), // 只保存最近50条
        dailyUpdates: this.simulator.dailyUpdates.slice(-30), // 只保存最近30天
        totalValue: this.simulator.getCurrentPortfolioValue()
      };

      const stateFilePath = path.join(this.tradeLogPath, 'current_state.json');
      await fs.writeFile(stateFilePath, JSON.stringify(state, null, 2), 'utf8');
      console.log(`💾 系统状态已保存: ${stateFilePath}`);
    } catch (error) {
      console.error(`❌ 保存系统状态失败:`, error.message);
    }
  }

  /**
   * 加载系统状态
   */
  async loadSystemState() {
    try {
      const stateFilePath = path.join(this.tradeLogPath, 'current_state.json');
      const stateData = await fs.readFile(stateFilePath, 'utf8');
      const state = JSON.parse(stateData);

      // 恢复状态
      this.simulator.portfolio = state.portfolio || {};
      this.simulator.currentCapital = state.cash;
      this.simulator.tradingDays = state.tradingDays || 0;
      this.simulator.transactionHistory = state.transactionHistory || [];
      this.simulator.dailyUpdates = state.dailyUpdates || [];

      console.log(`📂 系统状态已加载，当前总资产: ¥${this.simulator.getCurrentPortfolioValue().toFixed(2)}`);
    } catch (error) {
      console.log(`⚠️  未能加载系统状态 (可能首次运行):`, error.message);
      // 如果加载失败，使用默认状态
    }
  }

  /**
   * 计算下次交易时间（下一个交易日的上午9:30）
   */
  getNextTradingTime() {
    const now = new Date();
    let nextTradeTime = new Date(now);

    // 设置为当天9:30
    nextTradeTime.setHours(9, 30, 0, 0);

    // 如果已经过了今天的9:30，则设置为明天
    if (now > nextTradeTime) {
      nextTradeTime.setDate(nextTradeTime.getDate() + 1);
    }

    // 检查是否是周末，如果是则跳到周一
    let dayOfWeek = nextTradeTime.getDay();
    if (dayOfWeek === 0) { // Sunday
      nextTradeTime.setDate(nextTradeTime.getDate() + 1);
    } else if (dayOfWeek === 6) { // Saturday
      nextTradeTime.setDate(nextTradeTime.getDate() + 2);
    }

    return nextTradeTime;
  }

  /**
   * 检查是否为交易日
   */
  isTradingDay(date = new Date()) {
    const dayOfWeek = date.getDay();
    // A股交易日为周一到周五
    return dayOfWeek >= 1 && dayOfWeek <= 5;
  }

  /**
   * 启动定时交易
   */
  async startSchedule() {
    console.log("⏰ 启动A股模拟交易定时器...");
    
    // 初始化日志目录
    await this.initializeLogs();
    
    // 尝试加载之前的状态
    await this.loadSystemState();

    // 立即执行一次
    await this.executeDailyTrade();

    // 设置定时任务
    this.scheduleInterval = setInterval(async () => {
      const now = new Date();
      const currentHour = now.getHours();
      const currentMinute = now.getMinutes();

      // 在交易时间段内（9:30-15:00）每小时检查一次
      const isTradingTime = (currentHour === 9 && currentMinute >= 30) || 
                           (currentHour > 9 && currentHour < 15) ||
                           (currentHour === 15 && currentMinute === 0);

      if (this.isTradingDay(now) && isTradingTime) {
        await this.executeDailyTrade();
      }
    }, 60 * 60 * 1000); // 每小时检查一次

    console.log("✅ 定时交易已启动，每小时检查一次交易条件");
  }

  /**
   * 停止定时交易
   */
  stopSchedule() {
    if (this.scheduleInterval) {
      clearInterval(this.scheduleInterval);
      this.scheduleInterval = null;
      console.log("⏸️ 定时交易已停止");
    }
  }

  /**
   * 获取性能报告
   */
  async getPerformanceReport() {
    try {
      // 获取最近的日志文件来生成报告
      const logFiles = await fs.readdir(this.tradeLogPath);
      const recentLogs = logFiles
        .filter(file => file.startsWith('trade_log_') && file.endsWith('.json'))
        .sort()
        .slice(-30); // 最近30天

      let totalPnL = 0;
      let positiveDays = 0;
      let negativeDays = 0;
      let maxDailyGain = -Infinity;
      let maxDailyLoss = Infinity;

      for (const fileName of recentLogs) {
        const filePath = path.join(this.tradeLogPath, fileName);
        const logData = JSON.parse(await fs.readFile(filePath, 'utf8'));
        
        totalPnL += logData.dailyPnL;
        if (logData.dailyPnL > 0) positiveDays++;
        if (logData.dailyPnL < 0) negativeDays++;
        if (logData.dailyPnL > maxDailyGain) maxDailyGain = logData.dailyPnL;
        if (logData.dailyPnL < maxDailyLoss) maxDailyLoss = logData.dailyPnL;
      }

      const winRate = recentLogs.length > 0 ? (positiveDays / recentLogs.length * 100).toFixed(2) : 0;

      console.log("\n🏆 最近30日性能报告:");
      console.log(`📊 交易天数: ${recentLogs.length}`);
      console.log(`📈 总盈亏: ¥${totalPnL.toFixed(2)}`);
      console.log(`🎯 胜率: ${winRate}% (${positiveDays}胜/${negativeDays}负)`);
      console.log(`🔥 最大单日盈利: ¥${maxDailyGain !== -Infinity ? maxDailyGain.toFixed(2) : '0.00'}`);
      console.log(`📉 最大单日亏损: ¥${maxDailyLoss !== Infinity ? maxDailyLoss.toFixed(2) : '0.00'}`);

      // 显示系统当前状态
      this.simulator.getStatusReport();

      return {
        totalPnL,
        winRate: parseFloat(winRate),
        tradingDays: recentLogs.length,
        positiveDays,
        negativeDays,
        maxDailyGain: maxDailyGain !== -Infinity ? maxDailyGain : 0,
        maxDailyLoss: maxDailyLoss !== Infinity ? maxDailyLoss : 0,
        currentState: this.simulator.getStatusReport()
      };
    } catch (error) {
      console.error(`❌ 生成性能报告失败:`, error);
      return null;
    }
  }
}

// 如果直接运行此脚本，启动调度器
if (require.main === module) {
  console.log("🎯 A股AI策略模拟交易调度器");
  console.log("=" .repeat(50));
  
  // 使用提供的TuShare Token
  const TU_SHARE_TOKEN = '[REDACTED]';
  
  const scheduler = new TradingScheduler(100000, TU_SHARE_TOKEN);
  
  // 启动调度器
  scheduler.startSchedule()
    .then(() => {
      console.log("\n🚀 模拟交易调度器已启动！");
      console.log("💡 系统将在每个交易日的交易时间内每小时执行一次模拟交易");
      console.log("📊 可使用 scheduler.getPerformanceReport() 查看性能报告");
      console.log("⏸️  可使用 scheduler.stopSchedule() 停止调度");
      
      // 30秒后显示一次性能报告
      setTimeout(async () => {
        await scheduler.getPerformanceReport();
      }, 30000);
    })
    .catch(error => {
      console.error("❌ 启动调度器失败:", error);
    });

  // 设置优雅退出
  process.on('SIGINT', async () => {
    console.log('\n🛑 正在停止交易调度器...');
    scheduler.stopSchedule();
    
    // 保存最终状态
    try {
      await scheduler.saveSystemState();
      console.log('💾 最终状态已保存');
    } catch (error) {
      console.error('❌ 保存最终状态失败:', error);
    }
    
    process.exit(0);
  });
}

module.exports = TradingScheduler;