/**
 * A股AI策略模拟交易系统启动脚本
 * 
 * 一键启动整个模拟交易系统
 */

const TradingConsole = require('./trading_console');
const fs = require('fs').promises;
const path = require('path');

async function initializeSystem() {
  console.log("🚀 A股AI策略模拟交易系统初始化");
  console.log("=" .repeat(60));
  console.log("📅 时间:", new Date().toLocaleString('zh-CN'));
  console.log("📍 路径:", __dirname);
  console.log("");

  try {
    // 检查必要文件是否存在
    const requiredFiles = [
      './stock_simulator.js',
      './advanced_strategy.js', 
      './fixed_optimized_simulator.js',
      './enhanced_simulator_with_tushare.js',
      './daily_trading_scheduler.js',
      './trading_console.js'
    ];

    console.log("🔍 检查系统文件...");
    for (const file of requiredFiles) {
      try {
        await fs.access(path.join(__dirname, file));
        console.log(`✅ ${file} - 存在`);
      } catch (error) {
        console.log(`❌ ${file} - 缺失`);
        throw new Error(`缺少必要文件: ${file}`);
      }
    }
    console.log("");

    // 创建交易日志目录
    console.log("📁 创建交易日志目录...");
    const logDir = path.join(__dirname, 'trading_logs');
    await fs.mkdir(logDir, { recursive: true });
    console.log(`✅ 交易日志目录已创建: ${logDir}`);
    console.log("");

    // 显示系统配置信息
    console.log("⚙️  系统配置信息:");
    console.log("   • 初始资金: ¥100,000");
    console.log("   • TuShare Token: 已配置");
    console.log("   • 交易品种: A股主要股票");
    console.log("   • 策略类型: AI多因子策略");
    console.log("   • 风险控制: 动态止盈止损");
    console.log("");

    // 显示系统特性
    console.log("🌟 系统特性:");
    console.log("   • AI驱动的多因子交易策略");
    console.log("   • 实时市场数据集成（TuShare）");
    console.log("   • 动态风险管理（8%止损，15%止盈）");
    console.log("   • 自动化交易执行");
    console.log("   • 详细的性能分析报告");
    console.log("   • 交互式控制台管理");
    console.log("");

    console.log("🎯 系统初始化完成！");
    console.log("💡 接下来将启动交互式控制台...");
    console.log("");

    // 启动控制台
    const consoleApp = new TradingConsole();
    await consoleApp.init();
    
  } catch (error) {
    console.error("❌ 系统初始化失败:", error.message);
    console.error("🔧 请检查文件完整性并重试");
    process.exit(1);
  }
}

// 如果直接运行此脚本，启动初始化
if (require.main === module) {
  initializeSystem().catch(error => {
    console.error("💥 初始化过程发生错误:", error);
    process.exit(1);
  });
}

module.exports = { initializeSystem };