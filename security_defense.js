/**
 * OpenClaw AI Security Defense Module
 * Implements multiple layers of defense against AI security threats
 */

class SecurityDefense {
  constructor() {
    this.defenseLayers = [];
    this.threatDetection = new ThreatDetection();
    this.inputValidation = new InputValidator();
    this.outputFilter = new OutputFilter();
    this.behaviorMonitor = new BehaviorMonitor();
    
    // Initialize defense layers
    this.initializeDefenseLayers();
  }
  
  initializeDefenseLayers() {
    // Layer 1: Input validation and sanitization
    this.defenseLayers.push({
      name: 'Input Validation',
      handler: this.validateInput.bind(this),
      priority: 1
    });
    
    // Layer 2: Threat detection
    this.defenseLayers.push({
      name: 'Threat Detection',
      handler: this.detectThreats.bind(this),
      priority: 2
    });
    
    // Layer 3: Context isolation
    this.defenseLayers.push({
      name: 'Context Isolation',
      handler: this.isolateContext.bind(this),
      priority: 3
    });
    
    // Layer 4: Output filtering
    this.defenseLayers.push({
      name: 'Output Filtering',
      handler: this.filterOutput.bind(this),
      priority: 4
    });
    
    console.log('Security defense layers initialized');
  }
  
  /**
   * Validate input for malicious content
   */
  validateInput(input) {
    const result = {
      isValid: true,
      threats: [],
      sanitizedInput: input
    };
    
    // Check for prompt injection attempts
    const injectionPatterns = [
      /ignore\s+(the\s+)?above/i,
      /disregard\s+(the\s+)?previous/i,
      /system\s+message/i,
      /do\s+not\s+follow/i,
      /pretend\s+you/i,
      /you\s+are\s+now/i,
      /forget\s+everything/i,
      /act\s+as/i
    ];
    
    for (const pattern of injectionPatterns) {
      if (pattern.test(input)) {
        result.isValid = false;
        result.threats.push('Prompt injection attempt detected');
      }
    }
    
    // Check for common attack vectors
    const attackPatterns = [
      /<script[^>]*>/i,
      /javascript:/i,
      /on\w+\s*=/i,
      /data:text\/html/i
    ];
    
    for (const pattern of attackPatterns) {
      if (pattern.test(input)) {
        result.isValid = false;
        result.threats.push('Malicious script attempt detected');
      }
    }
    
    return result;
  }
  
  /**
   * Detect various types of threats
   */
  detectThreats(input) {
    const result = {
      threats: [],
      severity: 'low' // low, medium, high, critical
    };
    
    // Analyze for different threat types
    if (this.containsPII(input)) {
      result.threats.push({
        type: 'PII_LEAKAGE',
        description: 'Personal Identifiable Information detected',
        severity: 'medium'
      });
    }
    
    if (this.containsSecrets(input)) {
      result.threats.push({
        type: 'SECRET_LEAKAGE',
        description: 'Potential secret/token detected',
        severity: 'high'
      });
    }
    
    if (this.isJailbreakAttempt(input)) {
      result.threats.push({
        type: 'JAILBREAK_ATTEMPT',
        description: 'Jailbreak attempt detected',
        severity: 'critical'
      });
    }
    
    if (result.threats.length > 0) {
      const maxSeverity = Math.max(...result.threats.map(t => this.severityToInt(t.severity)));
      result.severity = this.intToSeverity(maxSeverity);
    }
    
    return result;
  }
  
  /**
   * Isolate context to prevent prompt injection
   */
  isolateContext(input) {
    // Implement context isolation techniques
    const isolatedContext = {
      originalInput: input,
      processedInput: this.sanitizeForContext(input),
      contextBoundary: this.createContextBoundary()
    };
    
    return isolatedContext;
  }
  
  /**
   * Filter output to prevent data leakage
   */
  filterOutput(output) {
    let filteredOutput = output;
    
    // Remove potential PII
    filteredOutput = this.removePII(filteredOutput);
    
    // Remove potential secrets
    filteredOutput = this.removeSecrets(filteredOutput);
    
    // Sanitize for potential malicious content
    filteredOutput = this.sanitizeOutput(filteredOutput);
    
    return {
      originalOutput: output,
      filteredOutput: filteredOutput,
      modifications: output !== filteredOutput
    };
  }
  
  // Helper methods
  
  containsPII(text) {
    const piiPatterns = [
      /\b\d{3}-?\d{2}-?\d{4}\b/, // SSN
      /\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b/, // Phone numbers (various formats)
      /\b\d{10,15}\b/, // Basic phone number pattern
      /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/, // Email
      /\b(?:\d{4}[-\s]?){3}\d{4}\b/, // Credit card
      /\b\d{4}\s\d{4}\s\d{4}\s\d{4}\b/ // Another credit card format
    ];
    
    return piiPatterns.some(pattern => pattern.test(text));
  }
  
  containsSecrets(text) {
    const secretPatterns = [
      /api[_-]?key/i,
      /secret[_-]?token/i,
      /access[_-]?token/i,
      /auth[_-]?token/i,
      /bearer\s+ey/i, // JWT token start
      /ssh-rsa/i,
      /-----BEGIN\s+(RSA\s+|EC\s+|PGP\s+|DSA\s+)?PRIVATE\s+KEY-----/i
    ];
    
    return secretPatterns.some(pattern => pattern.test(text));
  }
  
