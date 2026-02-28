"""设备调度模块
功能：
1. 设备台账
2. 设备状态管理
3. 设备调度安排
4. 设备利用率统计
"""

from datetime import datetime, timedelta
from enum import Enum

class EquipmentStatus(Enum):
    RUNNING = "运行中"
    IDLE = "闲置"
    MAINTENANCE = "维修中"
    BROKEN = "故障"
    SCRAP = "报废"

class EquipmentSystem:
    """设备调度管理系统"""
    
    def __init__(self):
        self.equipment = []  # 设备列表
        self.schedules = []  # 调度记录
        self.records = []   # 使用记录
        
    def add_equipment(self, name, model, category, purchase_date=None):
        """添加设备"""
        if purchase_date is None:
            purchase_date = datetime.now().strftime('%Y-%m-%d')
        
        eq = {
            'id': len(self.equipment) + 1,
            'name': name,
            'model': model,
            'category': category,
            'status': EquipmentStatus.IDLE.value,
            'purchase_date': purchase_date,
            'hours_used': 0,
            'maintenance_due': 500  # 每500小时保养
        }
        self.equipment.append(eq)
        return eq
    
    def update_status(self, equipment_id, status):
        """更新设备状态"""
        for eq in self.equipment:
            if eq['id'] == equipment_id:
                eq['status'] = status.value if isinstance(status, EquipmentStatus) else status
                return eq
        return None
    
    def get_equipment(self, category=None, status=None):
        """查询设备"""
        result = self.equipment
        
        if category:
            result = [e for e in result if e['category'] == category]
        if status:
            result = [e for e in result if e['status'] == status]
        
        return result
    
    def schedule(self, equipment_id, location, start_date, end_date, operator):
        """设备调度安排"""
        schedule = {
            'id': len(self.schedules) + 1,
            'equipment_id': equipment_id,
            'location': location,
            'start_date': start_date,
            'end_date': end_date,
            'operator': operator,
            'status': 'scheduled'
        }
        self.schedules.append(schedule)
        
        # 更新设备状态
        self.update_status(equipment_id, EquipmentStatus.RUNNING)
        
        return schedule
    
    def get_schedule(self, date=None):
        """获取调度安排"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        result = []
        for s in self.schedules:
            if s['start_date'] <= date <= s['end_date']:
                # 获取设备信息
                eq = [e for e in self.equipment if e['id'] == s['equipment_id']]
                if eq:
                    s['equipment_name'] = eq[0]['name']
                result.append(s)
        
        return result
    
    def get_utilization(self, start_date=None, end_date=None):
        """设备利用率统计"""
        if not start_date:
            start_date = datetime.now().replace(day=1).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        total = len(self.equipment)
        if total == 0:
            return {'total': 0, 'by_category': {}}
        
        # 统计运行时间
        running = len(self.get_equipment(status=EquipmentStatus.RUNNING.value))
        
        return {
            'total': total,
            'running': running,
            'idle': len(self.get_equipment(status=EquipmentStatus.IDLE.value)),
            'maintenance': len(self.get_equipment(status=EquipmentStatus.MAINTENANCE.value)),
            'utilization_rate': running / total * 100 if total > 0 else 0
        }
    
    def generate_report(self):
        """生成设备报表"""
        report = []
        report.append("="*50)
        report.append("设备台账报表")
        report.append("="*50)
        
        # 按类别统计
        categories = {}
        for eq in self.equipment:
            cat = eq['category']
            if cat not in categories:
                categories[cat] = {'total': 0, 'running': 0, 'idle': 0}
            categories[cat]['total'] += 1
            if eq['status'] == EquipmentStatus.RUNNING.value:
                categories[cat]['running'] += 1
            elif eq['status'] == EquipmentStatus.IDLE.value:
                categories[cat]['idle'] += 1
        
        report.append(f"\n设备总数: {len(self.equipment)}")
        
        for cat, data in categories.items():
            rate = data['running'] / data['total'] * 100 if data['total'] > 0 else 0
            report.append(f"\n【{cat}】")
            report.append(f"  总数: {data['total']}")
            report.append(f"  运行: {data['running']}")
            report.append(f"  闲置: {data['idle']}")
            report.append(f"  利用率: {rate:.1f}%")
        
        # 设备清单
        report.append("\n【设备清单】")
        for eq in self.equipment:
            status_icon = "🟢" if eq['status'] == EquipmentStatus.RUNNING.value else "⚪"
            report.append(f"  {status_icon} {eq['name']} ({eq['model']}) - {eq['status']}")
        
        return "\n".join(report)


# 测试
if __name__ == "__main__":
    es = EquipmentSystem()
    
    # 添加设备
    es.add_equipment('压路机1', 'CAT', '压路机')
    es.add_equipment('压路机2', 'CAT', '压路机')
    es.add_equipment('摊铺机1', 'VOGELE', '摊铺机')
    es.add_equipment('挖掘机1', 'CAT', '挖掘机')
    es.add_equipment('装载机1', 'LIEBHER', '装载机')
    
    # 更新状态
    es.update_status(1, EquipmentStatus.RUNNING)
    es.update_status(3, EquipmentStatus.RUNNING)
    es.update_status(4, EquipmentStatus.MAINTENANCE)
    
    # 调度安排
    es.schedule(1, 'K1+500', '2026-02-28', '2026-03-05', '张三')
    es.schedule(2, 'K2+000', '2026-03-01', '2026-03-10', '李四')
    es.schedule(3, 'K3+200', '2026-02-28', '2026-03-03', '王五')
    
    # 输出报表
    print(es.generate_report())
    
    print("\n" + "="*50)
    print("今日调度:")
    for s in es.get_schedule('2026-02-28'):
        print(f"  {s['equipment_name']}: {s['location']} - {s['operator']}")
