/**
 * A股AI策略模拟交易控制台
 * 
 * 提供交互式界面来监控和管理模拟交易系统
 */

const TradingScheduler = require('./daily_trading_scheduler');
const fs = require('fs').promises;
const path = require('path');

class TradingConsole {
  constructor() {
    this.scheduler = null;
    this.token = '[REDACTED]'; // 使用提供的Token
    this.running = false;
  }

  /**
   * 初始化系统
   */
  async init() {
    console.log("🎯 A股AI策略模拟交易控制台");
    console.log("=" .repeat(50));
    console.log("💡 系统初始化中...");
    
    this.scheduler = new TradingScheduler(100000, this.token);
    
    // 初始化调度器但不启动定时任务
    await this.scheduler.initializeLogs();
    await this.scheduler.loadSystemState();
    
    console.log("✅ 系统初始化完成");
    this.showMenu();
  }

  /**
   * 显示主菜单
   */
  showMenu() {
    console.log("\n" + "=".repeat(50));
    console.log("📋 A股AI策略模拟交易控制台 - 主菜单");
    console.log("=".repeat(50));
    console.log("1. 🚀 启动自动交易调度器");
    console.log("2. ⏸️  停止自动交易调度器");
    console.log("3. 📊 执行单次模拟交易");
    console.log("4. 📈 查看系统状态");
    console.log("5. 📊 查看性能报告");
    console.log("6. 📋 查看交易历史");
    console.log("7. 📅 查看最近交易日志");
    console.log("8. 🛠️  重新加载系统状态");
    console.log("9. ❓ 帮助信息");
    console.log("0. 🚪 退出系统");
    console.log("=".repeat(50));
    console.log("请输入选项编号 (0-9):");
  }

  /**
   * 处理用户输入
   */
  async handleInput(input) {
    const choice = input.trim();
    
    switch(choice) {
      case '1':
        await this.startScheduler();
        break;
      case '2':
        await this.stopScheduler();
        break;
      case '3':
        await this.executeSingleTrade();
        break;
      case '4':
        await this.showStatus();
        break;
      case '5':
        await this.showPerformance();
        break;
      case '6':
        await this.showTransactionHistory();
        break;
      case '7':
        await this.showRecentLogs();
        break;
      case '8':
        await this.reloadState();
        break;
      case '9':
        this.showHelp();
        break;
      case '0':
        await this.exit();
        return false; // 返回false表示退出
      default:
        console.log("❌ 无效选项，请输入0-9之间的数字");
    }
    
    // 显示菜单并继续等待输入
    this.showMenu();
    return true; // 返回true表示继续运行
  }

  /**
   * 启动调度器
   */
  async startScheduler() {
    if (this.running) {
      console.log("⚠️  调度器已在运行中！");
      return;
    }
    
    console.log("🚀 启动自动交易调度器...");
    try {
      await this.scheduler.startSchedule();
      this.running = true;
      console.log("✅ 自动交易调度器已启动");
    } catch (error) {
      console.error("❌ 启动调度器失败:", error.message);
    }
  }

  /**
   * 停止调度器
   */
  async stopScheduler() {
    if (!this.running) {
      console.log("⚠️  调度器未在运行！");
      return;
    }
    
    console.log("⏸️ 停止自动交易调度器...");
    this.scheduler.stopSchedule();
    this.running = false;
    console.log("✅ 自动交易调度器已停止");
  }

  /**
   * 执行单次模拟交易
   */
  async executeSingleTrade() {
    console.log("🔄 执行单次模拟交易...");
    try {
      await this.scheduler.executeDailyTrade();
      console.log("✅ 单次模拟交易执行完成");
    } catch (error) {
      console.error("❌ 单次模拟交易执行失败:", error.message);
    }
  }

  /**
   * 显示系统状态
   */
  async showStatus() {
    console.log("📈 获取系统状态...");
    try {
      this.scheduler.simulator.getStatusReport();
    } catch (error) {
      console.error("❌ 获取系统状态失败:", error.message);
    }
  }

  /**
   * 显示性能报告
   */
  async showPerformance() {
    console.log("📊 生成性能报告...");
    try {
      await this.scheduler.getPerformanceReport();
    } catch (error) {
      console.error("❌ 生成性能报告失败:", error.message);
    }
  }

