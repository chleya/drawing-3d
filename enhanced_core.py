# -*- coding: utf-8 -*-
"""
Drawing 3D - Enhanced Core Modules
增强版核心模块
"""

import os
import json
from datetime import datetime


# ==================== 增强版天气系统 ====================

class WeatherSystem:
    """施工天气管理系统 - 增强版"""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.cache = {}
        self.cache_ttl = 300  # 5分钟缓存
    
    def get_current(self, location):
        """获取当前天气"""
        return {
            'location': location,
            'temp': 25,
            'condition': 'sunny',
            'humidity': 60,
            'wind': 12,
            'update_time': datetime.now().isoformat()
        }
    
    def get_forecast(self, location, days=7):
        """获取天气预报"""
        return [self.get_current(location) for _ in range(days)]
    
    def analyze_impact(self, weather):
        """分析天气对施工的影响"""
        impacts = []
        
        if weather.get('condition') == 'rain':
            impacts.append('不建议室外施工')
        if weather.get('temp', 25) > 35:
            impacts.append('注意防暑降温')
        if weather.get('temp', 25) < 5:
            impacts.append('注意防寒保暖')
        if weather.get('wind', 0) > 25:
            impacts.append('高空作业需暂停')
        
        return impacts if impacts else ['天气适宜施工']


# ==================== 增强版成本系统 ====================

class CostSystem:
    """施工成本管理系统 - 增强版"""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.records = []
        self.unit_prices = {
            '沥青': 4500,
            '水泥': 520,
            '碎石': 85,
            '钢筋': 4800,
            '普工': 200,
            '技工': 350,
        }
    
    def add_material(self, name, quantity, price=None):
        """添加材料成本"""
        price = price or self.unit_prices.get(name, 0)
        record = {
            'type': 'material',
            'name': name,
            'quantity': quantity,
            'price': price,
            'total': quantity * price,
            'timestamp': datetime.now().isoformat()
        }
        self.records.append(record)
        return record
    
    def add_labor(self, worker_type, days, price=None):
        """添加人工成本"""
        price = price or self.unit_prices.get(worker_type, 200)
        record = {
            'type': 'labor',
            'name': worker_type,
            'days': days,
            'price': price,
            'total': days * price,
            'timestamp': datetime.now().isoformat()
        }
        self.records.append(record)
        return record
    
    def get_summary(self):
        """获取成本汇总"""
        total = sum(r['total'] for r in self.records)
        by_type = {}
        for r in self.records:
            t = r['type']
            by_type[t] = by_type.get(t, 0) + r['total']
        
        return {
            'total': total,
            'by_type': by_type,
            'count': len(self.records)
        }


# ==================== 增强版设备系统 ====================

class EquipmentSystem:
    """设备管理系统 - 增强版"""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.devices = []
        self.operations = []
    
    def add_device(self, name, device_type='construction', status='idle'):
        """添加设备"""
        device = {
            'id': len(self.devices) + 1,
            'name': name,
            'type': device_type,
            'status': status,
            'add_time': datetime.now().isoformat()
        }
        self.devices.append(device)
        return device
    
    def start_operation(self, device_id):
        """开始作业"""
        for d in self.devices:
            if d['id'] == device_id:
                d['status'] = 'operating'
                d['start_time'] = datetime.now().isoformat()
                return d
        return None
    
    def stop_operation(self, device_id):
        """停止作业"""
        for d in self.devices:
            if d['id'] == device_id:
                d['status'] = 'idle'
                if 'start_time' in d:
                    d['hours'] = d.get('hours', 0) + 1
                return d
        return None
    
    def get_status(self):
        """获取设备状态"""
        status = {'operating': 0, 'idle': 0, 'maintenance': 0}
        for d in self.devices:
            s = d.get('status', 'idle')
            status[s] = status.get(s, 0) + 1
        return status


# ==================== 增强版报告系统 ====================

