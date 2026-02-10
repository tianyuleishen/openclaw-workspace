#!/usr/bin/env node
/**
 * ClawHub Skill Package Security Scanner
 * Scans skills from clawhub.com before installation
 */

const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');

class SkillSecurityScanner {
  constructor(options = {}) {
    this.options = {
      workdir: options.workdir || '/home/admin/.openclaw/workspace',
      skillsDir: options.skillsDir || 'skills',
      quarantineDir: options.quarantineDir || '/home/admin/.openclaw/quarantine',
      logDir: options.logDir || '/home/admin/.openclaw/logs',
      ...options
    };
    
    // Suspicious patterns in skill files
    this.signatures = new Map([
      ['require("http")', 'HTTP network access'],
      ['require("https")', 'HTTPS network access'],
      ['require("dns")', 'DNS resolution'],
      ['require("net")', 'Socket operations'],
      ['require("fs")', 'File system access'],
      ['fs.writeFileSync', 'File write'],
      ['fs.unlinkSync', 'File deletion'],
      ['fs.readFileSync', 'File read'],
      ['require("child_process")', 'Process spawning'],
      ['exec(', 'Shell command execution'],
      ['execSync', 'Sync shell execution'],
      ['eval(', 'Dangerous eval'],
      ['Function(', 'Dynamic function creation'],
      ['process.env', 'Environment access'],
      ['process.exit', 'Process termination'],
      ['fetch(', 'Network fetch'],
      ['curl ', 'Curl command'],
      ['wget ', 'Wget command'],
    ]);
    
    this.highRiskPatterns = [
      { pattern: /curl\s+.*\|\s*sh/i, level: 'CRITICAL', message: 'Pipe to shell detected' },
      { pattern: /wget\s+.*\|\s*sh/i, level: 'CRITICAL', message: 'Pipe to shell detected' },
      { pattern: />\s*\/(?:etc|usr|bin|sbin)/i, level: 'HIGH', message: 'Writing to system directories' },
      { pattern: /\.env(?:\s|$|\/|\\)/i, level: 'HIGH', message: 'Accessing environment files' },
      { pattern: /chmod\s+[0-7]{3}/i, level: 'HIGH', message: 'Permission changes' },
      { pattern: /rm\s+-rf/i, level: 'HIGH', message: 'Recursive delete' },
    ];
    
    this.ensureDirectories();
    
    console.log('🔒 Skill Security Scanner initialized');
    console.log(`📁 Skills directory: ${this.options.skillsDir}`);
  }
  
