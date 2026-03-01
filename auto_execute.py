# -*- coding: utf-8 -*-
"""
智能执行层 - Auto Executor
自主触发动作（门禁/通知/设备控制）
"""

from datetime import datetime
import json
import os


class AutoExecutor:
    """智能执行层：自主触发动作（门禁/通知/设备）"""
    
    def __init__(self, action_log="data/action_log.jsonl"):
        self.action_log = action_log
        self.rules = {
            "high": ["lock_gate", "send_alert", "stop_crane"],
            "medium": ["send_warning", "increase_patrol"],
            "low": ["resume_normal"]
        }
        
        # 确保目录存在
        os.makedirs(os.path.dirname(action_log) if os.path.dirname(action_log) else "data", exist_ok=True)
    
    def execute(self, risk_level, context=None):
        """根据风险等级执行动作
        
        Args:
            risk_level: 风险等级 (high/medium/low)
            context: 上下文信息
        
        Returns:
            list: 执行的动作列表
        """
        if context is None:
            context = {}
        
        actions = self.rules.get(risk_level, [])
        executed = []
        
        for action in actions:
            result = self._execute_action(action, risk_level, context)
            executed.append(result)
        
        # 记录执行日志
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "risk_level": risk_level,
            "context": context,
            "executed_actions": executed
        }
        
        with open(self.action_log, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        
        return executed
    
    def _execute_action(self, action, risk_level, context):
        """执行单个动作
        
        Returns:
            dict: 动作执行结果
        """
        result = {
            "action": action,
            "status": "success",
            "message": ""
        }
        
        if action == "lock_gate":
            msg = "[AUTO] Locking gate: High-risk area restricted"
            print(msg)
            result["message"] = msg
            
        elif action == "send_alert":
            msg = "[AUTO] Sending emergency alert: All personnel must be notified"
            print(msg)
            result["message"] = msg
            
        elif action == "stop_crane":
            msg = "[AUTO] Stopping crane operation: High-risk trigger"
            print(msg)
            result["message"] = msg
            
        elif action == "send_warning":
            msg = "[AUTO] Sending warning: Increase safety awareness"
            print(msg)
            result["message"] = msg
            
        elif action == "increase_patrol":
            msg = "[AUTO] Increasing patrol frequency: Every 15 minutes"
            print(msg)
            result["message"] = msg
            
        elif action == "resume_normal":
            msg = "[AUTO] Resuming normal construction flow"
            print(msg)
            result["message"] = msg
        
        return result
    
    def get_action_history(self, limit=10):
        """获取动作历史"""
        if not os.path.exists(self.action_log):
            return []
        
        with open(self.action_log, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        history = []
        for line in lines[-limit:]:
            if line.strip():
                history.append(json.loads(line.strip()))
        
        return history
    
    def get_execution_stats(self):
        """获取执行统计"""
        history = self.get_action_history(limit=100)
        
        if not history:
            return {"total": 0}
        
        action_counts = {}
        for entry in history:
            for action in entry.get("executed_actions", []):
                name = action.get("action", "unknown") if isinstance(action, dict) else action
                action_counts[name] = action_counts.get(name, 0) + 1
        
        return {
            "total_executions": len(history),
            "action_counts": action_counts,
            "latest": history[-1] if history else None
        }


# 全局实例
_executor = None

def get_executor():
    """获取全局执行器"""
    global _executor
    if _executor is None:
        _executor = AutoExecutor()
    return _executor


# 测试
if __name__ == "__main__":
    print("="*50)
    print("Auto Executor Test")
    print("="*50)
    
    executor = AutoExecutor()
    
    # 测试高风险
    print("\n[1] High risk test:")
    result = executor.execute("high", {"persons": 12, "violations": 3})
    print(f"    Executed: {len(result)} actions")
    
    # 测试中风险
    print("\n[2] Medium risk test:")
    result = executor.execute("medium", {"persons": 6, "weather": "rain"})
    print(f"    Executed: {len(result)} actions")
    
    # 测试低风险
    print("\n[3] Low risk test:")
    result = executor.execute("low", {"persons": 3})
    print(f"    Executed: {len(result)} actions")
    
    # 统计
    print("\n[4] Execution stats:")
    stats = executor.get_execution_stats()
    print(f"    {stats}")
    
    # 历史
    print("\n[5] Recent history:")
    history = executor.get_action_history(limit=3)
    for h in history:
        print(f"    {h['risk_level']}: {[a['action'] for a in h['executed_actions']]}")
    
    print("\n[SUCCESS] Auto Executor working!")
