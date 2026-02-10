#!/usr/bin/env node
/**
 * OpenClaw Package Security Scanner
 * Scans downloaded packages for malware and security threats
 */

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

class PackageSecurityScanner {
  constructor(options = {}) {
    this.options = {
      quarantineDir: options.quarantineDir || '/home/admin/.openclaw/quarantine',
      logDir: options.logDir || '/home/admin/.openclaw/logs',
      scanTimeout: options.scanTimeout || 30000,
      enableHeuristic: options.enableHeuristic !== false,
      enableSignature: options.enableSignature !== false,
      enableBehavior: options.enableBehavior !== false,
      ...options
    };
    
    // Known malware signatures
    this.signatures = new Map([
      ['eval(', 'Dangerous eval usage detected'],
      ['exec(', 'Code execution found'],
      ['child_process.exec', 'Shell command execution'],
      ['process.env', 'Environment variable access'],
      ['require("fs")', 'File system access'],
      ['require("child_process")', 'Process spawning'],
      ['require("http")', 'Network access'],
      ['require("https")', 'HTTPS network access'],
      ['require("dns")', 'DNS resolution'],
      ['require("net")', 'TCP/UDP sockets'],
      ['require("tls")', 'TLS/SSL access'],
      ['require("crypto")', 'Cryptographic operations'],
      ['fs.writeFileSync', 'File write operation'],
      ['fs.unlinkSync', 'File deletion operation'],
      ['fs.readFileSync', 'File read operation'],
      ['process.exit', 'Process termination'],
      ['process.kill', 'Process killing'],
      ['os.userInfo', 'User information leak'],
      ['os.homedir', 'Home directory access'],
      ['Buffer.from', 'Buffer manipulation'],
      ['steal', 'Potentially malicious intent'],
      ['backdoor', 'Backdoor detection'],
      ['keylogger', 'Keylogger detection'],
      ['ransomware', 'Ransomware detection'],
    ]);
    
    // Suspicious package names
    this.suspiciousPackages = new Set([
      'malware', 'virus', 'trojan', 'backdoor', 'exploit',
      'hacker', 'stealer', 'logger', 'spyware', 'adware',
      'ransomware', 'rootkit', 'botnet', 'worm', 'cryptominer',
    ]);
    
    this.highRiskPermissions = new Set([
      'bindingCode', 'ignoreScripts', 'unsafePerm',
      'allowRoot', 'ignoreEngine'
    ]);
    
    this.riskLevels = {
      CRITICAL: 5,
      HIGH: 4,
      MEDIUM: 3,
      LOW: 2,
      INFO: 1,
      NONE: 0
    };
    
    this.ensureDirectories();
    
    console.log('🛡️  Package Security Scanner initialized');
    console.log(`📁 Quarantine: ${this.options.quarantineDir}`);
    console.log(`📝 Logging: ${this.options.logDir}`);
  }
  
