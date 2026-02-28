# Professional Review
import sys
sys.path.insert(0, '.')

print("="*60)
print("PROFESSIONAL CODE REVIEW")
print("="*60)

# Test imports
print("\n[1] Import Test")
try:
    from main import Road3D
    print("  main.py: OK")
except Exception as e:
    print(f"  main.py: FAIL - {e}")

try:
    from weather import WeatherSystem
    print("  weather.py: OK")
except Exception as e:
    print(f"  weather.py: FAIL - {e}")

try:
    from cost import CostSystem
    print("  cost.py: OK")
except Exception as e:
    print(f"  cost.py: FAIL - {e}")

try:
    from equipment import EquipmentSystem
    print("  equipment.py: OK")
except Exception as e:
    print(f"  equipment.py: FAIL - {e}")

try:
    from report import ReportSystem
    print("  report.py: OK")
except Exception as e:
    print(f"  report.py: FAIL - {e}")

try:
    from ai_qa_v2 import AIQAV2
    print("  ai_qa_v2.py: OK")
except Exception as e:
    print(f"  ai_qa_v2.py: FAIL - {e}")

try:
    from planning import PlanningAssistant
    print("  planning.py: OK")
except Exception as e:
    print(f"  planning.py: FAIL - {e}")

try:
    from quality_detection import QualityDetector
    print("  quality_detection.py: OK")
except Exception as e:
    print(f"  quality_detection.py: FAIL - {e}")

try:
    from safety import SafetyManager
    print("  safety.py: OK")
except Exception as e:
    print(f"  safety.py: FAIL - {e}")

# Test functionality
print("\n[2] Functionality Test")
try:
    road = Road3D()
    road.add_point(0, 0, 0)
    road.add_point(1, 100, 50)
    road.add_progress(0, 1, "completed", 100)
    road.add_material_cost('test', 100)
    road.add_device('d1', 'm1', 'c1')
    print("  Basic operations: OK")
except Exception as e:
    print(f"  Basic operations: FAIL - {e}")

# Test AI Q&A
print("\n[3] AI Q&A Test")
try:
    road = Road3D()
    qa = AIQAV2(road)
    answer = qa.understand("进度怎么样")
    print(f"  Q: 进度怎么样")
    print(f"  A: {answer[:50]}...")
except Exception as e:
    print(f"  AI Q&A: FAIL - {e}")

# Test planning
print("\n[4] Planning Test")
try:
    road = Road3D()
    road.add_device('d1', 'm1', 'c1')
    from planning import PlanningAssistant
    planner = PlanningAssistant(road)
    plan = planner.generate_plan(1, 'asphalt')
    print(f"  Plan generated: {plan.get('method', 'N/A')}")
except Exception as e:
    print(f"  Planning: FAIL - {e}")

# Test quality
print("\n[5] Quality Test")
try:
    road = Road3D()
    road.add_quality(1.5, "压实度", "96%", "ok")
    from quality_detection import QualityDetector
    qd = QualityDetector(road)
    result = qd.check_quality('compaction', '96%')
    print(f"  Quality check: {result.get('status', 'N/A')}")
except Exception as e:
    print(f"  Quality: FAIL - {e}")

# Test safety
print("\n[6] Safety Test")
try:
    road = Road3D()
    from safety import SafetyManager
    sm = SafetyManager(road)
    risks = sm.assess_risk()
    print(f"  Risks identified: {len(risks)}")
except Exception as e:
    print(f"  Safety: FAIL - {e}")

print("\n" + "="*60)
print("REVIEW COMPLETE")
print("="*60)
