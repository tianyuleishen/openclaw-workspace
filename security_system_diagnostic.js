/**
 * OpenClaw Security System Diagnostic Tool
 * Diagnoses and fixes issues with the security system
 */

const fs = require('fs');
const path = require('path');
const http = require('http');
const { exec } = require('child_process');
const util = require('util');
const execAsync = util.promisify(exec);

// Import security modules
const SecurityDefense = require('./security_defense');
const VulnerabilityScanner = require('./vulnerability_scanner');
const SecureConfigManager = require('./secure_config_manager');

class SecurityDiagnostic {
  constructor() {
    this.diagnostics = {
      components: {},
      services: {},
      configurations: {},
      issues: [],
      recommendations: []
    };
  }

  /**
   * Run complete diagnostic
   */
  async runDiagnostic() {
    console.log('🔍 Running OpenClaw Security System Diagnostic...\n');
    
    // Check components
    await this.checkComponents();
    
    // Check services
    await this.checkServices();
    
    // Check configurations
    await this.checkConfigurations();
    
    // Generate report
    this.generateReport();
    
    // Apply fixes if needed
    await this.applyFixes();
    
    return this.diagnostics;
  }

  /**
   * Check security components
   */
  async checkComponents() {
    console.log('📦 Checking security components...');
    
    try {
      // Test Security Defense
      const security = new SecurityDefense();
      const testInput = 'Normal test input';
      const result = security.applySecurityLayers(testInput);
      
      this.diagnostics.components.securityDefense = {
        status: 'operational',
        valid: result.isValid,
        threatsDetected: result.threatsDetected.length
      };
      
      console.log('   ✅ Security Defense: Operational');
    } catch (error) {
      this.diagnostics.components.securityDefense = {
        status: 'error',
        error: error.message
      };
      this.diagnostics.issues.push(`Security Defense error: ${error.message}`);
      console.log('   ❌ Security Defense: Error');
    }

    try {
      // Test Vulnerability Scanner
      const scanner = new VulnerabilityScanner();
      this.diagnostics.components.vulnerabilityScanner = {
        status: 'operational'
      };
      
      console.log('   ✅ Vulnerability Scanner: Operational');
    } catch (error) {
      this.diagnostics.components.vulnerabilityScanner = {
        status: 'error',
        error: error.message
      };
      this.diagnostics.issues.push(`Vulnerability Scanner error: ${error.message}`);
      console.log('   ❌ Vulnerability Scanner: Error');
    }

    try {
      // Test Secure Config Manager
      const configMgr = new SecureConfigManager();
      this.diagnostics.components.secureConfigManager = {
        status: 'operational'
      };
      
      console.log('   ✅ Secure Config Manager: Operational');
    } catch (error) {
      this.diagnostics.components.secureConfigManager = {
        status: 'error',
        error: error.message
      };
      this.diagnostics.issues.push(`Secure Config Manager error: ${error.message}`);
      console.log('   ❌ Secure Config Manager: Error');
    }
  }

  /**
   * Check security services
   */
  async checkServices() {
    console.log('\n📡 Checking security services...');
    
    // Check HTTP endpoints
    const endpoints = [
      { name: 'Health Check', url: 'http://localhost:3009/health' },
      { name: 'Status Check', url: 'http://localhost:3009/status' }
    ];

    for (const endpoint of endpoints) {
      try {
        const response = await this.httpGet(endpoint.url, 5000); // 5 second timeout
        this.diagnostics.services[endpoint.name] = {
          status: response.status === 200 ? 'reachable' : 'unreachable',
          statusCode: response.status,
          response: response.data
        };
        
        if (response.status === 200) {
          console.log(`   ✅ ${endpoint.name}: Reachable (200)`);
        } else {
          console.log(`   ⚠️  ${endpoint.name}: Unreachable (${response.status})`);
          this.diagnostics.issues.push(`${endpoint.name} returned status ${response.status}`);
        }
      } catch (error) {
        this.diagnostics.services[endpoint.name] = {
          status: 'unreachable',
          error: error.message
        };
        this.diagnostics.issues.push(`${endpoint.name} unreachable: ${error.message}`);
        console.log(`   ❌ ${endpoint.name}: Unreachable`);
      }
    }
  }

