"""
Drawing 3D - Phase 2: Simple Working Version

Run: python drawing_3d/draw_qa.py
"""

class DrawQA:
    """Drawing QA system"""
    
    def __init__(self):
        self.db = {}
    
    def add(self, key, value):
        """Add drawing info"""
        self.db[key] = value
    
    def query(self, keyword):
        """Query by keyword"""
        kw = keyword.lower()
        results = []
        for k, v in self.db.items():
            if kw in k.lower():
                results.append(f"{k} = {v}")
        return results if results else None


# Demo
print("="*50)
print("Drawing 3D - Phase 2: Drawing QA")
print("="*50)

qa = DrawQA()

# Add road drawings
qa.add("road_K5+800_thickness_40", "40 mm (surface)")
qa.add("road_K5+800_thickness_180", "180 mm (base)")
qa.add("road_K5+800_thickness_300", "300 mm (subbase)")
qa.add("road_K5+800_material_asphalt", "AC-13 asphalt concrete")
qa.add("road_K5+800_material_stone", "cement stabilized macadam")
qa.add("road_K5+800_compaction", "98%")

# Add bridge drawings
qa.add("bridge_K6+000_diameter", "25 mm rebar")
qa.add("bridge_K6+000_spacing", "150 mm")
qa.add("bridge_K6+000_concrete", "C50")
qa.add("bridge_K6+000_rebar", "HRB400")
qa.add("bridge_K6+000_cover", "30 mm")

# Add culvert
qa.add("culvert_K6+500_wall", "500 mm")
qa.add("culvert_K6+500_diameter", "2000 mm")
qa.add("culvert_K6+500_concrete", "C30")

print(f"\n[1] Knowledge base: {len(qa.db)} entries")

# QA Tests
print("\n[2] QA Test:")
questions = [
    "road",
    "thickness", 
    "asphalt",
    "bridge",
    "concrete",
    "K6+000",
    "compaction",
    "unknown"
]

for q in questions:
    results = qa.query(q)
    print(f"\nQ: {q}")
    if results:
        for r in results:
            print(f"  {r}")
    else:
        print("  Not found")

print("\n" + "="*50)
print("Phase 2 Complete!")
print("="*50)
