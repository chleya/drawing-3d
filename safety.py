# -*- coding: utf-8 -*-
"""
Drawing 3D - Predictive Safety Management
预测性安全管理

Features:
- Risk identification
- Behavior analysis
- Environmental monitoring
- Early warning system
"""


class SafetyManager:
    """Predictive Safety Management"""
    
    def __init__(self, road_system):
        self.road = road_system
        
        # Safety rules
        self.rules = {
            'ppe': {
                'name': 'PPE Check',
                'description': '安全装备检查',
                'risk': 'high',
                'check': ['安全帽', '反光衣', '安全鞋']
            },
            'fire': {
                'name': 'Fire Risk',
                'description': '火灾风险',
                'risk': 'critical',
                'triggers': ['明火', '吸烟', '高温']
            },
            'electrical': {
                'name': 'Electrical Safety',
                'description': '用电安全',
                'risk': 'high',
                'check': ['电缆', '配电箱', '接地']
            },
            'height': {
                'name': 'Height Work',
                'description': '高空作业',
                'risk': 'high',
                'check': ['安全带', '防护网', '脚手架']
            },
            'vehicle': {
                'name': 'Vehicle Safety',
                'description': '车辆安全',
                'risk': 'medium',
                'check': ['限速', '指挥', '警示标志']
            },
            'weather': {
                'name': 'Weather Alert',
                'description': '天气预警',
                'risk': 'medium',
                'triggers': ['暴雨', '大风', '雷电']
            }
        }
        
        # Risk log
        self.risk_log = []
    
    def assess_risk(self):
        """Assess current safety risks"""
        risks = []
        
        # Check weather
        try:
            w = self.road.get_weather()
            if w['weather'] in ['stormy', 'rainy']:
                risks.append({
                    'type': 'weather',
                    'level': 'medium',
                    'message': f'Weather: {w["weather"]} - Take precautions'
                })
            if w['wind_speed'] > 6:
                risks.append({
                    'type': 'weather',
                    'level': 'high',
                    'message': f'High wind: {w["wind_speed"]}m/s - No height work'
                })
            if w['temperature'] > 35:
                risks.append({
                    'type': 'heat',
                    'level': 'medium',
                    'message': f'High temp: {w["temperature"]}C - Heat stroke risk'
                })
        except:
            pass
        
        # Check time (night work is riskier)
        from datetime import datetime
        hour = datetime.now().hour
        if hour < 6 or hour > 20:
            risks.append({
                'type': 'time',
                'level': 'medium',
                'message': 'Night work - Ensure adequate lighting'
            })
        
        # Check equipment status
        try:
            util = self.road.get_device_utilization()
            if util['running'] > 5:
                risks.append({
                    'type': 'equipment',
                    'level': 'medium',
                    'message': f'{util["running"]} equipment running - Traffic control needed'
                })
        except:
            pass
        
        return risks
    
    def generate_warning(self, risks):
        """Generate warnings from risks"""
        warnings = []
        
        for risk in risks:
            if risk['level'] == 'critical':
                level = '!!!'
            elif risk['level'] == 'high':
                level = '!!'
            else:
                level = '!'
            
            warnings.append(f"{level} {risk['message']}")
        
        return warnings
    
    def safety_checklist(self):
        """Generate safety checklist"""
        checklist = []
        
        # Always include basic checks
        checklist.append({
            'category': 'Basic',
            'items': [
                'Safety briefing completed',
                'PPE all workers confirmed',
                'First aid kit available',
                'Emergency exit clear'
            ]
        })
        
        # Add category-specific checks
        checklist.append({
            'category': 'Equipment',
            'items': [
                'Equipment inspection done',
                'Safety guards in place',
                'Emergency stop functional'
            ]
        })
        
        checklist.append({
            'category': 'Environment',
            'items': [
                'Weather conditions checked',
                'Work area clear',
                'Signage in place'
            ]
        })
        
        return checklist
    
    def safety_report(self):
        """Generate comprehensive safety report"""
        # Assess risks
        risks = self.assess_risk()
        
        # Get warnings
        warnings = self.generate_warning(risks)
        
        # Get checklist
        checklist = self.safety_checklist()
        
        # Build report
        report = []
        report.append("="*50)
        report.append("Safety Management Report")
        report.append("="*50)
        
        # Risk level
        if not risks:
            level = "LOW"
            emoji = "[OK]"
        elif all(r['level'] == 'low' for r in risks):
            level = "LOW"
            emoji = "[OK]"
        elif any(r['level'] == 'critical' for r in risks):
            level = "CRITICAL"
            emoji = "[STOP]"
        else:
            level = "MEDIUM"
            emoji = "[WARN]"
        
        report.append(f"\n[Risk Level] {emoji} {level}")
        
        # Risks
        report.append(f"\n[Identified Risks] ({len(risks)} items)")
        if risks:
            for risk in risks:
                icon = {"low": "[-]", "medium": "[!]", "critical": "[!!]"}.get(risk['level'], "[-]")
                report.append(f"  {icon} {risk['message']}")
        else:
            report.append("  No significant risks identified")
        
        # Warnings
        if warnings:
            report.append(f"\n[Active Warnings] ({len(warnings)} items)")
            for w in warnings:
                report.append(f"  {w}")
        
        # Checklist summary
        report.append(f"\n[Safety Checklist]")
        for cat in checklist:
            report.append(f"  [{cat['category']}] {len(cat['items'])} items")
        
        return "\n".join(report)


# Demo
if __name__ == "__main__":
    import sys
    sys.path.insert(0, '.')
    from main import Road3D
    
    road = Road3D()
    
    # Test safety
    safety = SafetyManager(road)
    
    print("="*50)
    print("Safety Management Demo")
    print("="*50)
    
    # Risk assessment
    print("\n[Risk Assessment]")
    risks = safety.assess_risk()
    for r in risks:
        print(f"  [{r['level']}] {r['message']}")
    
    # Report
    print(safety.safety_report())
