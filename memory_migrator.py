#!/usr/bin/env python3
"""
MD → JSON 记忆迁移脚本
将纯文本MD文件迁移到结构化JSON记忆
"""

import json
import re
from datetime import datetime
from pathlib import Path
from structured_memory import StructuredMemory


class MemoryMigrator:
    """记忆迁移器"""
    
    def __init__(self):
        self.memory = StructuredMemory()
        self.migrated_count = 0
    
    def parse_decision_from_md(self, content: str, filename: str) -> list:
        """从MD文件中提取决策"""
        decisions = []
        
        # 匹配决策模式
        patterns = [
            r'##\s*(决策|DECISION)',  # 决策标题
            r'\*\*决策\*\*[:：]?\s*(.+)',  # 决策内容
            r'意图[:：]?\s*(.+)',  # 意图
            r'置信度[:：]?\s*(\d+)%?',  # 置信度
            r'执行决策[:：]?\s*(.+)',  # 执行决策
        ]
        
        # 简化：查找包含"决策"、"意图"、"置信度"的行
        lines = content.split('\n')
        current_decision = {}
        
        for line in lines:
            line = line.strip()
            
            # 检测置信度
            if '置信度' in line or 'confidence' in line.lower():
                match = re.search(r'(\d+)%?', line)
                if match:
                    current_decision['confidence'] = int(match.group(1)) / 100
            
            # 检测意图
            if '意图' in line or 'intent' in line.lower():
                match = re.search(r'意图[:：]?\s*(.+)', line)
                if match:
                    current_decision['intent'] = match.group(1).strip()
            
            # 检测执行
            if '执行' in line and ('决策' in line or 'action' in line.lower()):
                match = re.search(r'执行[:：]?\s*(.+)', line)
                if match:
                    current_decision['action'] = match.group(1).strip()
        
        if current_decision:
            current_decision['message'] = filename
            current_decision['source_file'] = filename
            decisions.append(current_decision)
        
        return decisions
    
    def parse_learning_from_md(self, content: str, filename: str) -> list:
        """从MD文件中提取学习"""
        learnings = []
        
        lines = content.split('\n')
        current_learning = {}
        
        for line in lines:
            line = line.strip()
            
            # 检测主题
            if line.startswith('##'):
                topic = line.replace('#', '').strip()
                if len(topic) < 100:
                    current_learning['topic'] = topic
            
            # 检测学习内容
            if any(kw in line for kw in ['学习', 'LEARN', 'INSIGHT', '洞察']):
                match = re.search(r'[:：]\s*(.+)', line)
                if match:
                    current_learning['insight'] = match.group(1).strip()
                    current_learning['source'] = 'MD_MIGRATION'
        
        if current_learning and 'insight' in current_learning:
            learnings.append(current_learning)
        
        return learnings
    
    def migrate_file(self, filepath: str) -> dict:
        """迁移单个MD文件"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        filename = Path(filepath).name
        result = {
            'file': filename,
            'decisions': 0,
            'learnings': 0,
            'lines': len(content.split('\n'))
        }
        
        # 提取决策
        decisions = self.parse_decision_from_md(content, filename)
        for d in decisions:
            self.memory.save_decision(
                intent=d.get('intent', 'MIGRATED'),
                action=d.get('action', 'MIGRATED'),
                confidence=d.get('confidence', 0.8),
                message=d.get('message', filename),
                context={'source': 'md_migration', 'file': filename}
            )
            result['decisions'] += 1
        
        # 提取学习
        learnings = self.parse_learning_from_md(content, filename)
        for l in learnings:
            self.memory.save_learning(
                topic=l.get('topic', 'MIGRATED'),
                insight=l.get('insight', filename),
                source='MD_MIGRATION'
            )
            result['learnings'] += 1
        
        self.migrated_count += 1
        
        return result
    
    def migrate_all(self, md_dir: str = 'memory') -> dict:
        """迁移所有MD文件"""
        results = {
            'files': 0,
            'decisions': 0,
            'learnings': 0,
            'details': []
        }
        
        md_path = Path(md_dir)
        
        for md_file in sorted(md_path.glob('*.md')):
            if 'backup' in str(md_file) or md_file.name == 'MEMORY.md':
                continue
            
            result = self.migrate_file(str(md_file))
            results['files'] += 1
            results['decisions'] += result['decisions']
            results['learnings'] += result['learnings']
            results['details'].append(result)
        
        return results


if __name__ == "__main__":
    print("=" * 70)
    print("MD → JSON 记忆迁移")
    print("=" * 70)
    print("")
    
    migrator = MemoryMigrator()
    
    print("开始迁移...")
    print("")
    
    results = migrator.migrate_all()
    
    print("📊 迁移结果:")
    print("-" * 50)
    print(f"  文件数: {results['files']}")
    print(f"  决策: {results['decisions']}")
    print(f"  学习: {results['learnings']}")
    print("")
    
    # 显示详情
    print("📁 迁移详情:")
    print("-" * 50)
    for detail in results['details'][:5]:
        print(f"  • {detail['file']}: {detail['decisions']}决策, {detail['learnings']}学习")
    
    if len(results['details']) > 5:
        print(f"  ... 共 {len(results['details'])} 个文件")
    
    print("")
    print("=" * 70)
    print("✅ 迁移完成!")
    print("=" * 70)
