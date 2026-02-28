# -*- coding: utf-8 -*-
"""
Drawing 3D - NeuralSite Light
Road Engineering Management System - Live Demo
"""

import sys
sys.path.insert(0, '.')
from main import Road3D


def setup_demo(road):
    """Setup demo data"""
    # Points
    for i in range(8):
        road.add_point(i, i * 100, i * 30)
    
    # Knowledge
    road.add_knowledge("asphalt_temp", "150-170C")
    road.add_knowledge("compaction", "95-98%")
    road.add_knowledge("layer_thickness", "50-80mm")
    
    # Photos
    road.add_photo(1.5, "K1+500.jpg", "Base layer")
    road.add_photo(2.3, "K2+300.jpg", "Asphalt paving")
    
    # Quality
    road.add_quality(1.5, "压实度", "96%", "ok")
    road.add_quality(1.5, "温度", "155C", "ok")
    road.add_quality(2.0, "压实度", "94%", "warning")
    road.add_quality(2.5, "压实度", "93%", "fail")
    
    # Progress
    road.add_progress(0, 1, "completed", 100)
    road.add_progress(1, 2, "completed", 100)
    road.add_progress(2, 3, "in_progress", 70)
    road.add_progress(3, 4, "in_progress", 40)
    road.add_progress(4, 5, "not_started", 0)
    road.add_progress(5, 6, "not_started", 0)
    road.add_progress(6, 7, "not_started", 0)
    
    # Cost
    road.add_material_cost('沥青', 500)
    road.add_material_cost('水泥', 200)
    road.add_material_cost('碎石', 3000)
    road.add_labor_cost('技工', 30)
    road.add_labor_cost('普工', 50)
    road.add_labor_cost('司机', 20)
    road.add_equipment_cost('压路机', 15)
    road.add_equipment_cost('摊铺机', 10)
    
    # Equipment
    road.add_device('压路机1', 'CAT', '压路机')
    road.add_device('压路机2', 'CAT', '压路机')
    road.add_device('摊铺机1', 'VOGELE', '摊铺机')
    road.add_device('挖掘机1', 'CAT', '挖掘机')
    road.add_device('装载机1', 'LIEBHER', '装载机')
    road.update_device_status(1, 'RUNNING')
    road.update_device_status(3, 'RUNNING')
    road.update_device_status(4, 'MAINTENANCE')
    road.schedule_device(1, 'K1+500', '2026-02-28', '2026-03-05', '张三')
    road.schedule_device(2, 'K2+000', '2026-03-01', '2026-03-10', '李四')
    
    # Reports
    road.add_daily_report('2026-02-28', 1.5, '沥青摊铺', 15, '压路机2台', '晴天')
    road.add_daily_report('2026-02-27', 1.2, '水稳层', 12, '摊铺机1台', '多云')
    road.add_quality_record('2026-02-28', 1.5, '压实度', '98%', 'ok', '张三')
    road.add_issue('2026-02-28', '压路机故障', 'medium', '已修复')


def main():
    print("="*60)
    print("  Drawing 3D - NeuralSite Light")
    print("  Road Engineering Management System")
    print("="*60)
    
    # Create road system
    road = Road3D()
    setup_demo(road)
    
    # 1. Project Overview
    print("\n" + "="*50)
    print("[1] PROJECT OVERVIEW")
    print("="*50)
    road.render()
    
    # 2. Weather
    print("\n" + "="*50)
    print("[2] WEATHER SYSTEM")
    print("="*50)
    w = road.get_weather()
    can, msg = road.can_construct_today()
    print(f"Weather: {w['weather']}, {w['temperature']}C")
    print(f"Construction: {'OK' if can else 'NO'}")
    print("\nImpact Analysis:")
    for i in road.get_weather_impact(w):
        print(f"  - {i['message']}")
    
    # 3. Cost
    print("\n" + "="*50)
    print("[3] COST MANAGEMENT")
    print("="*50)
    c = road.get_cost_summary()
    print(f"Total: {c['total']:,.0f} Yuan")
    print(f"  Material: {c['material']:,.0f}")
    print(f"  Labor: {c['labor']:,.0f}")
    print(f"  Equipment: {c['equipment']:,.0f}")
    
    # 4. Equipment
    print("\n" + "="*50)
    print("[4] EQUIPMENT MANAGEMENT")
    print("="*50)
    e = road.get_device_utilization()
    print(f"Total: {e['total']}, Running: {e['running']}, Idle: {e['idle']}")
    print(f"Utilization: {e['utilization_rate']:.1f}%")
    
    # 5. AI Planning
    print("\n" + "="*50)
    print("[5] AI CONSTRUCTION PLANNING")
    print("="*50)
    plan = road.generate_plan(2, 'asphalt')
    print(f"Method: {plan['method']}")
    print(f"Est. Days: {plan['estimated_days']}")
    print(f"Layers: {', '.join(plan['layers'])}")
    print("\nRisks:")
    for r in plan['risks']:
        print(f"  [{r['level']}] {r['message']}")
    print("\nRecommendations:")
    for r in plan['recommendations']:
        print(f"  - {r}")
    
    # 6. Quality Detection
    print("\n" + "="*50)
    print("[6] INTELLIGENT QUALITY DETECTION")
    print("="*50)
    print(road.quality_report())
    
    # 7. Safety Management
    print("\n" + "="*50)
    print("[7] PREDICTIVE SAFETY MANAGEMENT")
    print("="*50)
    print(road.safety_report())
    
    # 8. AI Q&A
    print("\n" + "="*50)
    print("[8] AI ASSISTANT (Q&A)")
    print("="*50)
    
    questions = [
        "进度怎么样？",
        "成本多少？",
        "天气有影响吗？",
        "有什么施工计划？",
        "质量怎么样？",
        "安全状态？"
    ]
    
    for q in questions:
        print(f"\nQ: {q}")
        print(f"A: {road.ask(q)}")
    
    # 9. Full Report
    print("\n" + "="*50)
    print("[9] FULL PROJECT REPORT")
    print("="*50)
    print(road.generate_full_report())
    
    print("\n" + "="*60)
    print("  Demo Complete!")
    print("  Run: python main.py -> menu option 12 for AI Assistant")
    print("  Or: python web.py -> http://localhost:8080")
    print("="*60)


if __name__ == "__main__":
    main()