class ReportSystem:
    """报告系统 - 增强版"""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.reports = []
    
    def generate(self, report_type='daily', data=None):
        """生成报告"""
        data = data or {}
        
        templates = {
            'daily': {
                'title': '日报',
                'sections': ['施工进度', '材料使用', '人员安排', '问题汇总']
            },
            'weekly': {
                'title': '周报',
                'sections': ['本周完成', '下周计划', '质量检查', '安全检查']
            },
            'monthly': {
                'title': '月报',
                'sections': ['月度总结', '成本分析', '进度评估', '下月安排']
            }
        }
        
        template = templates.get(report_type, templates['daily'])
        
        report = {
            'type': report_type,
            'title': template['title'],
            'sections': template['sections'],
            'data': data,
            'generate_time': datetime.now().isoformat()
        }
        
        self.reports.append(report)
        return report
    
    def get_reports(self, report_type=None):
        """获取报告列表"""
        if report_type:
            return [r for r in self.reports if r['type'] == report_type]
        return self.reports


# ==================== 增强版AI问答 ====================

class AIQAV2:
    """AI问答系统 - 增强版"""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.knowledge = {
            '进度': '项目整体进度正常，已完成{percent}%',
            '成本': '当前累计成本{total}元，预算执行率{rate}%',
            '天气': '今日天气{condition}，气温{temp}度',
            '安全': '本周安全检查通过，无事故',
            '质量': '质量检查合格率{pass_rate}%，符合标准',
        }
    
    def ask(self, question):
        """问答"""
        question = question.lower()
        
        for key, response in self.knowledge.items():
            if key in question:
                # 简单替换
                response = response.format(
                    percent=65,
                    total=1250000,
                    rate=78,
                    condition='晴',
                    temp=25,
                    pass_rate=98
                )
                return response
        
        return '感谢您的提问，请具体说明您想了解的内容'


# ==================== 主系统 ====================

class Drawing3D:
    """Drawing 3D 主系统 - 增强版"""
    
    def __init__(self, config_path='config.json'):
        self.config = self._load_config(config_path)
        self._init_systems()
    
    def _load_config(self, config_path):
        """加载配置"""
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'features': {}}
    
    def _init_systems(self):
        """初始化子系统"""
        features = self.config.get('features', {})
        
        self.weather = WeatherSystem(self.config) if features.get('weather', True) else None
        self.cost = CostSystem(self.config) if features.get('cost', True) else None
        self.equipment = EquipmentSystem(self.config) if features.get('equipment', True) else None
        self.report = ReportSystem(self.config) if features.get('report', True) else None
        self.ai_qa = AIQAV2(self.config) if features.get('ai_qa', True) else None
    
    def run(self):
        """运行演示"""
        print("\n" + "="*60)
        print("Drawing 3D - Enhanced Edition")
        print("="*60)
        
        # 天气
        if self.weather:
            w = self.weather.get_current("北京")
            print(f"\n[天气] {w['location']}: {w['condition']}, {w['temp']}°C")
            print(f"  影响: {self.weather.analyze_impact(w)}")
        
        # 成本
        if self.cost:
            self.cost.add_material('水泥', 100)
            self.cost.add_material('钢筋', 50)
            self.cost.add_labor('技工', 10)
            summary = self.cost.get_summary()
            print(f"\n[成本] 总计: {summary['total']}元")
            print(f"  明细: {summary['by_type']}")
        
        # 设备
        if self.equipment:
            d1 = self.equipment.add_device('挖掘机', 'excavator')
            d2 = self.equipment.add_device('起重机', 'crane')
            self.equipment.start_operation(d1['id'])
            status = self.equipment.get_status()
            print(f"\n[设备] 状态: {status}")
        
        # 报告
        if self.report:
            r = self.report.generate('daily', {'progress': 65})
            print(f"\n[报告] {r['title']} - {len(r['sections'])}个章节")
        
        # AI问答
        if self.ai_qa:
            print(f"\n[AI问答]")
            print(f"  问: 项目进度如何?")
            print(f"  答: {self.ai_qa.ask('进度')}")
        
        print("\n" + "="*60)
        print("System Ready!")
        print("="*60 + "\n")


# ==================== 运行 ====================

if __name__ == "__main__":
    system = Drawing3D()
    system.run()
