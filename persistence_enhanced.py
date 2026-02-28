# -*- coding: utf-8 -*-
"""
Drawing 3D - Data Persistence
数据持久化
"""

import os
import json
from datetime import datetime
from pathlib import Path


class DataPersistence:
    """数据持久化"""
    
    def __init__(self, data_dir='./data'):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # 子目录
        self.weather_dir = self.data_dir / 'weather'
        self.cost_dir = self.data_dir / 'cost'
        self.equipment_dir = self.data_dir / 'equipment'
        self.report_dir = self.data_dir / 'reports'
        
        for d in [self.weather_dir, self.cost_dir, self.equipment_dir, self.report_dir]:
            d.mkdir(exist_ok=True)
    
    # ==================== 天气数据 ====================
    
    def save_weather(self, location, data):
        """保存天气数据"""
        file_path = self.weather_dir / f'{location}.json'
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_weather(self, location):
        """加载天气数据"""
        file_path = self.weather_dir / f'{location}.json'
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    # ==================== 成本数据 ====================
    
    def save_cost_records(self, records):
        """保存成本记录"""
        file_path = self.cost_dir / 'records.json'
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
    
    def load_cost_records(self):
        """加载成本记录"""
        file_path = self.cost_dir / 'records.json'
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_cost_summary(self, summary):
        """保存成本汇总"""
        file_path = self.cost_dir / 'summary.json'
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
    
    def load_cost_summary(self):
        """加载成本汇总"""
        file_path = self.cost_dir / 'summary.json'
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    # ==================== 设备数据 ====================
    
    def save_devices(self, devices):
        """保存设备列表"""
        file_path = self.equipment_dir / 'devices.json'
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(devices, f, ensure_ascii=False, indent=2)
    
    def load_devices(self):
        """加载设备列表"""
        file_path = self.equipment_dir / 'devices.json'
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    # ==================== 报告数据 ====================
    
    def save_report(self, report):
        """保存报告"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_path = self.report_dir / f'report_{timestamp}.json'
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        return file_path
    
    def load_reports(self):
        """加载所有报告"""
        reports = []
        for f in self.report_dir.glob('report_*.json'):
            with open(f, 'r', encoding='utf-8') as fp:
                reports.append(json.load(fp))
        return reports
    
    # ==================== 系统数据 ====================
    
    def save_system_state(self, state):
        """保存系统状态"""
        file_path = self.data_dir / 'system_state.json'
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    
    def load_system_state(self):
        """加载系统状态"""
        file_path = self.data_dir / 'system_state.json'
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    # ==================== 备份与恢复 ====================
    
    def backup(self, backup_dir='./backups'):
        """备份所有数据"""
        import shutil
        backup_path = Path(backup_dir) / datetime.now().strftime('%Y%m%d_%H%M%S')
        shutil.copytree(self.data_dir, backup_path)
        return str(backup_path)
    
    def restore(self, backup_path):
        """恢复数据"""
        import shutil
        if Path(backup_path).exists():
            shutil.copytree(backup_path, self.data_dir, dirs_exist_ok=True)
            return True
        return False
    
    # ==================== 统计 ====================
    
    def get_stats(self):
        """获取统计信息"""
        stats = {
            'data_dir': str(self.data_dir),
            'weather_count': len(list(self.weather_dir.glob('*.json'))),
            'cost_records': len(self.load_cost_records()),
            'devices': len(self.load_devices()),
            'reports': len(self.load_reports()),
        }
        return stats


# ==================== 持久化集成 ====================

class PersistentDrawing3D:
    """带持久化的Drawing 3D"""
    
    def __init__(self, data_dir='./data'):
        from enhanced_core import Drawing3D
        self.system = Drawing3D()
        self.persistence = DataPersistence(data_dir)
        
        # 加载历史数据
        self._load_data()
    
    def _load_data(self):
        """加载历史数据"""
        # 加载设备
        devices = self.persistence.load_devices()
        if devices:
            self.system.equipment.devices = devices
        
        # 加载成本记录
        records = self.persistence.load_cost_records()
        if records:
            self.system.cost.records = records
    
    def _save_data(self):
        """保存数据"""
        self.persistence.save_devices(self.system.equipment.devices)
        self.persistence.save_cost_records(self.system.cost.records)
    
    def add_cost(self, name, quantity):
        """添加成本并保存"""
        result = self.system.cost.add_material(name, quantity)
        self._save_data()
        return result
    
    def add_device(self, name, device_type):
        """添加设备并保存"""
        result = self.system.equipment.add_device(name, device_type)
        self._save_data()
        return result
    
    def generate_report(self, report_type):
        """生成报告并保存"""
        report = self.system.report.generate(report_type)
        self.persistence.save_report(report)
        return report


# ==================== 运行 ====================

if __name__ == "__main__":
    # 测试持久化
    p = DataPersistence()
    
    # 保存测试数据
    p.save_weather('北京', {'temp': 25, 'condition': 'sunny'})
    p.save_cost_records([{'item': '水泥', 'amount': 1000}])
    p.save_devices([{'name': '挖掘机', 'status': 'idle'}])
    
    # 统计
    print("数据统计:", p.get_stats())
    
    # 恢复测试
    weather = p.load_weather('北京')
    print("北京天气:", weather)
