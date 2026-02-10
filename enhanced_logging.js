#!/usr/bin/env node
/**
 * OpenClaw Enhanced Logging System
 * Enhanced logging with crash recovery, log rotation, and structured output
 */

const fs = require('fs');
const path = require('path');
const { EventEmitter } = require('events');

class OpenClawLogger extends EventEmitter {
  constructor(options = {}) {
    super();
    
    this.options = {
      logDir: options.logDir || '/home/admin/.openclaw/logs',
      maxFileSize: options.maxFileSize || 10 * 1024 * 1024, // 10MB
      maxFiles: options.maxFiles || 10,
      retentionDays: options.retentionDays || 30,
      flushInterval: options.flushInterval || 5000, // 5 seconds
      enableConsole: options.enableConsole !== false,
      enableFile: options.enableFile !== false,
      logLevel: options.logLevel || 'info',
      ...options
    };
    
    this.logQueue = [];
    this.currentLogFile = null;
    this.currentLogSize = 0;
    this.startTime = new Date();
    this.crashRecoveryFile = path.join(this.options.logDir, '.crash_recovery.json');
    this.sessionId = this.generateSessionId();
    
    // Ensure log directory exists
    this.ensureLogDir();
    
    // Initialize current log file
    this.initLogFile();
    
    // Load crash recovery state
    this.loadCrashRecovery();
    
    // Start flush interval
    this.startFlushInterval();
    
    // Handle process events
    this.setupProcessHandlers();
    
    console.log('📝 OpenClaw Enhanced Logging System initialized');
    console.log(`📁 Log directory: ${this.options.logDir}`);
    console.log(`🆔 Session ID: ${this.sessionId}`);
  }
  
  generateSessionId() {
    const now = new Date();
    return `session_${now.getFullYear()}${(now.getMonth()+1).toString().padStart(2,'0')}${now.getDate().toString().padStart(2,'0')}_${now.getHours().toString().padStart(2,'0')}${now.getMinutes().toString().padStart(2,'0')}_${Math.random().toString(36).substr(2, 6)}`;
  }
  
  ensureLogDir() {
    if (!fs.existsSync(this.options.logDir)) {
      fs.mkdirSync(this.options.logDir, { recursive: true });
      console.log(`📁 Created log directory: ${this.options.logDir}`);
    }
  }
  
  initLogFile() {
    const now = new Date();
    const dateStr = now.toISOString().split('T')[0];
    const logFileName = `openclaw_${dateStr}.log`;
    this.currentLogFile = path.join(this.options.logDir, logFileName);
    this.currentLogSize = fs.existsSync(this.currentLogFile) ? fs.statSync(this.currentLogFile).size : 0;
    
    // Write session header if new file
    if (this.currentLogSize === 0) {
      this.writeToFile(`# OpenClaw Log File\n# Created: ${new Date().toISOString()}\n# Session ID: ${this.sessionId}\n\n`);
    }
  }
  
  loadCrashRecovery() {
    try {
      if (fs.existsSync(this.crashRecoveryFile)) {
        const data = JSON.parse(fs.readFileSync(this.crashRecoveryFile, 'utf8'));
        console.log('📄 Found crash recovery file');
        console.log(`   Last session: ${data.lastSessionId}`);
        console.log(`   Last crash: ${data.lastCrashTime || 'N/A'}`);
        console.log(`   Uptime: ${data.uptime || 'N/A'}`);
        
        // Log crash info to file
        this.log('warn', 'System Recovery', {
          message: 'Recovered from previous session',
          lastSessionId: data.lastSessionId,
          lastCrashTime: data.lastCrashTime,
          uptime: data.uptime
        });
      }
    } catch (error) {
      console.warn('Could not load crash recovery file:', error.message);
    }
  }
  
  setupProcessHandlers() {
    // Handle graceful shutdown
    process.on('SIGTERM', () => this.shutdown('SIGTERM'));
    process.on('SIGINT', () => this.shutdown('SIGINT'));
    
    // Handle uncaught exceptions
    process.on('uncaughtException', (error) => {
      this.log('error', 'Uncaught Exception', {
        message: error.message,
        stack: error.stack,
        pid: process.pid
      });
      this.shutdown('uncaughtException');
    });
    
    // Handle unhandled promise rejections
    process.on('unhandledRejection', (reason, promise) => {
      this.log('error', 'Unhandled Rejection', {
        reason: reason?.toString() || String(reason),
        pid: process.pid
      });
    });
    
    // Log process metrics periodically
    setInterval(() => {
      this.log('info', 'Process Metrics', {
        pid: process.pid,
        memoryUsage: process.memoryUsage(),
        cpuUsage: process.cpuUsage(),
        uptime: process.uptime()
      });
    }, 60000); // Every minute
  }
  
  startFlushInterval() {
    setInterval(() => {
      this.flush();
    }, this.options.flushInterval);
  }
  
  log(level, category, data) {
    const logEntry = {
      timestamp: new Date().toISOString(),
      level: level.toUpperCase(),
      category,
      data,
      sessionId: this.sessionId,
      pid: process.pid,
      memoryUsage: process.memoryUsage().heapUsed,
      uptime: process.uptime()
    };
    
    this.logQueue.push(logEntry);
    
    // Emit event for real-time processing
    this.emit('log', logEntry);
    
    // Console output
    if (this.options.enableConsole) {
      this.consoleOutput(logEntry);
    }
    
    // Check for crash recovery marker
    if (level === 'error' || level === 'fatal') {
      this.saveCrashMarker(logEntry);
    }
  }
  
