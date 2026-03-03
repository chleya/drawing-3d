# -*- coding: utf-8 -*-
"""
Drawing 3D - Unit Tests
"""

import sys
sys.path.insert(0, '.')

def test_weather():
    """Test weather system"""
    from weather import WeatherSystem
    ws = WeatherSystem()
    w = ws.get_weather()
    assert w is not None
    assert 'weather' in w
    print("[PASS] WeatherSystem")
    return True

def test_cost():
    """Test cost system"""
    from cost import CostSystem
    cs = CostSystem()
    cs.add_material('test', 100)
    total = cs.get_total_cost()
    assert total['total'] > 0
    print("[PASS] CostSystem")
    return True

def test_equipment():
    """Test equipment system"""
    from equipment import EquipmentSystem, EquipmentStatus
    es = EquipmentSystem()
    es.add_equipment('test', 'model', 'category')
    util = es.get_utilization()
    assert util['total'] >= 1
    print("[PASS] EquipmentSystem")
    return True

def test_report():
    """Test report system"""
    from report import ReportSystem
    rs = ReportSystem()
    rs.add_daily_record('2026-02-28', 1.0, 'test', 10, 'equipment', 'sunny')
    report = rs.generate_daily('2026-02-28')
    assert '2026-02-28' in report
    print("[PASS] ReportSystem")
    return True

def test_ai_qa():
    """Test AI Q&A"""
    from main import Road3D
    from ai_qa_v2 import AIQAV2
    road = Road3D()
    road.add_progress(0, 1, 'completed', 100)
    qa = AIQAV2(road)
    answer = qa.understand('进度怎么样')
    assert 'Progress' in answer or 'progress' in answer
    print("[PASS] AIQAV2")
    return True

def test_planning():
    """Test planning system"""
    from main import Road3D
    from planning import PlanningAssistant
    road = Road3D()
    road.add_device('d1', 'm1', 'c1')
    planner = PlanningAssistant(road)
    plan = planner.generate_plan(1, 'asphalt')
    assert 'method' in plan
    print("[PASS] PlanningAssistant")
    return True

def test_quality():
    """Test quality detection"""
    from main import Road3D
    from quality_detection import QualityDetector
    road = Road3D()
    road.add_quality(1.0, '压实度', '96%', 'ok')
    qd = QualityDetector(road)
    result = qd.check_quality('compaction', '96%')
    assert result['status'] == 'pass'
    print("[PASS] QualityDetector")
    return True

def test_safety():
    """Test safety management"""
    from main import Road3D
    from safety import SafetyManager
    road = Road3D()
    sm = SafetyManager(road)
    risks = sm.assess_risk()
    assert isinstance(risks, list)
    print("[PASS] SafetyManager")
    return True

def test_compliance():
    """Test compliance assistant"""
    from main import Road3D
    from compliance import ComplianceAssistant
    road = Road3D()
    ca = ComplianceAssistant(road)
    result = ca.check_compliance('压实度', '96%')
    assert 'status' in result
    print("[PASS] ComplianceAssistant")
    return True

def test_drone():
    """Test drone inspection"""
    from main import Road3D
    from drone import DroneInspector
    road = Road3D()
    di = DroneInspector(road)
    di.add_drone('test', 'model')
    mission = di.plan_mission(1, 2)
    assert 'id' in mission or 'error' in mission
    print("[PASS] DroneInspector")
    return True

def test_ar():
    """Test AR viewer"""
    from main import Road3D
    from ar_view import ARViewer
    road = Road3D()
    ar = ARViewer(road)
    marker = ar.add_marker(1.0, 100, 50, 0, 'test')
    assert marker['id'] == 1
    print("[PASS] ARViewer")
    return True

def test_material():
    """Test material scheduling"""
    from main import Road3D
    from material_scheduling import Inventory, Material
    road = Road3D()
    inv = Inventory()
    mat = Material('asphalt', '沥青', '道路材料', '吨', 500)
    inv.add_material(mat)
    assert 'asphalt' in inv.materials
    print("[PASS] MaterialScheduler")
    return True


def test_main():
    """Test main system"""
    from main import Road3D
    road = Road3D()
    road.add_point(0, 0, 0)
    road.add_progress(0, 1, 'completed', 100)
    road.add_material_cost('test', 100)
    road.add_device('d1', 'm1', 'c1')
    progress = road.get_progress()
    assert progress == 100
    print("[PASS] Road3D Main")
    return True


def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("RUNNING ALL TESTS")
    print("="*60)
    
    tests = [
        test_weather,
        test_cost,
        test_equipment,
        test_report,
        test_ai_qa,
        test_planning,
        test_quality,
        test_safety,
        test_compliance,
        test_drone,
        test_ar,
        test_material,
        test_main
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"[FAIL] {test.__name__}: {e}")
            failed += 1
    
    print("="*60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*60)
    
    return failed == 0


if __name__ == "__main__":
    run_all_tests()
