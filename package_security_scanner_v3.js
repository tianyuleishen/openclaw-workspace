#!/usr/bin/env node
/**
 * OpenClaw Enhanced Package Security Scanner - Version 3.0
 * Comprehensive vulnerability detection with CWE patterns
 */

const fs = require('fs');
const path = require('path');

class VulnerabilityScanner {
  constructor(options = {}) {
    this.options = {
      quarantineDir: options.quarantineDir || '/home/admin/.openclaw/quarantine',
      logDir: options.logDir || '/home/admin/.openclaw/logs',
      enableTyposquatting: options.enableTyposquatting !== false,
      enableVulnerabilities: options.enableVulnerabilities !== false,
      ...options
    };
    
    this.popularPackages = new Map([
      ['express', 'HIGH'], ['lodash', 'HIGH'], ['react', 'HIGH'],
      ['vue', 'HIGH'], ['axios', 'HIGH'], ['ws', 'HIGH'],
      ['koa', 'MEDIUM'], ['moment', 'MEDIUM'], ['typescript', 'HIGH'],
      ['webpack', 'HIGH'], ['babel', 'HIGH'], ['jest', 'HIGH'],
      ['mocha', 'MEDIUM'], ['mongoose', 'MEDIUM'], ['redis', 'MEDIUM'],
      ['mysql', 'MEDIUM'], ['mongodb', 'MEDIUM'], ['bcrypt', 'MEDIUM'],
    ]);
    
    this.suspiciousPackages = new Set([
      'malware', 'virus', 'trojan', 'backdoor', 'exploit',
      'hacker', 'stealer', 'logger', 'spyware', 'adware',
      'ransomware', 'rootkit', 'botnet', 'worm', 'cryptominer',
      'miner', 'coinhive', 'webminer', 'keylogger'
    ]);
    
    this.signatures = new Map([
      ['child_process.exec', 'Shell command'],
      ['exec(', 'Shell command'],
      ['fs.writeFileSync', 'File write'],
      ['fs.unlinkSync', 'File deletion'],
      ['require("http")', 'HTTP access'],
      ['eval(', 'Dangerous eval'],
      ['process.env', 'Env access'],
    ]);
    
    this.criticalPatterns = [
      { pattern: /curl\s+.*\|\s*sh/i, message: 'Pipe to shell' },
      { pattern: /wget\s+.*\|\s*sh/i, message: 'Pipe to shell' },
      { pattern: /rm\s+-rf/i, message: 'Recursive delete' },
      { pattern: /chmod\s+777/i, message: 'World-writable' },
    ];
    
    this.vulnerabilityPatterns = {
      xss: [
        { pattern: /innerHTML\s*=/i, level: 'HIGH', cwe: 'CWE-79', message: 'XSS: innerHTML' },
        { pattern: /outerHTML\s*=/i, level: 'HIGH', cwe: 'CWE-79', message: 'XSS: outerHTML' },
        { pattern: /document\.write\s*\(/i, level: 'HIGH', cwe: 'CWE-79', message: 'XSS: document.write' },
        { pattern: /location\.href\s*=/i, level: 'MEDIUM', cwe: 'CWE-79', message: 'XSS: location.href' },
      ],
      sqlInjection: [
        { pattern: /\+\s*['"].*['"]\s*\+/i, level: 'HIGH', cwe: 'CWE-89', message: 'SQLi: String concat' },
        { pattern: /UNION\s+SELECT/i, level: 'HIGH', cwe: 'CWE-89', message: 'SQLi: UNION' },
        { pattern: /OR\s+1\s*=\s*1/i, level: 'HIGH', cwe: 'CWE-89', message: 'SQLi: OR 1=1' },
        { pattern: /DROP\s+TABLE/i, level: 'HIGH', cwe: 'CWE-89', message: 'SQLi: DROP' },
      ],
      codeInjection: [
        { pattern: /eval\s*\(\s*['"].*\$/i, level: 'CRITICAL', cwe: 'CWE-94', message: 'Code Injection: eval' },
        { pattern: /exec\s*\(\s*['"].*\$/i, level: 'CRITICAL', cwe: 'CWE-94', message: 'Code Injection: exec' },
        { pattern: /Function\s*\(\s*['"].*\$/i, level: 'CRITICAL', cwe: 'CWE-94', message: 'Code Injection' },
      ],
      prototypePollution: [
        { pattern: /target\s*\[\s*['"]?\s*__proto__/i, level: 'CRITICAL', cwe: 'CWE-915', message: 'ProtoPollution: __proto__' },
        { pattern: /source\s*\[\s*['"]?\s*__proto__/i, level: 'CRITICAL', cwe: 'CWE-915', message: 'ProtoPollution: __proto__' },
        { pattern: /\.constructor\s*\[/i, level: 'HIGH', cwe: 'CWE-915', message: 'ProtoPollution: constructor' },
      ],
      sensitiveData: [
        { pattern: /api[_-]?key\s*=\s*['"][a-zA-Z0-9-_]{20,}['"]/i, level: 'HIGH', cwe: 'CWE-200', message: 'Secret: API key' },
        { pattern: /secret[_-]?token\s*=\s*['"][a-zA-Z0-9-_]{20,}['"]/i, level: 'HIGH', cwe: 'CWE-200', message: 'Secret: Token' },
        { pattern: /password\s*=\s*['"][^'"]+['"]/i, level: 'HIGH', cwe: 'CWE-200', message: 'Secret: Password' },
        { pattern: /PRIVATE\s+KEY/i, level: 'CRITICAL', cwe: 'CWE-200', message: 'Secret: Private key' },
        { pattern: /process\.env\s*\[\s*['"][^'"]*['"]\s*\]/i, level: 'MEDIUM', cwe: 'CWE-200', message: 'Secret: Env var' },
      ],
      cryptoMining: [
        { pattern: /coinhive/i, level: 'HIGH', cwe: 'CWE-506', message: 'Crypto Mining' },
        { pattern: /cryptonight/i, level: 'HIGH', cwe: 'CWE-506', message: 'Crypto Mining' },
        { pattern: /webminer/i, level: 'HIGH', cwe: 'CWE-506', message: 'Crypto Mining' },
        { pattern: /nicehash/i, level: 'HIGH', cwe: 'CWE-506', message: 'Crypto Mining' },
      ],
    };
    
    console.log('🛡️  Vulnerability Scanner v3.0 initialized');
    console.log('   CVE Categories:', Object.keys(this.vulnerabilityPatterns).length);
  }
  
  levenshteinDistance(a, b) {
    if (a.length === 0) return b.length;
    if (b.length === 0) return a.length;
    const matrix = [];
    for (let i = 0; i <= b.length; i++) matrix[i] = [i];
    for (let j = 0; j <= a.length; j++) matrix[0][j] = j;
    for (let i = 1; i <= b.length; i++) {
      for (let j = 1; j <= a.length; j++) {
        if (b.charAt(i - 1) === a.charAt(j - 1)) {
          matrix[i][j] = matrix[i - 1][j - 1];
        } else {
          matrix[i][j] = Math.min(matrix[i - 1][j - 1] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j] + 1);
        }
      }
    }
    return matrix[b.length][a.length];
  }
  
  detectTyposquatting(name) {
    const results = [];
    const normalized = name.toLowerCase().replace(/[@-][\d.]+/g, '').replace(/[^a-z0-9]/g, '');
    for (const [popular, risk] of this.popularPackages) {
      const dist = this.levenshteinDistance(normalized, popular.toLowerCase());
      const threshold = normalized.length <= 5 ? 1 : normalized.length <= 10 ? 2 : 3;
      const similarity = 1 - (dist / Math.max(normalized.length, popular.length));
      if (dist > 0 && dist <= threshold && similarity > 0.6) {
        results.push({ target: popular, risk, message: `Similar to '${popular}' (${dist} edits)` });
      }
    }
    return results.slice(0, 3);
  }
  
  async scanPackage(packagePath) {
    const packageInfo = { name: path.basename(packagePath), version: null };
    console.log(`\n🔍 Scanning: ${packageInfo.name}`);
    console.log('='.repeat(70));
    
    const result = {
      package: packageInfo, timestamp: new Date().toISOString(),
      status: 'scanned', risks: [], vulnerabilities: [],
      typosquatting: [], cweBreakdown: {}, overallRisk: 'INFO', recommendation: 'INSTALL'
    };
    
    // Typosquatting
    const typos = this.detectTyposquatting(packageInfo.name);
    if (typos.length > 0) {
      result.typosquatting = typos;
      typos.forEach(t => result.risks.push({ type: 'TYPOSQUATTING', level: t.risk, message: t.message }));
      console.log(`   ⚠️  Typosquatting: ${typos.length} matches`);
    }
    
    // Scan files
    const files = this.findFiles(packagePath);
    result.filesScanned = files.length;
    console.log(`   📂 Scanning ${files.length} files...`);
    
    for (const file of files) {
      try {
        const content = fs.readFileSync(file, 'utf8');
        const basename = path.basename(file);
        
        // Signatures
        for (const [sig, desc] of this.signatures) {
          if (content.includes(sig)) {
            result.risks.push({ type: 'SIGNATURE', level: 'MEDIUM', message: `${desc} in ${basename}` });
          }
        }
        
        // Critical patterns
        for (const { pattern, message } of this.criticalPatterns) {
          if (pattern.test(content)) {
            result.risks.push({ type: 'CRITICAL', level: 'CRITICAL', message: `${message} in ${basename}` });
          }
        }
        
        // Vulnerabilities
        for (const [category, patterns] of Object.entries(this.vulnerabilityPatterns)) {
          for (const { pattern, level, cwe, message } of patterns) {
            if (pattern.test(content)) {
              result.vulnerabilities.push({ category, cwe, level, message: `${message} in ${basename}` });
              result.cweBreakdown[cwe] = (result.cweBreakdown[cwe] || 0) + 1;
              result.risks.push({ type: 'VULNERABILITY', category, cwe, level, message: `${message} in ${basename}` });
            }
          }
        }
      } catch (e) {}
    }
    
    this.calculateRisk(result);
    this.printSummary(result);
    
    // Log
    const ts = new Date().toISOString().replace(/[:.]/g, '-');
    fs.writeFileSync(path.join(this.options.logDir, `vuln_scan_${ts}.json`), JSON.stringify(result, null, 2));
    
    return result;
  }
  
  findFiles(dir) {
    const files = [];
    const exclude = new Set(['node_modules', '.git', 'dist']);
    const scan = (d) => {
      if (!fs.existsSync(d)) return;
      for (const entry of fs.readdirSync(d)) {
        const full = path.join(d, entry);
        const stat = fs.statSync(full);
        if (stat.isDirectory() && !exclude.has(entry)) scan(full);
        else if (/\.(js|ts|py|rb|php|java)$/.test(entry)) files.push(full);
      }
    };
    scan(dir);
    return files;
  }
  
  calculateRisk(result) {
    const scores = { CRITICAL: 100, HIGH: 50, MEDIUM: 25, LOW: 10, INFO: 1 };
    let total = result.risks.reduce((sum, r) => sum + (scores[r.level] || 0), 0);
    total = Math.round(total / Math.max(result.filesScanned || 1, 1));
    
    if (total >= 75) result.overallRisk = 'CRITICAL';
    else if (total >= 50) result.overallRisk = 'HIGH';
    else if (total >= 25) result.overallRisk = 'MEDIUM';
    else if (total >= 10) result.overallRisk = 'LOW';
    else result.overallRisk = 'INFO';
    
    if (result.overallRisk === 'CRITICAL') result.recommendation = 'BLOCK';
    else if (result.overallRisk === 'HIGH') result.recommendation = 'REVIEW';
    else if (result.overallRisk === 'MEDIUM') result.recommendation = 'CAUTION';
    else result.recommendation = 'INSTALL';
  }
  
  printSummary(result) {
    const colors = { CRITICAL: '\x1b[31m', HIGH: '\x1b[35m', MEDIUM: '\x1b[33m', LOW: '\x1b[32m', INFO: '\x1b[36m' };
    const color = colors[result.overallRisk] || '\x1b[0m';
    
    console.log('\n' + '='.repeat(70));
    console.log(`📊 VULNERABILITY SCAN: ${result.package.name}`);
    console.log('='.repeat(70));
    console.log(`\n🎯 Risk: ${result.overallRisk} | 📋 Decision: ${result.recommendation}`);
    
    if (Object.keys(result.cweBreakdown).length > 0) {
      console.log('\n🐞 Vulnerabilities by CWE:');
      for (const [cwe, count] of Object.entries(result.cweBreakdown)) {
        console.log(`   ${cwe}: ${count}`);
      }
    }
    
    if (result.vulnerabilities.length > 0) {
      console.log('\n⚠️  Top Vulnerabilities:');
      result.vulnerabilities.slice(0, 5).forEach((v, i) => {
        console.log(`   ${i+1}. [${v.level}] ${v.cwe} - ${v.message}`);
      });
    }
    
    console.log(`\n${color}➤ FINAL: ${result.recommendation}${'\x1b[0m'}`);
    console.log('='.repeat(70) + '\n');
  }
}

module.exports = { VulnerabilityScanner };

if (require.main === module) {
  const args = process.argv.slice(2);
  const scanner = new VulnerabilityScanner();
  if (args[0]) scanner.scanPackage(args[0]).then(r => process.exit(r.recommendation === 'INSTALL' ? 0 : 1));
}
