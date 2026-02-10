#!/usr/bin/env node
/**
 * OpenClaw Hybrid Security Scanner - Phase 1 & 2
 * Based on Shannon AI Hacker Architecture
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

/**
 * CWE漏洞分类数据库
 */
const CWE_DATABASE = {
  'CWE-78': { name: 'OS Command Injection', category: 'Injection', severity: 'HIGH' },
  'CWE-89': { name: 'SQL Injection', category: 'Injection', severity: 'HIGH' },
  'CWE-79': { name: 'Cross-site Scripting', category: 'XSS', severity: 'HIGH' },
  'CWE-94': { name: 'Code Injection', category: 'Code Injection', severity: 'CRITICAL' },
  'CWE-200': { name: 'Sensitive Data Exposure', category: 'Sensitive Data', severity: 'MEDIUM' },
  'CWE-259': { name: 'Hard-coded Password', category: 'Sensitive Data', severity: 'HIGH' },
  'CWE-73': { name: 'File Manipulation', category: 'File Operations', severity: 'MEDIUM' },
  'CWE-22': { name: 'Path Traversal', category: 'File Operations', severity: 'MEDIUM' },
  'CWE-327': { name: 'Weak Crypto', category: 'Cryptography', severity: 'HIGH' },
  'CWE-918': { name: 'SSRF', category: 'Network', severity: 'HIGH' },
  'CWE-915': { name: 'Prototype Pollution', category: 'Proto Pollution', severity: 'HIGH' },
  'CWE-506': { name: 'Malicious Code', category: 'Malware', severity: 'CRITICAL' },
};

/**
 * 漏洞模式库
 */
