# -*- coding: utf-8 -*-
"""
Drawing 3D - CLI Interface
命令行界面
"""

import os
import sys
from enhanced_core import Drawing3D, WeatherSystem, CostSystem, EquipmentSystem, ReportSystem, AIQAV2


class CLI:
    """命令行界面"""
    
    def __init__(self):
        self.system = Drawing3D()
        self.running = True
    
    def print_menu(self):
        """打印菜单"""
        print("\n" + "="*50)
        print("Drawing 3D - Road Engineering Management")
        print("="*50)
        print("1. 天气查询")
        print("2. 成本管理")
        print("3. 设备管理")
        print("4. 报告生成")
        print("5. AI问答")
        print("6. 系统状态")
        print("0. 退出")
        print("="*50)
    
    def do_weather(self):
        """天气查询"""
        print("\n--- 天气查询 ---")
        location = input("地点 (默认北京): ") or "北京"
        weather = self.system.weather.get_current(location)
        print(f"\n{weather['location']}: {weather['condition']}, {weather['temp']}°C")
        print(f"湿度: {weather['humidity']}%, 风速: {weather['wind']}km/h")
        print(f"施工建议: {self.system.weather.analyze_impact(weather)}")
    
    def do_cost(self):
        """成本管理"""
        print("\n--- 成本管理 ---")
        print("1. 添加材料成本")
        print("2. 添加人工成本")
        print("3. 查看成本汇总")
        
        choice = input("选择: ")
        
        if choice == '1':
            name = input("材料名称: ")
            qty = float(input("数量: "))
            self.system.cost.add_material(name, qty)
            print("已添加!")
        elif choice == '2':
            worker = input("工种: ")
            days = float(input("天数: "))
            self.system.cost.add_labor(worker, days)
            print("已添加!")
        elif choice == '3':
            summary = self.system.cost.get_summary()
            print(f"\n总成本: {summary['total']}元")
            for t, v in summary['by_type'].items():
                print(f"  {t}: {v}元")
    
    def do_equipment(self):
        """设备管理"""
        print("\n--- 设备管理 ---")
        print("1. 添加设备")
        print("2. 设备列表")
        print("3. 设备状态")
        
        choice = input("选择: ")
        
        if choice == '1':
            name = input("设备名称: ")
            device_type = input("设备类型: ")
            self.system.equipment.add_device(name, device_type)
            print("已添加!")
        elif choice == '2':
            for d in self.system.equipment.devices:
                print(f"  {d['id']}. {d['name']} ({d['type']}) - {d['status']}")
        elif choice == '3':
            status = self.system.equipment.get_status()
            print(f"运行中: {status['operating']}, 空闲: {status['idle']}, 维护: {status['maintenance']}")
    
    def do_report(self):
        """报告生成"""
        print("\n--- 报告生成 ---")
        print("1. 日报")
        print("2. 周报")
        print("3. 月报")
        
        choice = input("选择: ")
        types = {'1': 'daily', '2': 'weekly', '3': 'monthly'}
        
        if choice in types:
            report = self.system.report.generate(types[choice])
            print(f"\n报告: {report['title']}")
            print(f"章节: {', '.join(report['sections'])}")
            print(f"生成时间: {report['generate_time']}")
    
    def do_ai_qa(self):
        """AI问答"""
        print("\n--- AI问答 ---")
        question = input("请输入问题: ")
        answer = self.system.ai_qa.ask(question)
        print(f"\n回答: {answer}")
    
    def do_status(self):
        """系统状态"""
        print("\n--- 系统状态 ---")
        print(f"天气系统: {'✓' if self.system.weather else '✗'}")
        print(f"成本系统: {'✓' if self.system.cost else '✗'}")
        print(f"设备系统: {'✓' if self.system.equipment else '✗'}")
        print(f"报告系统: {'✓' if self.system.report else '✗'}")
        print(f"AI问答: {'✓' if self.system.ai_qa else '✗'}")
    
    def run(self):
        """运行"""
        print("\n欢迎使用 Drawing 3D!")
        
        while self.running:
            self.print_menu()
            choice = input("\n选择: ")
            
            if choice == '1':
                self.do_weather()
            elif choice == '2':
                self.do_cost()
            elif choice == '3':
                self.do_equipment()
            elif choice == '4':
                self.do_report()
            elif choice == '5':
                self.do_ai_qa()
            elif choice == '6':
                self.do_status()
            elif choice == '0':
                self.running = False
                print("\n再见!")
            else:
                print("无效选择")


if __name__ == "__main__":
    cli = CLI()
    cli.run()