  /**
   * Check security configurations
   */
  async checkConfigurations() {
    console.log('\n⚙️  Checking security configurations...');
    
    // Check if secure config directory exists
    const secureConfigDir = path.join(__dirname, 'secure_configs');
    const configExists = fs.existsSync(secureConfigDir);
    
    this.diagnostics.configurations.secureConfigDir = {
      exists: configExists,
      path: secureConfigDir
    };
    
    if (configExists) {
      console.log('   ✅ Secure config directory: Exists');
    } else {
      console.log('   ❌ Secure config directory: Missing');
      this.diagnostics.issues.push(`Secure config directory missing: ${secureConfigDir}`);
    }

    // Check if encryption key exists
    const encryptionKeyPath = path.join(__dirname, '.encryption_key');
    const keyExists = fs.existsSync(encryptionKeyPath);
    
    this.diagnostics.configurations.encryptionKey = {
      exists: keyExists,
      path: encryptionKeyPath
    };
    
    if (keyExists) {
      console.log('   ✅ Encryption key: Exists');
    } else {
      console.log('   ❌ Encryption key: Missing');
      this.diagnostics.issues.push(`Encryption key missing: ${encryptionKeyPath}`);
    }

    // Check file permissions
    if (keyExists) {
      try {
        const stats = fs.statSync(encryptionKeyPath);
        // Check if file is only readable/writable by owner (600)
        const isSecure = (stats.mode & 0o777) === 0o600;
        
        this.diagnostics.configurations.encryptionKey.permissions = {
          mode: (stats.mode & 0o777).toString(8),
          secure: isSecure
        };
        
        if (isSecure) {
          console.log('   ✅ Encryption key permissions: Secure (600)');
        } else {
          console.log(`   ❌ Encryption key permissions: Insecure (${(stats.mode & 0o777).toString(8)})`);
          this.diagnostics.issues.push(`Encryption key has insecure permissions: ${(stats.mode & 0o777).toString(8)}`);
        }
      } catch (error) {
        console.log(`   ❌ Encryption key permissions: Error checking - ${error.message}`);
      }
    }

    // Check .env file permissions
    const envPath = path.join(__dirname, '.env');
    if (fs.existsSync(envPath)) {
      try {
        const stats = fs.statSync(envPath);
        const isSecure = (stats.mode & 0o007) === 0; // No access for group/others
        
        this.diagnostics.configurations.envFile = {
          exists: true,
          permissions: {
            mode: (stats.mode & 0o777).toString(8),
            secure: isSecure
          }
        };
        
        if (isSecure) {
          console.log('   ✅ .env file permissions: Secure');
        } else {
          console.log(`   ⚠️  .env file permissions: May be insecure (${(stats.mode & 0o777).toString(8)})`);
          this.diagnostics.recommendations.push(`Consider setting .env file permissions to 600: chmod 600 ${envPath}`);
        }
      } catch (error) {
        console.log(`   ⚠️  .env file permissions: Error checking - ${error.message}`);
      }
    } else {
      this.diagnostics.configurations.envFile = { exists: false };
      console.log('   ℹ️  .env file: Not found');
    }
  }

