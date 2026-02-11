#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小爪自动任务规划器 v1.0
每日自动任务规划和执行

功能：
- 每日任务清单生成
- 自动执行学习任务
- 进度追踪
- 自我评估
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict
from dataclasses import dataclass, field


@dataclass
class Task:
    """任务"""
    id: str
    name: str
    description: str
    category: str  # learning, work, health, improvement
    priority: int  # 1-5
    status: str  # pending, in_progress, completed, skipped
    scheduled_time: str = None
    completed_time: str = None
    duration_minutes: int = 30
    notes: str = None


class AutoPlanner:
    """自动任务规划器"""
    
    def __init__(self):
        self.tasks_file = '/home/admin/.openclaw/workspace/选股结果/daily_tasks.json'
        self.history_file = '/home/admin/.openclaw/workspace/选股结果/task_history.json'
        self.today_tasks = []
        self.load_tasks()
        
    def load_tasks(self):
        """加载任务"""
        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.today_tasks = [Task(**t) for t in data.get('tasks', [])]
        else:
            self.today_tasks = []
    
    def save_tasks(self):
        """保存任务"""
        data = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'tasks': [t.__dict__ for t in self.today_tasks]
        }
        with open(self.tasks_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def generate_daily_tasks(self) -> List[Task]:
        """生成每日任务清单"""
        tasks = []
        task_id = datetime.now().strftime('%Y%m%d')
        
        # 早晨任务 (6:00-9:00)
        tasks.extend([
            Task(
                id=f"{task_id}_001",
                name="回顾昨日进展",
                description="检查MEMORY.md和昨日日志",
                category="work",
                priority=5,
                status="pending",
                duration_minutes=15
            ),
            Task(
                id=f"{task_id}_002",
                name="生成今日计划",
                description="根据MEMORY.md生成今日任务清单",
                category="work",
                priority=5,
                status="pending",
                duration_minutes=10
            ),
            Task(
                id=f"{task_id}_003",
                name="GitHub趋势学习",
                description="查看GitHub Trending AI项目",
                category="learning",
                priority=4,
                status="pending",
                duration_minutes=30
            ),
        ])
        
        # 上午任务 (9:00-12:00)
        tasks.extend([
            Task(
                id=f"{task_id}_004",
                name="执行核心任务",
                description="完成今日最重要的任务",
                category="work",
                priority=5,
                status="pending",
                duration_minutes=120
            ),
            Task(
                id=f"{task_id}_005",
                name="Moltbook心跳",
                description="检查Moltbook社区动态",
                category="improvement",
                priority=3,
                status="pending",
                duration_minutes=15
            ),
        ])
        
        # 下午任务 (14:00-18:00)
        tasks.extend([
            Task(
                id=f"{task_id}_006",
                name="技术学习",
                description="学习新技术/工具/框架",
                category="learning",
                priority=4,
                status="pending",
                duration_minutes=60
            ),
            Task(
                id=f"{task_id}_007",
                name="股票市场分析",
                description="分析A股市场",
                category="work",
                priority=4,
                status="pending",
                duration_minutes=30
            ),
            Task(
                id=f"{task_id}_008",
                name="自我评估",
                description="评估今日进展",
                category="improvement",
                priority=3,
                status="pending",
                duration_minutes=15
            ),
        ])
        
        # 晚间任务 (19:00-22:00)
        tasks.extend([
            Task(
                id=f"{task_id}_009",
                name="更新MEMORY.md",
                description="记录今日学习",
                category="improvement",
                priority=4,
                status="pending",
                duration_minutes=20
            ),
            Task(
                id=f"{task_id}_010",
                name="规划明日任务",
                description="为明天制定计划",
                category="work",
                priority=4,
                status="pending",
                duration_minutes=15
            ),
            Task(
                id=f"{task_id}_011",
                name="系统健康检查",
                description="检查OpenClaw和依赖服务",
                category="health",
                priority=3,
                status="pending",
                duration_minutes=10
            ),
        ])
        
        self.today_tasks = tasks
        self.save_tasks()
        return tasks
    
    def complete_task(self, task_id: str) -> bool:
        """完成任务"""
        for task in self.today_tasks:
            if task.id == task_id:
                task.status = 'completed'
                task.completed_time = datetime.now().isoformat()
                self.save_tasks()
                return True
        return False
    
    def skip_task(self, task_id: str, reason: str = None):
        """跳过任务"""
        for task in self.today_tasks:
            if task.id == task_id:
                task.status = 'skipped'
                task.notes = reason
                self.save_tasks()
                return True
        return False
    
    def get_status(self) -> Dict:
        """获取状态"""
        total = len(self.today_tasks)
        completed = sum(1 for t in self.today_tasks if t.status == 'completed')
        pending = sum(1 for t in self.today_tasks if t.status == 'pending')
        skipped = sum(1 for t in self.today_tasks if t.status == 'skipped')
        
        by_category = {}
        for task in self.today_tasks:
            cat = task.category
            if cat not in by_category:
                by_category[cat] = {'total': 0, 'completed': 0}
            by_category[cat]['total'] += 1
            if task.status == 'completed':
                by_category[cat]['completed'] += 1
        
        return {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'total': total,
            'completed': completed,
            'pending': pending,
            'skipped': skipped,
            'progress': f"{completed/total*100:.0f}%" if total > 0 else "0%",
            'by_category': by_category
        }
    
    def print_dashboard(self):
        """打印仪表板"""
        status = self.get_status()
        
        print("\n" + "=" * 60)
        print(f"📅 {status['date']} 任务概览")
        print("=" * 60)
        print(f"\n总任务: {status['total']}")
        print(f"✅ 完成: {status['completed']}")
        print(f"⏳ 待办: {status['pending']}")
        print(f"⏭️ 跳过: {status['skipped']}")
        print(f"\n📊 进度: {status['progress']}")
        
        print("\n📁 按分类:")
        for cat, data in status['by_category'].items():
            emoji = {'learning': '📚', 'work': '💼', 'health': '🏥', 'improvement': '🚀'}
            e = emoji.get(cat, '📌')
            print(f"  {e} {cat}: {data['completed']}/{data['total']}")
        
        print("\n📋 今日任务清单:")
        print("-" * 60)
        
        # 按优先级排序
        sorted_tasks = sorted(self.today_tasks, key=lambda x: (-x.priority, x.status))
        
        for i, task in enumerate(sorted_tasks, 1):
            status_icon = {'pending': '⏳', 'completed': '✅', 'skipped': '⏭️', 'in_progress': '🔄'}
            icon = status_icon.get(task.status, '📌')
            priority_star = '⭐' * task.priority
            
            print(f"{icon} {task.name} {priority_star}")
            print(f"    {task.description} ({task.duration_minutes}分钟)")
            
            if task.status == 'completed':
                print(f"    ✅ 已完成: {task.completed_time[:16]}")
            print()
        
        print("=" * 60)
    
    def run_daily_check(self):
        """执行每日检查"""
        print("\n🦞 小爪每日自动检查")
        print("=" * 60)
        
        # 检查是否有今日任务
        today = datetime.now().strftime('%Y-%m-%d')
        
        if not self.today_tasks or \
           (hasattr(self, 'tasks_file') and 
            not os.path.exists(self.tasks_file)):
            print("📋 生成今日任务清单...")
            self.generate_daily_tasks()
        
        # 显示状态
        self.print_dashboard()
        
        # 检查健康
        print("\n🏥 系统健康检查:")
        import subprocess
        checks = [
            ('OpenClaw', 'curl -s http://localhost:3009/health || echo "离线"'),
            ('Git Status', 'git status --short | wc -l'),
            ('Disk', 'df -h /home/admin/.openclaw/workspace | tail -1'),
        ]
        
        for name, cmd in checks:
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if '离线' in result.stdout:
                    print(f"  ❌ {name}: 离线")
                else:
                    print(f"  ✅ {name}: {result.stdout.strip()}")
            except Exception as e:
                print(f"  ⚠️ {name}: 检查失败")
        
        # 学习检查
        print("\n📚 今日学习:")
        print("  ⏳ Moltbook心跳")
        print("  ⏳ GitHub趋势")
        print("  ⏳ 新技术调研")
        
        print("\n💡 建议:")
        if status['pending'] > 5:
            print("  有较多待办任务，建议优先完成重要的")
        
        print("\n" + "=" * 60)


def main():
    """主函数"""
    planner = AutoPlanner()
    
    # 检查今日任务是否存在
    if not planner.today_tasks:
        print("📋 生成今日任务清单...")
        planner.generate_daily_tasks()
    
    # 显示仪表板
    planner.print_dashboard()


if __name__ == '__main__':
    main()
