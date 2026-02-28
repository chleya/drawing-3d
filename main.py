# -*- coding: utf-8 -*-
"""
Drawing 3D - Complete System
All Phases Integrated with Weather, Cost, Equipment, Report, AI Q&A

Run: python drawing_3d/main.py
"""

import math
from weather import WeatherSystem
from cost import CostSystem
from equipment import EquipmentSystem, EquipmentStatus
from report import ReportSystem
from ai_qa_v2 import AIQAV2
from persistence import DataManager
from planning import PlanningAssistant
from quality_detection import QualityDetector
from safety import SafetyManager


class Road3D:
    """Complete 3D Road System"""
    
    def __init__(self):
        self.name = "Road Project"
        self.points = []  # Control points
        self.photos = []
        self.quality = []
        self.progress = []
        self.knowledge = {}
        
        # Integrated modules
        self.weather = WeatherSystem()
        self.cost = CostSystem()
        self.equipment = EquipmentSystem()
        self.report = ReportSystem()
        self.qa = AIQAV2(self)
        self.planner = PlanningAssistant(self)
        self.quality_detector = QualityDetector(self)
        self.safety = SafetyManager(self)
    
    # === Phase 1: Spatial ===
    def add_point(self, mileage, x, y):
        self.points.append((mileage, x, y))
    
    def mileage_to_xy(self, mileage):
        for i in range(len(self.points) - 1):
            m1, x1, y1 = self.points[i]
            m2, x2, y2 = self.points[i+1]
            if m1 <= mileage <= m2:
                t = (mileage - m1) / (m2 - m1)
                x = x1 + (x2 - x1) * t
                y = y1 + (y2 - y1) * t
                return x, y
        return None
    
    # === Phase 2: Knowledge ===
    def add_knowledge(self, key, value):
        self.knowledge[key] = value
    
    def query(self, keyword):
        kw = keyword.lower()
        results = []
        for k, v in self.knowledge.items():
            if kw in k.lower():
                results.append(f"{k} = {v}")
        return results if results else None
    
    # === Phase 3: Site ===
    def add_photo(self, mileage, filename, description=""):
        coord = self.mileage_to_xy(mileage)
        self.photos.append({
            'mileage': mileage,
            'file': filename,
            'description': description,
            'coord': coord
        })
    
    def add_quality(self, mileage, item, result, status="ok"):
        coord = self.mileage_to_xy(mileage)
        self.quality.append({
            'mileage': mileage,
            'item': item,
            'result': result,
            'status': status,
            'coord': coord
        })
    
    def add_progress(self, start_km, end_km, status, percent):
        self.progress.append({
            'start': start_km,
            'end': end_km,
            'status': status,
            'percent': percent
        })
    
    def get_progress(self):
        if not self.progress:
            return 0
        return sum(p['percent'] for p in self.progress) / len(self.progress)
    
    # === Weather Module ===
    def get_weather(self, date=None):
        """Get weather data"""
        return self.weather.get_weather(date)
    
    def get_weather_impact(self, weather=None):
        """Get weather impact analysis"""
        if weather is None:
            weather = self.get_weather()
        return self.weather.analyze_impact(weather)
    
    def can_construct_today(self):
        """Check if construction is possible today"""
        w = self.get_weather()
        return self.weather.can_construct(w)
    
    def get_weather_forecast(self, days=7):
        """Get weather forecast"""
        return self.weather.forecast(days)
    
    # === Cost Module ===
    def add_material_cost(self, name, quantity, unit='ton', date=None):
        """Add material cost"""
        return self.cost.add_material(name, quantity, unit, date)
    
    def add_labor_cost(self, role, days, date=None):
        """Add labor cost"""
        return self.cost.add_labor(role, days, date)
    
    def add_equipment_cost(self, name, days, date=None):
        """Add equipment cost"""
        return self.cost.add_equipment(name, days, date)
    
    def get_cost_summary(self):
        """Get cost summary"""
        return self.cost.get_total_cost()
    
    # === Equipment Module ===
    def add_device(self, name, model, category, purchase_date=None):
        """Add device"""
        return self.equipment.add_equipment(name, model, category, purchase_date)
    
    def update_device_status(self, device_id, status):
        """Update device status"""
        status_map = {
            'RUNNING': EquipmentStatus.RUNNING,
            'IDLE': EquipmentStatus.IDLE,
            'MAINTENANCE': EquipmentStatus.MAINTENANCE,
            'BROKEN': EquipmentStatus.BROKEN
        }
        return self.equipment.update_status(device_id, status_map.get(status, EquipmentStatus.IDLE))
    
    def schedule_device(self, device_id, location, start_date, end_date, operator):
        """Schedule device"""
        return self.equipment.schedule(device_id, location, start_date, end_date, operator)
    
    def get_device_utilization(self):
        """Get device utilization"""
        return self.equipment.get_utilization()
    
    # === Report Module ===
    def add_daily_report(self, date, mileage, work_type, workers, equipment, weather, notes=""):
        """Add daily report"""
        return self.report.add_daily_record(date, mileage, work_type, workers, equipment, weather, notes)
    
    def add_quality_record(self, date, mileage, item, result, status, inspector=""):
        """Add quality record"""
        return self.report.add_quality_record(date, mileage, item, result, status, inspector)
    
    def add_progress_record(self, mileage_start, mileage_end, status, percent, date=None):
        """Add progress record"""
        return self.report.add_progress_record(mileage_start, mileage_end, status, percent, date)
    
    def add_issue(self, date, description, severity, resolution=""):
        """Add issue"""
        return self.report.add_issue(date, description, severity, resolution)
    
    def generate_full_report(self):
        """Generate full report"""
        lines = []
        lines.append("="*50)
        lines.append("Full Project Report")
        lines.append("="*50)
        
        # Progress
        progress = self.get_progress()
        lines.append(f"\n[Progress] {progress:.1f}%")
        
        # Weather
        w = self.get_weather()
        can, msg = self.can_construct_today()
        lines.append(f"\n[Weather] {w['weather']}, {w['temperature']}C - {'OK' if can else 'NO'}")
        
        # Cost
        cost = self.get_cost_summary()
        lines.append(f"\n[Cost] Total: {cost['total']:,.2f}")
        lines.append(f"  Material: {cost['material']:,.2f}")
        lines.append(f"  Labor: {cost['labor']:,.2f}")
        lines.append(f"  Equipment: {cost['equipment']:,.2f}")
        
        # Equipment
        util = self.get_device_utilization()
        lines.append(f"\n[Equipment] Total: {util['total']}, Running: {util['running']}")
        lines.append(f"  Utilization: {util['utilization_rate']:.1f}%")
        
        return "\n".join(lines)
    
    # === AI Q&A Module ===
    def ask(self, question):
        """Ask AI assistant"""
        return self.qa.understand(question)
    
    # === Planning Module ===
    def generate_plan(self, target_km, method='asphalt'):
        """Generate construction plan"""
        return self.planner.generate_plan(target_km, method)
    
    # === Quality Module ===
    def check_quality(self, item, value):
        """Check quality against standard"""
        return self.quality_detector.check_quality(item, value)
    
    def quality_report(self):
        """Generate quality report"""
        return self.quality_detector.quality_report()
    
    # === Safety Module ===
    def safety_report(self):
        """Generate safety report"""
        return self.safety.safety_report()
    
    # === Phase 4: Visual ===
    def render(self):
        """Render 3D ASCII"""
        if not self.points:
            print("No points data")
            return
        
        # Get mileage range
        max_mileage = max(p[0] for p in self.points)
        
        # Simple ASCII rendering
        print(f"\nRoad Project: {self.name}")
        print(f"Total Length: {max_mileage} km")
        print(f"Control Points: {len(self.points)}")
        
        # Progress bar
        progress = self.get_progress()
        bar_length = 30
        filled = int(bar_length * progress / 100)
        bar = "=" * filled + "-" * (bar_length - filled)
        print(f"\nProgress: [{bar}] {progress:.1f}%")
        
        # Quality summary
        print(f"\nQuality Records: {len(self.quality)}")
        for q in self.quality[:5]:
            print(f"  K{q['mileage']}: {q['item']} = {q['result']} ({q['status']})")
        
        # Photo summary
        print(f"\nPhotos: {len(self.photos)}")
    
    # === Menu ===
    def menu(self):
        """Interactive menu"""
        while True:
            print("\n" + "="*40)
            print("Road 3D System Menu")
            print("="*40)
            print("1. Add Point")
            print("2. Add Knowledge")
            print("3. Query")
            print("4. Add Photo")
            print("5. Add Quality")
            print("6. Add Progress")
            print("7. Weather")
            print("8. Cost")
            print("9. Equipment")
            print("10. Report")
            print("11. Render")
            print("12. AI Assistant")
            print("13. Save Project")
            print("14. Load Project")
            print("0. Exit")
            
            choice = input("\nChoice: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                m = float(input("Mileage (km): "))
                x = float(input("X: "))
                y = float(input("Y: "))
                self.add_point(m, x, y)
                print("Point added!")
            elif choice == "2":
                key = input("Key: ")
                value = input("Value: ")
                self.add_knowledge(key, value)
                print("Knowledge added!")
            elif choice == "3":
                kw = input("Keyword: ")
                result = self.query(kw)
                if result:
                    for r in result:
                        print(r)
                else:
                    print("No results")
            elif choice == "7":
                w = self.get_weather()
                print(f"Weather: {w['weather']}, {w['temperature']}C")
                can, msg = self.can_construct_today()
                print(f"Construction: {'OK' if can else 'NO'} - {msg}")
            elif choice == "8":
                cost = self.get_cost_summary()
                print(f"Total Cost: {cost['total']:,.2f}")
            elif choice == "9":
                util = self.get_device_utilization()
                print(f"Equipment: {util['total']} total, {util['running']} running")
            elif choice == "10":
                print(self.generate_full_report())
            elif choice == "11":
                self.render()
            elif choice == "12":
                print("\n[AI Assistant] - Type 'exit' to quit")
                while True:
                    q = input("\nYou: ").strip()
                    if not q:
                        continue
                    if q.lower() in ['exit', 'quit', 'q']:
                        break
                    print(f"\nAI: {self.ask(q)}")
            elif choice == "13":
                filename = input("Filename (default: project_data.json): ").strip() or "project_data.json"
                DataManager.save(self, filename)
                print("Project saved!")
            elif choice == "14":
                filename = input("Filename (default: project_data.json): ").strip() or "project_data.json"
                DataManager.load(self, filename)
                print("Project loaded!")


def demo():
    """Demo function"""
    road = Road3D()
    
    # Add control points
    road.add_point(0, 0, 0)
    road.add_point(1, 100, 50)
    road.add_point(2, 200, 100)
    road.add_point(3, 300, 150)
    road.add_point(4, 400, 200)
    road.add_point(5, 500, 250)
    road.add_point(6, 600, 300)
    road.add_point(7, 700, 350)
    
    # Add knowledge
    road.add_knowledge("asphalt_temp", "150-170C")
    road.add_knowledge("compaction", "95-98%")
    road.add_knowledge("layer_thickness", "50-80mm")
    
    # Add photos
    road.add_photo(0.5, "photo_001.jpg", "Base layer")
    road.add_photo(1.5, "photo_002.jpg", "Subbase")
    road.add_photo(2.5, "photo_003.jpg", "沥青面层")
    
    # Add quality
    road.add_quality(0.5, "压实度", "96%", "ok")
    road.add_quality(1.5, "平整度", "3.2mm", "ok")
    road.add_quality(2.5, "厚度", "65mm", "ok")
    
    # Add progress
    road.add_progress(0, 1, "completed", 100)
    road.add_progress(1, 2, "completed", 100)
    road.add_progress(2, 3, "completed", 100)
    road.add_progress(3, 4, "in_progress", 70)
    road.add_progress(4, 5, "in_progress", 40)
    road.add_progress(5, 6, "not_started", 0)
    road.add_progress(6, 7, "not_started", 0)
    
    # === Test new modules ===
    # Weather
    w = road.get_weather()
    print("\n[Weather System]")
    print(f"  Current: {w['weather']}, {w['temperature']}C")
    can, msg = road.can_construct_today()
    print(f"  Construction: {'OK' if can else 'NO'}")
    
    # Cost
    road.add_material_cost('asphalt', 500)
    road.add_material_cost('cement', 200)
    road.add_material_cost('gravel', 3000)
    road.add_labor_cost('tech', 30)
    road.add_labor_cost('worker', 50)
    road.add_labor_cost('driver', 20)
    road.add_equipment_cost('roller', 15)
    road.add_equipment_cost('paver', 10)
    print("\n[Cost System]")
    cost = road.get_cost_summary()
    print(f"  Total: {cost['total']:,.2f}")
    print(f"  Material: {cost['material']:,.2f} | Labor: {cost['labor']:,.2f} | Equipment: {cost['equipment']:,.2f}")
    
    # Equipment
    road.add_device('roller1', 'CAT', 'roller')
    road.add_device('roller2', 'CAT', 'roller')
    road.add_device('paver1', 'VOGELE', 'paver')
    road.add_device('excavator1', 'CAT', 'excavator')
    road.add_device('loader1', 'LIEBHER', 'loader')
    road.update_device_status(1, 'RUNNING')
    road.update_device_status(3, 'RUNNING')
    road.update_device_status(4, 'MAINTENANCE')
    road.schedule_device(1, 'K1+500', '2026-02-28', '2026-03-05', 'Zhang San')
    road.schedule_device(2, 'K2+000', '2026-03-01', '2026-03-10', 'Li Si')
    print("\n[Equipment System]")
    util = road.get_device_utilization()
    print(f"  Total: {util['total']}, Running: {util['running']}, Idle: {util['idle']}")
    print(f"  Utilization: {util['utilization_rate']:.1f}%")
    
    # Report
    road.add_daily_report('2026-02-28', 1.5, 'asphalt', 15, 'roller2', 'sunny')
    road.add_daily_report('2026-02-27', 1.2, 'water stable', 12, 'paver1', 'cloudy')
    road.add_quality_record('2026-02-28', 1.5, 'compaction', '98%', 'ok', 'Zhang San')
    road.add_quality_record('2026-02-27', 1.2, 'temperature', '145C', 'ok', 'Li Si')
    road.add_progress_record(0, 1, 'completed', 100)
    road.add_progress_record(1, 2, 'in_progress', 70)
    road.add_issue('2026-02-28', 'roller故障', 'medium', '已修复')
    print("\n[Report System]")
    print("  Daily: 2, Quality: 2, Issues: 1")
    
    # Full report
    print(road.generate_full_report())
    
    # Render
    road.render()


if __name__ == "__main__":
    print("Run demo? (y/n): ", end="")
    if input().strip().lower() == "y":
        demo()
    else:
        road = Road3D()
        road.menu()