  /**
   * Generate diagnostic report
   */
  generateReport() {
    console.log('\n📋 Diagnostic Report:');
    console.log(`   Components checked: ${Object.keys(this.diagnostics.components).length}`);
    console.log(`   Services checked: ${Object.keys(this.diagnostics.services).length}`);
    console.log(`   Configurations checked: ${Object.keys(this.diagnostics.configurations).length}`);
    console.log(`   Issues found: ${this.diagnostics.issues.length}`);
    console.log(`   Recommendations: ${this.diagnostics.recommendations.length}`);

    if (this.diagnostics.issues.length > 0) {
      console.log('\n❗ Issues Found:');
      this.diagnostics.issues.forEach((issue, index) => {
        console.log(`   ${index + 1}. ${issue}`);
      });
    }

    if (this.diagnostics.recommendations.length > 0) {
      console.log('\n💡 Recommendations:');
      this.diagnostics.recommendations.forEach((rec, index) => {
        console.log(`   ${index + 1}. ${rec}`);
      });
    }

    // Overall status
    const hasCriticalIssues = this.diagnostics.issues.some(issue => 
      issue.includes('unreachable') || issue.includes('error')
    );
    
    if (hasCriticalIssues) {
      console.log('\n🔴 CRITICAL ISSUES DETECTED - IMMEDIATE ACTION REQUIRED');
    } else if (this.diagnostics.issues.length > 0) {
      console.log('\n🟡 ISSUES DETECTED - REVIEW AND FIX RECOMMENDED');
    } else {
      console.log('\n🟢 ALL SYSTEMS OPERATIONAL - SECURITY STATUS GOOD');
    }
  }

  /**
   * Apply automatic fixes
   */
  async applyFixes() {
    console.log('\n🔧 Applying automatic fixes...');
    
    let fixesApplied = 0;
    
    // Fix encryption key permissions
    const encryptionKeyPath = path.join(__dirname, '.encryption_key');
    if (fs.existsSync(encryptionKeyPath)) {
      try {
        fs.chmodSync(encryptionKeyPath, '600');
        console.log('   ✅ Fixed encryption key permissions (set to 600)');
        fixesApplied++;
      } catch (error) {
        console.log(`   ❌ Could not fix encryption key permissions: ${error.message}`);
      }
    }

    // Fix .env file permissions
    const envPath = path.join(__dirname, '.env');
    if (fs.existsSync(envPath)) {
      try {
        fs.chmodSync(envPath, '600');
        console.log('   ✅ Fixed .env file permissions (set to 600)');
        fixesApplied++;
      } catch (error) {
        console.log(`   ❌ Could not fix .env file permissions: ${error.message}`);
      }
    }

    // Check if security service needs to be restarted
    const healthUnreachable = this.diagnostics.services['Health Check']?.status === 'unreachable';
    const statusUnreachable = this.diagnostics.services['Status Check']?.status === 'unreachable';

    if (healthUnreachable || statusUnreachable) {
      console.log('   🔄 Security service appears down, attempting restart...');
      try {
        // Kill any existing security processes
        await execAsync('pkill -f start_advanced_security_system || true');
        
        // Start the security system
        exec('cd /home/admin/.openclaw/workspace && node start_advanced_security_system.js > /dev/null 2>&1 &', (error) => {
          if (error) {
            console.log(`   ❌ Could not restart security service: ${error.message}`);
          } else {
            console.log('   ✅ Security service restart initiated');
            fixesApplied++;
          }
        });
      } catch (error) {
        console.log(`   ❌ Could not restart security service: ${error.message}`);
      }
    }

    console.log(`\n   Applied ${fixesApplied} automatic fixes`);
  }

  /**
   * HTTP GET helper with timeout
   */
  httpGet(url, timeout = 5000) {
    return new Promise((resolve, reject) => {
      const request = http.get(url, (res) => {
        let data = '';
        
        res.on('data', (chunk) => {
          data += chunk;
        });
        
        res.on('end', () => {
          try {
            resolve({
              status: res.statusCode,
              data: JSON.parse(data) || data
            });
          } catch (e) {
            resolve({
              status: res.statusCode,
              data: data
            });
          }
        });
      }).on('error', (err) => {
        reject(err);
      });

      // Set timeout
      request.setTimeout(timeout, () => {
        request.destroy();
        reject(new Error('Request timeout'));
      });
    });
  }
}

// Run diagnostic if this script is executed directly
if (require.main === module) {
  const diagnostic = new SecurityDiagnostic();
  
  diagnostic.runDiagnostic()
    .then(() => {
      console.log('\n✅ Security diagnostic completed');
    })
    .catch(error => {
      console.error('❌ Security diagnostic failed:', error);
    });
}

module.exports = SecurityDiagnostic;

console.log('Security Diagnostic Tool loaded successfully');