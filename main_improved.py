# -*- coding: utf-8 -*-
"""
Drawing 3D - Main Entry Point
主入口 - 改进版
"""

import os
import sys
import json
from datetime import datetime

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ==================== 配置 ====================

class Config:
    """配置管理"""
    
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = self._load()
    
    def _load(self):
        default = {
            'debug': False,
            'log_level': 'INFO',
            'data_dir': './data',
            'features': {
                'weather': True,
                'cost': True,
                'equipment': True,
                'report': True,
                'ai_qa': True,
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return {**default, **json.load(f)}
            except:
                return default
        return default
    
    def get(self, key, default=None):
        keys = key.split('.')
        value = self.config
        for k in keys:
            value = value.get(k, default)
        return value


# ==================== 子系统 ====================

class WeatherSystem:
    """天气系统"""
    
    def __init__(self, config=None):
        self.config = config
    
    def get_current(self, location):
        """获取天气"""
        return {
            'location': location,
            'temp': 25,
            'condition': 'sunny',
            'humidity': 60
        }
    
    def get_forecast(self, location, days=7):
        """获取预报"""
        return [self.get_current(location) for _ in range(days)]


class CostSystem:
    """成本系统"""
    
    def __init__(self, config=None):
        self.config = config
        self.records = []
    
    def add_record(self, item, amount):
        """添加记录"""
        self.records.append({
            'item': item,
            'amount': amount,
            'timestamp': datetime.now().isoformat()
        })
        return True
    
    def get_total(self):
        """获取总额"""
        return sum(r['amount'] for r in self.records)


class EquipmentSystem:
    """设备系统"""
    
    def __init__(self, config=None):
        self.config = config
        self.devices = []
    
    def add_device(self, name, status='idle'):
        """添加设备"""
        self.devices.append({
            'name': name,
            'status': status,
            'timestamp': datetime.now().isoformat()
        })
        return True
    
    def get_devices(self):
        """获取设备列表"""
        return self.devices


class ReportSystem:
    """报告系统"""
    
    def __init__(self, config=None):
        self.config = config
    
    def generate(self, report_type='daily'):
        """生成报告"""
        return {
            'type': report_type,
            'content': f'{report_type} report generated',
            'timestamp': datetime.now().isoformat()
        }


class AIQAV2:
    """AI问答"""
    
    def __init__(self, config=None):
        self.config = config
    
    def ask(self, question):
        """问答"""
        # 简单模拟
        responses = {
            '进度': '项目进度正常',
            '成本': '成本在预算范围内',
            '天气': '今天天气晴朗',
        }
        
        for key, response in responses.items():
            if key in question:
                return response
        
        return '请详细描述您的问题'


# ==================== 主系统 ====================

class Drawing3D:
    """Drawing 3D 主系统"""
    
    def __init__(self):
        # 加载配置
        self.config = Config()
        
        # 初始化子系统
        self.weather = None
        self.cost = None
        self.equipment = None
        self.report = None
        self.ai_qa = None
        
        self._init_systems()
    
    def _init_systems(self):
        """初始化子系统"""
        features = self.config.get('features', {})
        
        if features.get('weather'):
            try:
                self.weather = WeatherSystem(self.config)
            except Exception as e:
                print(f"Weather init error: {e}")
        
        if features.get('cost'):
            try:
                self.cost = CostSystem(self.config)
            except Exception as e:
                print(f"Cost init error: {e}")
        
        if features.get('equipment'):
            try:
                self.equipment = EquipmentSystem(self.config)
            except Exception as e:
                print(f"Equipment init error: {e}")
        
        if features.get('report'):
            try:
                self.report = ReportSystem(self.config)
            except Exception as e:
                print(f"Report init error: {e}")
        
        if features.get('ai_qa'):
            try:
                self.ai_qa = AIQAV2(self.config)
            except Exception as e:
                print(f"AI Q&A init error: {e}")
    
    def run(self):
        """运行"""
        print("\n" + "="*60)
        print("Drawing 3D - Road Engineering Management")
        print("="*60)
        
        # 测试子系统
        if self.weather:
            print(f"\n[Weather] {self.weather.get_current('Beijing')}")
        
        if self.cost:
            self.cost.add_record('水泥', 10000)
            self.cost.add_record('钢材', 20000)
            print(f"\n[Cost] Total: {self.cost.get_total()}")
        
        if self.equipment:
            self.equipment.add_device('挖掘机')
            self.equipment.add_device('起重机')
            print(f"\n[Equipment] {len(self.equipment.get_devices())} devices")
        
        if self.report:
            print(f"\n[Report] {self.report.generate()}")
        
        if self.ai_qa:
            print(f"\n[AI Q&A] 进度如何？→ {self.ai_qa.ask('项目进度如何')}")
        
        print("\n" + "="*60)
        print("System Ready!")
        print("="*60 + "\n")


# ==================== 主程序 ====================

if __name__ == "__main__":
    system = Drawing3D()
    system.run()
