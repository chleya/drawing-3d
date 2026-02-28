"""
Drawing 3D - Complete System with All Features

Run: python drawing_3d/full_system.py
"""

import os

class RoadProject3D:
    """Complete 3D Road Project System"""
    
    def __init__(self, name="Road Project"):
        self.name = name
        self.road_points = []
        self.photos = []
        self.quality = []
        self.progress = []
        self.knowledge = {}
        self.drawings = []
    
    # === Spatial ===
    def add_road_point(self, mileage, x, y):
        self.road_points.append((mileage, x, y))
    
    def mileage_to_xy(self, mileage):
        for i in range(len(self.road_points) - 1):
            m1, x1, y1 = self.road_points[i]
            m2, x2, y2 = self.road_points[i+1]
            if m1 <= mileage <= m2:
                t = (mileage - m1) / (m2 - m1)
                return x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
        return None
    
    # === Knowledge ===
    def add_knowledge(self, key, value):
        self.knowledge[key] = value
    
    def query_knowledge(self, keyword):
        kw = keyword.lower()
        results = []
        for k, v in self.knowledge.items():
            if kw in k.lower():
                results.append(f"{k} = {v}")
        return results if results else None
    
    # === Photos ===
    def add_photo(self, mileage, filename, description=""):
        coord = self.mileage_to_xy(mileage)
        self.photos.append({
            'mileage': mileage,
            'file': filename,
            'description': description,
            'coord': coord
        })
    
    # === Quality ===
    def add_quality(self, mileage, item, result, status="ok"):
        coord = self.mileage_to_xy(mileage)
        self.quality.append({
            'mileage': mileage,
            'item': item,
            'result': result,
            'status': status,
            'coord': coord
        })
    
    # === Progress ===
    def add_progress(self, start_km, end_km, status, percent):
        self.progress.append({
            'start': start_km,
            'end': end_km,
            'status': status,
            'percent': percent
        })
    
    def get_total_progress(self):
        if not self.progress:
            return 0
        return sum(p['percent'] for p in self.progress) / len(self.progress)
    
    # === Render ===
    def render(self):
        print("\n" + "="*60)
        print(f"ROAD PROJECT: {self.name}")
        print("="*60)
        
        # Progress
        total = self.get_total_progress()
        bar_len = 40
        filled = int(bar_len * total / 100)
        bar = "#" * filled + "." * (bar_len - filled)
        
        print(f"\n[Progress] {total:.0f}%")
        print(f"|{bar}|")
        
        # Sections
        print("\n[Sections]")
        for p in self.progress:
            status_map = {'completed': '[DONE]', 'in_progress': '[WORK]', 'not_started': '[WAIT]'}
            s = status_map.get(p['status'], '[???]')
            print(f"  K{p['start']:.0f}-K{p['end']:.0f}: {s} {p['percent']}%")
        
        # Quality
        print("\n[Quality Records]")
        for q in self.quality:
            icon = "[OK]" if q['status'] == 'ok' else "[!!]"
            print(f"  K{q['mileage']:.1f}: {icon} {q['item']} = {q['result']}")
        
        # Photos
        print("\n[Photos]")
        for p in self.photos:
            print(f"  K{p['mileage']:.1f}: {p['file']} - {p['description']}")
        
        # Knowledge
        print("\n[Knowledge Base]")
        print(f"  Total: {len(self.knowledge)} entries")
        
        # Demo queries
        print("\n[Demo Queries]")
        queries = ["thickness", "material", "compaction", "asphalt"]
        for q in queries:
            results = self.query_knowledge(q)
            if results:
                print(f"  '{q}': {len(results)} found")
    
    def interactive_menu(self):
        """Interactive menu"""
        print("\n" + "="*40)
        print("MENU")
        print("="*40)
        print("1. Query Knowledge")
        print("2. Show Progress")
        print("3. Show Photos")
        print("4. Show Quality")
        print("5. Full Render")
        print("6. Exit")
        
        while True:
            choice = input("\n> ").strip()
            
            if choice == '1':
                q = input("Search: ").strip()
                results = self.query_knowledge(q)
                if results:
                    for r in results:
                        print(f"  {r}")
                else:
                    print("  Not found")
            
            elif choice == '2':
                print(f"  Progress: {self.get_total_progress():.0f}%")
            
            elif choice == '3':
                for p in self.photos:
                    print(f"  K{p['mileage']}: {p['file']}")
            
            elif choice == '4':
                for q in self.quality:
                    print(f"  K{q['mileage']}: {q['item']} = {q['result']}")
            
            elif choice == '5':
                self.render()
            
            elif choice == '6':
                break


def demo():
    """Demo with sample data"""
    project = RoadProject3D("351 Provincial Road Project")
    
    # Road points
    for i in range(8):
        project.add_road_point(i, i * 100, i * 30)
    
    # Knowledge
    project.add_knowledge("K5+800_surface_thickness", "40mm AC-13")
    project.add_knowledge("K5+800_base_thickness", "180mm CSM")
    project.add_knowledge("K5+800_subbase_thickness", "300mm")
    project.add_knowledge("K5+800_material", "AC-13 Asphalt Concrete")
    project.add_knowledge("K5+800_compaction", "98%")
    project.add_knowledge("K6+000_bridge_material", "C50 Concrete")
    project.add_knowledge("K6+000_rebar", "HRB400 25mm")
    project.add_knowledge("K6+500_culvert_material", "C30 Concrete")
    
    # Photos
    project.add_photo(1.5, "IMG_001.jpg", "Water stable layer")
    project.add_photo(2.3, "IMG_002.jpg", "Asphalt paving")
    project.add_photo(3.8, "IMG_003.jpg", "Compaction test")
    project.add_photo(5.2, "IMG_004.jpg", "Bridge deck")
    
    # Quality
    project.add_quality(1.5, "compaction", "98%", "ok")
    project.add_quality(2.3, "temperature", "145C", "ok")
    project.add_quality(3.8, "compaction", "96%", "warning")
    project.add_quality(5.2, "strength", "C50", "ok")
    
    # Progress
    project.add_progress(0, 1, "completed", 100)
    project.add_progress(1, 2, "completed", 100)
    project.add_progress(2, 3, "completed", 100)
    project.add_progress(3, 4, "in_progress", 70)
    project.add_progress(4, 5, "in_progress", 40)
    project.add_progress(5, 6, "not_started", 0)
    project.add_progress(6, 7, "not_started", 0)
    
    # Render
    project.render()
    
    print("\n" + "="*60)
    print("Full System Demo Complete!")
    print("="*60)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--menu':
        project = RoadProject3D()
        # Add some demo data
        for i in range(5):
            project.add_road_point(i, i * 100, i * 30)
        project.add_progress(0, 1, "completed", 100)
        project.add_progress(1, 2, "in_progress", 50)
        project.add_knowledge("test", "value")
        project.interactive_menu()
    else:
        demo()
