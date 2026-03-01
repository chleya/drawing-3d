# -*- coding: utf-8 -*-
"""
多场景模拟与压力测试 - Multi-Scenario Test
不同工况下的自主执行 + 监督干预
"""

import random
import time
import os
from autonomous_decision import AutonomousDecisionEngine
from supervision_interface import SupervisionInterface


def run_multi_scenario_test(scenarios=10):
    """运行多场景测试
    
    Args:
        scenarios: 场景数量
    
    Returns:
        list: 测试结果
    """
    print("\n" + "="*50)
    print("NeuralSite Light - Multi-Scenario Test")
    print("="*50)
    print(f"Running {scenarios} scenarios...\n")
    
    # 初始化
    engine = AutonomousDecisionEngine()
    sup = SupervisionInterface()
    
    results = []
    
    for i in range(scenarios):
        # 随机生成场景参数
        risk_level = random.choice(["low", "medium", "high"])
        persons = random.randint(0, 20)
        violations = random.randint(0, 5)
        
        # 40%概率人类干预
        human_intervene = random.random() < 0.4
        
        print(f"[Scenario {i+1}] Risk={risk_level}, Persons={persons}, Violations={violations}")
        
        if human_intervene:
            # 人类干预
            result = sup.supervised_decide(
                risk_level, 
                persons, 
                violations, 
                human_override=True,
                override_action=random.choice(["resume_normal", "send_warning"]),
                reason="Manual intervention test"
            )
            print(f"  -> Human intervention: {result['decision']} (override)")
        else:
            # AI自主决策
            result = engine.decide_and_execute(risk_level, persons, violations)
            print(f"  -> AI decision: {result['action']} (reward: {result['reward']})")
        
        results.append({
            "scenario": i + 1,
            "risk": risk_level,
            "persons": persons,
            "violations": violations,
            "intervene": human_intervene,
            "decision": result.get("decision", result.get("action", "unknown")),
            "source": "human" if human_intervene else "ai"
        })
        
        # 模拟真实间隔
        time.sleep(0.3)
    
    # 统计
    ai_count = sum(1 for r in results if r["source"] == "ai")
    human_count = len(results) - ai_count
    
    print("\n" + "="*50)
    print("Test Summary")
    print("="*50)
    print(f"Total scenarios: {scenarios}")
    print(f"AI autonomous: {ai_count} ({ai_count/scenarios:.1%})")
    print(f"Human intervention: {human_count} ({human_count/scenarios:.1%})")
    
    # 风险分布
    risk_counts = {"low": 0, "medium": 0, "high": 0}
    for r in results:
        risk_counts[r["risk"]] += 1
    print(f"\nRisk distribution:")
    print(f"  Low: {risk_counts['low']}")
    print(f"  Medium: {risk_counts['medium']}")
    print(f"  High: {risk_counts['high']}")
    
    # 检查日志
    print("\n" + "-"*30)
    print("Log files verification:")
    
    log_files = [
        "data/decision_log.jsonl",
        "data/intervention_log.jsonl"
    ]
    
    for log_file in log_files:
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                lines = f.readlines()
            print(f"  {log_file}: {len(lines)} lines")
        else:
            print(f"  {log_file}: NOT FOUND")
    
    print("="*50 + "\n")
    
    return results


def run_stress_test(duration=60):
    """压力测试
    
    Args:
        duration: 持续时间(秒)
    """
    print(f"\n{'='*50}")
    print(f"Stress Test - Duration: {duration}s")
    print(f"{'='*50}\n")
    
    engine = AutonomousDecisionEngine()
    sup = SupervisionInterface()
    
    start_time = time.time()
    count = 0
    
    while time.time() - start_time < duration:
        risk = random.choice(["low", "medium", "high"])
        persons = random.randint(0, 15)
        violations = random.randint(0, 3)
        
        result = engine.decide_and_execute(risk, persons, violations)
        count += 1
        
        if count % 10 == 0:
            print(f"Processed {count} decisions in {time.time() - start_time:.1f}s")
        
        time.sleep(0.1)
    
    print(f"\nStress test completed: {count} decisions in {duration}s")
    print(f"Average: {count/duration:.1f} decisions/second")
    
    return count


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Multi-Scenario Test')
    parser.add_argument('--scenarios', type=int, default=10, help='Number of scenarios')
    parser.add_argument('--stress', action='store_true', help='Run stress test')
    parser.add_argument('--duration', type=int, default=30, help='Stress test duration')
    args = parser.parse_args()
    
    if args.stress:
        run_stress_test(duration=args.duration)
    else:
        run_multi_scenario_test(scenarios=args.scenarios)
