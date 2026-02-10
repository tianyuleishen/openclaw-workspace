#!/usr/bin/env node

/*
 * System Status Checker for OpenClaw Integrated A-Share Trading System
 * This script checks the status of the integrated system
 */

const fs = require('fs');
const path = require('path');

function checkSystemStatus() {
    console.log('🔍 Checking OpenClaw Integrated A-Share Trading System Status...\n');
    
    // Check if main files exist
    const mainFiles = [
        'openclaw_integration_main.js',
        'integration_controller.js',
        'trading_system.js',
        'config/openclaw_config.json'
    ];
    
    console.log('📁 File Structure Check:');
    for (const file of mainFiles) {
        const filePath = path.join(__dirname, file);
        const exists = fs.existsSync(filePath);
        console.log(`   ${exists ? '✅' : '❌'} ${file}`);
    }
    
    // Check directories
    const directories = [
        'data',
        'logs',
        'reports',
        'trading_logs',
        'config',
        '../memory'
    ];
    
    console.log('\n📂 Directory Check:');
    for (const dir of directories) {
        const dirPath = path.join(__dirname, dir);
        const exists = fs.existsSync(dirPath);
        console.log(`   ${exists ? '✅' : '❌'} ${dir}/`);
    }
    
    // Check config file content
    console.log('\n⚙️  Configuration Check:');
    const configPath = path.join(__dirname, 'config', 'openclaw_config.json');
    if (fs.existsSync(configPath)) {
        try {
            const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
            
            console.log('   ✅ Config file is valid JSON');
            console.log(`   🏭 Agents configured: ${config.agents?.list?.length || 0}`);
            console.log(`   ⏰ Cron enabled: ${config.cron?.enabled ? 'Yes' : 'No'}`);
            console.log(`   🧠 Memory search enabled: ${config.memorySearch?.enabled ? 'Yes' : 'No'}`);
        } catch (error) {
            console.log(`   ❌ Config file error: ${error.message}`);
        }
    } else {
        console.log('   ❌ Config file does not exist');
    }
    
    // Check recent trading logs
    console.log('\n📈 Recent Trading Activity:');
    const logsDir = path.join(__dirname, 'trading_logs');
    if (fs.existsSync(logsDir)) {
        const logFiles = fs.readdirSync(logsDir).filter(f => f.endsWith('.json')).sort().reverse();
        
        if (logFiles.length > 0) {
            console.log(`   ✅ Found ${logFiles.length} trading log files`);
            
            // Check the most recent log
            if (logFiles[0]) {
                try {
                    const recentLogPath = path.join(logsDir, logFiles[0]);
                    const recentLog = JSON.parse(fs.readFileSync(recentLogPath, 'utf8'));
                    
                    if (Array.isArray(recentLog) && recentLog.length > 0) {
                        const lastEntry = recentLog[recentLog.length - 1];
                        console.log(`   📅 Last activity: ${new Date(lastEntry.timestamp).toLocaleString()}`);
                        console.log(`   💰 Balance: ¥${lastEntry.balance?.toLocaleString()}`);
                        console.log(`   📊 Trades executed: ${lastEntry.executions?.length || 0}`);
                    }
                } catch (error) {
                    console.log(`   ❌ Error reading recent log: ${error.message}`);
                }
            }
        } else {
            console.log('   📋 No trading logs found (system may be new)');
        }
    } else {
        console.log('   ❌ Trading logs directory does not exist');
    }
    
    // Check performance reports
    console.log('\n📋 Performance Reports:');
    const reportsDir = path.join(__dirname, 'reports');
    if (fs.existsSync(reportsDir)) {
        const reportFiles = fs.readdirSync(reportsDir).filter(f => f.endsWith('.json')).sort().reverse();
        
        if (reportFiles.length > 0) {
            console.log(`   ✅ Found ${reportFiles.length} performance reports`);
            
            if (reportFiles[0]) {
                try {
                    const recentReportPath = path.join(reportsDir, reportFiles[0]);
                    const recentReport = JSON.parse(fs.readFileSync(recentReportPath, 'utf8'));
                    
                    if (recentReport.summary) {
                        console.log(`   📅 Latest report: ${reportFiles[0].replace('_performance.json', '')}`);
                        console.log(`   💰 Portfolio value: ¥${recentReport.summary.portfolioValue?.toLocaleString()}`);
                        console.log(`   📈 Total return: ${recentReport.summary.totalReturn}`);
                    }
                } catch (error) {
                    console.log(`   ❌ Error reading recent report: ${error.message}`);
                }
            }
        } else {
            console.log('   📋 No performance reports found');
        }
    } else {
        console.log('   ❌ Reports directory does not exist');
    }
    
    // Check memory directory
    console.log('\n🧠 Memory System:');
    const memoryDir = path.join(__dirname, '..', 'memory');
    if (fs.existsSync(memoryDir)) {
        const memoryFiles = fs.readdirSync(memoryDir).filter(f => f.endsWith('.json'));
        console.log(`   ✅ Memory directory exists with ${memoryFiles.length} items`);
    } else {
        console.log('   ℹ️  Memory directory does not exist (may be created when needed)');
    }
    
    // System readiness summary
    console.log('\n🎯 System Readiness Summary:');
    
    const hasMainFiles = mainFiles.every(file => fs.existsSync(path.join(__dirname, file)));
    const hasRequiredDirs = ['data', 'logs', 'reports', 'trading_logs'].every(dir => fs.existsSync(path.join(__dirname, dir)));
    const hasConfig = fs.existsSync(configPath);
    
    const readinessScore = [
        hasMainFiles,
        hasRequiredDirs,
        hasConfig,
        fs.existsSync(logsDir),
        fs.existsSync(reportsDir)
    ].filter(Boolean).length;
    
    const totalChecks = 5;
    const percentage = Math.round((readinessScore / totalChecks) * 100);
    
    console.log(`   Status: ${percentage}% ready (${readinessScore}/${totalChecks} critical components)`);
    
    if (percentage === 100) {
        console.log('   🟢 System is fully ready for operation!');
        console.log('   🚀 Run: node openclaw_integration_main.js');
    } else if (percentage >= 80) {
        console.log('   🟡 System is mostly ready, minor components missing');
        console.log('   💡 Consider running the system to initialize missing components');
    } else {
        console.log('   🔴 System needs additional setup before operation');
        console.log('   ❗ Please ensure all required files and directories exist');
    }
    
    console.log('\n💡 Quick Start Command:');
    console.log('   cd ~/.openclaw/workspace/a_stock_simulation');
    console.log('   node openclaw_integration_main.js');
}

// Run the check if executed directly
if (require.main === module) {
    checkSystemStatus();
}

module.exports = checkSystemStatus;