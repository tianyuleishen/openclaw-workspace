#!/usr/bin/env python3
"""
Experience Optimizer - 经验优化器
实现：
1. 记录每次执行的效果
2. 对比新旧执行，选择更好的
3. 自动更新更好的经验
4. 累积形成最优方案
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
from structured_memory import StructuredMemory


class ExperienceOptimizer:
    """
    经验优化器
    
    功能：
    1. 记录每次执行 - 记录任务执行的详细信息
    2. 对比评估 - 评估新执行是否比旧经验更好
    3. 经验更新 - 自动更新更好的经验到记忆
    4. 累积优化 - 多次执行后形成最优方案
    
    核心思想：
    - 每次执行都评估效果
    - 好的执行更新旧记忆
    - 累积形成最佳实践
    """
    
    def __init__(self):
        self.memory = StructuredMemory()
        self.execution_history = {}  # 执行历史
    
    # ========== 1. 记录执行 ==========
    
    def record_execution(self, task: str, execution: Dict) -> Dict:
        """
        记录一次执行
        
        Args:
            task: 任务名称
            execution: 执行信息
                {
                    "steps": ["步骤1", "步骤2"],
                    "result": "结果",
                    "quality": 0.9,  # 质量评分 0-1
                    "efficiency": 0.8,  # 效率评分 0-1
                    "feedback": "用户反馈",
                    "confidence": 0.85  # 执行置信度
                }
        
        Returns:
            执行记录
        """
        record = {
            "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "steps": execution.get("steps", []),
            "result": execution.get("result", ""),
            "quality": execution.get("quality", 0.5),
            "efficiency": execution.get("efficiency", 0.5),
            "feedback": execution.get("feedback", ""),
            "confidence": execution.get("confidence", 0.5),
            "execution_count": 1
        }
        
        # 保存到历史
        if task not in self.execution_history:
            self.execution_history[task] = []
        
        self.execution_history[task].append(record)
        
        # 保存到记忆
        self.memory.save_learning(
            topic=f"执行经验: {task}",
            insight=f"质量:{record['quality']*100:.0f}% 效率:{record['efficiency']*100:.0f}% 结果:{record['result'][:30]}",
            source="execution"
        )
        
        return record
    
    # ========== 2. 对比评估 ==========
    
    def evaluate_execution(self, task: str, new_execution: Dict) -> Dict:
        """
        评估新执行是否比旧经验更好
        
        Args:
            task: 任务名称
            new_execution: 新的执行信息
            
        Returns:
            {
                "is_better": True/False,
                "improvement": 0.1,  # 改进幅度
                "old_score": 0.75,
                "new_score": 0.85,
                "decision": "UPDATE" / "KEEP" / "CREATE"
            }
        """
        # 计算新执行得分
        new_score = self._calculate_score(new_execution)
        
        # 获取历史最佳
        best_record = self._get_best_execution(task)
        
        result = {
            "task": task,
            "is_better": False,
            "improvement": 0.0,
            "old_score": 0.0,
            "new_score": new_score,
            "decision": "CREATE"
        }
        
        if best_record:
            old_score = self._calculate_score(best_record)
            result["old_score"] = old_score
            result["new_score"] = new_score
            result["improvement"] = new_score - old_score
            
            if new_score > old_score:
                result["is_better"] = True
                result["decision"] = "UPDATE"
            elif abs(new_score - old_score) < 0.05:
                result["decision"] = "KEEP_SIMILAR"
            else:
                result["decision"] = "KEEP_BETTER"
        
        return result
    
    def _calculate_score(self, execution: Dict) -> float:
        """计算执行得分 (加权平均)"""
        quality = execution.get("quality", 0.5)
        efficiency = execution.get("efficiency", 0.5)
        confidence = execution.get("confidence", 0.5)
        
        # 权重: 质量50%, 效率30%, 置信度20%
        score = quality * 0.5 + efficiency * 0.3 + confidence * 0.2
        
        return min(1.0, max(0.0, score))
    
    def _get_best_execution(self, task: str) -> Optional[Dict]:
        """获取任务历史最佳执行"""
        if task not in self.execution_history:
            return None
        
        records = self.execution_history[task]
        
        if not records:
            return None
        
        # 找出得分最高的
        best = max(records, key=lambda r: self._calculate_score(r))
        
        return best
    
    # ========== 3. 经验更新 ==========
    
    def optimize_and_save(self, task: str, new_execution: Dict) -> Dict:
        """
        优化并保存经验
        
        如果新执行比旧经验好，自动更新
        
        Args:
            task: 任务名称
            new_execution: 新的执行信息
                {
                    "steps": [...],
                    "result": "结果",
                    "quality": 0.9,
                    "efficiency": 0.8,
                    "feedback": "用户反馈",
                    "confidence": 0.85
                }
        
        Returns:
            {
                "task": "xxx",
                "updated": True/False,
                "improvement": 0.1,
                "old_score": 0.75,
                "new_score": 0.85,
                "message": "更新了经验" / "保持了最佳经验"
            }
        """
        # 记录新执行
        record_execution(task, new_execution)
        
        # 评估是否更好
        eval_result = self.evaluate_execution(task, new_execution)
        
        result = {
            "task": task,
            "updated": False,
            "improvement": eval_result["improvement"],
            "old_score": eval_result["old_score"],
            "new_score": eval_result["new_score"],
            "message": ""
        }
        
        # 如果更好，更新记忆中的经验
        if eval_result["is_better"]:
            result["updated"] = True
            result["message"] = f"✅ 更新了经验 (改进{eval_result['improvement']*100:.1f}%)"
            
            # 保存优化的经验
            self.memory.save_learning(
                topic=f"优化经验: {task}",
                insight=f"新最佳: 质量{new_execution.get('quality',0)*100:.0f}% 效率{new_execution.get('efficiency',0)*100:.0f}%",
                source="experience_optimization"
            )
            
            # 更新任务模式的置信度
            self._update_pattern_confidence(task, eval_result["new_score"])
            
        elif eval_result["decision"] == "KEEP_BETTER":
            result["message"] = "ℹ️ 保持了历史最佳经验"
        else:
            result["message"] = "ℹ️ 新执行与最佳经验相似"
        
        return result
    
    def _update_pattern_confidence(self, task: str, score: float):
        """更新任务模式的置信度"""
        # 提高下次执行的置信度
        pass  # 可以在proactive_learner中集成
    
    # ========== 4. 累积优化 ==========
    
    def get_optimized_experience(self, task: str) -> Dict:
        """
        获取任务的累积优化经验
        
        Returns:
            {
                "task": "xxx",
                "best_execution": {...},  # 最佳执行
                "execution_count": 5,    # 执行次数
                "average_score": 0.78,   # 平均得分
                "improvement_trend": "up",  # 改进趋势
                "optimized_steps": ["步骤1", "步骤2"]  # 优化后的步骤
            }
        """
        if task not in self.execution_history:
            return {
                "task": task,
                "exists": False,
                "execution_count": 0,
                "average_score": 0.0,
                "improvement_trend": "➡️ 无数据",
                "optimized_steps": [],
                "message": "暂无执行经验"
            }
        
        records = self.execution_history[task]
        
        # 计算平均得分
        scores = [self._calculate_score(r) for r in records]
        avg_score = sum(scores) / len(scores) if scores else 0.5
        
        # 计算改进趋势
        if len(scores) >= 2:
            recent_avg = sum(scores[-3:]) / min(3, len(scores))
            early_avg = sum(scores[:2]) / 2
            if recent_avg > early_avg + 0.05:
                trend = "📈 上升趋势"
            elif recent_avg < early_avg - 0.05:
                trend = "📉 下降趋势"
            else:
                trend = "➡️ 稳定"
        else:
            trend = "➡️ 刚开始"
        
        # 获取最佳执行
        best = self._get_best_execution(task)
        
        return {
            "task": task,
            "exists": True,
            "best_execution": best,
            "execution_count": len(records),
            "average_score": avg_score,
            "improvement_trend": trend,
            "optimized_steps": best["steps"] if best else []
        }
    
    def apply_experience(self, task: str) -> Dict:
        """
        应用累积的经验来执行任务
        
        Returns:
            {
                "task": "xxx",
                "can_execute": True/False,
                "confidence": 0.85,  # 基于经验的置信度
                "steps": ["步骤1", "步骤2"],  # 最佳步骤
                "message": "基于X次执行经验，建议..."
            }
        """
        experience = self.get_optimized_experience(task)
        
        if not experience["exists"]:
            return {
                "task": task,
                "can_execute": False,
                "confidence": 0.5,
                "message": "暂无执行经验，需要用户指导"
            }
        
        return {
            "task": task,
            "can_execute": True,
            "confidence": experience["best_execution"]["confidence"] if experience["best_execution"] else 0.7,
            "steps": experience["optimized_steps"],
            "execution_count": experience["execution_count"],
            "average_score": experience["average_score"],
            "message": f"基于{experience['execution_count']}次执行经验，平均得分{experience['average_score']*100:.0f}%"
        }


# 全局优化器
_optimizer = None

def get_optimizer():
    """获取全局经验优化器"""
    global _optimizer
    if _optimizer is None:
        _optimizer = ExperienceOptimizer()
    return _optimizer


# 便捷函数
def record_execution(task: str, execution: Dict):
    """记录执行"""
    return get_optimizer().record_execution(task, execution)

def optimize_experience(task: str, execution: Dict) -> Dict:
    """优化经验"""
    return get_optimizer().optimize_and_save(task, execution)

def get_experience(task: str) -> Dict:
    """获取累积经验"""
    return get_optimizer().get_optimized_experience(task)

def apply_experience(task: str) -> Dict:
    """应用经验"""
    return get_optimizer().apply_experience(task)


if __name__ == "__main__":
    print("=" * 70)
    print("Experience Optimizer Test")
    print("=" * 70)
    
    optimizer = ExperienceOptimizer()
    
    # 第一次执行 (一般)
    print("\n1. 第一次执行...")
    exec1 = {
        "steps": ["步骤A", "步骤B", "步骤C"],
        "result": "成功",
        "quality": 0.7,
        "efficiency": 0.6,
        "confidence": 0.7
    }
    result1 = optimizer.optimize_and_save("创建模块", exec1)
    print(f"   得分: {result1['new_score']*100:.0f}%")
    print(f"   消息: {result1['message']}")
    
    # 第二次执行 (更好)
    print("\n2. 第二次执行 (改进)...")
    exec2 = {
        "steps": ["优化步骤A", "步骤B", "步骤C", "步骤D"],
        "result": "更好",
        "quality": 0.85,
        "efficiency": 0.8,
        "confidence": 0.85
    }
    result2 = optimizer.optimize_and_save("创建模块", exec2)
    print(f"   得分: {result2['new_score']*100:.0f}%")
    print(f"   消息: {result2['message']}")
    
    # 第三次执行 (再次改进)
    print("\n3. 第三次执行 (再次改进)...")
    exec3 = {
        "steps": ["最佳步骤A", "最佳步骤B", "步骤C"],
        "result": "最佳",
        "quality": 0.95,
        "efficiency": 0.9,
        "confidence": 0.92
    }
    result3 = optimizer.optimize_and_save("创建模块", exec3)
    print(f"   得分: {result3['new_score']*100:.0f}%")
    print(f"   消息: {result3['message']}")
    
    # 获取累积经验
    print("\n4. 获取累积经验...")
    exp = optimizer.get_optimized_experience("创建模块")
    print(f"   执行次数: {exp['execution_count']}")
    print(f"   平均得分: {exp['average_score']*100:.0f}%")
    print(f"   趋势: {exp['improvement_trend']}")
    print(f"   最佳步骤: {len(exp['optimized_steps'])}步")
    
    # 应用经验
    print("\n5. 应用经验...")
    apply = optimizer.apply_experience("创建模块")
    print(f"   可执行: {apply['can_execute']}")
    print(f"   置信度: {apply['confidence']*100:.0f}%")
    print(f"   消息: {apply['message']}")
    
    print("\n" + "=" * 70)
    print("Experience optimization works!")
    print("=" * 70)
