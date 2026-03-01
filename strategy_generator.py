# -*- coding: utf-8 -*-
"""
施工策略自动生成引擎 - Strategy Generator
副驾驶核心建议模块
"""

from risk_predictor import RiskPredictor
from datetime import datetime


class StrategyGenerator:
    """施工策略生成引擎（副驾驶核心建议）"""
    
    def __init__(self):
        self.predictor = RiskPredictor()
        self.history = []  # 记录历史决策
    
    def generate_strategy(self, current_risk, persons, violations, weather="normal"):
        """根据风险等级 + 上下文生成策略建议
        
        Args:
            current_risk: 当前风险等级 (low/medium/high)
            persons: 当前人数
            violations: 违章次数
            weather: 天气状况
        
        Returns:
            dict: 策略建议
        """
        base_advice = self.predictor._generate_advice(current_risk)
        
        strategies = []
        
        # 根据风险等级生成策略
        if current_risk == "high":
            # 高风险策略
            strategies.append("STOP: Immediately pause high-risk work (高空/吊装)")
            strategies.append("CHECK: Full site safety helmet inspection")
            strategies.append("ALERT: Notify project manager & safety officer")
            strategies.append("ACTION: Violators must correct immediately")
            
        elif current_risk == "medium":
            # 中风险策略
            strategies.append("PATROL: Increase inspection frequency (every 30min)")
            strategies.append("REMIND: All workers must wear PPE")
            
            # 天气相关
            if weather in ["rain", "storm", "wind"]:
                strategies.append("ADJUST: Pause outdoor high-altitude work, switch to indoor")
            
            # 人数相关
            if persons > 8:
                strategies.append("CROWD: Consider staggered breaks to reduce density")
                
        else:  # low
            # 低风险策略
            strategies.append("OK: Continue normal construction")
            strategies.append("MAINTAIN: Keep current safety measures")
            strategies.append("MONITOR: Routine checks sufficient")
        
        # 记录决策
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "risk": current_risk,
            "persons": persons,
            "violations": violations,
            "weather": weather,
            "primary_advice": base_advice,
            "strategies": strategies
        })
        
        return {
            "risk": current_risk,
            "primary_advice": base_advice,
            "detailed_strategies": strategies,
            "priority": "high" if current_risk == "high" else "normal",
            "persons": persons,
            "violations": violations,
            "weather": weather
        }
    
    def get_recent_strategies(self, limit=5):
        """获取最近策略记录"""
        return self.history[-limit:]
    
    def get_strategy_stats(self):
        """获取策略统计"""
        if not self.history:
            return {"total": 0}
        
        risk_counts = {"high": 0, "medium": 0, "low": 0}
        for h in self.history:
            r = h.get("risk", "low")
            risk_counts[r] = risk_counts.get(r, 0) + 1
        
        return {
            "total": len(self.history),
            "risk_counts": risk_counts,
            "latest": self.history[-1] if self.history else None
        }


# 全局实例
_strategy_gen = None

def get_strategy_generator():
    """获取全局策略生成器"""
    global _strategy_gen
    if _strategy_gen is None:
        _strategy_gen = StrategyGenerator()
    return _strategy_gen


# 测试
if __name__ == "__main__":
    print("="*50)
    print("Strategy Generator Test")
    print("="*50)
    
    gen = StrategyGenerator()
    
    # 测试不同风险等级
    print("\n[1] High risk test:")
    result = gen.generate_strategy("high", 10, 2, "rain")
    print(f"    Risk: {result['risk']}")
    print(f"    Primary: {result['primary_advice']}")
    print(f"    Strategies: {result['detailed_strategies']}")
    
    print("\n[2] Medium risk test:")
    result = gen.generate_strategy("medium", 5, 0, "normal")
    print(f"    Risk: {result['risk']}")
    print(f"    Primary: {result['primary_advice']}")
    print(f"    Strategies: {result['detailed_strategies']}")
    
    print("\n[3] Low risk test:")
    result = gen.generate_strategy("low", 3, 0, "sunny")
    print(f"    Risk: {result['risk']}")
    print(f"    Primary: {result['primary_advice']}")
    print(f"    Strategies: {result['detailed_strategies']}")
    
    # 统计
    print("\n[4] Stats:")
    stats = gen.get_strategy_stats()
    print(f"    {stats}")
    
    # 最近策略
    print("\n[5] Recent strategies:")
    recent = gen.get_recent_strategies(limit=3)
    for r in recent:
        print(f"    {r['risk']}: {r['primary_advice'][:40]}")
    
    print("\n[SUCCESS] Strategy Generator working!")
