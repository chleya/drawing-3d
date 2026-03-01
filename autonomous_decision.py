# -*- coding: utf-8 -*-
"""
自主决策引擎 - Autonomous Decision Engine
规则 + Q-learning 混合决策
"""

import random
import json
import os
from datetime import datetime


class AutonomousDecisionEngine:
    """自主决策引擎（规则 + 强化学习雏形）"""
    
    def __init__(self):
        self.executor = None  # 延迟导入
        self.q_table = {}  # state -> action -> Q值
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.exploration_rate = 0.3
        self.decision_log = "data/decision_log.jsonl"
        
        # 动作空间
        self.actions = ["lock_gate", "send_alert", "stop_crane", 
                       "send_warning", "increase_patrol", "resume_normal"]
        
        # 确保目录存在
        os.makedirs("data", exist_ok=True)
    
    def get_state_key(self, risk_level, persons, violations):
        """状态编码"""
        # risk_level: high/medium/low
        # persons: 分箱 (0-5, 6-10, 10+)
        # violations: 0, 1, 2+
        persons_bin = min(persons // 5, 4)  # 0,1,2,3,4
        violations_bin = min(violations, 2)  # 0,1,2
        
        return f"{risk_level}_{persons_bin}_{violations_bin}"
    
    def choose_action(self, state):
        """ε-greedy 选择动作
        
        Args:
            state: 状态key
        
        Returns:
            str: 选择的动作
        """
        # 探索：随机动作
        if random.random() < self.exploration_rate:
            return random.choice(self.actions)
        
        # 利用：选Q值最高的动作
        if state in self.q_table and self.q_table[state]:
            return max(self.q_table[state], key=self.q_table[state].get)
        
        # 默认：根据风险等级选择
        if "high" in state:
            return "stop_crane"
        elif "medium" in state:
            return "send_warning"
        else:
            return "resume_normal"
    
    def update_q_value(self, state, action, reward, next_state):
        """Q-learning 更新
        
        Q(s,a) = Q(s,a) + alpha * (reward + gamma * max(Q(s',a')) - Q(s,a))
        """
        # 初始化Q表
        if state not in self.q_table:
            self.q_table[state] = {a: 0.0 for a in self.actions}
        if next_state not in self.q_table:
            self.q_table[next_state] = {a: 0.0 for a in self.actions}
        
        # 获取Q值
        old_q = self.q_table[state].get(action, 0.0)
        
        # 计算max Q(s',a')
        max_next_q = max(self.q_table[next_state].values()) if self.q_table[next_state] else 0.0
        
        # Q-learning 更新
        new_q = old_q + self.learning_rate * (reward + self.discount_factor * max_next_q - old_q)
        self.q_table[state][action] = new_q
    
    def decide_and_execute(self, risk_level, persons, violations):
        """决策 + 执行
        
        Args:
            risk_level: 风险等级
            persons: 人数
            violations: 违章次数
        
        Returns:
            dict: 决策结果
        """
        # 获取状态
        state = self.get_state_key(risk_level, persons, violations)
        
        # 选择动作
        action = self.choose_action(state)
        
        # 导入并执行
        from auto_execute import AutoExecutor
        if self.executor is None:
            self.executor = AutoExecutor()
        
        # 执行动作
        executed = self.executor.execute(risk_level, {
            "persons": persons,
            "violations": violations,
            "decision": "auto"
        })
        
        # 计算奖励
        # 高风险 -> stop_crane = 好, resume_normal = 差
        if risk_level == "high":
            reward = 1 if action == "stop_crane" else -1
        elif risk_level == "medium":
            reward = 1 if action in ["send_warning", "increase_patrol"] else 0
        else:
            reward = 1 if action == "resume_normal" else -1
        
        # 更新Q表 (next_state简化为low)
        next_state = self.get_state_key("low", persons, violations)
        self.update_q_value(state, action, reward, next_state)
        
        # 记录决策
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "state": state,
            "action": action,
            "risk_level": risk_level,
            "persons": persons,
            "violations": violations,
            "reward": reward,
            "q_value": self.q_table[state].get(action, 0)
        }
        
        with open(self.decision_log, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        
        return {
            "action": action,
            "reward": reward,
            "state": state,
            "q_table_size": len(self.q_table),
            "executed": executed
        }
    
    def get_decision_history(self, limit=10):
        """获取决策历史"""
        if not os.path.exists(self.decision_log):
            return []
        
        with open(self.decision_log, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        history = []
        for line in lines[-limit:]:
            if line.strip():
                history.append(json.loads(line.strip()))
        
        return history
    
    def get_q_table_summary(self):
        """获取Q表摘要"""
        if not self.q_table:
            return {"size": 0}
        
        # 统计
        states = list(self.q_table.keys())
        actions = set()
        for s in self.q_table.values():
            actions.update(s.keys())
        
        return {
            "states": len(states),
            "actions": len(actions),
            "sample_states": states[:3]
        }


# 全局实例
_decision_engine = None

def get_decision_engine():
    """获取全局决策引擎"""
    global _decision_engine
    if _decision_engine is None:
        _decision_engine = AutonomousDecisionEngine()
    return _decision_engine


# 测试
if __name__ == "__main__":
    print("="*50)
    print("Autonomous Decision Engine Test")
    print("="*50)
    
    engine = AutonomousDecisionEngine()
    
    # 测试决策
    print("\n[1] Testing decisions...")
    test_cases = [
        ("high", 12, 3),
        ("high", 8, 1),
        ("medium", 6, 0),
        ("low", 3, 0),
    ]
    
    for risk, persons, violations in test_cases:
        result = engine.decide_and_execute(risk, persons, violations)
        print(f"    Risk={risk}, Persons={persons}, Viol={violations}")
        print(f"      Action: {result['action']}, Reward: {result['reward']}")
    
    # Q表摘要
    print("\n[2] Q-table summary:")
    summary = engine.get_q_table_summary()
    print(f"    {summary}")
    
    # 决策历史
    print("\n[3] Recent decisions:")
    history = engine.get_decision_history(limit=3)
    for h in history:
        print(f"    {h['state']} -> {h['action']} (reward: {h['reward']})")
    
    print("\n[SUCCESS] Autonomous Decision Engine working!")
