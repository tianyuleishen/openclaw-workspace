#!/usr/bin/env python3
"""
OpenClaw系统集成配置
集成JSON结构化记忆优化
"""

import json
import os
from pathlib import Path

# ==================== 配置 ====================

class SystemConfig:
    """系统配置"""
    
    # 优化配置
    OPTIMIZATION = {
        "enabled": True,
        "memory_system": "structured_json",  # structured_json 或 legacy
        "cache_enabled": True,
        "max_context_size": 50000,
        "compression_threshold": 0.7
    }
    
    # 记忆配置
    MEMORY = {
        "type": "structured_json",
        "structured_dir": "/home/admin/.openclaw/workspace/memory/structured",
        "legacy_dir": "/home/admin/.openclaw/workspace/memory",
        "auto_migrate": True
    }
    
    # 性能配置
    PERFORMANCE = {
        "context_cache_ttl": 3600,
        "entity_cache_size": 100,
        "event_cache_size": 50,
        "async_loading": True
    }


class SystemIntegrator:
    """系统集成器"""
    
    def __init__(self, config: SystemConfig = None):
        self.config = config or SystemConfig()
        self.backup_dir = Path("/home/admin/.openclaw/workspace/.system_backup")
        self.backup_dir.mkdir(exist_ok=True)
    
    def integrate(self) -> dict:
        """执行集成"""
        results = {
            "success": True,
            "steps": [],
            "errors": []
        }
        
        # Step 1: 创建集成模块
        results["steps"].append(self._create_integration_module())
        
        # Step 2: 迁移现有记忆
        results["steps"].append(self._migrate_memory())
        
        # Step 3: 创建系统钩子
        results["steps"].append(self._create_system_hooks())
        
        # Step 4: 更新配置文件
        results["steps"].append(self._update_config())
        
        # Step 5: 验证集成
        results["steps"].append(self._verify_integration())
        
        return results
    
    def _create_integration_module(self) -> dict:
        """创建集成模块"""
        try:
            # 复制优化模块到系统路径
            import shutil
            src = "/home/admin/.openclaw/workspace/structured_memory_system.py"
            dst = "/home/admin/.openclaw/workspace/clawlet_structured_memory.py"
            shutil.copy(src, dst)
            
            return {
                "step": "create_integration_module",
                "status": "success",
                "message": f"集成模块已创建: {dst}"
            }
        except Exception as e:
            return {
                "step": "create_integration_module",
                "status": "failed",
                "message": str(e)
            }
    
    def _migrate_memory(self) -> dict:
        """迁移现有记忆"""
        try:
            from structured_memory_system import StructuredMemory
            
            memory = StructuredMemory()
            
            # 迁移现有文件
            legacy_dir = Path(self.config.MEMORY["legacy_dir"])
            if legacy_dir.exists():
                for md_file in legacy_dir.glob("*.md"):
                    if md_file.name not in ["MEMORY.md", "SYSTEM_FIX.md"]:
                        # 读取并迁移
                        with open(md_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # 添加为实体
                        memory.add_entity(
                            "document",
                            md_file.stem,
                            {
                                "file": str(md_file),
                                "content_hash": hash(content) % 1000000,
                                "migrated": True
                            }
                        )
            
            return {
                "step": "migrate_memory",
                "status": "success",
                "message": "记忆迁移完成"
            }
        except Exception as e:
            return {
                "step": "migrate_memory",
                "status": "failed",
                "message": str(e)
            }
    
    def _create_system_hooks(self) -> dict:
        """创建系统钩子"""
        try:
            # 创建快速访问API
            hook_code = '''#!/usr/bin/env python3
"""
OpenClaw快速记忆访问API
集成JSON结构化记忆系统
"""

from structured_memory_system import StructuredMemory, MemorySearch

# 全局实例
_memory = None
_search = None

def get_memory() -> StructuredMemory:
    """获取记忆实例"""
    global _memory
    if _memory is None:
        _memory = StructuredMemory()
    return _memory

def get_search() -> MemorySearch:
    """获取搜索实例"""
    global _search
    if _search is None:
        _search = MemorySearch(get_memory())
    return _search

# 便捷函数
def update_context(key: str, value):
    """更新上下文"""
    get_memory().update_context(key, value)

def get_context(key: str, default=None):
    """获取上下文"""
    return get_memory().get_context(key, default)

def add_event(type: str, description: str, data: dict = None):
    """添加事件"""
    get_memory().add_event(type, description, data)

def add_entity(entity_type: str, entity_id: str, data: dict):
    """添加实体"""
    get_memory().add_entity(entity_type, entity_id, data)

def get_ai_context() -> str:
    """获取AI上下文"""
    return get_memory().get_context_for_ai()

def get_system_status() -> dict:
    """获取系统状态"""
    memory = get_memory()
    return {
        "session_id": memory.context.get("session_id"),
        "current_task": memory.context.get("current_task"),
        "entities_count": len(memory.entities),
        "events_count": len(memory.events.get("today", [])),
        "memory_size": memory.index.get("size_bytes", 0)
    }

if __name__ == "__main__":
    # 测试
    status = get_system_status()
    print("系统状态:", status)
'''
            
            with open("/home/admin/.openclaw/workspace/memory_api.py", 'w', encoding='utf-8') as f:
                f.write(hook_code)
            
            return {
                "step": "create_system_hooks",
                "status": "success",
                "message": "系统钩子已创建: memory_api.py"
            }
        except Exception as e:
            return {
                "step": "create_system_hooks",
                "status": "failed",
                "message": str(e)
            }
    
    def _update_config(self) -> dict:
        """更新配置文件"""
        try:
            config = {
                "optimization": self.config.OPTIMIZATION,
                "memory": self.config.MEMORY,
                "performance": self.config.PERFORMANCE,
                "integrated_at": "2026-02-10T15:13:00",
                "version": "2.0"
            }
            
            with open("/home/admin/.openclaw/workspace/system_optimization_config.json", 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            return {
                "step": "update_config",
                "status": "success",
                "message": "配置文件已更新"
            }
        except Exception as e:
            return {
                "step": "update_config",
                "status": "failed",
                "message": str(e)
            }
    
    def _verify_integration(self) -> dict:
        """验证集成"""
        try:
            # 测试导入
            import sys
            sys.path.insert(0, "/home/admin/.openclaw/workspace")
            
            from structured_memory_system import StructuredMemory
            memory = StructuredMemory()
            
            # 测试功能
            memory.update_context("test_key", "test_value")
            value = memory.get_context("test_key")
            
            assert value == "test_value", "上下文读取失败"
            
            return {
                "step": "verify_integration",
                "status": "success",
                "message": "集成验证通过"
            }
        except Exception as e:
            return {
                "step": "verify_integration",
                "status": "failed",
                "message": str(e)
            }
    
    def rollback(self) -> dict:
        """回滚"""
        try:
            # 恢复备份
            import shutil
            if Path("/home/admin/.openclaw/workspace/MEMORY_backup.md").exists():
                shutil.copy(
                    "/home/admin/.openclaw/workspace/MEMORY_backup.md",
                    "/home/admin/.openclaw/workspace/MEMORY.md"
                )
            
            return {
                "status": "success",
                "message": "已回滚到备份"
            }
        except Exception as e:
            return {
                "status": "failed",
                "message": str(e)
            }


# ==================== 主函数 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 OpenClaw系统集成")
    print("=" * 60)
    
    integrator = SystemIntegrator()
    
    print("\n📦 开始集成...")
    results = integrator.integrate()
    
    print("\n📊 集成结果:")
    for step in results["steps"]:
        status = "✅" if step["status"] == "success" else "❌"
        print(f"  {status} {step['step']}: {step['message']}")
    
    if results["success"]:
        print("\n✅ 系统集成完成!")
        print("\n📁 创建的文件:")
        print("  • clawlet_structured_memory.py")
        print("  • memory_api.py")
        print("  • system_optimization_config.json")
    else:
        print("\n⚠️ 集成部分失败")
        print("错误:", results["errors"])
