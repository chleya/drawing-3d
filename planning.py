# -*- coding: utf-8 -*-
"""
Drawing 3D - AI Planning Assistant
AI辅助施工规划

Features:
- Generate construction plans
- Optimize resource allocation
- Analyze constraints
- Risk assessment
"""


class PlanningAssistant:
    """AI Construction Planning"""
    
    def __init__(self, road_system):
        self.road = road_system
        
        # Construction methods
        self.methods = {
            'asphalt': {
                'name': '沥青路面',
                'layers': ['沥青面层', '水稳基层', '底基层'],
                'temp_range': (140, 170),  # Celsius
                'thickness': [40, 180, 300],  # mm
                'equipment': ['摊铺机', '压路机', '洒水车'],
                'days_per_km': 0.5
            },
            'concrete': {
                'name': '水泥混凝土',
                'layers': ['面层', '基层'],
                'temp_range': (5, 35),
                'thickness': [250, 200],
                'equipment': ['搅拌机', '摊铺机', '切缝机'],
                'days_per_km': 0.7
            }
        }
        
        # Resource constraints
        self.constraints = {
            'max_workers': 50,
            'max_equipment': 10,
            'min_temperature': 5,
            'max_rain_prob': 0.3
        }
    
    def analyze_conditions(self):
        """Analyze current conditions"""
        conditions = {}
        
        # Weather
        w = self.road.get_weather()
        conditions['weather'] = w['weather']
        conditions['temperature'] = w['temperature']
        
        # Progress
        prog = self.road.get_progress()
        conditions['progress'] = prog
        
        # Equipment availability
        util = self.road.get_device_utilization()
        conditions['available_equipment'] = util['idle']
        
        # Cost status
        cost = self.road.get_cost_summary()
        conditions['budget_used'] = cost['total']
        
        return conditions
    
    def generate_plan(self, target_km, method='asphalt'):
        """Generate construction plan"""
        if method not in self.methods:
            return {"error": f"Unknown method: {method}"}
        
        m = self.methods[method]
        conditions = self.analyze_conditions()
        
        # Calculate days needed
        days_needed = target_km * m['days_per_km']
        
        # Check constraints
        risks = self._check_risks(conditions, method)
        
        # Generate plan
        plan = {
            'method': m['name'],
            'target_km': target_km,
            'estimated_days': days_needed,
            'layers': m['layers'],
            'thickness': m['thickness'],
            'equipment_needed': m['equipment'],
            'temperature_range': m['temp_range'],
            'conditions': conditions,
            'risks': risks,
            'recommendations': self._generate_recommendations(conditions, risks)
        }
        
        return plan
    
    def _check_risks(self, conditions, method):
        """Check potential risks"""
        risks = []
        
        # Weather risk
        if conditions['temperature'] < 5:
            risks.append({
                'level': 'high',
                'type': 'temperature',
                'message': '温度过低，不宜施工'
            })
        elif conditions['temperature'] > 35:
            risks.append({
                'level': 'medium',
                'type': 'temperature',
                'message': '温度过高，注意防暑'
            })
        
        if conditions['weather'] in ['rainy', 'stormy']:
            risks.append({
                'level': 'high',
                'type': 'weather',
                'message': '天气不佳，建议推迟'
            })
        
        # Equipment risk
        if conditions['available_equipment'] < 2:
            risks.append({
                'level': 'medium',
                'type': 'equipment',
                'message': '设备不足，需调度'
            })
        
        # Progress risk
        if conditions['progress'] < 50:
            risks.append({
                'level': 'low',
                'type': 'progress',
                'message': '进度正常'
            })
        
        return risks
    
    def _generate_recommendations(self, conditions, risks):
        """Generate recommendations"""
        recs = []
        
        # Based on risks
        high_risks = [r for r in risks if r['level'] == 'high']
        
        if high_risks:
            recs.append("存在高风险，建议调整计划")
        else:
            recs.append("条件适宜，可以施工")
        
        # Weather recommendations
        if conditions['weather'] == 'sunny':
            recs.append("晴天适合沥青摊铺")
        elif conditions['weather'] == 'rainy':
            recs.append("建议室内作业")
        
        # Equipment
        if conditions['available_equipment'] >= 3:
            recs.append("设备充足，可加快进度")
        
        return recs
    
    def optimize_plan(self, plan, constraints=None):
        """Optimize existing plan"""
        if constraints is None:
            constraints = {}
        
        optimized = plan.copy()
        
        # Try to reduce days
        if 'max_days' in constraints:
            if optimized['estimated_days'] > constraints['max_days']:
                optimized['suggestion'] = "需要增加资源才能在要求时间内完成"
        
        # Try to reduce cost
        if 'budget' in constraints:
            # Rough estimate
            cost_per_km = 500000  # placeholder
            total_cost = optimized['target_km'] * cost_per_km
            
            if total_cost > constraints['budget']:
                optimized['budget_risk'] = "可能超出预算"
        
        return optimized


# Demo
if __name__ == "__main__":
    import sys
    sys.path.insert(0, '.')
    from main import Road3D
    
    road = Road3D()
    
    # Setup
    for i in range(5):
        road.add_point(i, i*100, i*30)
    
    road.add_progress(0, 1, "completed", 100)
    road.add_progress(1, 2, "completed", 100)
    road.add_progress(2, 3, "in_progress", 50)
    
    road.add_device('压路机1', 'CAT', '压路机')
    road.add_device('压路机2', 'CAT', '压路机')
    road.add_device('摊铺机1', 'VOGELE', '摊铺机')
    
    # Test planning
    planner = PlanningAssistant(road)
    
    print("="*50)
    print("AI Planning Assistant Demo")
    print("="*50)
    
    # Current conditions
    print("\n[Current Conditions]")
    cond = planner.analyze_conditions()
    print(f"  Weather: {cond['weather']}, {cond['temperature']}C")
    print(f"  Progress: {cond['progress']:.0f}%")
    print(f"  Available Equipment: {cond['available_equipment']}")
    
    # Generate plan
    print("\n[Generate Plan: 2km asphalt]")
    plan = planner.generate_plan(2, 'asphalt')
    
    print(f"  Method: {plan['method']}")
    print(f"  Estimated Days: {plan['estimated_days']}")
    print(f"  Layers: {plan['layers']}")
    print(f"  Equipment: {plan['equipment_needed']}")
    
    print("\n[Risks]")
    for risk in plan['risks']:
        print(f"  [{risk['level']}] {risk['message']}")
    
    print("\n[Recommendations]")
    for rec in plan['recommendations']:
        print(f"  - {rec}")
