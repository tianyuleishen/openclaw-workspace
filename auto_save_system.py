#!/usr/bin/env python3
"""
小爪自动记忆持久化系统
自动保存关键数据，会话间快速恢复
"""

import json
import os
import shutil
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import time

# ==================== 配置 ====================

class AutoSaveConfig:
    """自动保存配置"""
    # 存储目录
    SESSION_DIR = "/home/admin/.openclaw/workspace/memory/sessions"
    BACKUP_DIR = "/home/admin/.openclaw/workspace/memory/backups"
    
    # 保存策略
    AUTO_SAVE_INTERVAL = 60  # 自动保存间隔（秒）
    KEEP_BACKUPS = 5  # 保留的备份数量
    
    # 关键数据
    CRITICAL_KEYS = [
        "session_id",
        "user_info",
        "current_task",
        "system_state",
        "completed_tasks",
        "pending_actions"
    ]


# ==================== 自动保存系统 ====================

class AutoSaveSystem:
    """自动保存系统"""
    
    def __init__(self, config: AutoSaveConfig = None):
        self.config = config or AutoSaveConfig()
        
        # 创建目录
        Path(self.config.SESSION_DIR).mkdir(parents=True, exist_ok=True)
        Path(self.config.BACKUP_DIR).mkdir(parents=True, exist_ok=True)
        
        # 状态
        self.last_save_time = None
        self.pending_changes = False
        self.current_session_id = None
    
    def start_session(self, session_data: Dict = None) -> Dict:
        """开始新会话，自动恢复上次数据"""
        session_id = f"session_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.current_session_id = session_id
        
        # 创建会话目录
        session_dir = Path(self.config.SESSION_DIR) / session_id
        session_dir.mkdir(exist_ok=True)
        
        # 恢复上次会话数据
        restored_data = self._restore_latest_session()
        
        # 合并新会话数据
        if session_data:
            restored_data.update(session_data)
        
        # 保存初始化状态
        self._save_session(session_id, restored_data)
        
        # 更新状态
        self.last_save_time = time.time()
        self.pending_changes = False
        
        print(f"✅ 会话开始: {session_id}")
        print(f"   恢复数据: {len(restored_data)} 项")
        
        return restored_data
    
    def save_checkpoint(self, key: str, data: Any):
        """保存检查点（关键数据）"""
        session_id = self.current_session_id
        if not session_id:
            return
        
        # 加载当前会话
        session_data = self._load_session(session_id)
        
        # 更新关键数据
        session_data[key] = {
            "value": data,
            "timestamp": datetime.now().isoformat(),
            "version": self._generate_version()
        }
        
        # 保存
        self._save_session(session_id, session_data)
        self.pending_changes = True
        
        print(f"💾 保存检查点: {key}")
    
    def save_all(self, full_data: Dict):
        """保存全部数据"""
        if not self.current_session_id:
            return
        
        session_data = {
            "session_id": self.current_session_id,
            "saved_at": datetime.now().isoformat(),
            "data": full_data,
            "version": self._generate_version()
        }
        
        self._save_session(self.current_session_id, session_data)
        self._create_backup(self.current_session_id, session_data)
        
        self.last_save_time = time.time()
        self.pending_changes = False
        
        print(f"✅ 数据已保存: {self.current_session_id}")
    
    def end_session(self, final_data: Dict = None):
        """结束会话，保存所有数据"""
        if not self.current_session_id:
            return
        
        # 保存最终数据
        if final_data:
            self.save_all(final_data)
        elif self.pending_changes:
            # 保存当前状态
            session_data = self._load_session(self.current_session_id)
            self._save_session(self.current_session_id, session_data)
        
        # 创建最终备份
        self._create_backup(self.current_session_id, self._load_session(self.current_session_id))
        
        print(f"🏁 会话结束: {self.current_session_id}")
        
        self.current_session_id = None
        self.pending_changes = False
    
    def get_latest_session(self) -> Optional[Dict]:
        """获取最新会话数据"""
        return self._restore_latest_session()
    
    # ==================== 内部方法 ====================
    
    def _save_session(self, session_id: str, data: Dict):
        """保存会话到文件"""
        session_dir = Path(self.config.SESSION_DIR) / session_id
        
        # 保存主文件
        main_file = session_dir / "session.json"
        with open(main_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # 保存关键数据快照
        critical_file = session_dir / "critical.json"
        if "data" in data:
            critical = self._extract_critical_data(data["data"])
            with open(critical_file, 'w', encoding='utf-8') as f:
                json.dump(critical, f, ensure_ascii=False, indent=2)
        
        # 更新时间戳
        timestamp_file = session_dir / "last_modified.txt"
        with open(timestamp_file, 'w') as f:
            f.write(datetime.now().isoformat())
    
    def _load_session(self, session_id: str) -> Dict:
        """加载会话"""
        session_dir = Path(self.config.SESSION_DIR) / session_id
        main_file = session_dir / "session.json"
        
        if main_file.exists():
            with open(main_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return {}
    
    def _restore_latest_session(self) -> Dict:
        """恢复最新会话"""
        sessions = self._get_session_list()
        
        if not sessions:
            return {}
        
        # 获取最新会话
        latest_session = sessions[0]  # 按时间排序，最新的在前面
        session_data = self._load_session(latest_session["id"])
        
        if "data" in session_data:
            print(f"🔄 恢复会话: {latest_session['id']}")
            print(f"   数据项: {len(session_data['data'])}")
            return session_data["data"]
        
        return {}
    
    def _create_backup(self, session_id: str, data: Dict):
        """创建备份"""
        backup_dir = Path(self.config.BACKUP_DIR) / session_id
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # 备份文件名带时间戳
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = backup_dir / f"backup_{timestamp}.json"
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # 清理旧备份
        self._cleanup_old_backups(session_id)
    
    def _cleanup_old_backups(self, session_id: str):
        """清理旧备份"""
        backup_dir = Path(self.config.BACKUP_DIR) / session_id
        if not backup_dir.exists():
            return
        
        backups = sorted(backup_dir.glob("backup_*.json"), reverse=True)
        
        # 只保留最新备份
        for backup in backups[self.config.KEEP_BACKUPS:]:
            backup.unlink()
    
    def _get_session_list(self) -> list:
        """获取会话列表（按修改时间排序）"""
        sessions = []
        
        for session_id in os.listdir(self.config.SESSION_DIR):
            session_dir = Path(self.config.SESSION_DIR) / session_id
            timestamp_file = session_dir / "last_modified.txt"
            
            if timestamp_file.exists():
                with open(timestamp_file, 'r') as f:
                    modified = f.read().strip()
                
                sessions.append({
                    "id": session_id,
                    "modified": modified
                })
        
        # 按修改时间排序（最新的在前）
        sessions.sort(key=lambda x: x["modified"], reverse=True)
        
        return sessions
    
    def _extract_critical_data(self, data: Dict) -> Dict:
        """提取关键数据"""
        critical = {}
        
        for key in self.config.CRITICAL_KEYS:
            if key in data:
                critical[key] = data[key]
        
        return critical
    
    def _generate_version(self) -> str:
        """生成版本号"""
        return hashlib.md5(f"{datetime.now().isoformat()}".encode()).hexdigest()[:8]


# ==================== 使用示例 ====================

if __name__ == "__main__":
    print("=" * 70)
    print("🚀 自动记忆持久化系统测试")
    print("=" * 70)
    
    # 初始化
    auto_save = AutoSaveSystem()
    
    # 1. 开始会话（自动恢复上次数据）
    print("\n📝 1. 开始新会话")
    session_data = auto_save.start_session({
        "user_info": {"name": "雷哥"},
        "current_task": "视频制作"
    })
    print(f"   初始数据: {session_data}")
    
    # 2. 保存关键数据
    print("\n💾 2. 保存检查点")
    auto_save.save_checkpoint("task_progress", 75)
    auto_save.save_checkpoint("last_message", "测试消息")
    
    # 3. 保存全部数据
    print("\n💾 3. 保存全部数据")
    full_data = {
        "user_info": {"name": "雷哥"},
        "current_task": "视频制作",
        "task_progress": 75,
        "completed_frames": 3,
        "pending_frames": 1
    }
    auto_save.save_all(full_data)
    
    # 4. 结束会话
    print("\n🏁 4. 结束会话")
    auto_save.end_session()
    
    # 5. 模拟下次会话
    print("\n🔄 5. 开始新会话（测试恢复）")
    new_session = auto_save.start_session()
    print(f"   恢复的数据: {new_session}")
    
    # 6. 查看会话历史
    print("\n📚 6. 会话历史")
    sessions = auto_save._get_session_list()
    for session in sessions[:3]:
        print(f"   - {session['id']} ({session['modified']})")
    
    print("\n" + "=" * 70)
    print("✅ 自动记忆持久化测试完成!")
    print("=" * 70)
