# -*- coding: utf-8 -*-
"""
人类监督与干预层 - Supervision Interface
确保自动驾驶在人类可控范围内
"""

import json
import os
from datetime import datetime


class SupervisionInterface:
    """人类监督与干预层"""
    
    def __init__(self, intervention_log="data/intervention_log.jsonl"):
        self.engine = None  # 延迟导入
        self.intervention_log = intervention_log
        
        # 确保目录存在
        os.makedirs(os.path.dirname(intervention_log) if os.path.dirname(intervention_log) else "data", exist_ok=True)
    
    def _get_engine(self):
        """获取决策引擎"""
        if self.engine is None:
            from autonomous_decision import AutonomousDecisionEngine
            self.engine = AutonomousDecisionEngine()
        return self.engine
    
    def record_intervention(self, ai_action, ai_risk, human_decision, reason="", context=None):
        """记录人类干预
        
        Args:
            ai_action: AI原始决策
            ai_risk: 风险等级
            human_decision: 人类决策 (override / accept / reject)
            reason: 干预原因
            context: 上下文信息
        
        Returns:
            dict: 干预记录
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "ai_action": ai_action,
            "ai_risk": ai_risk,
            "human_decision": human_decision,
            "reason": reason,
            "override_action": None if human_decision != "override" else "resume_normal",
            "context": context or {}
        }
        
        with open(self.intervention_log, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        
        print(f"[SUPERVISION] Intervention recorded: {human_decision} - {reason}")
        
        return entry
    
    def supervised_decide(self, risk_level, persons, violations, human_override=False, override_action=None, reason=""):
        """监督决策：人类可覆盖AI决策
        
        Args:
            risk_level: 风险等级
            persons: 人数
            violations: 违章次数
            human_override: 是否人类干预
            override_action: 干预动作
            reason: 干预原因
        
        Returns:
            dict: 最终决策结果
        """
        engine = self._get_engine()
        
        # AI决策
        ai_result = engine.decide_and_execute(risk_level, persons, violations)
        ai_action = ai_result["action"]
        
        if human_override:
            # 人类干预
            final_decision = override_action or "resume_normal"
            human_decision = "override"
            
            # 记录干预
            self.record_intervention(
                ai_action=ai_action,
                ai_risk=risk_level,
                human_decision=human_decision,
                reason=reason,
                context={"persons": persons, "violations": violations}
            )
            
            # 执行干预动作
            from auto_execute import AutoExecutor
            executor = AutoExecutor()
            executor.execute(risk_level, {
                "persons": persons,
                "violations": violations,
                "source": "human_override"
            })
            
            return {
                "decision": final_decision,
                "source": "human_override",
                "original_ai_action": ai_action,
                "reason": reason
            }
        else:
            # 接受AI决策
            self.record_intervention(
                ai_action=ai_action,
                ai_risk=risk_level,
                human_decision="accept",
                reason="AI decision accepted",
                context={"persons": persons, "violations": violations}
            )
            
            return {
                "decision": ai_action,
                "source": "ai",
                "q_value": ai_result.get("q_value", 0)
            }
    
    def get_intervention_history(self, limit=10):
        """获取干预历史"""
        if not os.path.exists(self.intervention_log):
            return []
        
        with open(self.intervention_log, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        history = []
        for line in lines[-limit:]:
            if line.strip():
                history.append(json.loads(line.strip()))
        
        return history
    
    def get_intervention_stats(self):
        """获取干预统计"""
        history = self.get_intervention_history(limit=100)
        
        if not history:
            return {"total": 0}
        
        # 统计
        decisions = {"override": 0, "accept": 0, "reject": 0}
        for h in history:
            d = h.get("human_decision", "accept")
            decisions[d] = decisions.get(d, 0) + 1
        
        return {
            "total": len(history),
            "decisions": decisions,
            "override_rate": decisions.get("override", 0) / len(history) if history else 0
        }
    
    def get_recent_interventions(self, limit=5):
        """获取最近干预"""
        return self.get_intervention_history(limit)


# 全局实例
_supervision = None

def get_supervision():
    """获取全局监督实例"""
    global _supervision
    if _supervision is None:
        _supervision = SupervisionInterface()
    return _supervision


# 测试
if __name__ == "__main__":
    print("="*50)
    print("Supervision Interface Test")
    print("="*50)
    
    sup = SupervisionInterface()
    
    # 测试AI决策
    print("\n[1] AI decision (no override):")
    result = sup.supervised_decide("high", 10, 2)
    print(f"    Decision: {result['decision']}, Source: {result['source']}")
    
    # 测试人类覆盖
    print("\n[2] Human override:")
    result = sup.supervised_decide("high", 10, 2, 
                                  human_override=True, 
                                  override_action="resume_normal",
                                  reason="Site conditions allow continuation")
    print(f"    Decision: {result['decision']}, Source: {result['source']}")
    print(f"    Reason: {result['reason']}")
    
    # 统计
    print("\n[3] Intervention stats:")
    stats = sup.get_intervention_stats()
    print(f"    {stats}")
    
    # 历史
    print("\n[4] Recent interventions:")
    history = sup.get_recent_interventions(limit=3)
    for h in history:
        print(f"    {h['human_decision']}: {h['ai_action']} -> {h.get('override_action', 'accepted')}")
    
    print("\n[SUCCESS] Supervision Interface working!")
