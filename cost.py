"""成本管理模块
功能：
1. 材料成本记录
2. 人工成本统计
3. 设备租赁费用
4. 成本汇总报表
"""

from datetime import datetime, timedelta

class CostSystem:
    """施工成本管理系统"""
    
    def __init__(self):
        self.materials = []      # 材料成本
        self.labor = []           # 人工成本
        self.equipment = []       # 设备成本
        self.contracts = []        # 合同/付款
        
        # 单价表
        self.unit_prices = {
            # 材料 (元/吨)
            '沥青': 4500,
            '水泥': 520,
            '碎石': 85,
            '沙子': 65,
            '钢筋': 4800,
            # 人工 (元/天)
            '普工': 200,
            '技工': 350,
            '司机': 280,
            '技术员': 400,
            '安全员': 350,
            # 设备 (元/天)
            '压路机': 1500,
            '摊铺机': 2500,
            '挖掘机': 1200,
            '装载机': 800,
            '自卸车': 600
        }
    
    # === 材料成本 ===
    def add_material(self, name, quantity, unit='吨', date=None):
        """添加材料成本"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        unit_price = self.unit_prices.get(name, 1000)
        cost = quantity * unit_price
        
        record = {
            'date': date,
            'type': 'material',
            'name': name,
            'quantity': quantity,
            'unit': unit,
            'unit_price': unit_price,
            'cost': cost
        }
        self.materials.append(record)
        return record
    
    def get_material_cost(self, start_date=None, end_date=None):
        """获取材料成本汇总"""
        total = sum(m['cost'] for m in self.materials)
        
        # 按材料类型汇总
        by_type = {}
        for m in self.materials:
            name = m['name']
            if name not in by_type:
                by_type[name] = {'quantity': 0, 'cost': 0}
            by_type[name]['quantity'] += m['quantity']
            by_type[name]['cost'] += m['cost']
        
        return {
            'total': total,
            'by_type': by_type,
            'records': len(self.materials)
        }
    
    # === 人工成本 ===
    def add_labor(self, role, days, date=None):
        """添加人工成本"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        unit_price = self.unit_prices.get(role, 300)
        cost = days * unit_price
        
        record = {
            'date': date,
            'type': 'labor',
            'role': role,
            'days': days,
            'unit_price': unit_price,
            'cost': cost
        }
        self.labor.append(record)
        return record
    
    def get_labor_cost(self):
        """获取人工成本汇总"""
        total = sum(l['cost'] for l in self.labor)
        
        by_role = {}
        for l in self.labor:
            role = l['role']
            if role not in by_role:
                by_role[role] = {'days': 0, 'cost': 0}
            by_role[role]['days'] += l['days']
            by_role[role]['cost'] += l['cost']
        
        return {
            'total': total,
            'by_role': by_role,
            'records': len(self.labor)
        }
    
    # === 设备成本 ===
    def add_equipment(self, name, days, date=None):
        """添加设备成本"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        unit_price = self.unit_prices.get(name, 1000)
        cost = days * unit_price
        
        record = {
            'date': date,
            'type': 'equipment',
            'name': name,
            'days': days,
            'unit_price': unit_price,
            'cost': cost
        }
        self.equipment.append(record)
        return record
    
    def get_equipment_cost(self):
        """获取设备成本汇总"""
        total = sum(e['cost'] for e in self.equipment)
        
        by_name = {}
        for e in self.equipment:
            name = e['name']
            if name not in by_name:
                by_name[name] = {'days': 0, 'cost': 0}
            by_name[name]['days'] += e['days']
            by_name[name]['cost'] += e['cost']
        
        return {
            'total': total,
            'by_name': by_name,
            'records': len(self.equipment)
        }
    
    # === 成本汇总 ===
    def get_total_cost(self):
        """获取总成本"""
        material = self.get_material_cost()
        labor = self.get_labor_cost()
        equipment = self.get_equipment_cost()
        
        total = material['total'] + labor['total'] + equipment['total']
        
        return {
            'total': total,
            'material': material['total'],
            'labor': labor['total'],
            'equipment': equipment['total'],
            'material_count': material['records'],
            'labor_count': labor['records'],
            'equipment_count': equipment['records']
        }
    
    # === 报表 ===
    def generate_report(self):
        """生成成本报表"""
        total = self.get_total_cost()
        
        report = []
        report.append("="*50)
        report.append("施工成本报表")
        report.append("="*50)
        report.append(f"\n总成本: ¥{total['total']:,.2f}")
        
        report.append(f"\n【材料成本】¥{total['material']:,.2f}")
        mat = self.get_material_cost()
        for name, data in mat['by_type'].items():
            report.append(f"  {name}: {data['quantity']:.1f}吨 × ¥{data['cost']/data['quantity']:.0f} = ¥{data['cost']:,.0f}")
        
        report.append(f"\n【人工成本】¥{total['labor']:,.2f}")
        lab = self.get_labor_cost()
        for role, data in lab['by_role'].items():
            report.append(f"  {role}: {data['days']}天 × ¥{data['cost']/data['days']:.0f} = ¥{data['cost']:,.0f}")
        
        report.append(f"\n【设备成本】¥{total['equipment']:,.2f}")
        eq = self.get_equipment_cost()
        for name, data in eq['by_name'].items():
            report.append(f"  {name}: {data['days']}天 × ¥{data['cost']/data['days']:.0f} = ¥{data['cost']:,.0f}")
        
        return "\n".join(report)


# 测试
if __name__ == "__main__":
    cs = CostSystem()
    
    # 添加测试数据
    cs.add_material('沥青', 500)
    cs.add_material('水泥', 200)
    cs.add_material('碎石', 3000)
    
    cs.add_labor('技工', 30)
    cs.add_labor('普工', 50)
    cs.add_labor('司机', 20)
    
    cs.add_equipment('压路机', 15)
    cs.add_equipment('摊铺机', 10)
    cs.add_equipment('挖掘机', 8)
    
    # 输出报表
    print(cs.generate_report())
