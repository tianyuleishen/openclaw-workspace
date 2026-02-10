#!/usr/bin/env node
/**
 * OpenClaw System Monitor
 * Monitors OpenClaw processes, handles crashes, and ensures continuous operation
 */

const { spawn, exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const http = require('http');

class OpenClawSystemMonitor {
  constructor(options = {}) {
    this.options = {
      watchDir: options.watchDir || '/home/admin/.openclaw',
      logDir: options.logDir || '/home/admin/.openclaw/logs',
      maxMemory: options.maxMemory || 500 * 1024 * 1024, // 500MB
      maxRestarts: options.maxRestarts || 5,
      restartDelay: options.restartDelay || 5000, // 5 seconds
      healthCheckInterval: options.healthCheckInterval || 30000, // 30 seconds
      ...options
    };
    
    this.processes = new Map();
    this.restartCount = 0;
    this.startTime = new Date();
    this.crashHistory = [];
    this.status = 'initializing';
    
    // Ensure directories
    this.ensureDirs();
    
    // Setup crash recovery
    this.setupCrashRecovery();
    
    console.log('🛡️  OpenClaw System Monitor initialized');
    console.log(`📁 Watch directory: ${this.options.watchDir}`);
    console.log(`📁 Log directory: ${this.options.logDir}`);
    
    // Start monitoring
    this.start();
  }
  
  ensureDirs() {
    for (const dir of [this.options.logDir, path.join(this.options.logDir, 'archive')]) {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
        console.log(`📁 Created directory: ${dir}`);
      }
    }
  }
  
  setupCrashRecovery() {
    this.crashRecoveryFile = path.join(this.options.logDir, '.system_monitor_recovery.json');
    
    try {
      if (fs.existsSync(this.crashRecoveryFile)) {
        const data = JSON.parse(fs.readFileSync(this.crashRecoveryFile, 'utf8'));
        console.log('📄 Found previous crash recovery data');
        console.log(`   Last crash: ${data.lastCrashTime || 'N/A'}`);
        console.log(`   Total restarts since then: ${data.totalRestarts || 0}`);
        
        // Log crash summary
        if (data.crashDetails && data.crashDetails.length > 0) {
          console.log('\n📊 Recent Crashes:');
          data.crashDetails.slice(-5).forEach((crash, i) => {
            console.log(`   ${i+1}. ${crash.timestamp}`);
            console.log(`      Exit code: ${crash.exitCode}`);
            console.log(`      Signal: ${crash.signal || 'N/A'}`);
            console.log(`      Memory: ${Math.round(crash.memoryUsage/1024/1024)}MB`);
          });
        }
      }
    } catch (error) {
      console.warn('Could not load crash recovery:', error.message);
    }
  }
  
  async start() {
    this.status = 'running';
    
    // Start watching for OpenClaw processes
    this.startProcessWatcher();
    
    // Start health check server
    this.startHealthServer();
    
    // Start periodic health checks
    this.startHealthChecks();
    
    console.log('✅ System monitor is running');
    console.log(`🆔 Monitor ID: ${this.generateMonitorId()}`);
    console.log('\n📊 Process Status:');
    this.printProcessStatus();
  }
  
  generateMonitorId() {
    const now = new Date();
    return `monitor_${now.getFullYear()}${(now.getMonth()+1).toString().padStart(2,'0')}${now.getDate().toString().padStart(2,'0')}_${now.getHours().toString().padStart(2,'0')}${now.getMinutes().toString().padStart(2,'0')}`;
  }
  
  startProcessWatcher() {
    // Watch for new OpenClaw processes
    setInterval(() => {
      this.checkRunningProcesses();
    }, 5000);
  }
  
  checkRunningProcesses() {
    // Get all running node processes
    exec('ps aux | grep -E "(node|openclaw)" | grep -v grep', (error, stdout, stderr) => {
      if (error) return;
      
      const lines = stdout.trim().split('\n');
      const processes = [];
      
      lines.forEach(line => {
        const parts = line.trim().split(/\s+/);
        if (parts.length >= 2 && parts[0] === 'admin') {
          const pid = parseInt(parts[1]);
          const command = parts.slice(10).join(' ');
          
          if (command.includes('openclaw') || 
              command.includes('entry.mjs') ||
              command.includes('gateway')) {
            processes.push({ pid, command, memory: parseFloat(parts[5]) * 1024 });
          }
        }
      });
      
      // Check memory usage
      for (const proc of processes) {
        if (proc.memory > this.options.maxMemory) {
          console.log(`⚠️  High memory usage detected: PID ${proc.memory} MB`);
          this.logProcessEvent('high_memory', proc);
        }
      }
    });
  }
  
  async startOpenClaw() {
    if (this.restartCount >= this.options.maxRestarts) {
      console.log('❌ Max restarts reached, stopping...');
      this.status = 'stopped';
      return;
    }
    
    this.restartCount++;
    console.log(`\n🚀 Starting OpenClaw (attempt ${this.restartCount}/${this.options.maxRestarts})`);
    
    const env = {
      ...process.env,
      OPENCLAW_LOG_DIR: this.options.logDir,
      OPENCLAW_MONITOR_ID: this.generateMonitorId()
    };
    
    // Try to find and start OpenClaw
    const openclawPath = path.join(this.options.watchDir, 'node_modules/.bin/openclaw');
    
    let openclawProcess;
    if (fs.existsSync(openclawPath)) {
      openclawProcess = spawn(openclawPath, ['gateway', 'start'], {
        env,
        cwd: this.options.watchDir,
        stdio: ['pipe', 'pipe', 'pipe']
      });
    } else {
      // Try direct node execution
      console.log('⚠️  openclaw command not found, monitoring directory only');
      return;
    }
    
    // Setup process handlers
    openclawProcess.stdout.on('data', (data) => {
      this.logProcessOutput('stdout', data.toString());
    });
    
    openclawProcess.stderr.on('data', (data) => {
      this.logProcessOutput('stderr', data.toString());
    });
    
    openclawProcess.on('exit', (code, signal) => {
      this.handleProcessExit(code, signal);
    });
    
    openclawProcess.on('error', (error) => {
      console.error(`❌ Process error: ${error.message}`);
      this.logProcessEvent('error', { error: error.message });
    });
    
    // Store process info
    this.processes.set(openclawProcess.pid, {
      process: openclawProcess,
      startTime: new Date(),
      restartNumber: this.restartCount
    });
    
    console.log(`✅ OpenClaw started with PID ${openclawProcess.pid}`);
  }
  
  logProcessOutput(type, data) {
    const logFile = path.join(this.options.logDir, 'process_output.log');
    const timestamp = new Date().toISOString();
    const prefix = `[${timestamp}] [${type.toUpperCase()}]`;
    
    fs.appendFileSync(logFile, `${prefix} ${data}`);
  }
  
  handleProcessExit(code, signal) {
    console.log(`\n⚠️  OpenClaw process exited with code ${code}, signal ${signal || 'N/A'}`);
    
    // Log crash
    const crashInfo = {
      timestamp: new Date().toISOString(),
      exitCode: code,
      signal: signal,
      restartNumber: this.restartCount,
      uptime: process.uptime(),
      memoryUsage: process.memoryUsage(),
      pid: this.processes.get(code)?.process?.pid
    };
    
    this.crashHistory.push(crashInfo);
    this.saveCrashInfo(crashInfo);
    
    // Remove from processes
    this.processes.delete(code);
    
    // Schedule restart
    if (this.restartCount < this.options.maxRestarts) {
      console.log(`⏰ Scheduling restart in ${this.options.restartDelay/1000} seconds...`);
      setTimeout(() => {
        this.startOpenClaw();
      }, this.options.restartDelay);
    } else {
      console.log('❌ Max restarts reached, not restarting');
      this.status = 'stopped';
    }
  }
  
  saveCrashInfo(crashInfo) {
    try {
      const crashLogFile = path.join(this.options.logDir, 'crash_history.log');
      const logEntry = `\n=== Crash Report ===\nTimestamp: ${crashInfo.timestamp}\nExit Code: ${crashInfo.exitCode}\nSignal: ${crashInfo.signal}\nRestart Number: ${crashInfo.restartNumber}\nUptime: ${crashInfo.uptime}s\nMemory: ${Math.round(crashInfo.memoryUsage.heapUsed/1024/1024)}MB / ${Math.round(crashInfo.memoryUsage.heapTotal/1024/1024)}MB\n\n`;
      
      fs.appendFileSync(crashLogFile, logEntry);
      
      // Update recovery file
      const recoveryData = {
        lastCrashTime: crashInfo.timestamp,
        lastExitCode: crashInfo.exitCode,
        totalRestarts: this.restartCount,
        crashDetails: this.crashHistory.slice(-10)
      };
      
      fs.writeFileSync(this.crashRecoveryFile, JSON.stringify(recoveryData, null, 2));
    } catch (error) {
      console.error('Error saving crash info:', error.message);
    }
  }
  
  logProcessEvent(event, data) {
    const logFile = path.join(this.options.logDir, 'monitor_events.log');
    const timestamp = new Date().toISOString();
    const entry = `[${timestamp}] [${event}] ${JSON.stringify(data)}\n`;
    
    fs.appendFileSync(logFile, entry);
  }
  
  startHealthServer() {
    const server = http.createServer((req, res) => {
      const health = this.getHealthStatus();
      
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(health, null, 2));
    });
    
    server.listen(3008, () => {
      console.log('📊 Health check server running on http://localhost:3008');
    });
  }
  
  getHealthStatus() {
    return {
      status: this.status,
      monitorId: this.generateMonitorId(),
      uptime: process.uptime(),
      restartCount: this.restartCount,
      activeProcesses: this.processes.size,
      crashHistory: this.crashHistory.slice(-5),
      memoryUsage: process.memoryUsage(),
      diskSpace: this.getDiskSpace(),
      lastCheck: new Date().toISOString()
    };
  }
  
  getDiskSpace() {
    try {
      const stats = fs.statSync(this.options.logDir);
      const dirSize = this.getDirSize(this.options.logDir);
      
      return {
        logDirectorySize: dirSize,
        freeSpace: require('os').freemem()
      };
    } catch (error) {
      return { error: error.message };
    }
  }
  
  getDirSize(dir) {
    let size = 0;
    if (!fs.existsSync(dir)) return 0;
    
    const files = fs.readdirSync(dir);
    for (const file of files) {
      const filePath = path.join(dir, file);
      const stat = fs.statSync(filePath);
      if (stat.isDirectory()) {
        size += this.getDirSize(filePath);
      } else {
        size += stat.size;
      }
    }
    return size;
  }
  
  startHealthChecks() {
    setInterval(() => {
      const health = this.getHealthStatus();
      
      // Log health status
      this.logProcessEvent('health_check', health);
      
      // Check for issues
      if (health.memoryUsage.heapUsed > this.options.maxMemory) {
        console.log('⚠️  Memory usage too high, scheduling restart...');
        this.logProcessEvent('memory_warning', { 
          current: health.memoryUsage.heapUsed,
          limit: this.options.maxMemory
        });
      }
      
      // Print status
      console.log(`\n📊 Health Check - ${health.lastCheck.split('T')[1].split('.')[0]}`);
      console.log(`   Status: ${health.status}`);
      console.log(`   Uptime: ${Math.floor(health.uptime)}s`);
      console.log(`   Restarts: ${health.restartCount}`);
      console.log(`   Memory: ${Math.round(health.memoryUsage.heapUsed/1024/1024)}MB`);
      
    }, this.options.healthCheckInterval);
  }
  
  printProcessStatus() {
    if (this.processes.size === 0) {
      console.log('   No active OpenClaw processes');
    } else {
      this.processes.forEach((info, pid) => {
        console.log(`   PID ${pid}: Running (started ${info.startTime.toISOString()})`);
      });
    }
  }
}

// Export for use
module.exports = { OpenClawSystemMonitor };

// CLI usage
if (require.main === module) {
  const monitor = new OpenClawSystemMonitor({
    watchDir: process.argv[2] || '/home/admin/.openclaw',
    logDir: process.argv[3] || '/home/admin/.openclaw/logs'
  });
  
  console.log('\n🛡️  System monitor is running. Press Ctrl+C to exit.\n');
}