  ensureDirectories() {
    for (const dir of [this.options.quarantineDir, this.options.logDir]) {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
      }
    }
  }
  
  /**
   * Parse clawhub inspect output (table format)
   */
  parseInspectOutput(output) {
    const lines = output.split('\n').filter(l => l.trim());
    const result = { slug: '', name: '', summary: '', owner: '', created: '', updated: '', latest: '', tags: {} };
    
    // Find the slug from first line (usually after "Fetching skill")
    for (const line of lines) {
      if (line.includes('Fetching skill')) continue;
      
      // Parse "slug  Name" format
      const parts = line.trim().split(/\s{2,}/);
      if (parts.length >= 2) {
        result.slug = parts[0].trim();
        result.name = parts[1].trim();
        continue;
      }
      
      // Parse "Key: Value" format
      const keyValueMatch = line.match(/^(\w+):\s*(.+)$/);
      if (keyValueMatch) {
        const key = keyValueMatch[1];
        const value = keyValueMatch[2].trim();
        
        switch (key) {
          case 'Summary': result.summary = value; break;
          case 'Owner': result.owner = value; break;
          case 'Created': result.created = value; break;
          case 'Updated': result.updated = value; break;
          case 'Latest': result.latest = value; break;
          case 'Tags': 
            const tagMatch = value.match(/latest=(\d+\.\d+\.\d+)/);
            if (tagMatch) result.tags.latest = tagMatch[1];
            break;
        }
      }
    }
    
    return result;
  }
  
  /**
   * Inspect a skill from clawhub
   */
  async inspectSkill(slug) {
    return new Promise((resolve) => {
      const cmd = `/home/admin/.npm-global/bin/clawhub inspect ${slug} --workdir ${this.options.workdir}`;
      
      exec(cmd, { timeout: 30000 }, (error, stdout, stderr) => {
        if (error) {
          resolve({ error: { message: stderr || error.message }, slug });
        } else {
          const parsed = this.parseInspectOutput(stdout);
          resolve({ ...parsed, slug });
        }
      });
    });
  }
  
  /**
   * Scan a skill from clawhub
   */
  async scanSkill(slug) {
    console.log(`\n🔍 Scanning skill: ${slug}`);
    console.log('='.repeat(60));
    
    const result = {
      slug,
      timestamp: new Date().toISOString(),
      status: 'scanned',
      risks: [],
      permissions: [],
      files: [],
      overallRisk: 'INFO',
      recommendation: 'INSTALL',
      metadata: null
    };
    
    // Get skill metadata
    console.log('\n📋 Fetching skill metadata...');
    const inspect = await this.inspectSkill(slug);
    
    if (inspect.error) {
      result.risks.push({
        type: 'INSPECT_FAILED',
        level: 'HIGH',
        message: `Failed to fetch: ${inspect.error.message}`
      });
      this.printResult(result);
      return result;
    }
    
    result.metadata = {
      name: inspect.name || slug,
      summary: inspect.summary || '',
      owner: inspect.owner || 'unknown',
      created: inspect.created,
      updated: inspect.updated,
      latestVersion: inspect.latest || inspect.tags?.latest || 'unknown'
    };
    
    console.log(`   Name: ${result.metadata.name}`);
    console.log(`   Owner: ${result.metadata.owner}`);
    console.log(`   Version: ${result.metadata.latestVersion}`);
    
    // Download and scan skill files
    console.log('\n📦 Downloading and scanning skill files...');
    await this.downloadAndScanSkill(slug, result);
    
    // Check owner reputation
    this.checkOwnerReputation(result);
    
    // Calculate risk
    this.calculateOverallRisk(result);
    this.generateRecommendation(result);
    
    this.logResult(result);
    this.printResult(result);
    
    return result;
  }
  
  async downloadAndScanSkill(slug, result) {
    const tempDir = path.join(this.options.workdir, '.temp_scan', slug);
    
    try {
      fs.mkdirSync(tempDir, { recursive: true, mode: 0o700 });
      
      // Download skill
      await this.execCommand(`/home/admin/.npm-global/bin/clawhub install ${slug} --workdir ${tempDir} --no-input`, 60000);
      
      // Scan files
      const files = this.findSkillFiles(tempDir);
      result.filesScanned = files.length;
      
      console.log(`   Scanning ${files.length} files...`);
      
      for (const file of files) {
        if (this.isScannable(file)) {
          try {
            const content = fs.readFileSync(file, 'utf8');
            const relativePath = path.relative(tempDir, file);
            
            this.scanSignatures(content, relativePath, result);
            this.scanHighRiskPatterns(content, relativePath, result);
            this.heuristicAnalysis(content, relativePath, result);
          } catch (e) {
            // Skip binary files
          }
        }
      }
      
      this.cleanupTempDir(tempDir);
      
    } catch (error) {
      result.risks.push({
        type: 'DOWNLOAD_FAILED',
        level: 'MEDIUM',
        message: `Download failed: ${error.message}`
      });
    }
  }
  
  findSkillFiles(dir) {
    const files = [];
    const excludeDirs = new Set(['node_modules', '.git', '.temp_scan']);
    
    const scan = (currentDir) => {
      if (!fs.existsSync(currentDir)) return;
      const entries = fs.readdirSync(currentDir);
      
      for (const entry of entries) {
        const fullPath = path.join(currentDir, entry);
        const stat = fs.statSync(fullPath);
        
        if (stat.isDirectory()) {
          if (!excludeDirs.has(entry)) scan(fullPath);
        } else if (this.isScannable(fullPath)) {
          files.push(fullPath);
        }
      }
    };
    
    scan(dir);
    return files;
  }
  
  isScannable(file) {
    const ext = path.extname(file).toLowerCase();
    const scannableExts = ['.js', '.ts', '.py', '.rb', '.php', '.java', '.c', '.cpp', '.h', '.lua', '.go', '.rs', '.sh', '.bash'];
    return scannableExts.includes(ext) || file.endsWith('package.json') || file.endsWith('.md');
  }
  
  scanSignatures(content, filePath, result) {
    const basename = path.basename(filePath);
    
    for (const [signature, description] of this.signatures) {
      if (content.includes(signature)) {
        result.risks.push({
          type: 'SIGNATURE',
          level: this.getRiskLevel(description),
          message: `${description} in ${basename}`,
          location: filePath
        });
      }
    }
  }
  
  scanHighRiskPatterns(content, filePath, result) {
    const basename = path.basename(filePath);
    
    for (const { pattern, level, message } of this.highRiskPatterns) {
      if (pattern.test(content)) {
        result.risks.push({
          type: 'HIGH_RISK_PATTERN',
          level,
          message: `${message} in ${basename}`,
          location: filePath
        });
      }
    }
  }
  
  heuristicAnalysis(content, filePath, result) {
    const basename = path.basename(filePath);
    
    // Obfuscation check
    const obfuscationPatterns = [
      /String\.fromCharCode/g, /\\x[0-9a-f]{2}/gi, /eval\s*\(/g
    ];
    
    let obfuscationCount = 0;
    for (const pattern of obfuscationPatterns) {
      const matches = content.match(pattern);
      if (matches) obfuscationCount += matches.length;
    }
    
    if (obfuscationCount > 2) {
      result.risks.push({
        type: 'OBFUSCATED',
        level: 'MEDIUM',
        message: `${obfuscationCount} obfuscation patterns in ${basename}`
      });
    }
    
    // Base64 check
    const base64Pattern = /([A-Za-z0-9+\/]{100,}=*\s*){3,}/g;
    if (base64Pattern.test(content)) {
      result.risks.push({
        type: 'BASE64_PAYLOAD',
        level: 'MEDIUM',
        message: `Encoded content in ${basename}`
      });
    }
  }
  
  checkOwnerReputation(result) {
    if (!result.metadata?.owner) return;
    
    const owner = result.metadata.owner;
    const trustedOwners = new Set(['steipete', 'openclaw', '官方', 'admin', 'system']);
    const suspiciousPatterns = ['hacker', 'malware', 'exploit', 'anonymous'];
    
    for (const pattern of suspiciousPatterns) {
      if (owner.toLowerCase().includes(pattern)) {
        result.risks.push({
          type: 'OWNER_REPUTATION',
          level: 'HIGH',
          message: `Suspicious owner: ${owner}`
        });
      }
    }
    
    if (trustedOwners.has(owner)) {
      result.permissions.push({ type: 'trusted_owner', level: 'INFO', message: `Trusted owner: ${owner}` });
    }
  }
  
  getRiskLevel(description) {
    if (/Shell|Pipe|exfiltrat/i.test(description)) return 'CRITICAL';
    if (/execute|spawn|write|delete|chmod/i.test(description)) return 'HIGH';
    if (/access|process|crypt|network/i.test(description)) return 'MEDIUM';
    return 'LOW';
  }
  
  calculateOverallRisk(result) {
    const riskScores = { CRITICAL: 100, HIGH: 50, MEDIUM: 25, LOW: 10, INFO: 1 };
    
    let totalScore = 0;
    const breakdown = {};
    
    for (const risk of result.risks) {
      totalScore += riskScores[risk.level] || 0;
      breakdown[risk.level] = (breakdown[risk.level] || 0) + 1;
    }
    
    totalScore = Math.round(totalScore / Math.max(result.filesScanned || 1, 1));
    
    if (totalScore >= 75) result.overallRisk = 'CRITICAL';
    else if (totalScore >= 50) result.overallRisk = 'HIGH';
    else if (totalScore >= 25) result.overallRisk = 'MEDIUM';
    else if (totalScore >= 10) result.overallRisk = 'LOW';
    else result.overallRisk = 'INFO';
    
    result.riskBreakdown = breakdown;
    result.riskScore = totalScore;
  }
  
  generateRecommendation(result) {
    const { overallRisk } = result;
    
    if (overallRisk === 'CRITICAL') {
      result.recommendation = 'BLOCK';
      result.reason = 'Critical security risks';
    } else if (overallRisk === 'HIGH') {
      result.recommendation = 'REVIEW';
      result.reason = 'High-risk patterns';
    } else if (overallRisk === 'MEDIUM') {
      result.recommendation = 'CAUTION';
      result.reason = 'Medium-risk patterns';
    } else {
      result.recommendation = 'INSTALL';
      result.reason = 'No significant risks';
    }
  }
  
  logResult(result) {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const logFile = path.join(this.options.logDir, `skill_scan_${timestamp}.json`);
    fs.writeFileSync(logFile, JSON.stringify(result, null, 2));
    
    const logPath = path.join(this.options.logDir, 'skill_scans.log');
    const logEntry = `[${result.timestamp}] ${result.slug}: ${result.overallRisk} - ${result.recommendation} - Files: ${result.filesScanned || 0}\n`;
    fs.appendFileSync(logPath, logEntry);
  }
  
  printResult(result) {
    const colors = {
      CRITICAL: '\x1b[31m', HIGH: '\x1b[35m', MEDIUM: '\x1b[33m',
      LOW: '\x1b[32m', INFO: '\x1b[36m'
    };
    
    console.log('\n' + '='.repeat(60));
    console.log(`📦 CLAWHUB SKILL SCAN: ${result.slug}`);
    console.log('='.repeat(60));
    
    if (result.metadata) {
      console.log(`\n📋 Skill Info:`);
      console.log(`   Name: ${result.metadata.name}`);
      console.log(`   Owner: ${result.metadata.owner}`);
      console.log(`   Version: ${result.metadata.latestVersion}`);
      console.log(`   Files Scanned: ${result.filesScanned || 0}`);
    }
    
    console.log(`\n🎯 Risk: ${result.overallRisk}`);
    console.log(`📋 Decision: ${result.recommendation}`);
    
    if (result.riskBreakdown) {
      console.log('\n📈 Breakdown:', 
        `Critical:${result.riskBreakdown.CRITICAL||0} ` +
        `High:${result.riskBreakdown.HIGH||0} ` +
        `Medium:${result.riskBreakdown.MEDIUM||0} ` +
        `Low:${result.riskBreakdown.LOW||0}`);
    }
    
    if (result.risks.length > 0) {
      console.log('\n⚠️  Top Risks:');
      result.risks.slice(0, 3).forEach((r, i) => {
        console.log(`   ${i+1}. [${r.level}] ${r.message}`);
      });
    }
    
    const color = colors[result.overallRisk] || '\x1b[0m';
    console.log(`\n${color}➤ FINAL: ${result.recommendation}${'\x1b[0m'}`);
    console.log('='.repeat(60) + '\n');
  }
  
  execCommand(cmd, timeout = 30000) {
    return new Promise((resolve, reject) => {
      exec(cmd, { timeout }, (error, stdout, stderr) => {
        if (error) reject(new Error(stderr || error.message));
        else resolve(stdout);
      });
    });
  }
  
  cleanupTempDir(tempDir) {
    try {
      if (fs.existsSync(tempDir)) {
        fs.rmSync(tempDir, { recursive: true, force: true });
      }
    } catch (e) {
      console.warn(`Warning: ${e.message}`);
    }
  }
}

