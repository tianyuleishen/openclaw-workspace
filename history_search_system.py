#!/usr/bin/env python3
"""
历史会话搜索系统
快速检索任意时间的会话内容
"""

import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional

# ==================== 配置 ====================

class HistorySearchConfig:
    """历史搜索配置"""
    SESSIONS_DIR = "/home/admin/.openclaw/workspace/memory/sessions"
    BACKUPS_DIR = "/home/admin/.openclaw/workspace/memory/backups"
    MAX_HISTORY_DAYS = 365  # 保留365天历史
    INDEX_FILE = "history_index.json"


# ==================== 历史会话搜索系统 ====================

class HistorySearchSystem:
    """历史会话搜索系统"""
    
    def __init__(self, config: HistorySearchConfig = None):
        self.config = config or HistorySearchConfig()
        
        # 创建索引
        self.index_file = Path(self.config.SESSIONS_DIR) / self.config.INDEX_FILE
        self.index = self._load_index()
    
    def _load_index(self) -> Dict:
        """加载索引"""
        if self.index_file.exists():
            with open(self.index_file, 'r') as f:
                return json.load(f)
        return {"sessions": [], "keywords": {}}
    
    def _save_index(self):
        """保存索引"""
        with open(self.index_file, 'w') as f:
            json.dump(self.index, f, ensure_ascii=False, indent=2)
    
    def _build_index_for_session(self, session_id: str) -> Dict:
        """为会话构建索引"""
        session_dir = Path(self.config.SESSIONS_DIR) / session_id
        session_file = session_dir / "session.json"
        
        if not session_file.exists():
            return {}
        
        with open(session_file, 'r') as f:
            session_data = json.load(f)
        
        # 提取关键词
        keywords = set()
        
        if "data" in session_data:
            data = session_data["data"]
            
            # 从key中提取
            for key in data.keys():
                keywords.update(self._extract_keywords(key))
            
            # 从value中提取
            for value in data.values():
                if isinstance(value, str):
                    keywords.update(self._extract_keywords(value))
                elif isinstance(value, dict):
                    for v in value.values():
                        if isinstance(v, str):
                            keywords.update(self._extract_keywords(v))
        
        # 更新索引
        return {
            "session_id": session_id,
            "saved_at": session_data.get("saved_at", ""),
            "keywords": list(keywords),
            "has_context": "current_task" in str(session_data.get("data", {})),
            "has_user_info": "user_info" in str(session_data.get("data", {}))
        }
    
    def _extract_keywords(self, text: str) -> set:
        """提取关键词"""
        # 提取中文、英文单词
        chinese = re.findall(r'[\u4e00-\u9fff]+', text)
        english = re.findall(r'[a-zA-Z_]+', text)
        
        # 过滤短词
        keywords = {w for w in chinese + english if len(w) >= 2}
        
        return keywords
    
    def reindex_all(self):
        """重建所有索引"""
        print("🔄 重建历史索引...")
        
        sessions = []
        keywords_index = {}
        
        for session_id in os.listdir(self.config.SESSIONS_DIR):
            if session_id == self.config.INDEX_FILE:
                continue
            
            session_info = self._build_index_for_session(session_id)
            
            if session_info:
                sessions.append(session_info)
                
                # 更新关键词索引
                for keyword in session_info.get("keywords", []):
                    if keyword not in keywords_index:
                        keywords_index[keyword] = []
                    keywords_index[keyword].append(session_id)
        
        self.index = {
            "sessions": sessions,
            "keywords": keywords_index,
            "last_updated": datetime.now().isoformat()
        }
        
        self._save_index()
        
        print(f"✅ 索引完成: {len(sessions)} 个会话, {len(keywords_index)} 个关键词")
    
    def search(self, query: str, days: int = 30, limit: int = 10) -> List[Dict]:
        """
        搜索历史会话
        
        Args:
            query: 搜索关键词
            days: 搜索最近N天
            limit: 返回结果数量
        """
        # 计算日期范围
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # 提取搜索关键词
        search_keywords = self._extract_keywords(query)
        
        results = []
        
        # 遍历会话
        for session_info in self.index.get("sessions", []):
            # 检查日期
            session_date = datetime.fromisoformat(session_info.get("saved_at", ""))
            if session_date < cutoff_date:
                continue
            
            # 匹配关键词
            session_keywords = set(session_info.get("keywords", []))
            
            # 计算匹配分数
            match_score = len(search_keywords & session_keywords)
            
            if match_score > 0:
                # 获取会话详情
                session_data = self._get_session_content(session_info["session_id"])
                
                results.append({
                    "session_id": session_info["session_id"],
                    "saved_at": session_info["saved_at"],
                    "match_score": match_score,
                    "keywords_found": list(search_keywords & session_keywords),
                    "data": session_data
                })
        
        # 按匹配分数排序
        results.sort(key=lambda x: x["match_score"], reverse=True)
        
        return results[:limit]
    
    def _get_session_content(self, session_id: str) -> Dict:
        """获取会话内容"""
        session_dir = Path(self.config.SESSIONS_DIR) / session_id
        session_file = session_dir / "session.json"
        
        if session_file.exists():
            with open(session_file, 'r') as f:
                return json.load(f)
        
        return {}
    
    def get_recent_sessions(self, limit: int = 5) -> List[Dict]:
        """获取最近会话"""
        sessions = []
        
        for session_info in self.index.get("sessions", [])[:limit]:
            session_data = self._get_session_content(session_info["session_id"])
            
            sessions.append({
                "session_id": session_info["session_id"],
                "saved_at": session_info["saved_at"],
                "has_context": session_info.get("has_context", False),
                "has_user_info": session_info.get("has_user_info", False),
                "data_summary": list(session_data.get("data", {}).keys()) if "data" in session_data else []
            })
        
        return sessions
    
    def get_session_detail(self, session_id: str) -> Optional[Dict]:
        """获取会话详情"""
        session_data = self._get_session_content(session_id)
        
        if not session_data:
            return None
        
        return {
            "session_id": session_id,
            "saved_at": session_data.get("saved_at", ""),
            "version": session_data.get("version", ""),
            "data": session_data.get("data", {})
        }
    
    def search_by_date(self, start_date: str, end_date: str = None) -> List[Dict]:
        """按日期范围搜索
        
        Args:
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)，默认今天
        """
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        results = []
        
        for session_info in self.index.get("sessions", []):
            session_date = datetime.fromisoformat(session_info.get("saved_at", ""))
            
            if start <= session_date <= end:
                results.append({
                    "session_id": session_info["session_id"],
                    "saved_at": session_info["saved_at"],
                    "data": self._get_session_content(session_info["session_id"])
                })
        
        return results
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        sessions = self.index.get("sessions", [])
        
        # 按日期统计
        dates = []
        for s in sessions:
            try:
                date = datetime.fromisoformat(s.get("saved_at", "")).strftime('%Y-%m-%d')
                dates.append(date)
            except:
                pass
        
        return {
            "total_sessions": len(sessions),
            "unique_dates": len(set(dates)),
            "date_range": f"{min(dates) if dates else 'N/A'} ~ {max(dates) if dates else 'N/A'}",
            "keywords_count": len(self.index.get("keywords", {})),
            "sessions_with_context": len([s for s in sessions if s.get("has_context")]),
            "sessions_with_user": len([s for s in sessions if s.get("has_user_info")])
        }


