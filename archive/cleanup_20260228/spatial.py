"""
Drawing 3D - Phase 1: Spatial Engine

Run: python drawing_3d/spatial.py
"""

import math

class Road:
    """Road coordinate system"""
    
    def __init__(self):
        self.points = []
    
    def add_point(self, mileage, x, y):
        self.points.append((mileage, x, y))
    
    def mileage_to_xy(self, mileage):
        """Convert mileage to XY coordinate"""
        for i in range(len(self.points) - 1):
            m1, x1, y1 = self.points[i]
            m2, x2, y2 = self.points[i+1]
            if m1 <= mileage <= m2:
                t = (mileage - m1) / (m2 - m1)
                x = x1 + (x2 - x1) * t
                y = y1 + (y2 - y1) * t
                return x, y
        return None
    
    def xy_to_mileage(self, x, y):
        """Convert XY to mileage (simplified)"""
        min_dist = float('inf')
        best_m = None
        for m, px, py in self.points:
            d = math.sqrt((x - px)**2 + (y - py)**2)
            if d < min_dist:
                min_dist = d
                best_m = m
        return best_m, min_dist


class SpatialDB:
    """Spatial database"""
    
    def __init__(self, road):
        self.road = road
        self.photos = []
        self.quality = []
    
    def add_photo(self, mileage, filename, description=""):
        coord = self.road.mileage_to_xy(mileage)
        self.photos.append({
            'mileage': mileage,
            'file': filename,
            'desc': description,
            'coord': coord
        })
    
    def add_quality(self, mileage, item, result):
        coord = self.road.mileage_to_xy(mileage)
        self.quality.append({
            'mileage': mileage,
            'item': item,
            'result': result,
            'coord': coord
        })
    
    def query(self, start_km, end_km):
        """Query by mileage range"""
        results = {'photos': [], 'quality': []}
        for p in self.photos:
            if start_km <= p['mileage'] <= end_km:
                results['photos'].append(p)
        for q in self.quality:
            if start_km <= q['mileage'] <= end_km:
                results['quality'].append(q)
        return results


# Demo
print("="*50)
print("Drawing 3D - Phase 1: Spatial Engine")
print("="*50)

# Create road
road = Road()
road.add_point(0, 0, 0)
road.add_point(1, 100, 50)
road.add_point(2, 250, 80)
road.add_point(3, 400, 60)
road.add_point(4, 550, 100)
road.add_point(5, 700, 150)

print("\n[1] Road centerline: 5 control points")

# Test mileage to XY
print("\n[2] Mileage -> XY:")
for m in [0.5, 1.5, 2.5, 3.5, 4.5]:
    c = road.mileage_to_xy(m)
    if c:
        print(f"    K{m} -> ({round(c[0],1)}, {round(c[1],1)})")

# Spatial database
print("\n[3] Spatial Database:")
db = SpatialDB(road)

db.add_photo(1.5, "photo1.jpg", "water stable layer")
db.add_photo(2.3, "photo2.jpg", "asphalt paving")
db.add_photo(3.8, "photo3.jpg", "compaction")

db.add_quality(1.5, "compaction", "98%")
db.add_quality(2.3, "temperature", "145C")
db.add_quality(3.8, "compaction", "96%")

print(f"    Photos: {len(db.photos)}")
print(f"    Quality: {len(db.quality)}")

# Query
print("\n[4] Query K1.0-K3.0:")
results = db.query(1.0, 3.0)
print(f"    Photos: {len(results['photos'])}")
print(f"    Quality: {len(results['quality'])}")

for p in results['photos']:
    print(f"      - {p['desc']} (K{p['mileage']})")

for q in results['quality']:
    print(f"      - {q['item']}: {q['result']} (K{q['mileage']})")

print("\n" + "="*50)
print("Phase 1 Complete!")
print("="*50)