module.exports = { SkillSecurityScanner };

// CLI
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args[0] === '--help') {
    console.log('\n🔒 ClawHub Skill Security Scanner');
    console.log('==================================');
    console.log('\nUsage:');
    console.log('  node skill_security_scanner.js scan <slug>      # Scan skill');
    console.log('  node skill_security_scanner.js install <slug>   # Secure install');
    console.log('\nExamples:');
    console.log('  node skill_security_scanner.js scan openai-whisper');
    console.log('  node skill_security_scanner.js install blogwatcher');
  } else if (args[0] === 'scan' && args[1]) {
    const scanner = new SkillSecurityScanner();
    scanner.scanSkill(args[1]).then(result => {
      process.exit(result.recommendation === 'INSTALL' ? 0 : 1);
    });
  } else if (args[0] === 'install' && args[1]) {
    console.log('Install mode - scan first then install');
    const scanner = new SkillSecurityScanner();
    scanner.scanSkill(args[1]).then(result => {
      if (['INSTALL', 'CAUTION'].includes(result.recommendation)) {
        console.log(`\n✅ Skill passed security scan. Ready to install.`);
        console.log(`   Run: clawhub install ${args[1]}`);
      } else {
        console.log(`\n❌ Skill blocked or requires review.`);
      }
    });
  }
}