  ensureDirectories() {
    for (const dir of [this.options.quarantineDir, this.options.logDir]) {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
      }
    }
  }
  
  levenshteinDistance(a, b) {
    const matrix = [];
    for (let i = 0; i <= b.length; i++) {
      matrix[i] = [i];
    }
    for (let j = 0; j <= a.length; j++) {
      matrix[0][j] = j;
    }
    for (let i = 1; i <= b.length; i++) {
      for (let j = 1; j <= a.length; j++) {
        if (b.charAt(i - 1) === a.charAt(j - 1)) {
          matrix[i][j] = matrix[i - 1][j - 1];
        } else {
          matrix[i][j] = Math.min(
            matrix[i - 1][j - 1] + 1,
            matrix[i][j - 1] + 1,
            matrix[i - 1][j] + 1
          );
        }
      }
    }
    return matrix[b.length][a.length];
  }
  
  async scanPackage(packagePath) {
    const packageInfo = this.parsePackagePath(packagePath);
    
    console.log(`\n🔍 Scanning: ${packageInfo.name}@${packageInfo.version || 'unknown'}`);
    
    const scanResult = {
      package: packageInfo,
      timestamp: new Date().toISOString(),
      status: 'scanned',
      risks: [],
      permissions: [],
      files: [],
      overallRisk: 'NONE',
      recommendation: 'INSTALL'
    };
    
    this.checkPackageName(packageInfo, scanResult);
    await this.checkPackageJson(packagePath, scanResult);
    await this.scanSourceFiles(packagePath, scanResult);
    this.checkPermissions(packagePath, scanResult);
    this.calculateOverallRisk(scanResult);
    this.generateRecommendation(scanResult);
    await this.finalizeScan(scanResult);
    
    return scanResult;
  }
  
  parsePackagePath(packagePath) {
    const name = path.basename(packagePath);
    const versionMatch = name.match(/@?([\w-]+)@?([\d.]+)/);
    return {
      name: versionMatch ? versionMatch[1] : name,
      version: versionMatch ? versionMatch[2] : null,
      path: path.resolve(packagePath),
      dirname: path.dirname(packagePath)
    };
  }
  
  checkPackageName(packageInfo, scanResult) {
    const name = packageInfo.name.toLowerCase();
    
    for (const suspicious of this.suspiciousPackages) {
      if (name.includes(suspicious)) {
        scanResult.risks.push({
          type: 'MALICIOUS_NAME',
          level: 'HIGH',
          message: `Package name contains: ${suspicious}`,
          location: 'package name'
        });
      }
    }
    
    const popularPackages = ['express', 'lodash', 'react', 'vue', 'axios', 'ws', 'koa'];
    for (const popular of popularPackages) {
      if (name !== popular && this.levenshteinDistance(name, popular) <= 2) {
        scanResult.risks.push({
          type: 'TYPOSQUATTING',
          level: 'HIGH',
          message: `Similar to: ${popular}`,
          location: 'package name'
        });
      }
    }
  }
  
  async checkPackageJson(packagePath, scanResult) {
    const packageJsonPath = path.join(packagePath, 'package.json');
    
    if (!fs.existsSync(packageJsonPath)) {
      scanResult.risks.push({
        type: 'MISSING_MANIFEST',
        level: 'INFO',
        message: 'No package.json found'
      });
      return;
    }
    
    try {
      const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
      scanResult.packageJson = packageJson;
      
      // Check scripts
      if (packageJson.scripts) {
        for (const [scriptName, script] of Object.entries(packageJson.scripts)) {
          const risks = this.analyzeScript(script);
          for (const risk of risks) {
            scanResult.risks.push({
              type: 'SUSPICIOUS_SCRIPT',
              level: risk.level,
              message: `Script '${scriptName}': ${risk.message}`,
              location: `package.json scripts.${scriptName}`
            });
          }
        }
      }
      
      // Check high-risk permissions
      for (const perm of this.highRiskPermissions) {
        if (packageJson[perm] === true) {
          scanResult.permissions.push({
            type: perm,
            level: 'HIGH',
            message: `High-risk: ${perm}`
          });
        }
      }
      
    } catch (error) {
      scanResult.risks.push({
        type: 'INVALID_MANIFEST',
        level: 'INFO',
        message: error.message
      });
    }
  }
  
  analyzeScript(script) {
    const risks = [];
    const lowerScript = script.toLowerCase();
    const dangerousPatterns = [
      { pattern: /curl\s+.*\|\s*sh/i, level: 'CRITICAL', message: 'Pipe to shell' },
      { pattern: /wget\s+.*\|\s*sh/i, level: 'CRITICAL', message: 'Pipe to shell' },
      { pattern: /node\s+.*eval/i, level: 'HIGH', message: 'Eval usage' },
      { pattern: /fs\.(write|unlink|rename)/i, level: 'MEDIUM', message: 'File operations' },
      { pattern: /process\.env/i, level: 'MEDIUM', message: 'Env access' },
      { pattern: /require\(['"](child_process|exec|spawn)/i, level: 'HIGH', message: 'Process spawn' },
      { pattern: /rm\s+-rf/i, level: 'HIGH', message: 'Recursive delete' },
    ];
    
    for (const { pattern, level, message } of dangerousPatterns) {
      if (pattern.test(lowerScript)) {
        risks.push({ level, message });
      }
    }
    
    return risks;
  }
  
  async scanSourceFiles(packagePath, scanResult) {
    const excludeDirs = new Set(['node_modules', '.git', 'dist', 'build', 'coverage']);
    const files = this.findSourceFiles(packagePath, excludeDirs);
    scanResult.filesScanned = files.length;
    
    for (const file of files) {
      const content = fs.readFileSync(file, 'utf8');
      const relativePath = path.relative(packagePath, file);
      
      if (this.options.enableSignature) {
        this.scanSignatures(content, relativePath, scanResult);
      }
      
      if (this.options.enableHeuristic) {
        this.heuristicAnalysis(content, relativePath, scanResult);
      }
    }
  }
  
  findSourceFiles(dir, excludeDirs) {
    const files = [];
    
    const scan = (currentDir) => {
      if (!fs.existsSync(currentDir)) return;
      
      const entries = fs.readdirSync(currentDir);
      
      for (const entry of entries) {
        const fullPath = path.join(currentDir, entry);
        const stat = fs.statSync(fullPath);
        
        if (stat.isDirectory()) {
          if (!excludeDirs.has(entry)) {
            scan(fullPath);
          }
        } else if (/\.(js|ts|py|rb|php|java|cpp|c|h|lua|go|rs)$/.test(entry)) {
          files.push(fullPath);
        }
      }
    };
    
    scan(dir);
    return files;
  }
  
  scanSignatures(content, filePath, scanResult) {
    for (const [signature, description] of this.signatures) {
      if (content.includes(signature)) {
        scanResult.risks.push({
          type: 'SIGNATURE_MATCH',
          level: this.getRiskLevel(description),
          message: `${description} in ${path.basename(filePath)}`,
          location: filePath
        });
      }
    }
  }
  
  getRiskLevel(description) {
    const highKeywords = ['Dangerous', 'Execution', 'Shell', 'Backdoor', 'Exploit'];
    const mediumKeywords = ['Access', 'Operation'];
    
    for (const keyword of highKeywords) {
      if (description.includes(keyword)) return 'HIGH';
    }
    for (const keyword of mediumKeywords) {
      if (description.includes(keyword)) return 'MEDIUM';
    }
    return 'LOW';
  }
  
  heuristicAnalysis(content, filePath, scanResult) {
    // Check for obfuscation
    const obfuscationPatterns = [
      /String\.fromCharCode/g,
      /\\u[0-9a-f]{4}/gi,
      /eval\s*\(/g,
      /Function\s*\(/g,
    ];
    
    let obfuscationCount = 0;
    for (const pattern of obfuscationPatterns) {
      const matches = content.match(pattern);
      if (matches) obfuscationCount += matches.length;
    }
    
    if (obfuscationCount > 3) {
      scanResult.risks.push({
        type: 'OBFUSCATED_CODE',
        level: 'MEDIUM',
        message: `${obfuscationCount} patterns in ${path.basename(filePath)}`
      });
    }
    
    // Check for suspicious base64 payloads
    const base64Pattern = /([A-Za-z0-9+\/]{100,}=*\s*){3,}/g;
    if (base64Pattern.test(content)) {
      scanResult.risks.push({
        type: 'BASE64_PAYLOAD',
        level: 'MEDIUM',
        message: `Encoded content in ${path.basename(filePath)}`
      });
    }
  }
  
  checkPermissions(packagePath, scanResult) {
    const npmrcPath = path.join(packagePath, '.npmrc');
    if (fs.existsSync(npmrcPath)) {
      const npmrc = fs.readFileSync(npmrcPath, 'utf8');
      if (npmrc.includes('unsafe-perm=true')) {
        scanResult.permissions.push({
          type: 'unsafe-perm',
          level: 'HIGH',
          message: 'Uses unsafe-perm in .npmrc'
        });
      }
    }
    
    const lockPath = path.join(packagePath, 'package-lock.json');
    if (!fs.existsSync(lockPath)) {
      scanResult.permissions.push({
        type: 'noIntegrity',
        level: 'LOW',
        message: 'No package-lock.json'
      });
    }
  }
  
  calculateOverallRisk(scanResult) {
    const riskScores = { CRITICAL: 100, HIGH: 50, MEDIUM: 25, LOW: 10, INFO: 1 };
    
    let totalScore = 0;
    const riskCounts = {};
    
    for (const risk of scanResult.risks) {
      totalScore += riskScores[risk.level] || 0;
      riskCounts[risk.level] = (riskCounts[risk.level] || 0) + 1;
    }
    
    totalScore = Math.round(totalScore / Math.max(scanResult.filesScanned || 1, 1));
    
    if (totalScore >= 75) scanResult.overallRisk = 'CRITICAL';
    else if (totalScore >= 50) scanResult.overallRisk = 'HIGH';
    else if (totalScore >= 25) scanResult.overallRisk = 'MEDIUM';
    else if (totalScore >= 10) scanResult.overallRisk = 'LOW';
    else scanResult.overallRisk = 'INFO';
    
    scanResult.riskBreakdown = riskCounts;
    scanResult.riskScore = totalScore;
  }
  
  generateRecommendation(scanResult) {
    const { overallRisk } = scanResult;
    
    if (overallRisk === 'CRITICAL') {
      scanResult.recommendation = 'BLOCK';
      scanResult.reason = 'Critical risks';
    } else if (overallRisk === 'HIGH') {
      scanResult.recommendation = 'REVIEW';
      scanResult.reason = 'High risks';
    } else if (overallRisk === 'MEDIUM') {
      scanResult.recommendation = 'CAUTION';
      scanResult.reason = 'Medium risks';
    } else {
      scanResult.recommendation = 'INSTALL';
      scanResult.reason = 'Acceptable risk';
    }
  }
  
  async finalizeScan(scanResult) {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const logFile = path.join(this.options.logDir, `scan_${timestamp}.json`);
    
    fs.writeFileSync(logFile, JSON.stringify(scanResult, null, 2));
    
    if (['BLOCK', 'REVIEW'].includes(scanResult.recommendation)) {
      const quarantineLog = path.join(this.options.logDir, 'quarantine.log');
      const logEntry = `[${scanResult.timestamp}] ${scanResult.package.name}: ${scanResult.overallRisk} - ${scanResult.recommendation}\n`;
      fs.appendFileSync(quarantineLog, logEntry);
    }
    
    this.printSummary(scanResult);
  }
  
  printSummary(scanResult) {
    const colors = {
      CRITICAL: '\x1b[31m', HIGH: '\x1b[35m', MEDIUM: '\x1b[33m',
      LOW: '\x1b[32m', INFO: '\x1b[36m', NONE: '\x1b[32m'
    };
    
    console.log('\n' + '='.repeat(60));
    console.log(`📊 SCAN RESULT: ${scanResult.package.name}@${scanResult.package.version}`);
    console.log('='.repeat(60));
    console.log(`\n🎯 Risk: ${scanResult.overallRisk}`);
    console.log(`📋 Decision: ${scanResult.recommendation}`);
    
    if (scanResult.riskBreakdown) {
      console.log('\n📈 Breakdown:', scanResult.riskBreakdown);
    }
    
    if (scanResult.risks.length > 0) {
      console.log('\n⚠️  Top risks:');
      scanResult.risks.slice(0, 3).forEach((r, i) => {
        console.log(`   ${i+1}. [${r.level}] ${r.message}`);
      });
    }
    
    const color = colors[scanResult.overallRisk] || '\x1b[0m';
    console.log(`\n${color}➤ FINAL: ${scanResult.recommendation}${'\x1b[0m'}`);
    console.log('='.repeat(60) + '\n');
  }
  
  async scanNpmPackage(packageName) {
    console.log(`\n📦 Pre-scan npm: ${packageName}`);
    
    const scanResult = {
      package: { name: packageName },
      timestamp: new Date().toISOString(),
      status: 'pre-install',
      risks: [],
      overallRisk: 'INFO',
      recommendation: 'INSTALL'
    };
    
    this.checkPackageName({ name: packageName }, scanResult);
    this.calculateOverallRisk(scanResult);
    this.generateRecommendation(scanResult);
    
    console.log(`\n📦 NPM: ${packageName}`);
    console.log(`   Risk: ${scanResult.overallRisk}`);
    console.log(`   Decision: ${scanResult.recommendation}\n`);
    
    return scanResult;
  }
  
  getStatus() {
    return {
      initialized: true,
      signaturesCount: this.signatures.size,
      suspiciousPackagesCount: this.suspiciousPackages.size,
      quarantineDir: this.options.quarantineDir,
      logDir: this.options.logDir
    };
  }
}

module.exports = { PackageSecurityScanner };

if (require.main === module) {
  const scanner = new PackageSecurityScanner();
  
  console.log('\n🛡️  Package Security Scanner\n');
  
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('Usage:');
    console.log('  node package_security_scanner.js <path>    # Scan local package');
    console.log('  node package_security_scanner.js npm:<name> # Pre-scan npm package');
    console.log('  node package_security_scanner.js --status  # Status');
    console.log('\nStatus:', JSON.stringify(scanner.getStatus(), null, 2));
  } else if (args[0] === '--status') {
    console.log(JSON.stringify(scanner.getStatus(), null, 2));
  } else if (args[0].startsWith('npm:')) {
    const packageName = args[0].substring(4);
    scanner.scanNpmPackage(packageName);
  } else {
    const packagePath = args[0];
    if (fs.existsSync(packagePath)) {
      scanner.scanPackage(packagePath);
    } else {
      console.error(`❌ Not found: ${packagePath}`);
    }
  }
}
