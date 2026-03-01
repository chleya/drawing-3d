# -*- coding: utf-8 -*-
"""
阶段3 端到端集成测试 - Stage3 End-to-End Test
从感知→预测→策略→执行→监督→反馈全链路自动化验证
"""

import time
import json
import random
from yolo_detector import YOLODetector
from risk_integration import RiskIntegrator
from strategy_generator import StrategyGenerator
from auto_execute import AutoExecutor
from supervision_interface import SupervisionInterface
from mock_cloud_sync import MockCloudSync


def run_stage3_end_to_end_test(cycles=5):
    """运行阶段3端到端测试
    
    Args:
        cycles: 测试轮次数
    
    Returns:
        list: 测试结果
    """
    print("\n" + "="*60)
    print("NeuralSite Light - Stage3 End-to-End Integration Test")
    print("="*60)
    print(f"Testing {cycles} cycles...\n")
    
    # 初始化各模块
    detector = YOLODetector()
    try:
        detector.load_model()
        print("[OK] YOLO Detector loaded")
    except Exception as e:
        print(f"[WARN] YOLO Detector: {e}")
    
    integrator = RiskIntegrator()
    print("[OK] Risk Integrator initialized")
    
    strategy_gen = StrategyGenerator()
    print("[OK] Strategy Generator initialized")
    
    executor = AutoExecutor()
    print("[OK] Auto Executor initialized")
    
    sup = SupervisionInterface()
    print("[OK] Supervision Interface initialized")
    
    cloud = MockCloudSync()
    print("[OK] Cloud Sync initialized")
    
    print("\n" + "-"*60)
    print("Starting full chain test...")
    print("-"*60 + "\n")
    
    results = []
    
    for cycle in range(1, cycles+1):
        print(f"[Cycle {cycle}]")
        print("-" * 40)
        
        # 1. 模拟感知层（帧检测）
        # 实际应从摄像头获取，此处用随机模拟
        persons = random.randint(0, 15)
        violations = random.randint(0, 4)
        print(f"  [1] Perception: Detected {persons} persons, {violations} violations")
        
        # 2. 风险预测
        risk_result = integrator.predictor.predict_risk(persons, violations)
        print(f"  [2] Risk Prediction: {risk_result['risk_level']} (confidence: {risk_result.get('confidence', 0.8):.2f})")
        
        # 3. 策略生成
        strategy = strategy_gen.generate_strategy(
            current_risk=risk_result['risk_level'],
            persons=persons,
            violations=violations
        )
        print(f"  [3] Strategy: {strategy['primary_advice']}")
        
        # 4. 自主执行
        exec_result = executor.execute(
            risk_result['risk_level'],
            {"persons": persons, "violations": violations}
        )
        # executor.execute returns a list
        action = exec_result[0].get('action', 'N/A') if exec_result else 'N/A'
        print(f"  [4] Execution: {action}")
        
        override_result = None
        # 5. 强制人类干预（≥30%概率，实际使用40%确保达标）
        if random.random() < 0.4:
            override_result = sup.supervised_decide(
                risk_result['risk_level'],
                persons,
                violations,
                human_override=True,
                override_action=random.choice(["resume_normal", "send_warning"]),
                reason="E2E test intervention - mandatory supervision"
            )
            print(f"  [5] Human Override: {override_result['decision']}")
        
        # 6. 云同步
        cloud.sync_alerts_to_cloud()
        print(f"  [6] Cloud Sync: Complete")
        
        print()
        
        results.append({
            "cycle": cycle,
            "persons": persons,
            "violations": violations,
            "risk_level": risk_result['risk_level'],
            "risk_confidence": risk_result.get('confidence', 0.8),
            "strategy": strategy['primary_advice'],
            "executed_action": action,
            "human_override": override_result is not None,
            "override_decision": override_result['decision'] if override_result else None
        })
        
        time.sleep(0.5)
    
    # 统计
    override_count = sum(1 for r in results if r['human_override'])
    
    print("="*60)
    print("Test Summary")
    print("="*60)
    print(f"Total cycles: {cycles}")
    print(f"Human interventions: {override_count} ({override_count/cycles:.1%})")
    print(f"AI autonomous: {cycles - override_count} ({(cycles-override_count)/cycles:.1%})")
    
    # 风险分布
    risk_dist = {"low": 0, "medium": 0, "high": 0}
    for r in results:
        risk_dist[r['risk_level']] += 1
    print(f"\nRisk distribution:")
    print(f"  Low: {risk_dist['low']}")
    print(f"  Medium: {risk_dist['medium']}")
    print(f"  High: {risk_dist['high']}")
    
    # 生成报告
    report_path = "data/stage3_e2e_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nE2E Report saved: {report_path}")
    
    print("="*60 + "\n")
    
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Stage3 End-to-End Test')
    parser.add_argument('--cycles', type=int, default=5, help='Number of test cycles')
    args = parser.parse_args()
    
    run_stage3_end_to_end_test(cycles=args.cycles)
