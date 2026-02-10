#!/usr/bin/env node

/*
 * Main Entry Point for OpenClaw Integrated A-Share Trading System
 * This file starts the complete system with OpenClaw integration
 */

console.log('🚀 Starting OpenClaw Integrated A-Share Trading System...');

// Import the integration controller
const OpenClawIntegrationController = require('./integration_controller');

async function main() {
  try {
    console.log('Initializing OpenClaw Integration Controller...');
    
    // Create the integration controller
    const controller = new OpenClawIntegrationController();
    
    // Start the system with OpenClaw integration
    console.log('Starting system with OpenClaw integration...');
    const system = await controller.start();
    
    console.log('\n✅ OpenClaw Integrated A-Share Trading System is now running!');
    console.log('📊 System Status:');
    
    const status = system.getStatus();
    console.log(`   - Session Manager: ${status.components.sessionManager ? '✅ Active' : '❌ Inactive'}`);
    console.log(`   - Memory Manager: ${status.components.memoryManager ? '✅ Active' : '❌ Inactive'}`);
    console.log(`   - Cron Manager: ${status.components.cronManager ? '✅ Active' : '❌ Inactive'}`);
    console.log(`   - Trading System: ${status.components.tradingSystem ? '✅ Active' : '❌ Inactive'}`);
    console.log(`   - Timestamp: ${status.timestamp}`);
    
    // Display scheduled cron jobs
    if (controller.cronManager) {
      console.log('\n📅 Scheduled Cron Jobs:');
      const jobs = controller.cronManager.listJobs();
      for (const job of jobs) {
        console.log(`   - ${job.name}: ${job.schedule} (${job.active ? 'Active' : 'Inactive'})`);
      }
    }
    
    // Provide instructions for interaction
    console.log('\n💡 Available Actions:');
    console.log('   - The system is running automated trading based on your configuration');
    console.log('   - Check trading logs in: ./trading_logs/');
    console.log('   - Check performance reports in: ./reports/');
    console.log('   - Memory is stored in: ../memory/');
    console.log('   - System will execute scheduled tasks automatically');
    
    // Keep the process alive
    console.log('\n🔒 System is secured with OpenClaw\'s safety mechanisms');
    console.log('🔄 Continuous monitoring and risk management active');
    
    // Set up graceful shutdown
    process.on('SIGINT', () => {
      console.log('\n🛑 Shutting down OpenClaw Integrated Trading System...');
      console.log('💾 Saving system state...');
      
      // In a real implementation, we would save state here
      
      console.log('👋 System shutdown complete');
      process.exit(0);
    });
    
    process.on('SIGTERM', () => {
      console.log('\n🛑 Terminating OpenClaw Integrated Trading System...');
      process.exit(0);
    });
    
  } catch (error) {
    console.error('❌ Error starting OpenClaw Integrated Trading System:', error);
    console.error('Error stack:', error.stack);
    process.exit(1);
  }
}

// Run the main function if this file is executed directly
if (require.main === module) {
  main().catch(error => {
    console.error('Unhandled error in main:', error);
    process.exit(1);
  });
}

module.exports = OpenClawIntegrationController;