# -*- coding: utf-8 -*-
"""
Drawing 3D - Compliance Assistant
智能合规助手

Features:
- Regulation knowledge base
- Auto compliance checking
- Q&A for regulations
"""

class ComplianceAssistant:
    """Smart Compliance Assistant"""
    
    def __init__(self, road_system):
        self.road = road_system
        
        # Regulations database
        self.regulations = {
            # National standards
            'JTG F40': {
                'name': '公路沥青路面施工技术规范',
                'items': [
                    {'item': '压实度', 'standard': '>=95%', 'method': '核子密实度仪'},
                    {'item': '厚度', 'standard': '>=设计厚度', 'method': '钻芯取样'},
                    {'item': '平整度', 'standard': '<3mm', 'method': '3m直尺'}
                ]
            },
            'JTG F80': {
                'name': '公路工程质量检验评定标准',
                'items': [
                    {'item': '压实度', 'standard': '>=95%', 'method': '核子仪/钻芯'},
                    {'item': '平整度', 'standard': 'IRI<2.0', 'method': '平整度仪'}
                ]
            },
            # Safety regulations
            'JGJ59': {
                'name': '建筑施工安全检查标准',
                'items': [
                    {'item': '安全帽', 'standard': '100%佩戴', 'method': '检查'},
                    {'item': '安全网', 'standard': '完整', 'method': '检查'},
                    {'item': '防护栏', 'standard': '高度>=1.2m', 'method': '测量'}
                ]
            }
        }
    
    def check_compliance(self, item, value):
        """Check compliance for an item"""
        # Find matching regulation
        for reg_id, reg in self.regulations.items():
            for std_item in reg.get('items', []):
                if std_item['item'] in item:
                    # Check if value meets standard
                    standard = std_item['standard']
                    
                    # Simple comparison
                    if '>=' in standard:
                        threshold = float(standard.replace('>=', '').replace('%', ''))
                        try:
                            if float(value.replace('%', '')) >= threshold:
                                return {'status': 'pass', 'standard': standard, 'regulation': reg['name']}
                            else:
                                return {'status': 'fail', 'standard': standard, 'regulation': reg['name']}
                        except:
                            pass
                    
                    if '<' in standard:
                        threshold = float(standard.replace('<', '').replace('%', '').replace('mm', ''))
                        try:
                            val = float(value.replace('%', '').replace('mm', ''))
                            if val <= threshold:
                                return {'status': 'pass', 'standard': standard, 'regulation': reg['name']}
                            else:
                                return {'status': 'fail', 'standard': standard, 'regulation': reg['name']}
                        except:
                            pass
        
        return {'status': 'unknown', 'message': 'No matching standard found'}
    
    def query_regulation(self, keyword):
        """Query regulations by keyword"""
        results = []
        
        for reg_id, reg in self.regulations.items():
            # Check name
            if keyword in reg['name']:
                results.append({
                    'id': reg_id,
                    'name': reg['name'],
                    'items': reg.get('items', [])
                })
                continue
            
            # Check items
            for item in reg.get('items', []):
                if keyword in item['item']:
                    results.append({
                        'id': reg_id,
                        'name': reg['name'],
                        'item': item
                    })
        
        return results
    
    def generate_report(self):
        """Generate compliance report"""
        report = []
        report.append("="*50)
        report.append("Compliance Report")
        report.append("="*50)
        
        # List all regulations
        report.append("\n[Regulations Database]")
        for reg_id, reg in self.regulations.items():
            report.append(f"\n[{reg_id}] {reg['name']}")
            for item in reg.get('items', []):
                report.append(f"  - {item['item']}: {item['standard']}")
        
        return "\n".join(report)


# Demo
if __name__ == "__main__":
    import sys
    sys.path.insert(0, '.')
    from main import Road3D
    
    road = Road3D()
    ca = ComplianceAssistant(road)
    
    print("="*50)
    print("Compliance Assistant Demo")
    print("="*50)
    
    # Check compliance
    print("\n[Check: compaction 96%]")
    result = ca.check_compliance('压实度', '96%')
    print(f"  Status: {result.get('status')}")
    print(f"  Standard: {result.get('standard')}")
    
    # Query
    print("\n[Query: 压实度]")
    results = ca.query_regulation('压实度')
    for r in results:
        print(f"  {r.get('name')}: {r.get('item')}")
    
    # Report
    print(ca.generate_report())
