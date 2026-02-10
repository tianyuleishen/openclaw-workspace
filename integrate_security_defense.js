/**
 * Integrate Security Defense Module with OpenClaw System
 * This script integrates the security defense module with the existing OpenClaw system
 */

const fs = require('fs');
const path = require('path');
const SecurityDefense = require('./security_defense');

class SecurityIntegration {
  constructor() {
    this.securityDefense = new SecurityDefense();
    this.config = this.loadConfig();
    this.integrationStatus = {
      securityModuleLoaded: true,
      hooksInstalled: false,
      monitoringActive: false
    };
  }

  loadConfig() {
    // Load existing OpenClaw configuration
    const configPath = path.join(__dirname, '..', 'config.json');
    try {
      if (fs.existsSync(configPath)) {
        return JSON.parse(fs.readFileSync(configPath, 'utf8'));
      }
    } catch (error) {
      console.warn('Could not load existing config, using defaults:', error.message);
    }
    
    return {
      security: {
        enabled: true,
        inputValidation: true,
        threatDetection: true,
        outputFiltering: true,
        behaviorMonitoring: true,
        logging: true
      }
    };
  }

  /**
   * Install security hooks into OpenClaw system
   */
  installSecurityHooks() {
    console.log('Installing security hooks into OpenClaw system...');
    
    // Hook into message processing
    this.installMessageProcessingHook();
    
    // Hook into tool execution
    this.installToolExecutionHook();
    
    // Hook into memory operations
    this.installMemoryOperationHook();
    
    this.integrationStatus.hooksInstalled = true;
    console.log('Security hooks installed successfully');
  }

  /**
   * Hook into message processing pipeline
   */
  installMessageProcessingHook() {
    // This would typically modify the OpenClaw message processing pipeline
    // Since we can't directly modify the core system, we'll create a wrapper
    
    const originalMessageHandler = global.messageHandler || ((msg) => msg);
    
    global.messageHandler = (message) => {
      // Apply security checks before processing
      const securityCheck = this.securityDefense.applySecurityLayers(message);
      
      if (!securityCheck.isValid) {
        console.warn('Security violation detected:', securityCheck.threatsDetected);
        return this.handleSecurityViolation(message, securityCheck);
      }
      
      // Process message normally
      return originalMessageHandler(securityCheck.processedInput);
    };
    
    console.log('Message processing hook installed');
  }

  /**
   * Hook into tool execution
   */
  installToolExecutionHook() {
    // Create a wrapper for tool execution
    const originalToolExecutor = global.toolExecutor || ((tool, params) => {});
    
    global.toolExecutor = (tool, params) => {
      // Validate tool parameters for security
      const paramCheck = this.securityDefense.applySecurityLayers(JSON.stringify(params));
      
      if (!paramCheck.isValid) {
        console.warn('Tool parameter security violation detected:', paramCheck.threatsDetected);
        return this.handleSecurityViolation({tool, params}, paramCheck);
      }
      
      // Execute tool normally
      return originalToolExecutor(tool, JSON.parse(paramCheck.processedInput));
    };
    
    console.log('Tool execution hook installed');
  }

  /**
   * Hook into memory operations
   */
  installMemoryOperationHook() {
    // Create a wrapper for memory operations
    const originalMemoryOp = global.memoryOperation || ((op, data) => {});
    
    global.memoryOperation = (operation, data) => {
      // Validate memory operation data
      const dataCheck = this.securityDefense.applySecurityLayers(JSON.stringify(data));
      
      if (!dataCheck.isValid) {
        console.warn('Memory operation security violation detected:', dataCheck.threatsDetected);
        return this.handleSecurityViolation({operation, data}, dataCheck);
      }
      
      // Perform memory operation normally
      return originalMemoryOp(operation, JSON.parse(dataCheck.processedInput));
    };
    
    console.log('Memory operation hook installed');
  }

  /**
   * Handle security violations
   */
  handleSecurityViolation(originalData, securityCheck) {
    // Log the violation
    this.logSecurityViolation(originalData, securityCheck);
    
    // Determine response based on severity
    if (securityCheck.securityLevel === 'maximum') {
      // For maximum security level, block the request
      return {
        blocked: true,
        reason: 'Security violation detected',
        threats: securityCheck.threatsDetected
      };
    } else if (securityCheck.securityLevel === 'high') {
      // For high security level, flag for review
      this.flagForReview(originalData, securityCheck);
      return {
        flagged: true,
        reason: 'Potential security issue detected',
        threats: securityCheck.threatsDetected
      };
    } else {
      // For lower levels, just log
      return originalData;
    }
  }

  /**
   * Log security violations
   */
  logSecurityViolation(originalData, securityCheck) {
    const logEntry = {
      timestamp: new Date().toISOString(),
      type: 'SECURITY_VIOLATION',
      severity: securityCheck.securityLevel,
      threats: securityCheck.threatsDetected,
      originalData: typeof originalData === 'string' ? originalData.substring(0, 100) : JSON.stringify(originalData).substring(0, 100),
      context: 'OpenClaw Security Defense System'
    };
    
    // Write to security log
    const logDir = path.join(__dirname, 'logs');
    if (!fs.existsSync(logDir)) {
      fs.mkdirSync(logDir, { recursive: true });
    }
    
    const logFile = path.join(logDir, `security_violations_${new Date().toISOString().split('T')[0]}.log`);
    fs.appendFileSync(logFile, JSON.stringify(logEntry) + '\n');
    
    console.log('Security violation logged:', logEntry);
  }