  /**
   * 显示交易历史
   */
  async showTransactionHistory() {
    console.log("📋 获取交易历史...");
    try {
      const history = this.scheduler.simulator.transactionHistory;
      const recent = history.slice(-10); // 显示最近10笔交易
      
      if (recent.length === 0) {
        console.log("📊 暂无交易历史");
        return;
      }
      
      console.log(`\n📊 最近 ${recent.length} 笔交易:`);
      for (let i = 0; i < recent.length; i++) {
        const tx = recent[i];
        console.log(`   ${i+1}. ${tx.date.split('T')[0]} ${tx.action} ${tx.symbol} ${tx.quantity}股 @ ¥${tx.price.toFixed(2)} (${tx.value > 0 ? '+' : ''}${tx.value.toFixed(2)})`);
      }
    } catch (error) {
      console.error("❌ 获取交易历史失败:", error.message);
    }
  }

  /**
   * 显示最近日志
   */
  async showRecentLogs() {
    console.log("📅 获取最近交易日志...");
    try {
      const logPath = path.join(__dirname, 'trading_logs');
      const logFiles = await fs.readdir(logPath);
      const recentLogs = logFiles
        .filter(file => file.startsWith('trade_log_') && file.endsWith('.json'))
        .sort()
        .slice(-5); // 最近5个日志文件

      if (recentLogs.length === 0) {
        console.log("📊 暂无交易日志");
        return;
      }

      console.log(`\n📊 最近 ${recentLogs.length} 天的交易摘要:`);
      for (const fileName of recentLogs) {
        const filePath = path.join(logPath, fileName);
        const logData = JSON.parse(await fs.readFile(filePath, 'utf8'));
        const date = fileName.replace('trade_log_', '').replace('.json', '');
        console.log(`   ${date}: ${logData.dailyReturn > 0 ? '+' : ''}${logData.dailyReturn.toFixed(2)}% (${logData.tradeCount}笔交易)`);
      }
    } catch (error) {
      console.error("❌ 获取交易日志失败:", error.message);
    }
  }

  /**
   * 重新加载系统状态
   */
  async reloadState() {
    console.log("🔄 重新加载系统状态...");
    try {
      await this.scheduler.loadSystemState();
      console.log("✅ 系统状态已重新加载");
    } catch (error) {
      console.error("❌ 重新加载系统状态失败:", error.message);
    }
  }

  /**
   * 显示帮助信息
   */
  showHelp() {
    console.log("\n❓ 帮助信息:");
    console.log("🎯 A股AI策略模拟交易系统");
    console.log("");
    console.log("📊 系统功能:");
    console.log("   • AI驱动的交易策略");
    console.log("   • 动态止盈止损机制");
    console.log("   • 风险管理系统");
    console.log("   • 实时性能监控");
    console.log("");
    console.log("🔐 Token信息:");
    console.log("   • 已配置TuShare Token");
    console.log("   • 积分余额: 2000分");
    console.log("   • 请注意调用频率限制");
    console.log("");
    console.log("📈 策略参数:");
    console.log("   • 最大持仓: 8只股票");
    console.log("   • 单次风险: 3%");
    console.log("   • 止损线: 8%");
    console.log("   • 止盈线: 15%");
    console.log("");
    console.log("💡 使用建议:");
    console.log("   1. 首次使用请执行单次交易测试");
    console.log("   2. 然后启动自动调度器进行持续交易");
    console.log("   3. 定期查看性能报告调整策略");
    console.log("   4. 监控账户状态和风险指标");
  }

  /**
   * 退出系统
   */
  async exit() {
    console.log("🛑 正在退出系统...");
    
    // 如果调度器在运行，先停止它
    if (this.running) {
      this.scheduler.stopSchedule();
      this.running = false;
      console.log("✅ 调度器已停止");
    }
    
    // 保存最终状态
    try {
      await this.scheduler.saveSystemState();
      console.log("💾 最终状态已保存");
    } catch (error) {
      console.error("❌ 保存最终状态失败:", error.message);
    }
    
    console.log("👋 感谢使用A股AI策略模拟交易系统！");
  }

  /**
   * 启动控制台
   */
  async start() {
    await this.init();
    
    // 设置输入监听
    const readline = require('readline');
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    // 显示菜单
    this.showMenu();

    rl.on('line', async (input) => {
      const continueRunning = await this.handleInput(input);
      if (!continueRunning) {
        rl.close();
      }
    });

    rl.on('close', () => {
      console.log('\n👋 控制台已关闭');
      process.exit(0);
    });
  }
}

// 如果直接运行此脚本，启动控制台
if (require.main === module) {
  const consoleApp = new TradingConsole();
  consoleApp.start().catch(error => {
    console.error("❌ 控制台启动失败:", error);
    process.exit(1);
  });
}

module.exports = TradingConsole;