# ==================== 使用示例 ====================

if __name__ == "__main__":
    print("=" * 80)
    print("🚀 历史会话搜索系统测试")
    print("=" * 80)
    
    # 初始化
    search = HistorySearchSystem()
    
    # 重建索引
    print("\n📚 1. 重建历史索引")
    search.reindex_all()
    
    # 查看统计
    print("\n📊 2. 查看统计信息")
    stats = search.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # 获取最近会话
    print("\n🕐 3. 获取最近会话")
    recent = search.get_recent_sessions(limit=5)
    for i, session in enumerate(recent, 1):
        print(f"   {i}. {session['session_id']}")
        print(f"      时间: {session['saved_at']}")
        print(f"      包含上下文: {'是' if session['has_context'] else '否'}")
        print(f"      数据项: {session['data_summary']}")
    
    # 搜索测试
    print("\n🔍 4. 搜索测试")
    
    test_queries = [
        "视频制作",
        "系统优化",
        "用户信息",
        "任务状态"
    ]
    
    for query in test_queries:
        results = search.search(query, days=30, limit=3)
        print(f"\n   搜索'{query}': {len(results)} 个结果")
        
        for r in results[:2]:
            print(f"      - {r['session_id']} (匹配: {r['match_score']}个关键词)")
            print(f"        关键词: {r['keywords_found']}")
    
    # 按日期搜索
    print("\n📅 5. 按日期搜索")
    today = datetime.now().strftime('%Y-%m-%d')
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    date_results = search.search_by_date(week_ago, today)
    print(f"   从 {week_ago} 到 {today}: {len(date_results)} 个会话")
    
    print("\n" + "=" * 80)
    print("✅ 历史会话搜索测试完成!")
    print("=" * 80)
