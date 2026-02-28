"""
Drawing 3D - Phase 4: 3D Visualization

Features:
- 3D road visualization
- Progress visualization
- Quality markers

Run: python drawing_3d/visual.py
"""

# Simple ASCII 3D visualization
class Visual3D:
    """Simple 3D visualization"""
    
    def __init__(self, road_length=10):
        self.length = road_length
        self.data = {}  # mileage -> data
    
    def add_data(self, mileage, data):
        """Add data at mileage"""
        self.data[mileage] = data
    
    def render_progress(self):
        """Render progress bar"""
        print("\n=== 3D Progress View ===")
        
        segments = 20
        segment_size = self.length / segments
        
        for i in range(segments):
            start = i * segment_size
            end = (i + 1) * segment_size
            
            # Find data for this segment
            status = "not_started"
            for m, d in self.data.items():
                if start <= m < end:
                    status = d.get('status', 'unknown')
                    break
            
            # Render
            if status == "completed":
                char = "#"
            elif status == "in_progress":
                char = "o"
            else:
                char = "."
            
            print(char, end="")
        
        print()
        print("  # = Done    o = Working    . = Not started")
    
    def render_quality(self):
        """Render quality markers"""
        print("\n=== Quality Map ===")
        
        for m, d in self.data.items():
            if 'quality' in d:
                status = d['quality']
                if status == 'ok':
                    mark = "[OK]"
                elif status == 'warning':
                    mark = "[!!]"
                else:
                    mark = "[??]"
                
                print(f"  K{m:.1f}: {mark} {d.get('item', '')}")


class ThreeView:
    """Three view (front/side/top)"""
    
    def __init__(self):
        pass
    
    def top_view(self, road_length=5):
        """Top view (plan)"""
        print("\n=== Top View (Plan) ===")
        
        for y in range(5):
            line = ""
            for x in range(int(road_length * 10)):
                # Road center
                if 15 <= y <= 25:
                    line += "-"
                # Road edges
                elif y == 14 or y == 26:
                    line += "="
                else:
                    line += " "
            print(line)
        
        print("  |----|----|----|----|----|")
        print("  K0   K1   K2   K3   K4   K5")
    
    def side_view(self, road_length=5):
        """Side view (profile)"""
        print("\n=== Side View (Profile) ===")
        
        layers = ["Surface", "Base", "Subbase", "Subgrade"]
        
        for layer in layers:
            if layer == "Surface":
                print("  " + "=" * int(road_length * 8))
            elif layer == "Base":
                print("  " + "#" * int(road_length * 8))
            elif layer == "Subbase":
                print("  " + "+" * int(road_length * 8))
            else:
                print("  " + "." * int(road_length * 8))
        
        print("  |----|----|----|----|----|")
        print("  K0   K1   K2   K3   K4   K5")


# Demo
print("="*50)
print("Drawing 3D - Phase 4: 3D Visualization")
print("="*50)

# Visual3D
print("\n[1] Progress Visualization:")
v3d = Visual3D(road_length=5)

v3d.add_data(0.5, {'status': 'completed'})
v3d.add_data(1.5, {'status': 'completed'})
v3d.add_data(2.5, {'status': 'in_progress'})
v3d.add_data(3.5, {'status': 'in_progress'})
v3d.add_data(4.5, {'status': 'not_started'})

v3d.render_progress()

# Quality markers
v3d.add_data(1.5, {'quality': 'ok', 'item': 'compaction 98%'})
v3d.add_data(2.5, {'quality': 'ok', 'item': 'temp 145C'})
v3d.add_data(3.5, {'quality': 'warning', 'item': 'compaction 96%'})

v3d.render_quality()

# Three views
print("\n[2] Three Views:")
tv = ThreeView()
tv.top_view(5)
tv.side_view(5)

# Combined view
print("\n[3] Combined 3D View:")
print("""
       Surface  ===================
       Base     #################
       Subbase  +++++++++++++++++
       Subgrade .................
       
       |----|----|----|----|----|
       K0   K1   K2   K3   K4   K5
       
       Legend:
       = Surface layer (completed)
       # Base layer (completed)
       + Subbase (in progress)
       . Subgrade (not started)
""")

print("="*50)
print("Phase 4 Complete!")
print("="*50)