const VULNERABILITY_PATTERNS = {
  commandInjection: [
    { pattern: /exec\(/gi, cwe: 'CWE-78', severity: 'HIGH' },
    { pattern: /child_process\.(exec|execSync|spawn)/gi, cwe: 'CWE-78', severity: 'HIGH' },
    { pattern: /`\$[^`]+`/gi, cwe: 'CWE-78', severity: 'HIGH' },
  ],
  sqlInjection: [
    { pattern: /\+\s*['"].*\+\s*['"]/gi, cwe: 'CWE-89', severity: 'HIGH' },
    { pattern: /UNION\s+SELECT/gi, cwe: 'CWE-89', severity: 'HIGH' },
    { pattern: /OR\s+1\s*=\s*1/gi, cwe: 'CWE-89', severity: 'HIGH' },
  ],
  xss: [
    { pattern: /innerHTML\s*=/gi, cwe: 'CWE-79', severity: 'HIGH' },
    { pattern: /document\.write\s*\(/gi, cwe: 'CWE-79', severity: 'HIGH' },
  ],
  codeInjection: [
    { pattern: /eval\s*\(/gi, cwe: 'CWE-94', severity: 'CRITICAL' },
    { pattern: /Function\s*\(/gi, cwe: 'CWE-94', severity: 'CRITICAL' },
  ],
  sensitiveData: [
    { pattern: /api[_-]?key\s*=\s*['"][a-zA-Z0-9-_]{20,}['"]/gi, cwe: 'CWE-200', severity: 'HIGH' },
    { pattern: /password\s*=\s*['"][^'"]+['"]/gi, cwe: 'CWE-259', severity: 'HIGH' },
    { pattern: /PRIVATE\s+KEY/gi, cwe: 'CWE-200', severity: 'CRITICAL' },
  ],
  fileOperations: [
    { pattern: /fs\.writeFileSync/gi, cwe: 'CWE-73', severity: 'HIGH' },
    { pattern: /fs\.unlinkSync/gi, cwe: 'CWE-73', severity: 'HIGH' },
    { pattern: /fs\.rmSync/gi, cwe: 'CWE-73', severity: 'HIGH' },
    { pattern: /\.\.\/.*\.js/gi, cwe: 'CWE-22', severity: 'MEDIUM' },
  ],
  prototypePollution: [
    { pattern: /__proto__/gi, cwe: 'CWE-915', severity: 'HIGH' },
    { pattern: /constructor\[.*\]/gi, cwe: 'CWE-915', severity: 'HIGH' },
  ],
  cryptoMining: [
    { pattern: /coinhive/gi, cwe: 'CWE-506', severity: 'CRITICAL' },
    { pattern: /cryptonight/gi, cwe: 'CWE-506', severity: 'CRITICAL' },
    { pattern: /webminer/gi, cwe: 'CWE-506', severity: 'CRITICAL' },
  ],
  dangerousDownloads: [
    { pattern: /curl\s+.*\|\s*sh/gi, cwe: 'CWE-78', severity: 'CRITICAL' },
    { pattern: /wget\s+.*\|\s*sh/gi, cwe: 'CWE-78', severity: 'CRITICAL' },
    { pattern: /rm\s+-rf/gi, cwe: 'CWE-73', severity: 'HIGH' },
  ],
};

/**
 * Phase 1: Recon Agent
 */
class ReconAgent {
  constructor() { this.name = 'ReconAgent'; }
  
  async analyze(packagePath) {
    console.log('🔍 [ReconAgent] Analyzing package structure...');
    const info = { packagePath, packageJson: null, files: [], dependencies: [], scripts: [], permissions: [] };
    
    const packageJsonPath = path.join(packagePath, 'package.json');
    if (fs.existsSync(packageJsonPath)) {
      try {
        info.packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
        info.dependencies = Object.keys(info.packageJson.dependencies || {});
        info.scripts = Object.keys(info.packageJson.scripts || {});
        info.permissions = this.extractPermissions(info.packageJson);
      } catch (e) {
        console.error('❌ [ReconAgent] Failed to parse package.json:', e.message);
      }
    }
    
    info.files = this.findAllFiles(packagePath);
    console.log(`✅ [ReconAgent] Found ${info.files.length} files, ${info.dependencies.length} dependencies`);
    return info;
  }
  
  findAllFiles(dir) {
    const files = [];
    const exclude = new Set(['node_modules', '.git', 'dist', 'build']);
    const scan = (d) => {
      if (!fs.existsSync(d)) return;
      for (const entry of fs.readdirSync(d)) {
        const full = path.join(d, entry);
        const stat = fs.statSync(full);
        if (stat.isDirectory() && !exclude.has(entry)) scan(full);
        else if (/\.(js|ts|py|rb|php|java|cpp|c|h|lua|go|rs|sh|json|md)$/i.test(entry)) files.push(full);
      }
    };
    scan(dir);
    return files;
  }
  
  extractPermissions(pkg) {
    const perms = [];
    if (pkg.unsafePerm) perms.push('unsafe-perm');
    if (pkg.ignoreScripts) perms.push('ignore-scripts');
    if (pkg.allowRoot) perms.push('allow-root');
    return perms;
  }
}

/**
 * Phase 2: Analysis Agent (并行处理)
 */
class AnalysisAgent {
  constructor() { this.name = 'AnalysisAgent'; this.stats = { filesScanned: 0, patternsMatched: 0, startTime: Date.now() }; }
  
  async analyze(reconData) {
    console.log('🔍 [AnalysisAgent] Parallel vulnerability analysis...');
    const results = { vulnerabilities: [], heuristics: [], stats: this.stats };
    const scanPromises = [];
    
    for (const [category, patterns] of Object.entries(VULNERABILITY_PATTERNS)) {
      scanPromises.push(this.scanCategory(reconData, category, patterns));
    }
    scanPromises.push(this.scanScripts(reconData));
    scanPromises.push(this.scanMetadata(reconData));
    
    const scanResults = await Promise.all(scanPromises);
    for (const sr of scanResults) {
      results.vulnerabilities.push(...sr.vulnerabilities);
      results.heuristics.push(...sr.heuristics);
    }
    
    this.stats.endTime = Date.now();
    this.stats.duration = this.stats.endTime - this.stats.startTime;
    this.stats.filesScanned = reconData.files.length;
    console.log(`✅ [AnalysisAgent] Found ${results.vulnerabilities.length} vulnerabilities in ${this.stats.duration}ms`);
    return results;
  }
  
  async scanCategory(reconData, category, patterns) {
    const result = { vulnerabilities: [], heuristics: [] };
    for (const file of reconData.files) {
      try {
        const content = fs.readFileSync(file, 'utf8');
        const relPath = path.relative(reconData.packagePath, file);
        for (const patternDef of patterns) {
          const regex = new RegExp(patternDef.pattern.source, patternDef.pattern.flags);
          let match;
          while ((match = regex.exec(content)) !== null) {
            const lineNum = content.substring(0, match.index).split('\n').length;
            result.vulnerabilities.push({
              id: crypto.randomUUID(), cwe: patternDef.cwe, category,
              severity: patternDef.severity, file: relPath, line: lineNum,
              code: match[0].substring(0, 80),
              description: CWE_DATABASE[patternDef.cwe]?.name || 'Unknown'
            });
            this.stats.patternsMatched++;
          }
        }
      } catch (e) {}
    }
    return result;
  }
  
  async scanScripts(reconData) {
    const result = { vulnerabilities: [], heuristics: [] };
    if (reconData.packageJson?.scripts) {
      for (const [name, script] of Object.entries(reconData.packageJson.scripts)) {
        const lower = script.toLowerCase();
        if (/curl\s+.*\|\s*sh|wget\s+.*\|\s*sh|rm\s+-rf|eval\s*\(/i.test(script)) {
          result.vulnerabilities.push({
            id: crypto.randomUUID(), cwe: 'CWE-78', category: 'Script', severity: 'CRITICAL',
            file: 'package.json', script: name, code: script.substring(0, 80), description: `Dangerous script: ${name}`
          });
        }
      }
    }
    return result;
  }
  
  async scanMetadata(reconData) {
    const result = { vulnerabilities: [], heuristics: [] };
    if (reconData.permissions.includes('unsafe-perm')) {
      result.heuristics.push({ type: 'permission', severity: 'HIGH', message: 'unsafe-perm detected', recommendation: 'Review before install' });
    }
    if (!reconData.packageJson?.author && !reconData.packageJson?.maintainers?.length) {
      result.heuristics.push({ type: 'metadata', severity: 'MEDIUM', message: 'No maintainers', recommendation: 'Verify package source' });
    }
    return result;
  }
}

/**
 * Phase 3: Risk Prioritizer
 */
class RiskPrioritizer {
  prioritize(vulnerabilities) {
    const scored = vulnerabilities.map(v => ({ ...v, score: this.calculateScore(v) }));
    scored.sort((a, b) => b.score - a.score);
    return scored.map((v, i) => ({ ...v, priority: this.getPriorityLevel(v.score), rank: i + 1 }));
  }
  
  calculateScore(v) {
    const cweScore = { CRITICAL: 1.0, HIGH: 0.8, MEDIUM: 0.5, LOW: 0.3 }[v.severity] || 0.5;
    return cweScore * 0.6 + (v.confidence === 'HIGH' ? 0.4 : v.confidence === 'MEDIUM' ? 0.25 : 0.1);
  }
  
  getPriorityLevel(score) {
    if (score >= 0.8) return 'CRITICAL';
    if (score >= 0.6) return 'HIGH';
    if (score >= 0.4) return 'MEDIUM';
    return 'LOW';
  }
}

/**
 * Phase 4: Report Agent
 */
class ReportAgent {
  generate(reconData, analysisResult, duration) {
    console.log('📝 [ReportAgent] Generating report...');
    const prioritizer = new RiskPrioritizer();
    const prioritized = prioritizer.prioritize(analysisResult.vulnerabilities);
    const cweStats = this.groupByCWE(prioritized);
    const severityStats = this.groupBySeverity(prioritized);
    const recommendation = this.generateRecommendation(prioritized, analysisResult.heuristics);
    
    const report = {
      timestamp: new Date().toISOString(),
      summary: { total: prioritized.length, ...severityStats, cweCategories: Object.keys(cweStats).length, duration },
      vulnerabilities: prioritized,
      cweBreakdown: cweStats,
      severityBreakdown: severityStats,
      heuristics: analysisResult.heuristics,
      statistics: { filesScanned: analysisResult.stats.filesScanned, patternsMatched: analysisResult.stats.patternsMatched },
      recommendation,
    };
    console.log(`✅ [ReportAgent] Report generated with ${report.summary.total} findings`);
    return report;
  }
  
  groupByCWE(vulns) {
    const grouped = {};
    for (const v of vulns) {
      if (!grouped[v.cwe]) grouped[v.cwe] = { name: CWE_DATABASE[v.cwe]?.name || 'Unknown', count: 0, maxSeverity: v.severity };
      grouped[v.cwe].count++;
    }
    return grouped;
  }
  
  groupBySeverity(vulns) {
    const grouped = {};
    for (const v of vulns) grouped[v.severity] = (grouped[v.severity] || 0) + 1;
    return grouped;
  }
  
  generateRecommendation(vulns, heuristics) {
    const critical = vulns.filter(v => v.priority === 'CRITICAL').length;
    const high = vulns.filter(v => v.priority === 'HIGH').length;
    const dangerousScripts = heuristics.filter(h => h.type === 'script' && h.severity === 'CRITICAL').length;
    
    if (critical > 0 || dangerousScripts > 0) return { action: 'BLOCK', reason: 'Critical vulnerabilities detected' };
    if (high > 0) return { action: 'REVIEW', reason: 'High-risk issues require review' };
    return { action: 'INSTALL', reason: 'No significant issues detected' };
  }
}

/**
 * 主扫描器类
 */
class HybridSecurityScanner {
  constructor(options = {}) {
    this.options = { logDir: options.logDir || '/home/admin/.openclaw/logs', ...options };
    this.agents = { recon: new ReconAgent(), analysis: new AnalysisAgent(), report: new ReportAgent() };
    console.log('🛡️  Hybrid Security Scanner v2.0 initialized');
    console.log(`   CWE Database: ${Object.keys(CWE_DATABASE).length} vulnerabilities`);
    console.log(`   Pattern Database: ${Object.keys(VULNERABILITY_PATTERNS).reduce((sum, cat) => sum + VULNERABILITY_PATTERNS[cat].length, 0)} patterns`);
  }
  
  async scan(packagePath) {
    console.log(`\n🚀 Starting scan: ${packagePath}`);
    console.log('='.repeat(70));
    const startTime = Date.now();
    
    try {
      const reconData = await this.agents.recon.analyze(packagePath);
      const analysisResult = await this.agents.analysis.analyze(reconData);
      const report = this.agents.report.generate(reconData, analysisResult, Date.now() - startTime);
      await this.saveReport(report);
      this.printSummary(report);
      return report;
    } catch (error) {
      console.error('❌ Scan failed:', error.message);
      throw error;
    }
  }
  
  async saveReport(report) {
    const ts = new Date().toISOString().replace(/[:.]/g, '-');
    const reportFile = path.join(this.options.logDir, `hybrid_scan_${ts}.json`);
    fs.writeFileSync(reportFile, JSON.stringify(report, null, 2));
    const indexFile = path.join(this.options.logDir, 'hybrid_scans.log');
    fs.appendFileSync(indexFile, `[${report.timestamp}] ${report.summary.total} issues - Decision: ${report.recommendation.action}\n`);
    console.log(`✅ Report saved: ${reportFile}`);
  }
  
  printSummary(report) {
    const colors = { CRITICAL: '\x1b[31m', HIGH: '\x1b[35m', MEDIUM: '\x1b[33m', LOW: '\x1b[32m', INFO: '\x1b[36m' };
    const reset = '\x1b[0m';
    
    console.log('\n' + '='.repeat(70));
    console.log('📊 SECURITY SCAN SUMMARY');
    console.log('='.repeat(70));
    console.log(`\n🎯 Overall Risk: ${report.summary.total > 0 ? report.recommendation.action : 'INFO'}`);
    console.log(`📋 Decision: ${report.recommendation.action}`);
    
    if (report.summary.CRITICAL) console.log(`${colors.CRITICAL}CRITICAL: ${report.summary.CRITICAL}${reset}`);
    if (report.summary.HIGH) console.log(`${colors.HIGH}HIGH: ${report.summary.HIGH}${reset}`);
    if (report.summary.MEDIUM) console.log(`${colors.MEDIUM}MEDIUM: ${report.summary.MEDIUM}${reset}`);
    if (report.summary.LOW) console.log(`${colors.LOW}LOW: ${report.summary.LOW}${reset}`);
    
    if (Object.keys(report.cweBreakdown).length > 0) {
      console.log('\n🐞 Vulnerabilities by CWE:');
      for (const [cwe, data] of Object.entries(report.cweBreakdown)) {
        const color = colors[data.maxSeverity] || colors.LOW;
        console.log(`   ${color}${cwe}${reset}: ${data.name} (${data.count})`);
      }
    }
    
    if (report.vulnerabilities.length > 0) {
      console.log('\n⚠️  Top Issues:');
      report.vulnerabilities.slice(0, 3).forEach((v, i) => {
        const color = colors[v.priority] || colors.LOW;
        console.log(`   ${i+1}. [${color}${v.priority}${reset}] ${v.cwe} - ${v.description} in ${v.file}`);
      });
    }
    
    console.log('\n' + '='.repeat(70));
  }
}

module.exports = { HybridSecurityScanner };

if (require.main === module) {
  const args = process.argv.slice(2);
  const scanner = new HybridSecurityScanner();
  
  console.log('\n🛡️  OpenClaw Hybrid Security Scanner v2.0\n');
  
  if (args[0]) {
    scanner.scan(args[0]).then(r => process.exit(r.recommendation.action === 'INSTALL' ? 0 : 1));
  } else {
    console.log('Usage: node hybrid_security_scanner.js <path>');
    console.log('Example: node hybrid_security_scanner.js ./suspicious_package\n');
  }
}
