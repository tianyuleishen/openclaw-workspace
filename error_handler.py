#!/usr/bin/env python3
"""
Error Handler - 优化错误处理和日志记录
"""

import traceback
import json
from datetime import datetime
from pathlib import Path

class ErrorHandler:
    """错误处理器"""
    
    def __init__(self):
        self.error_log = Path.home() / ".openclaw/workspace/.memory/error_log.json"
        self.error_log.parent.mkdir(exist_ok=True, parents=True)
    
    def capture_error(self, error: Exception, context: str = "") -> dict:
        """捕获错误"""
        error_info = {
            "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "timestamp": datetime.now().isoformat(),
            "type": type(error).__name__,
            "message": str(error),
            "traceback": traceback.format_exc(),
            "context": context
        }
        
        # 保存到日志
        self._save_error(error_info)
        
        return error_info
    
    def _save_error(self, error_info: dict):
        """保存错误"""
        errors = []
        if self.error_log.exists():
            with open(self.error_log, 'r') as f:
                try:
                    errors = json.load(f)
                except:
                    errors = []
        
        errors.append(error_info)
        
        # 只保留最近50个错误
        errors = errors[-50:]
        
        with open(self.error_log, 'w') as f:
            json.dump(errors, f, ensure_ascii=False, indent=2)
    
    def get_recent_errors(self, limit: int = 10) -> list:
        """获取最近错误"""
        if not self.error_log.exists():
            return []
        
        with open(self.error_log, 'r') as f:
            try:
                errors = json.load(f)
                return errors[-limit:]
            except:
                return []
    
    def analyze_errors(self) -> dict:
        """分析错误模式"""
        errors = self.get_recent_errors(50)
        
        if not errors:
            return {"total": 0, "types": {}}
        
        type_counts = {}
        for e in errors:
            etype = e.get("type", "Unknown")
            type_counts[etype] = type_counts.get(etype, 0) + 1
        
        return {
            "total": len(errors),
            "types": type_counts,
            "recent_contexts": [e.get("context", "") for e in errors[-5:]]
        }


# 全局错误处理器
_handler = None

def get_error_handler():
    """获取全局错误处理器"""
    global _handler
    if _handler is None:
        _handler = ErrorHandler()
    return _handler


def safe_execute(func):
    """安全执行装饰器"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            handler = get_error_handler()
            error_info = handler.capture_error(e, context=func.__name__)
            print(f"Error in {func.__name__}: {e}")
            return None
    return wrapper


if __name__ == "__main__":
    print("Error Handler Test")
    print("=" * 50)
    
    handler = ErrorHandler()
    
    # 测试
    try:
        raise ValueError("Test error")
    except Exception as e:
        error_info = handler.capture_error(e, "test")
        print(f"Captured error: {error_info['id']}")
    
    # 分析
    analysis = handler.analyze_errors()
    print(f"Error analysis: {analysis}")