  /**
   * Flag data for review
   */
  flagForReview(originalData, securityCheck) {
    const reviewEntry = {
      timestamp: new Date().toISOString(),
      type: 'REVIEW_REQUIRED',
      severity: securityCheck.securityLevel,
      threats: securityCheck.threatsDetected,
      originalData: originalData,
      context: 'OpenClaw Security Defense System'
    };
    
    // Write to review queue
    const reviewDir = path.join(__dirname, 'review_queue');
    if (!fs.existsSync(reviewDir)) {
      fs.mkdirSync(reviewDir, { recursive: true });
    }
    
    const reviewFile = path.join(reviewDir, `review_required_${Date.now()}.json`);
    fs.writeFileSync(reviewFile, JSON.stringify(reviewEntry, null, 2));
    
    console.log('Item flagged for review:', reviewFile);
  }

  /**
   * Enable behavior monitoring
   */
  enableBehaviorMonitoring() {
    console.log('Enabling behavior monitoring...');
    
    // Set up periodic behavior analysis
    setInterval(() => {
      this.analyzeSystemBehavior();
    }, 30000); // Check every 30 seconds
    
    this.integrationStatus.monitoringActive = true;
    console.log('Behavior monitoring enabled');
  }

  /**
   * Analyze system behavior for anomalies
   */
  analyzeSystemBehavior() {
    // This would typically connect to the actual system metrics
    // For now, we'll simulate basic behavior monitoring
    
    const behaviorData = {
      timestamp: new Date().toISOString(),
      messageCount: global.messageCount || 0,
      toolExecutions: global.toolExecutions || 0,
      securityViolations: global.securityViolations || 0,
      activeSessions: global.activeSessions || 0
    };
    
    // Simple anomaly detection
    if (behaviorData.messageCount > 100 || behaviorData.toolExecutions > 50) {
      console.warn('Unusual activity detected:', behaviorData);
      this.logAnomaly(behaviorData);
    }
    
    global.messageCount = 0;
    global.toolExecutions = 0;
  }

  /**
   * Log anomalies
   */
  logAnomaly(behaviorData) {
    const logEntry = {
      timestamp: new Date().toISOString(),
      type: 'ANOMALY_DETECTED',
      data: behaviorData,
      context: 'OpenClaw Behavior Monitoring'
    };
    
    const logDir = path.join(__dirname, 'logs');
    if (!fs.existsSync(logDir)) {
      fs.mkdirSync(logDir, { recursive: true });
    }
    
    const logFile = path.join(logDir, `anomalies_${new Date().toISOString().split('T')[0]}.log`);
    fs.appendFileSync(logFile, JSON.stringify(logEntry) + '\n');
  }

  /**
   * Start the security integration
   */
  start() {
    console.log('Starting OpenClaw Security Defense Integration...');
    
    // Install security hooks
    this.installSecurityHooks();
    
    // Enable behavior monitoring
    this.enableBehaviorMonitoring();
    
    // Update configuration to enable security features
    this.updateConfig();
    
    console.log('OpenClaw Security Defense Integration started successfully');
    console.log('Integration status:', this.integrationStatus);
    
    return this.integrationStatus;
  }

  /**
   * Update configuration to reflect security settings
   */
  updateConfig() {
    // Add security configuration to the config
    if (!this.config.security) {
      this.config.security = {};
    }
    
    this.config.security.enabled = true;
    this.config.security.lastUpdated = new Date().toISOString();
    
    // Save updated config
    const configPath = path.join(__dirname, '..', 'config.json');
    fs.writeFileSync(configPath, JSON.stringify(this.config, null, 2));
    
    console.log('Configuration updated with security settings');
  }

  /**
   * Get security status
   */
  getStatus() {
    return {
      ...this.integrationStatus,
      config: this.config.security,
      timestamp: new Date().toISOString()
    };
  }
}

// Initialize and start the security integration when the module is run directly
if (require.main === module) {
  const securityIntegration = new SecurityIntegration();
  const status = securityIntegration.start();
  
  // Save the security integration instance globally so other parts of the system can access it
  global.securityIntegration = securityIntegration;
  
  console.log('\nSecurity Defense System Status:');
  console.log(JSON.stringify(status, null, 2));
  
  console.log('\nSecurity Defense System has been integrated with OpenClaw!');
  console.log('Features enabled:');
  console.log('- Input validation and threat detection');
  console.log('- Context isolation');
  console.log('- Output filtering');
  console.log('- Behavior monitoring');
  console.log('- Security violation logging');
  console.log('- Anomaly detection');
}

module.exports = SecurityIntegration;

console.log('Security Integration Module loaded successfully');