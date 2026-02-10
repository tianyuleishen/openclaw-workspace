#!/usr/bin/env node
/**
 * Autonomous Memory Management System
 * 自动记忆管理系统
 * 
 * 功能:
 * - 自动记忆检索和索引
 * - 分层记忆架构
 * - 定期维护和摘要
 */

const fs = require('fs');
const path = require('path');

class AutonomousMemoryManager {
  constructor() {
    this.workspace = '/home/admin/.openclaw/workspace';
    this.memoryDir = path.join(this.workspace, 'memory');
    this.memoryFile = path.join(this.workspace, 'MEMORY.md');
    
    // 记忆统计
    this.stats = {
      totalFiles: 0,
      totalLines: 0,
      keywords: new Set(),
      categories: {}
    };
  }

  /**
   * 自动索引所有记忆文件
   */
  async indexMemoryFiles() {
    console.log('🔍 开始自动索引记忆文件...');
    
    const files = fs.readdirSync(this.memoryDir)
      .filter(f => f.endsWith('.md'))
      .sort();
    
    this.stats.totalFiles = files.length;
    this.stats.totalLines = 0;
    this.stats.keywords = new Set();
    
    const index = {
      files: [],
      keywords: {},
      lastUpdated: new Date().toISOString()
    };
    
    for (const file of files) {
      const content = fs.readFileSync(path.join(this.memoryDir, file), 'utf8');
      const lines = content.split('\n');
      this.stats.totalLines += lines.length;
      
      // 提取关键词
      const keywords = this.extractKeywords(content);
      keywords.forEach(kw => {
        if (!index.keywords[kw]) index.keywords[kw] = [];
        index.keywords[kw].push(file);
        this.stats.keywords.add(kw);
      });
      
      index.files.push({
        name: file,
        lines: lines.length,
        updated: fs.statSync(path.join(this.memoryDir, file)).mtime
      });
    }
    
    // 保存索引
    fs.writeFileSync(
      path.join(this.memoryDir, '.index.json'),
      JSON.stringify(index, null, 2)
    );
    
    console.log(`✅ 索引完成: ${files.length} 个文件, ${this.stats.keywords.size} 个关键词`);
    return index;
  }

  /**
   * 提取关键词
   */
  extractKeywords(content) {
    const keywords = new Set();
    const patterns = [
      /\*\*([^*]+)\*\*/g,  // 粗体文本
      /## ([^#\n]+)/g,     // 二级标题
      /### ([^#\n]+)/g,    // 三级标题
      /- ([^*]+):/g,       // 列表项带冒号
      /`([^`]+)`/g         // 代码块
    ];
    
    patterns.forEach(pattern => {
      let match;
      while ((match = pattern.exec(content)) !== null) {
        const words = match[1].toLowerCase().split(/\s+/);
        words.forEach(w => {
          if (w.length > 3) keywords.add(w);
        });
      }
    });
    
    return keywords;
  }

  /**
   * 快速检索记忆
   */
  search(query) {
    const indexPath = path.join(this.memoryDir, '.index.json');
    if (!fs.existsSync(indexPath)) {
      this.indexMemoryFiles();
    }
    
    const index = JSON.parse(fs.readFileSync(indexPath, 'utf8'));
    const queryLower = query.toLowerCase();
    const results = [];
    
    // 在关键词索引中搜索
    Object.entries(index.keywords).forEach(([keyword, files]) => {
      if (keyword.includes(queryLower) || queryLower.includes(keyword)) {
        files.forEach(f => {
          if (!results.find(r => r.file === f)) {
            results.push({
              file: f,
              relevance: this.calculateRelevance(keyword, queryLower)
            });
          }
        });
      }
    });
    
    // 按相关性排序
    results.sort((a, b) => b.relevance - a.relevance);
    
    return {
      query,
      results: results.slice(0, 10),
      total: results.length,
      indexed: index.lastUpdated
    };
  }

  /**
   * 计算相关性分数
   */
  calculateRelevance(keyword, query) {
    if (keyword === query) return 1.0;
    if (keyword.startsWith(query)) return 0.8;
    if (keyword.includes(query)) return 0.6;
    return 0.3;
  }

  /**
   * 生成每日摘要
   */
  generateDailySummary() {
    const today = new Date().toISOString().split('T')[0];
    const summary = {
      date: today,
      memoryFiles: this.stats.totalFiles,
      totalLines: this.stats.totalLines,
      keywords: this.stats.keywords.size,
      recentChanges: [],
      recommendations: []
    };
    
    // 检查最近更改的文件
    const files = fs.readdirSync(this.memoryDir)
      .filter(f => f.endsWith('.md') && f !== '.index.json');
    
    files.slice(-5).forEach(f => {
      const stat = fs.statSync(path.join(this.memoryDir, f));
      summary.recentChanges.push({
        file: f,
        modified: stat.mtime
      });
    });
    
    // 生成建议
    if (this.stats.totalLines > 10000) {
      summary.recommendations.push('考虑压缩或归档旧记忆');
    }
    if (this.stats.keywords.size < 50) {
      summary.recommendations.push('建议添加更多关键词标签');
    }
    
    return summary;
  }

  /**
   * 获取记忆统计
   */
  getStats() {
    return {
      ...this.stats,
      memoryDir: this.memoryDir,
      lastIndexed: new Date().toISOString()
    };
  }
}

// CLI接口
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];
  const manager = new AutonomousMemoryManager();
  
  switch (command) {
    case 'index':
      manager.indexMemoryFiles().then(() => {
        console.log('📊 统计:', JSON.stringify(manager.getStats(), null, 2));
      });
      break;
      
    case 'search':
      const query = args[1];
      if (query) {
        const results = manager.search(query);
        console.log('🔍 搜索结果:', JSON.stringify(results, null, 2));
      } else {
        console.log('用法: node memory_manager.js search "关键词"');
      }
      break;
      
    case 'summary':
      console.log('📋 每日摘要:', JSON.stringify(manager.generateDailySummary(), null, 2));
      break;
      
    case 'stats':
      console.log('📊 统计:', JSON.stringify(manager.getStats(), null, 2));
      break;
      
    default:
      console.log(`
🤖 自主记忆管理系统

用法:
  node memory_manager.js index      # 索引所有记忆文件
  node memory_manager.js search "关键词"  # 搜索记忆
  node memory_manager.js summary   # 生成每日摘要
  node memory_manager.js stats     # 查看统计

功能:
  - 自动索引记忆文件
  - 快速关键词搜索
  - 生成摘要和建议
  - 统计记忆使用情况
      `);
  }
}

module.exports = AutonomousMemoryManager;
