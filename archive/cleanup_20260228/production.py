"""
Drawing 3D - Production Ready System

Features:
1. OCR Reading
2. Knowledge Base
3. Query Interface
4. Report Generation
5. Multi-drawing Support

Run: python drawing_3d/production.py
"""

import easyocr
from PIL import Image, ImageDraw
import os
import json
from datetime import datetime

class ProductionSystem:
    """Production-ready drawing processing system"""
    
    def __init__(self):
        print("Initializing Production System...")
        self.reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
        self.knowledge_base = {}
        self.drawings = []
        print("Ready!")
    
    def process_drawing(self, filepath, station=None):
        """Process a drawing and add to knowledge base"""
        print(f"\nProcessing: {os.path.basename(filepath)}")
        
        # OCR
        result = self.reader.readtext(filepath, detail=0)
        print(f"  OCR: {len(result)} lines")
        
        # Extract
        data = self._extract_data(result)
        if station:
            data['station'] = station
        
        # Store
        key = station or os.path.basename(filepath)
        self.knowledge_base[key] = data
        self.drawings.append({
            'file': filepath,
            'station': station,
            'data': data,
            'time': datetime.now().isoformat()
        })
        
        print(f"  Extracted: {len(data)} items")
        return data
    
    def _extract_data(self, ocr_results):
        """Extract structured data from OCR"""
        import re
        
        data = {}
        
        for line in ocr_results:
            line_clean = line.upper().replace('O', '0').replace('S', '5').replace('I', '1')
            
            # Station
            if 'K' in line and '+' in line:
                m = re.search(r'K\d+\+\d+', line, re.I)
                if m:
                    data['station'] = m.group()
            
            # Thickness
            m = re.search(r'(\d{2,3})\s*MM', line_clean)
            if m:
                val = int(m.group(1))
                if 20 <= val <= 1000:
                    # Find layer
                    layer = "unknown"
                    if any(x in line.upper() for x in ['SURFACE', 'Surtace']):
                        layer = "surface"
                    elif any(x in line.upper() for x in ['BASE', 'Bse']):
                        layer = "base"
                    elif any(x in line.upper() for x in ['SUBBASE', 'Subbus']):
                        layer = "subbase"
                    
                    if layer != "unknown":
                        data[f'{layer}_thickness'] = str(val) + 'mm'
            
            # Compaction
            if 'COMPACT' in line_clean:
                m = re.search(r'\d+', line)
                if m:
                    val = int(m.group(1))
                    if 90 <= val <= 100:
                        data['compaction'] = str(val) + '%'
            
            # Temperature
            if 'TEMP' in line_clean:
                m = re.search(r'\d+', line)
                if m:
                    val = int(m.group(1))
                    if 100 <= val <= 200:
                        data['temperature'] = str(val) + 'C'
            
            # Material
            materials = ['AC-13', 'AC-16', 'CSM', 'CTSM', 'GAB', 'SMA']
            for mat in materials:
                if mat in line_clean:
                    data['material'] = mat
        
        return data
    
    def query(self, keyword):
        """Query knowledge base"""
        keyword = keyword.lower()
        results = []
        
        for station, data in self.knowledge_base.items():
            for key, value in data.items():
                if keyword in key.lower() or keyword in str(value).lower():
                    results.append({
                        'station': station,
                        'key': key,
                        'value': value
                    })
        
        return results
    
    def generate_report(self):
        """Generate project report"""
        report = f"""
============================================================
DRAWING PROCESSING REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
============================================================

Total Drawings Processed: {len(self.drawings)}

"""
        
        # Summary by station
        stations = list(self.knowledge_base.keys())
        if stations:
            report += "STATIONS:\n"
            for s in stations:
                report += f"  - {s}\n"
            report += "\n"
        
        # Common fields
        all_keys = set()
        for data in self.knowledge_base.values():
            all_keys.update(data.keys())
        
        if all_keys:
            report += "EXTRACTED DATA:\n"
            for key in sorted(all_keys):
                values = [str(d.get(key, '-')) for d in self.knowledge_base.values()]
                report += f"  {key}: {', '.join(values)}\n"
        
        return report


# Demo
print("="*60)
print("Production System Demo")
print("="*60)

system = ProductionSystem()

# Create sample drawings
print("\n[Creating sample drawings...]")

drawings = [
    ("K5+800", "Surface AC-13 40mm\nBase CTSM 180mm\nSubbase GAB 300mm\nCompaction: 98%\nTemp: 145C"),
    ("K6+000", "Surface AC-16 50mm\nBase CTSM 200mm\nSubbase GAB 350mm\nCompaction: 98%\nTemp: 150C"),
    ("K6+500", "Surface AC-16 50mm\nBase CTSM 180mm\nSubbase GAB 300mm\nCompaction: 97%\nTemp: 148C"),
]

for station, content in drawings:
    img = Image.new('RGB', (300, 150), 'white')
    d = ImageDraw.Draw(img)
    d.text((10, 10), f"Station {station}", fill='black')
    y = 40
    for line in content.split('\n'):
        d.text((10, y), line, fill='black')
        y += 25
    path = f"temp_{station.replace('+', '_')}.png"
    img.save(path)
    system.process_drawing(path, station)

# Query
print("\n[Query Test]")
print("-"*40)
for q in ["thickness", "compaction", "temperature", "material"]:
    results = system.query(q)
    print(f"\n{q}:")
    for r in results:
        print(f"  {r['station']}: {r['key']} = {r['value']}")

# Report
print("\n" + system.generate_report())

# Cleanup
for station, _ in drawings:
    path = f"temp_{station.replace('+', '_')}.png"
    if os.path.exists(path):
        os.remove(path)

print("\n" + "="*60)
print("Production Demo Complete!")
print("="*60)
