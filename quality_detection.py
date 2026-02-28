# -*- coding: utf-8 -*-
"""
Drawing 3D - Intelligent Quality Detection
智能质量检测

Features:
- Quality standard checking
- Auto defect detection
- Real-time alerts
- Quality history tracking
"""


class QualityDetector:
    """Intelligent Quality Detection"""
    
    def __init__(self, road_system):
        self.road = road_system
        
        # Quality standards (threshold values)
        self.standards = {
            'compaction': {
                'name': '压实度',
                'unit': '%',
                'min': 95,
                'max': 100,
                'warning': 95
            },
            'thickness': {
                'name': '厚度',
                'unit': 'mm',
                'min': 50,
                'max': 80,
                'warning': 55
            },
            'temperature': {
                'name': '温度',
                'unit': 'C',
                'min': 140,
                'max': 170,
                'warning': 145
            },
            'flatness': {
                'name': '平整度',
                'unit': 'mm',
                'min': 0,
                'max': 3,
                'warning': 2.5
            },
            'moisture': {
                'name': '含水率',
                'unit': '%',
                'min': 0,
                'max': 5,
                'warning': 4
            }
        }
    
    def check_quality(self, item, value):
        """Check if quality meets standard"""
        if item not in self.standards:
            return {'status': 'unknown', 'message': f'Unknown item: {item}'}
        
        std = self.standards[item]
        
        # Check value
        if isinstance(value, str):
            # Try to extract number
            try:
                value = float(value.replace('%', '').replace('mm', '').replace('C', ''))
            except:
                return {'status': 'unknown', 'message': f'Cannot parse value: {value}'}
        
        # Determine status
        if value < std['min'] or value > std['max']:
            status = 'fail'
            message = f'{std["name"]}不达标: {value}{std["unit"]} (要求: {std["min"]}-{std["max"]}{std["unit"]})'
        elif value < std['warning']:
            status = 'warning'
            message = f'{std["name"]}偏低: {value}{std["unit"]} (建议: >{std["warning"]}{std["unit"]})'
        else:
            status = 'pass'
            message = f'{std["name"]}合格: {value}{std["unit"]}'
        
        return {
            'status': status,
            'item': item,
            'value': value,
            'standard': std,
            'message': message
        }
    
    def check_all_standards(self, data_dict):
        """Check multiple quality items"""
        results = []
        
        for item, value in data_dict.items():
            result = self.check_quality(item, value)
            results.append(result)
        
        # Summary
        pass_count = sum(1 for r in results if r['status'] == 'pass')
        warning_count = sum(1 for r in results if r['status'] == 'warning')
        fail_count = sum(1 for r in results if r['status'] == 'fail')
        
        summary = {
            'total': len(results),
            'pass': pass_count,
            'warning': warning_count,
            'fail': fail_count,
            'overall': 'pass' if fail_count == 0 else ('warning' if warning_count == 0 else 'fail')
        }
        
        return {'results': results, 'summary': summary}
    
    def auto_detect(self):
        """Auto detect quality from road data"""
        detected = []
        
        # Check existing quality records
        for q in self.road.quality:
            item = q.get('item', '').lower()
            result = q.get('result', '')
            
            # Map item names
            if '压实' in item:
                item = 'compaction'
            elif '厚度' in item:
                item = 'thickness'
            elif '温度' in item:
                item = 'temperature'
            elif '平整' in item:
                item = 'flatness'
            elif '含水' in item:
                item = 'moisture'
            else:
                continue
            
            check = self.check_quality(item, result)
            check['mileage'] = q.get('mileage')
            detected.append(check)
        
        return detected
    
    def generate_alert(self, detected_issues):
        """Generate alerts for issues"""
        alerts = []
        
        for issue in detected_issues:
            if issue['status'] == 'fail':
                alerts.append({
                    'level': 'critical',
                    'mileage': issue.get('mileage', 'N/A'),
                    'message': issue['message']
                })
            elif issue['status'] == 'warning':
                alerts.append({
                    'level': 'warning',
                    'mileage': issue.get('mileage', 'N/A'),
                    'message': issue['message']
                })
        
        return alerts
    
    def quality_report(self):
        """Generate quality report"""
        # Auto detect
        detected = self.auto_detect()
        
        report = []
        report.append("="*50)
        report.append("Quality Detection Report")
        report.append("="*50)
        
        if not detected:
            report.append("\nNo quality data available")
            return "\n".join(report)
        
        # Summary
        statuses = {'pass': 0, 'warning': 0, 'fail': 0, 'unknown': 0}
        for d in detected:
            statuses[d['status']] = statuses.get(d['status'], 0) + 1
        
        report.append(f"\n[Summary]")
        report.append(f"  Total: {len(detected)}")
        report.append(f"  Pass: {statuses['pass']}")
        report.append(f"  Warning: {statuses['warning']}")
        report.append(f"  Fail: {statuses['fail']}")
        
        # Issues
        issues = [d for d in detected if d['status'] in ['warning', 'fail']]
        
        if issues:
            report.append(f"\n[Issues] ({len(issues)} items)")
            for issue in issues:
                icon = "[FAIL]" if issue['status'] == 'fail' else "[WARN]"
                report.append(f"  {icon} K{issue.get('mileage', 'N/A')}: {issue['message']}")
        
        # Alerts
        alerts = self.generate_alert(issues)
        if alerts:
            report.append(f"\n[Alerts] ({len(alerts)} items)")
            for alert in alerts:
                icon = "!!!" if alert['level'] == 'critical' else "!!"
                report.append(f"  {icon} {alert['message']}")
        
        return "\n".join(report)


# Demo
if __name__ == "__main__":
    import sys
    sys.path.insert(0, '.')
    from main import Road3D
    
    road = Road3D()
    
    # Add quality data
    road.add_quality(1.5, "压实度", "96%", "ok")
    road.add_quality(1.5, "温度", "155C", "ok")
    road.add_quality(2.0, "压实度", "94%", "warning")
    road.add_quality(2.0, "厚度", "58mm", "ok")
    road.add_quality(2.5, "压实度", "93%", "fail")
    
    # Test detection
    detector = QualityDetector(road)
    
    print("="*50)
    print("Quality Detection Demo")
    print("="*50)
    
    # Check single
    print("\n[Check Single: compaction 96%]")
    result = detector.check_quality('compaction', '96%')
    print(f"  Status: {result['status']}")
    print(f"  Message: {result['message']}")
    
    # Auto detect
    print("\n[Auto Detect]")
    detected = detector.auto_detect()
    for d in detected:
        print(f"  K{d.get('mileage')}: {d['status']} - {d['message']}")
    
    # Full report
    print(detector.quality_report())
