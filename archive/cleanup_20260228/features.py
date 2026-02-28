"""
Drawing 3D - Enhanced Features

New Features:
1. Report Generation
2. Data Export
3. Alerts & Notifications
4. Timeline View
5. Comparison Analysis

Run: python drawing_3d/features.py
"""

import json
from datetime import datetime

class EnhancedRoadProject:
    """Road Project with enhanced features"""
    
    def __init__(self, name):
        self.name = name
        self.road_points = []
        self.photos = []
        self.quality = []
        self.progress = []
        self.knowledge = {}
        self.alerts = []
    
    # === Basic Methods ===
    def add_road_point(self, mileage, x, y):
        self.road_points.append((mileage, x, y))
    
    def add_knowledge(self, key, value):
        self.knowledge[key] = value
    
    def add_photo(self, mileage, filename, description=""):
        self.photos.append({
            'mileage': mileage,
            'file': filename,
            'description': description,
            'date': datetime.now().isoformat()
        })
    
    def add_quality(self, mileage, item, result, status="ok"):
        self.quality.append({
            'mileage': mileage,
            'item': item,
            'result': result,
            'status': status,
            'date': datetime.now().isoformat()
        })
    
    def add_progress(self, start_km, end_km, status, percent):
        self.progress.append({
            'start': start_km,
            'end': end_km,
            'status': status,
            'percent': percent
        })
    
    # === Feature 1: Alerts ===
    def check_alerts(self):
        """Check and generate alerts"""
        self.alerts = []
        
        # Quality warnings
        for q in self.quality:
            if q['status'] == 'warning':
                self.alerts.append({
                    'type': 'quality_warning',
                    'message': f"K{q['mileage']}: {q['item']} = {q['result']}",
                    'severity': 'high'
                })
        
        # Progress delays
        for p in self.progress:
            if p['status'] == 'in_progress' and p['percent'] < 50:
                self.alerts.append({
                    'type': 'progress_delay',
                    'message': f"K{p['start']}-K{p['end']}: Only {p['percent']}% complete",
                    'severity': 'medium'
                })
        
        return self.alerts
    
    # === Feature 2: Report Generation ===
    def generate_report(self):
        """Generate project report"""
        total_progress = sum(p['percent'] for p in self.progress) / len(self.progress) if self.progress else 0
        quality_ok = sum(1 for q in self.quality if q['status'] == 'ok')
        quality_warn = sum(1 for q in self.quality if q['status'] == 'warning')
        
        report = f"""
============================================================
PROJECT REPORT: {self.name}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
============================================================

[OVERVIEW]
- Total Sections: {len(self.progress)}
- Total Photos: {len(self.photos)}
- Quality Records: {len(self.quality)}
- Knowledge Entries: {len(self.knowledge)}

[PROGRESS]
- Overall Progress: {total_progress:.1f}%
- Completed: {sum(1 for p in self.progress if p['status'] == 'completed')}
- In Progress: {sum(1 for p in self.progress if p['status'] == 'in_progress')}
- Not Started: {sum(1 for p in self.progress if p['status'] == 'not_started')}

[QUALITY]
- OK: {quality_ok}
- Warnings: {quality_warn}

[ALERTS]
{chr(10).join(f"- {a['message']}" for a in self.alerts) if self.alerts else "- No alerts"}

============================================================
"""
        return report
    
    # === Feature 3: Export ===
    def export_json(self, filename):
        """Export to JSON"""
        data = {
            'name': self.name,
            'progress': self.progress,
            'quality': self.quality,
            'photos': self.photos,
            'knowledge': self.knowledge
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return filename
    
    # === Feature 4: Timeline ===
    def get_timeline(self):
        """Get timeline view"""
        events = []
        
        # Add progress events
        for p in self.progress:
            events.append({
                'type': 'progress',
                'start': p['start'],
                'end': p['end'],
                'status': p['status'],
                'percent': p['percent']
            })
        
        # Add quality events
        for q in self.quality:
            events.append({
                'type': 'quality',
                'mileage': q['mileage'],
                'item': q['item'],
                'result': q['result'],
                'status': q['status']
            })
        
        return sorted(events, key=lambda x: x.get('start', x.get('mileage', 0)))
    
    # === Feature 5: Comparison ===
    def compare_sections(self):
        """Compare sections"""
        comparison = []
        
        for p in self.progress:
            section = {
                'range': f"K{p['start']:.0f}-K{p['end']:.0f}",
                'status': p['status'],
                'percent': p['percent']
            }
            
            # Find quality for this section
            section_quality = [q for q in self.quality 
                            if p['start'] <= q['mileage'] <= p['end']]
            section['quality_count'] = len(section_quality)
            section['quality_ok'] = sum(1 for q in section_quality if q['status'] == 'ok')
            
            # Find photos
            section_photos = [ph for ph in self.photos 
                           if p['start'] <= ph['mileage'] <= p['end']]
            section['photo_count'] = len(section_photos)
            
            comparison.append(section)
        
        return comparison


# Demo
print("="*60)
print("Enhanced Features Demo")
print("="*60)

# Create project
project = EnhancedRoadProject("351 Road Project")

# Add data
for i in range(8):
    project.add_road_point(i, i * 100, i * 30)

# Progress
project.add_progress(0, 1, "completed", 100)
project.add_progress(1, 2, "completed", 100)
project.add_progress(2, 3, "completed", 100)
project.add_progress(3, 4, "in_progress", 70)
project.add_progress(4, 5, "in_progress", 40)
project.add_progress(5, 6, "not_started", 0)
project.add_progress(6, 7, "not_started", 0)

# Quality
project.add_quality(1.5, "compaction", "98%", "ok")
project.add_quality(2.3, "temperature", "145C", "ok")
project.add_quality(3.8, "compaction", "96%", "warning")
project.add_quality(5.2, "strength", "C50", "ok")

# Photos
project.add_photo(1.5, "photo1.jpg", "Water stable")
project.add_photo(2.3, "photo2.jpg", "Asphalt")
project.add_photo(3.8, "photo3.jpg", "Compaction")

# Knowledge
project.add_knowledge("test1", "value1")
project.add_knowledge("test2", "value2")

# Feature 1: Alerts
print("\n[1] Alerts Check:")
project.check_alerts()
for alert in project.alerts:
    print(f"  [{alert['severity'].upper()}] {alert['message']}")

# Feature 2: Report
print("\n[2] Report:")
print(project.generate_report())

# Feature 3: Timeline
print("\n[3] Timeline:")
for event in project.get_timeline():
    if event['type'] == 'progress':
        print(f"  Progress K{event['start']:.0f}-{event['end']:.0f}: {event['percent']}%")
    else:
        print(f"  Quality K{event['mileage']}: {event['item']} = {event['result']}")

# Feature 4: Comparison
print("\n[4] Section Comparison:")
for comp in project.compare_sections():
    print(f"  {comp['range']}: {comp['percent']}% | Q:{comp['quality_count']}({comp['quality_ok']}) | P:{comp['photo_count']}")

print("\n" + "="*60)
print("Enhanced Features Complete!")
print("="*60)