  consoleOutput(entry) {
    const colors = {
      debug: '\x1b[90m',
      info: '\x1b[32m',
      warn: '\x1b[33m',
      error: '\x1b[31m',
      fatal: '\x1b[35m'
    };
    
    const color = colors[entry.level] || '\x1b[0m';
    const reset = '\x1b[0m';
    
    const timestamp = entry.timestamp.split('T')[1].split('.')[0];
    const message = typeof entry.data === 'object' 
      ? JSON.stringify(entry.data, null, 2)
      : entry.data;
    
    console.log(`${color}[${timestamp}] [${entry.level.toUpperCase()}] [${entry.category}]${reset}`);
    console.log(`  ${message}`);
  }
  
  writeToFile(content) {
    if (!this.options.enableFile) return;
    
    try {
      fs.appendFileSync(this.currentLogFile, content);
      this.currentLogSize += Buffer.byteLength(content);
      
      // Check for log rotation
      if (this.currentLogSize > this.options.maxFileSize) {
        this.rotateLogs();
      }
    } catch (error) {
      console.error('Error writing to log file:', error.message);
    }
  }
  
  flush() {
    if (this.logQueue.length === 0) return;
    
    const entries = [...this.logQueue];
    this.logQueue = [];
    
    // Format for file output
    const content = entries.map(entry => {
      const dataStr = typeof entry.data === 'object' 
        ? JSON.stringify(entry.data, null, 2).replace(/\n/g, '\n  ')
        : entry.data;
      
      return `[${entry.timestamp}] [${entry.level}] [${entry.category}] [PID:${entry.pid}] [Uptime:${entry.uptime.toFixed(1)}s]
  ${dataStr}
`;
    }).join('\n');
    
    this.writeToFile(content + '\n');
    
    // Update crash recovery
    this.updateCrashRecovery();
  }
  
  rotateLogs() {
    const dateStr = new Date().toISOString().split('T')[0];
    const timestamp = new Date().toTimeString().split(' ')[0].replace(/:/g, '-');
    const archiveName = `openclaw_${dateStr}_${timestamp}.log`;
    const archivePath = path.join(this.options.logDir, 'archive', archiveName);
    
    try {
      // Create archive directory if needed
      const archiveDir = path.join(this.options.logDir, 'archive');
      if (!fs.existsSync(archiveDir)) {
        fs.mkdirSync(archiveDir, { recursive: true });
      }
      
      // Move current log to archive
      fs.renameSync(this.currentLogFile, archivePath);
      console.log(`📦 Rotated log: ${archiveName}`);
      
      // Compress old logs
      this.compressOldLogs();
      
      // Initialize new log file
      this.initLogFile();
    } catch (error) {
      console.error('Error rotating logs:', error.message);
    }
  }
  
  compressOldLogs() {
    const archiveDir = path.join(this.options.logDir, 'archive');
    if (!fs.existsSync(archiveDir)) return;
    
    const files = fs.readdirSync(archiveDir)
      .filter(f => f.endsWith('.log') && !f.endsWith('.gz'))
      .sort()
      .reverse();
    
    // Keep only maxFiles
    if (files.length > this.options.maxFiles) {
      const toDelete = files.slice(this.options.maxFiles);
      for (const file of toDelete) {
        const filePath = path.join(archiveDir, file);
        fs.unlinkSync(filePath);
        console.log(`🗑️  Deleted old log: ${file}`);
      }
    }
  }
  
  saveCrashMarker(errorEntry) {
    try {
      const crashMarker = {
        lastSessionId: this.sessionId,
        lastCrashTime: new Date().toISOString(),
        lastError: errorEntry,
        pid: process.pid,
        uptime: process.uptime(),
        memoryUsage: process.memoryUsage()
      };
      
      fs.writeFileSync(this.crashRecoveryFile, JSON.stringify(crashMarker, null, 2));
    } catch (error) {
      console.error('Error saving crash marker:', error.message);
    }
  }
  
  updateCrashRecovery() {
    try {
      const recoveryData = {
        lastSessionId: this.sessionId,
        lastActivityTime: new Date().toISOString(),
        uptime: process.uptime(),
        pid: process.pid,
        totalLogsWritten: this.currentLogSize
      };
      
      fs.writeFileSync(this.crashRecoveryFile, JSON.stringify(recoveryData, null, 2));
    } catch (error) {
      // Silent fail for recovery updates
    }
  }
  
  shutdown(signal) {
    console.log(`\n🛑 Received ${signal}, shutting down gracefully...`);
    
    // Flush remaining logs
    this.flush();
    
    // Save final crash recovery state
    const recoveryData = {
      lastSessionId: this.sessionId,
      shutdownTime: new Date().toISOString(),
      shutdownSignal: signal,
      uptime: process.uptime(),
      totalLogsWritten: this.currentLogSize,
      status: 'graceful_shutdown'
    };
    
    fs.writeFileSync(this.crashRecoveryFile, JSON.stringify(recoveryData, null, 2));
    
    console.log(`✅ Logging system shut down gracefully`);
    console.log(`📊 Session Summary:`);
    console.log(`   Session ID: ${this.sessionId}`);
    console.log(`   Total logs written: ${this.currentLogSize} bytes`);
    console.log(`   Uptime: ${process.uptime()} seconds`);
    
    process.exit(0);
  }
}

// Export for use
module.exports = { OpenClawLogger };

// CLI usage
if (require.main === module) {
  const logger = new OpenClawLogger({
    logDir: process.argv[2] || '/home/admin/.openclaw/logs',
    enableConsole: true,
    enableFile: true
  });
  
  // Test logging
  logger.log('info', 'System Startup', { message: 'Enhanced logging system started' });
  logger.log('warn', 'Test Warning', { test: 'This is a test warning' });
  logger.log('error', 'Test Error', { test: 'This is a test error', code: 123 });
  
  console.log('\n✅ Enhanced logging system is running. Press Ctrl+C to exit.\n');
}
