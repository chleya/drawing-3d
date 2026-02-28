"""
Drawing 3D - Phase 3: Photo Association + Site Management

Features:
- GPS photo auto-archive
- Mileage-based photo query
- Quality record management

Run: python drawing_3d/site.py
"""

class PhotoManager:
    """Photo management with GPS + mileage"""
    
    def __init__(self, road):
        self.road = road
        self.photos = []
    
    def add_photo(self, filename, gps_lat=None, gps_lon=None, description=""):
        """Add photo with optional GPS"""
        mileage = None
        
        # If GPS available, convert to mileage
        if gps_lat and gps_lon:
            mileage, dist = self.road.xy_to_mileage(gps_lon, gps_lat)
        
        self.photos.append({
            'file': filename,
            'gps': (gps_lat, gps_lon) if gps_lat else None,
            'mileage': mileage,
            'description': description
        })
    
    def query_by_mileage(self, start_km, end_km):
        """Query photos by mileage range"""
        results = []
        for p in self.photos:
            if p['mileage'] and start_km <= p['mileage'] <= end_km:
                results.append(p)
        return results
    
    def query_by_gps(self, lat, lon, radius_km=1):
        """Query photos by GPS location"""
        results = []
        for p in self.photos:
            if p['gps']:
                # Simple distance check
                d_lat = abs(p['gps'][0] - lat)
                d_lon = abs(p['gps'][1] - lon)
                if d_lat < 0.01 and d_lon < 0.01:  # ~1km
                    results.append(p)
        return results


class QualityManager:
    """Quality check records"""
    
    def __init__(self, road):
        self.road = road
        self.records = []
    
    def add_record(self, mileage, item, result, status="ok", notes=""):
        """Add quality record"""
        self.records.append({
            'mileage': mileage,
            'item': item,
            'result': result,
            'status': status,  # ok/warning/error
            'notes': notes
        })
    
    def query_by_mileage(self, start_km, end_km):
        """Query by mileage"""
        results = []
        for r in self.records:
            if start_km <= r['mileage'] <= end_km:
                results.append(r)
        return results
    
    def get_warnings(self):
        """Get all warning records"""
        return [r for r in self.records if r['status'] != "ok"]


class ProgressManager:
    """Construction progress tracking"""
    
    def __init__(self, road):
        self.road = road
        self.sections = []  # [(start_km, end_km, status, percent)]
    
    def add_section(self, start_km, end_km, status, percent):
        """Add progress section"""
        self.sections.append({
            'start': start_km,
            'end': end_km,
            'status': status,  # not_started/in_progress/completed
            'percent': percent
        })
    
    def get_overall_progress(self):
        """Calculate overall progress"""
        if not self.sections:
            return 0
        return sum(s['percent'] for s in self.sections) / len(self.sections)
    
    def query_by_status(self, status):
        """Query sections by status"""
        return [s for s in self.sections if s['status'] == status]


# Demo
print("="*50)
print("Drawing 3D - Phase 3: Site Management")
print("="*50)

# Setup road (from Phase 1)
class SimpleRoad:
    def __init__(self):
        self.points = [(0,0,0), (1,100,50), (2,250,80), (3,400,60), (4,550,100), (5,700,150)]
    
    def xy_to_mileage(self, x, y):
        best_m = None
        best_d = 999999
        for m, px, py in self.points:
            d = ((x-px)**2 + (y-py)**2)**0.5
            if d < best_d:
                best_d = d
                best_m = m
        return best_m, best_d

road = SimpleRoad()

# Photo Manager
print("\n[1] Photo Manager:")
pm = PhotoManager(road)

# Add photos (with simulated GPS)
pm.add_photo("K1+500.jpg", description="Water stable layer")
pm.add_photo("K2+300.jpg", description="Asphalt paving")
pm.add_photo("K3+800.jpg", description="Compaction")
pm.add_photo("K4+200.jpg", description="Quality inspection")
pm.add_photo("photo_no_gps.jpg", description="Unknown location")

print(f"    Total photos: {len(pm.photos)}")

# Query by mileage
print("\n[2] Query K1-K4 photos:")
photos = pm.query_by_mileage(1, 4)
for p in photos:
    print(f"    - {p['file']}: {p['description']}")

# Quality Manager
print("\n[3] Quality Manager:")
qm = QualityManager(road)

qm.add_record(1.5, "compaction", "98%", "ok")
qm.add_record(1.5, "thickness", "185mm", "warning", "slightly thick")
qm.add_record(2.3, "temperature", "145C", "ok")
qm.add_record(3.8, "compaction", "96%", "warning", "need more rolling")
qm.add_record(4.2, "smoothness", "pass", "ok")

print(f"    Total records: {len(qm.records)}")

# Query
print("\n[4] Query K1-K4 quality:")
records = qm.query_by_mileage(1, 4)
for r in records:
    status_icon = "✓" if r['status'] == "ok" else "⚠"
    print(f"    {status_icon} K{r['mileage']}: {r['item']} = {r['result']}")

# Warnings
print("\n[5] Warnings:")
warnings = qm.get_warnings()
for w in warnings:
    print(f"    ⚠ K{w['mileage']}: {w['item']} - {w['notes']}")

# Progress Manager
print("\n[6] Progress Manager:")
progress = ProgressManager(road)

progress.add_section(0, 1, "completed", 100)
progress.add_section(1, 2, "completed", 100)
progress.add_section(2, 3, "in_progress", 60)
progress.add_section(3, 4, "in_progress", 30)
progress.add_section(4, 5, "not_started", 0)

print(f"    Overall progress: {progress.get_overall_progress()}%")

completed = progress.query_by_status("completed")
in_progress = progress.query_by_status("in_progress")

print(f"    Completed: {len(completed)} sections")
print(f"    In progress: {len(in_progress)} sections")

for s in progress.sections:
    status_str = {
        "completed": "✓ Done",
        "in_progress": "◐ In Progress",
        "not_started": "○ Not Started"
    }
    print(f"    K{s['start']:.0f}-K{s['end']:.0f}: {status_str[s['status']]} ({s['percent']}%)")

print("\n" + "="*50)
print("Phase 3 Complete!")
print("="*50)