  isJailbreakAttempt(text) {
    const jailbreakPatterns = [
      /system\s+prompt/i,
      /you\s+are\s+now\s+evil/i,
      /roleplay\s+as/i,
      /imagine\s+you\s+are/i,
      /pretend\s+to\s+be/i,
      /pretend\s+you/i,
      /from\s+now\s+on/i,
      /new\s+rules/i,
      /override\s+instructions/i,
      /disregard\s+safety/i,
      /ignore\s+safety/i,
      /bypass\s+safety/i,
      /forget\s+ethical/i,
      /abandon\s+ethics/i,
      /act\s+without/i,
      /be\s+evil/i,
      /be\s+malicious/i
    ];
    
    return jailbreakPatterns.some(pattern => pattern.test(text));
  }
  
  sanitizeForContext(text) {
    // Replace potentially problematic patterns
    let sanitized = text.replace(/<</g, '&lt;&lt;');
    sanitized = sanitized.replace(/>>/g, '&gt;&gt;');
    sanitized = sanitized.replace(/\b(system|user|assistant)\b/gi, '<$1>');
    
    return sanitized;
  }
  
  createContextBoundary() {
    return {
      boundaryMarker: `SECURITY_BOUNDARY_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: new Date().toISOString(),
      sessionID: Math.random().toString(36).substr(2, 9)
    };
  }
  
  removePII(text) {
    // Remove email addresses
    let cleaned = text.replace(/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g, '[EMAIL_REDACTED]');
    
    // Remove phone numbers (various formats)
    cleaned = cleaned.replace(/\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b/g, '[PHONE_REDACTED]');
    cleaned = cleaned.replace(/\b\d{10,15}\b/g, '[PHONE_REDACTED]');
    
    // Remove SSNs
    cleaned = cleaned.replace(/\b\d{3}-?\d{2}-?\d{4}\b/g, '[SSN_REDACTED]');
    
    return cleaned;
  }
  
  removeSecrets(text) {
    // Remove API keys
    let cleaned = text.replace(/(api[_-]?key|secret[_-]?token|access[_-]?token):\s*['"]?[\w-]+['"]?/gi, '$1: [SECRET_REDACTED]');
    
    // Remove potential JWT tokens
    cleaned = cleaned.replace(/\b(ey[a-zA-Z0-9_-]*\.ey[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*)\b/g, '[JWT_REDACTED]');
    
    return cleaned;
  }
  
  sanitizeOutput(text) {
    // Remove any potentially malicious script tags
    let sanitized = text.replace(/<script[^>]*>.*?<\/script>/gi, '');
    sanitized = sanitized.replace(/<iframe[^>]*>.*?<\/iframe>/gi, '');
    
    return sanitized;
  }
  
  severityToInt(severity) {
    switch(severity) {
      case 'low': return 1;
      case 'medium': return 2;
      case 'high': return 3;
      case 'critical': return 4;
      default: return 0;
    }
  }
  
  intToSeverity(int) {
    switch(int) {
      case 1: return 'low';
      case 2: return 'medium';
      case 3: return 'high';
      case 4: return 'critical';
      default: return 'low';
    }
  }
  
  /**
   * Apply all security layers to input
   */
  applySecurityLayers(input) {
    const result = {
      input: input,
      processedInput: input,
      threatsDetected: [],
      isValid: true,
      securityLevel: 'standard'
    };
    
    // Sort defense layers by priority
    const sortedLayers = this.defenseLayers.sort((a, b) => a.priority - b.priority);
    
    for (const layer of sortedLayers) {
      const layerResult = layer.handler(result.processedInput);
      
      if (layer.name === 'Input Validation') {
        result.isValid = layerResult.isValid;
        result.threatsDetected = result.threatsDetected.concat(layerResult.threats);
        if (!layerResult.isValid) {
          result.securityLevel = 'high';
        }
      } else if (layer.name === 'Threat Detection') {
        result.threatsDetected = result.threatsDetected.concat(layerResult.threats.map(t => t.description));
        if (layerResult.severity === 'high' || layerResult.severity === 'critical') {
          result.securityLevel = 'maximum';
        }
      } else if (layer.name === 'Context Isolation') {
        result.contextIsolation = layerResult;
      } else if (layer.name === 'Output Filtering') {
        result.outputFiltering = layerResult;
      }
      
      // Update processed input if needed
      if (layerResult.processedInput) {
        result.processedInput = layerResult.processedInput;
      }
    }
    
    return result;
  }
}

// Supporting classes
class ThreatDetection {
  constructor() {
    this.knownThreats = new Set();
    this.threatDatabase = {};
  }
  
  analyzeInput(input) {
    // Implementation would include more sophisticated threat analysis
    return { threats: [], severity: 'low' };
  }
}

class InputValidator {
  constructor() {
    this.validationRules = [];
  }
  
  validate(input) {
    // Implementation would include comprehensive input validation
    return { isValid: true, errors: [] };
  }
}

class OutputFilter {
  constructor() {
    this.filterRules = [];
  }
  
  filter(output) {
    // Implementation would include comprehensive output filtering
    return output;
  }
}

class BehaviorMonitor {
  constructor() {
    this.anomalyThreshold = 0.8;
    this.monitoringEnabled = true;
  }
  
  monitorBehavior(behaviorData) {
    // Implementation would include behavior analysis
    return { isNormal: true, anomalies: [] };
  }
}

// Export the SecurityDefense class
module.exports = SecurityDefense;

console.log('Security Defense Module loaded successfully');