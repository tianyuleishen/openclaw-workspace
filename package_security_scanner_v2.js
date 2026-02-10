#!/usr/bin/env node
/**
 * OpenClaw Enhanced Package Security Scanner - Version 2.0
 * With improved typosquatting detection and advanced analysis
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

class EnhancedPackageScanner {
  constructor(options = {}) {
    this.options = {
      quarantineDir: options.quarantineDir || '/home/admin/.openclaw/quarantine',
      logDir: options.logDir || '/home/admin/.openclaw/logs',
      enableHeuristic: options.enableHeuristic !== false,
      enableSignature: options.enableSignature !== false,
      enableTyposquatting: options.enableTyposquatting !== false,
      ...options
    };
    
    // Popular packages for typosquatting comparison
    this.popularPackages = new Map([
      ['express', 'HIGH'], ['lodash', 'HIGH'], ['react', 'HIGH'],
      ['vue', 'HIGH'], ['axios', 'HIGH'], ['ws', 'HIGH'],
      ['koa', 'MEDIUM'], ['moment', 'MEDIUM'], ['typescript', 'HIGH'],
      ['webpack', 'HIGH'], ['babel', 'HIGH'], ['jest', 'HIGH'],
      ['mocha', 'MEDIUM'], ['mongoose', 'MEDIUM'], ['redis', 'MEDIUM'],
      ['mysql', 'MEDIUM'], ['mongodb', 'MEDIUM'], ['bcrypt', 'MEDIUM'],
      ['axios', 'HIGH'], ['socket.io', 'HIGH'], ['graphql', 'HIGH'],
      ['puppeteer', 'HIGH'], ['playwright', 'HIGH'], ['pm2', 'MEDIUM'],
    ]);
    
    this.suspiciousPackages = new Set([
      'malware', 'virus', 'trojan', 'backdoor', 'exploit',
      'hacker', 'stealer', 'logger', 'spyware', 'adware',
      'ransomware', 'rootkit', 'botnet', 'worm', 'cryptominer',
      'miner', 'coinhive', 'webminer', 'keylogger'
    ]);
    
    // Enhanced signatures
    this.signatures = new Map([
      ['child_process.exec', 'Shell command execution'],
      ['child_process.execSync', 'Sync shell execution'],
      ['child_process.spawn', 'Process spawning'],
      ['exec(', 'Shell command execution'],
      ['fs.writeFileSync', 'File write synchronization'],
      ['fs.unlinkSync', 'File deletion synchronization'],
      ['fs.rmSync', 'Recursive delete synchronization'],
      ['fs.readFileSync', 'File read synchronization'],
      ['require("http")', 'HTTP network access'],
      ['require("https")', 'HTTPS network access'],
      ['require("dns")', 'DNS resolution'],
      ['require("net")', 'Network socket access'],
      ['require("child_process")', 'Process spawning module'],
      ['eval(', 'Dangerous eval usage'],
      ['Function(', 'Dynamic function creation'],
      ['process.env', 'Environment variable access'],
      ['process.exit', 'Process termination'],
      ['process.kill', 'Process killing'],
      ['os.userInfo', 'User information leak'],
      ['os.homedir', 'Home directory access'],
      ['fetch(', 'Fetch API usage'],
      ['axios.', 'Axios HTTP client'],
      ['crypto.', 'Cryptographic operations'],
      ['Buffer.from', 'Buffer creation'],
      ['steal', 'Data stealing intent'],
      ['backdoor', 'Backdoor detection'],
      ['ransomware', 'Ransomware detection'],
    ]);
    
    // CRITICAL patterns
    this.criticalPatterns = [
      { pattern: /curl\s+.*\|\s*sh/i, message: 'Pipe to shell (curl | sh)' },
      { pattern: /wget\s+.*\|\s*sh/i, message: 'Pipe to shell (wget | sh)' },
      { pattern: />\s*\/(?:etc|usr|bin|sbin)/i, message: 'Write to system directory' },
      { pattern: /rm\s+-rf/i, message: 'Recursive delete (rm -rf)' },
      { pattern: /chmod\s+777/i, message: 'World-writable permission' },
      { pattern: /chmod\s+[0-7]{3}\s+[us]/i, message: 'Setuid/setgid permission' },
      { pattern: /sudo\s+/i, message: 'Sudo command usage' },
      { pattern: /chown\s+.*root/i, message: 'Ownership to root' },
      { pattern: /echo\s+.*>\s*\/(?:etc|usr)/i, message: 'Echo to system file' },
    ];
    
    this.highRiskPermissions = new Set([
      'unsafe-perm', 'ignore-scripts', 'ignore-engine', 'allow-root'
    ]);
    
    this.ensureDirectories();
    
    console.log('🛡️  Enhanced Package Security Scanner v2.0');
    console.log(`   Quarantine: ${this.options.quarantineDir}`);
    console.log(`   Logging: ${this.options.logDir}`);
  }
  
  ensureDirectories() {
    for (const dir of [this.options.quarantineDir, this.options.logDir]) {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
      }
    }
  }
  
  // Levenshtein distance
  levenshteinDistance(a, b) {
    if (a.length === 0) return b.length;
    if (b.length === 0) return a.length;
    
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
  
  // Jaccard similarity (n-gram)
  jaccardSimilarity(str1, str2, n = 2) {
    const getNGrams = (str) => {
      const ngrams = [];
      for (let i = 0; i <= str.length - n; i++) {
        ngrams.push(str.substring(i, i + n));
      }
      return ngrams;
    };
    
    const set1 = new Set(getNGrams(str1));
    const set2 = new Set(getNGrams(str2));
    const intersection = new Set([...set1].filter(x => set2.has(x)));
    const union = new Set([...set1, ...set2]);
    
    return union.size === 0 ? 0 : intersection.size / union.size;
  }
  
  // Soundex for phonetic similarity
  soundex(str) {
    const codes = {
      'a': '0', 'e': '0', 'i': '0', 'o': '0', 'u': '0',
      'b': '1', 'f': '1', 'p': '1', 'v': '1',
      'c': '2', 'g': '2', 'j': '2', 'k': '2', 'q': '2', 's': '2', 'x': '2', 'z': '2',
      'd': '3', 't': '3',
      'l': '4',
      'm': '5', 'n': '5',
      'r': '6'
    };
    
    let result = str.charAt(0).toUpperCase();
    let prev = codes[str.charAt(0).toLowerCase()] || '';
    
    for (let i = 1; i < str.length && result.length < 4; i++) {
      const char = str.charAt(i).toLowerCase();
      const code = codes[char] || '';
      if (code !== '0' && code !== prev) {
        result += code;
      }
      prev = code;
    }
    
    return (result + '000').substring(0, 4);
  }
  
  // Detect homoglyphs
  hasHomoglyphs(str) {
    const homoglyphs = {
      'a': ['а', 'ɑ', 'α'], 'c': ['с', 'ϲ'], 'e': ['е', 'ɛ'],
      'i': ['і', 'ι'], 'o': ['о', '0', 'ο'], 'p': ['р', 'ρ'],
      's': ['ѕ', 'ꜱ'], 'x': ['х', 'ⅹ'], 'y': ['у', 'γ']
    };
    
    let homoglyphCount = 0;
    for (const char of str.toLowerCase()) {
      for (const [latin, lookalikes] of Object.entries(homoglyphs)) {
        if (lookalikes.includes(char) && char !== latin) {
          homoglyphCount++;
        }
      }
    }
    
    return homoglyphCount / str.length > 0.3;
  }
  
  // Main typosquatting detection
  detectTyposquatting(packageName) {
    const results = [];
    const name = packageName.toLowerCase().replace(/[@-][\d.]+/g, '').replace(/[^a-z0-9]/g, '');
    
    for (const [popular, riskLevel] of this.popularPackages) {
      const popularNorm = popular.toLowerCase();
      
      // Levenshtein distance
      const levDist = this.levenshteinDistance(name, popularNorm);
      const maxLen = Math.max(name.length, popularNorm.length);
      const levSimilarity = 1 - (levDist / maxLen);
      const levThreshold = name.length <= 5 ? 1 : name.length <= 10 ? 2 : 3;
      
      if (levDist > 0 && levDist <= levThreshold && levSimilarity > 0.6) {
        results.push({
          type: 'LEVENSHTEIN', target: popular, risk: riskLevel,
          message: `Similar to '${popular}' (${levDist} edits, ${Math.round(levSimilarity * 100)}% similar)`
        });
        continue;
      }
      
      // Jaccard similarity
      const jaccard = this.jaccardSimilarity(name, popularNorm);
      if (jaccard > 0.7 && jaccard < 1.0) {
        results.push({
          type: 'JACCARD', target: popular, risk: riskLevel,
          message: `N-gram similarity to '${popular}' (${Math.round(jaccard * 100)}%)`
        });
        continue;
      }
      
      // Soundex
      if (this.soundex(name) === this.soundex(popularNorm) && name !== popularNorm) {
        results.push({
          type: 'SOUNDEX', target: popular, risk: riskLevel,
          message: `Phonetically similar to '${popular}'`
        });
        continue;
      }
      
      // Homoglyphs
      if (this.hasHomoglyphs(name)) {
        results.push({
          type: 'HOMOGLYPH', target: popular, risk: 'HIGH',
          message: `Homoglyph attack detected`
        });
      }
    }
    
    // Sort by risk
    const riskOrder = { 'HIGH': 4, 'MEDIUM': 3, 'LOW': 2 };
    results.sort((a, b) => riskOrder[b.risk] - riskOrder[a.risk]);
    
    return results.slice(0, 3);
  }
  
  async scanPackage(packagePath) {
    const packageInfo = this.parsePackagePath(packagePath);
    
    console.log(`\n🔍 Enhanced Scanning: ${packageInfo.name}@${packageInfo.version || '?'}`);
    console.log('='.repeat(70));
    
    const result = {
      package: packageInfo, timestamp: new Date().toISOString(),
      status: 'scanned', risks: [], typosquatting: [],
      permissions: [], files: [], overallRisk: 'NONE', recommendation: 'INSTALL'
    };
    
    // Typosquatting check
    if (this.options.enableTyposquatting) {
      console.log('\n📝 Checking typosquatting...');
      const typos = this.detectTyposquatting(packageInfo.name);
      if (typos.length > 0) {
        result.typosquatting = typos;
        typos.forEach(t => {
          result.risks.push({ type: 'TYPOSQUATTING', level: t.risk, message: t.message, location: 'package name' });
        });
        console.log(`   ⚠️  Found ${typos.length} typosquatting match(es)`);
      } else {
        console.log(`   ✅ No typosquatting detected`);
      }
    }
    
    // Package name check
    this.checkPackageName(packageInfo, result);
    
    // Package.json check
    await this.checkPackageJson(packagePath, result);
    
    // File scanning
    await this.scanSourceFiles(packagePath, result);
    
    // Permissions check
    this.checkPermissions(packagePath, result);
    
    // Calculate risk
    this.calculateOverallRisk(result);
    this.generateRecommendation(result);
    
    await this.finalizeScan(result);
    this.printSummary(result);
    
    return result;
  }
  
  parsePackagePath(packagePath) {
    const name = path.basename(packagePath);
    const versionMatch = name.match(/@?([\w-]+)@?([\d.]+)/);
    return {
      name: versionMatch ? versionMatch[1] : name,
      version: versionMatch ? versionMatch[2] : null,
      path: path.resolve(packagePath)
    };
  }
  
  checkPackageName(packageInfo, result) {
    const name = packageInfo.name.toLowerCase();
    for (const suspicious of this.suspiciousPackages) {
      if (name.includes(suspicious)) {
        result.risks.push({ type: 'MALICIOUS_NAME', level: 'HIGH',
          message: `Package name contains: ${suspicious}`, location: 'package name' });
      }
    }
  }
  
  async checkPackageJson(packagePath, result) {
    const jsonPath = path.join(packagePath, 'package.json');
    if (!fs.existsSync(jsonPath)) {
      result.risks.push({ type: 'MISSING_MANIFEST', level: 'INFO', message: 'No package.json' });
      return;
    }
    
    try {
      const pkg = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
      result.packageJson = pkg;
      
      // Scripts check
      if (pkg.scripts) {
        for (const [name, script] of Object.entries(pkg.scripts)) {
          const risks = this.analyzeScript(script);
          risks.forEach(r => {
            result.risks.push({ type: 'SUSPICIOUS_SCRIPT', level: r.level,
              message: `Script '${name}': ${r.message}`, location: `package.json scripts.${name}` });
          });
        }
      }
      
      // Permissions
      for (const perm of this.highRiskPermissions) {
        if (pkg[perm] === true) {
          result.permissions.push({ type: perm, level: 'HIGH', message: `High-risk: ${perm}` });
        }
      }
    } catch (e) {
      result.risks.push({ type: 'INVALID_MANIFEST', level: 'INFO', message: e.message });
    }
  }
  
  analyzeScript(script) {
    const risks = [];
    const lower = script.toLowerCase();
    for (const { pattern, message } of this.criticalPatterns) {
      if (pattern.test(lower)) {
        risks.push({ level: 'CRITICAL', message });
      }
    }
    return risks;
  }
  
  async scanSourceFiles(packagePath, result) {
    const exclude = new Set(['node_modules', '.git', 'dist', 'build']);
    const files = this.findSourceFiles(packagePath, exclude);
    result.filesScanned = files.length;
    
    console.log(`\n📂 Scanning ${files.length} files...`);
    
    for (const file of files) {
      try {
        const content = fs.readFileSync(file, 'utf8');
        const basename = path.basename(file);
        
        // Signatures
        for (const [sig, desc] of this.signatures) {
          if (content.includes(sig)) {
            result.risks.push({ type: 'SIGNATURE', level: this.getRiskLevel(desc),
              message: `${desc} in ${basename}`, location: file });
          }
        }
        
        // Heuristics
        this.heuristicAnalysis(content, basename, result);
        // Vulnerability scanning
        this.scanVulnerabilities(content, basename, result);
      } catch (e) {}
    }
    
    console.log(`   Scanned ${files.length} files`);
  }
  
  findSourceFiles(dir, exclude) {
    const files = [];
    const scan = (d) => {
      if (!fs.existsSync(d)) return;
      for (const entry of fs.readdirSync(d)) {
        const full = path.join(d, entry);
        const stat = fs.statSync(full);
        if (stat.isDirectory()) {
          if (!exclude.has(entry)) scan(full);
        } else if (/\.(js|ts|py|rb|php|java|cpp|c|h|lua|go|rs)$/.test(entry)) {
          files.push(full);
        }
      }
    };
    scan(dir);
    return files;
  }
  
  heuristicAnalysis(content, basename, result) {
    // Obfuscation
    const obfPatterns = [String.fromCharCode, /\x[0-9a-f]{2}/gi, /eval\s*\(/g];
    let obfCount = 0;
    for (const p of obfPatterns) {
      const matches = content.match(p);
      if (matches) obfCount += matches.length;
    }
    if (obfCount > 3) {
      result.risks.push({ type: 'OBFUSCATED', level: 'MEDIUM',
        message: `${obfCount} obfuscation patterns in ${basename}`, location: basename });
    }
    
    // Crypto mining
    if (/coinhive|cryptonight|webminer|ethash/i.test(content)) {
      result.risks.push({ type: 'CRYPTO_MINING', level: 'HIGH',
        message: `Crypto mining in ${basename}`, location: basename });
    }
    
    // Ransomware
    if (/ransom|encrypt.*\.lock|bitcoin.*payment/i.test(content)) {
      result.risks.push({ type: 'RANSOMWARE', level: 'HIGH',
        message: `Ransomware pattern in ${basename}`, location: basename });
    }
  }
  
  getRiskLevel(desc) {
    if (/Shell|Pipe|system|root|sudo/i.test(desc)) return 'HIGH';
    if (/execute|spawn|write|delete/i.test(desc)) return 'MEDIUM';
    return 'LOW';
  }
  
  checkPermissions(packagePath, result) {
    const npmrc = path.join(packagePath, '.npmrc');
    if (fs.existsSync(npmrc)) {
      const content = fs.readFileSync(npmrc, 'utf8');
      if (/unsafe-perm\s*=\s*true/i.test(content)) {
        result.permissions.push({ type: 'unsafe-perm', level: 'HIGH', message: 'unsafe-perm in .npmrc' });
      }
    }
  }
  
  calculateOverallRisk(result) {
    const scores = { CRITICAL: 100, HIGH: 50, MEDIUM: 25, LOW: 10, INFO: 1 };
    let total = 0;
    const breakdown = {};
    
    for (const r of result.risks) {
      total += scores[r.level] || 0;
      breakdown[r.level] = (breakdown[r.level] || 0) + 1;
    }
    
    total = Math.round(total / Math.max(result.filesScanned || 1, 1));
    
    if (total >= 75) result.overallRisk = 'CRITICAL';
    else if (total >= 50) result.overallRisk = 'HIGH';
    else if (total >= 25) result.overallRisk = 'MEDIUM';
    else if (total >= 10) result.overallRisk = 'LOW';
    else result.overallRisk = 'INFO';
    
    result.riskBreakdown = breakdown;
    result.riskScore = total;
  }
  
  generateRecommendation(result) {
    if (result.overallRisk === 'CRITICAL') {
      result.recommendation = 'BLOCK';
      result.reason = 'Critical security risks';
    } else if (result.overallRisk === 'HIGH') {
      result.recommendation = 'REVIEW';
      result.reason = 'High-risk patterns';
    } else if (result.overallRisk === 'MEDIUM') {
      result.recommendation = 'CAUTION';
      result.reason = 'Medium-risk patterns';
    } else {
      result.recommendation = 'INSTALL';
      result.reason = 'Acceptable risk';
    }
  }
  
  async finalizeScan(result) {
    const ts = new Date().toISOString().replace(/[:.]/g, '-');
    const logFile = path.join(this.options.logDir, `enhanced_scan_${ts}.json`);
    fs.writeFileSync(logFile, JSON.stringify(result, null, 2));
    
    const logPath = path.join(this.options.logDir, 'enhanced_scans.log');
    const entry = `[${result.timestamp}] ${result.package.name}: ${result.overallRisk} - ${result.recommendation}\n`;
    fs.appendFileSync(logPath, entry);
  }
  
  printSummary(result) {
    const colors = { CRITICAL: '\x1b[31m', HIGH: '\x1b[35m', MEDIUM: '\x1b[33m',
      LOW: '\x1b[32m', INFO: '\x1b[36m' };
    
    console.log('\n' + '='.repeat(70));
    console.log(`📊 ENHANCED SCAN RESULT: ${result.package.name}`);
    console.log('='.repeat(70));
    
    console.log(`\n🎯 Risk: ${result.overallRisk} | 📋 Decision: ${result.recommendation}`);
    
    if (result.riskBreakdown) {
      console.log('\n📈 Breakdown:', 
        `Critical:${result.riskBreakdown.CRITICAL||0} ` +
        `High:${result.riskBreakdown.HIGH||0} ` +
        `Medium:${result.riskBreakdown.MEDIUM||0} ` +
        `Low:${result.riskBreakdown.LOW||0}`);
    }
    
    if (result.typosquatting.length > 0) {
      console.log('\n⚠️  Typosquatting detected:');
      result.typosquatting.forEach((t, i) => console.log(`   ${i+1}. [${t.risk}] ${t.message}`));
    }
    
    if (result.risks.length > 0 && result.risks.length <= 5) {
      console.log('\n⚠️  Risks:');
      result.risks.forEach((r, i) => console.log(`   ${i+1}. [${r.level}] ${r.message}`));
    }
    
    const color = colors[result.overallRisk] || '\x1b[0m';
    console.log(`\n${color}➤ FINAL: ${result.recommendation}${'\x1b[0m'}`);
    console.log('='.repeat(70) + '\n');
  }
}

module.exports = { EnhancedPackageScanner };

if (require.main === module) {
  const args = process.argv.slice(2);
  const scanner = new EnhancedPackageScanner();
  
  console.log('\n🛡️  Enhanced Package Security Scanner v2.0\n');
  
  if (args[0] && args[0] !== '--help') {
    scanner.scanPackage(args[0]).then(r => process.exit(r.recommendation === 'INSTALL' ? 0 : 1));
  } else {
    console.log('Usage: node package_security_scanner_v2.js <path>');
    console.log('Example: node package_security_scanner_v2.js ./suspicious_package\n');
  }
}

  // Vulnerability-specific patterns
  this.vulnerabilityPatterns = {
    // XSS Vulnerabilities
    xss: [
      { pattern: /innerHTML\s*=/i, level: 'HIGH', message: 'XSS: innerHTML assignment' },
      { pattern: /outerHTML\s*=/i, level: 'HIGH', message: 'XSS: outerHTML assignment' },
      { pattern: /document\.write\s*\(/i, level: 'HIGH', message: 'XSS: document.write' },
      { pattern: /location\.href\s*=/i, level: 'MEDIUM', message: 'XSS: location.href assignment' },
      { pattern: /window\.location\s*=/i, level: 'MEDIUM', message: 'XSS: window.location assignment' },
      { pattern: /eval\s*\(\s*(?:user|input|param|data)/i, level: 'CRITICAL', message: 'XSS: eval with user input' },
      { pattern: /\<script\>.*\<\/script\>/i, level: 'HIGH', message: 'XSS: Script tag detected' },
    ],
    
    // SQL Injection
    sqlInjection: [
      { pattern: /\+\s*['"].*['"]\s*\+/i, level: 'HIGH', message: 'SQLi: String concatenation' },
      { pattern: /SELECT\s+.*\s+FROM/i, level: 'INFO', message: 'SQL: SELECT statement' },
      { pattern: /INSERT\s+.*\s+INTO/i, level: 'INFO', message: 'SQL: INSERT statement' },
      { pattern: /DELETE\s+.*\s+FROM/i, level: 'INFO', message: 'SQL: DELETE statement' },
      { pattern: /DROP\s+TABLE/i, level: 'HIGH', message: 'SQLi: DROP TABLE' },
      { pattern: /UNION\s+SELECT/i, level: 'HIGH', message: 'SQLi: UNION attack' },
      { pattern: /OR\s+1\s*=\s*1/i, level: 'HIGH', message: 'SQLi: OR 1=1 tautology' },
      { pattern: /'\s+OR\s+'1'\s*=\s*'1/i, level: 'HIGH', message: 'SQLi: Classic OR injection' },
    ],
    
    // Prototype Pollution
    prototypePollution: [
      { pattern: /target\s*\[\s*['"]?\s*__proto__\s*['"]?\s*\]/i, level: 'CRITICAL', message: 'ProtoPollution: __proto__ assignment' },
      { pattern: /source\s*\[\s*['"]?\s*__proto__\s*['"]?\s*\]/i, level: 'CRITICAL', message: 'ProtoPollution: __proto__ in source' },
      { pattern: /target\s*\.\s*constructor\s*\[/i, level: 'CRITICAL', message: 'ProtoPollution: constructor access' },
      { pattern: /Object\.assign\s*\(\s*\{\s*\}\s*,/i, level: 'MEDIUM', message: 'ProtoPollution: Unsafe Object.assign' },
      { pattern: /for\s*\(.*\s+in\s+.*\)\s*\{\s*[^}]*target\s*\[/i, level: 'HIGH', message: 'ProtoPollution: Unsafe for-in loop' },
    ],
    
    // Secrets Exposure
    secretsExposure: [
      { pattern: /api[_-]?key\s*=\s*['"][a-zA-Z0-9-_]{20,}['"]/i, level: 'HIGH', message: 'Secret: API key exposed' },
      { pattern: /secret[_-]?token\s*=\s*['"][a-zA-Z0-9-_]{20,}['"]/i, level: 'HIGH', message: 'Secret: Token exposed' },
      { pattern: /password\s*=\s*['"][^'"]+['"]/i, level: 'HIGH', message: 'Secret: Password hardcoded' },
      { pattern: /private[_-]?key/i, level: 'HIGH', message: 'Secret: Private key' },
      { pattern: /BEGIN\s+(?:RSA|EC|DSA|OPENSSH)?\s*PRIVATE\s+KEY/i, level: 'CRITICAL', message: 'Secret: Private key file' },
      { pattern: /process\.env\s*\[\s*['"]\w*(?:API|TOKEN|KEY|SECRET|PASSWORD)\w*['"]\s*\]/i, level: 'MEDIUM', message: 'Secret: Env variable access' },
      { pattern: /aws[_-]?access[_-]?key/i, level: 'HIGH', message: 'Secret: AWS credentials' },
      { pattern: /github[_-]?token/i, level: 'HIGH', message: 'Secret: GitHub token' },
    ],
    
    // Command Injection
    commandInjection: [
      { pattern: /\`\s*\$\{/i, level: 'HIGH', message: 'CmdInj: Template literal with variable' },
      { pattern: /exec\s*\(\s*['"`]\s*\$\{/i, level: 'CRITICAL', message: 'CmdInj: exec with template literal' },
      { pattern: /execSync\s*\(\s*['"`]/i, level: 'HIGH', message: 'CmdInj: execSync with user input' },
      { pattern: /spawn\s*\(\s*['"`].*\$\{/i, level: 'HIGH', message: 'CmdInj: spawn with variable' },
    ],
    
    // Path Traversal
    pathTraversal: [
      { pattern: /\.\.\/.*\.js/i, level: 'MEDIUM', message: 'Path: Directory traversal' },
      { pattern: /require\s*\(\s*['"]\.\.\//i, level: 'MEDIUM', message: 'Path: Relative path traversal' },
      { pattern: /fs\.readFile\s*\(\s*['"`]\//i, level: 'INFO', message: 'Path: Absolute path access' },
      { pattern: /__dirname\s*\+\s*['"]\/../i, level: 'MEDIUM', message: 'Path: Path traversal with dirname' },
    ]
  };
  
  // Vulnerability-specific scanning
  scanVulnerabilities(content, filePath, result) {
    const basename = path.basename(filePath);
    
    for (const [category, patterns] of Object.entries(this.vulnerabilityPatterns)) {
      for (const { pattern, level, message } of patterns) {
        if (pattern.test(content)) {
          // Skip if already detected
          const exists = result.risks.some(r => 
            r.type === 'VULNERABILITY' && 
            r.message === message &&
            r.location === basename
          );
          
          if (!exists) {
            result.risks.push({
              type: 'VULNERABILITY',
              category: category.toUpperCase(),
              level,
              message: `${message} in ${basename}`,
              location: basename,
              signature: pattern.toString().substring(0, 50)
            });
          }
        }
      }
    }
  }
  
