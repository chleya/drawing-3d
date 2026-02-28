"""
Road Project Data Format (JSON Schema)

Designed for:
- 351 Highway / Road Engineering
- Station-based data (K5+800, K6+000, etc.)
- Multi-layer structure (surface, base, subbase, subgrade)
- Quality, progress, photos, documents

Run: python drawing_3d/data_format.py
"""

import json
from datetime import datetime

# ============================================================
# DATA FORMAT SPECIFICATION
# ============================================================

"""
ROAD PROJECT JSON SCHEMA
========================

{
  "project": {
    "name": "351 Provincial Road",
    "code": "351PP-2024",
    "total_length_km": 6.877,
    "start_station": "K0+000",
    "end_station": "K6+877"
  },
  
  "stations": {
    "K5+800": {
      "position_km": 5.8,
      "layers": {
        "surface": {
          "material": "AC-13",
          "thickness_mm": 40,
          " compaction": 98
        },
        "base": {
          "material": "CTSM",
          "thickness_mm": 180
        },
        "subbase": {
          "material": "GAB",
          "thickness_mm": 300
        }
      },
      "quality": [
        {"item": "compaction", "value": 98, "unit": "%", "status": "ok", "date": "2024-06-15"}
      ],
      "photos": ["IMG_001.jpg", "IMG_002.jpg"],
      "notes": ""
    }
  },
  
  "sections": [
    {
      "start": "K0+000",
      "end": "K1+000",
      "status": "completed",
      "progress_percent": 100,
      "start_date": "2024-01-01",
      "end_date": "2024-03-15"
    }
  ],
  
  "materials": [...],
  "documents": [...],
  "team": [...]
}
"""

class RoadProjectData:
    """Road Project Data Manager"""
    
    def __init__(self, name, code):
        self.data = {
            "project": {
                "name": name,
                "code": code,
                "created": datetime.now().isoformat(),
                "version": "1.0"
            },
            "metadata": {
                "total_length_km": 0,
                "stations": {},
                "sections": [],
                "materials": [],
                "documents": [],
                "team": []
            }
        }
    
    # === Station Management ===
    def add_station(self, station, position_km=None):
        """Add a station"""
        if position_km is None:
            # Parse K5+800 -> 5.8
            try:
                k, rest = station.split('K')[1].split('+')
                position_km = float(k) + float(rest)/1000
            except:
                position_km = 0
        
        self.data["metadata"]["stations"][station] = {
            "position_km": position_km,
            "layers": {},
            "quality": [],
            "photos": [],
            "documents": [],
            "notes": ""
        }
        return self.data["metadata"]["stations"][station]
    
    def set_layer(self, station, layer, material, thickness_mm, **kwargs):
        """Set layer data"""
        if station not in self.data["metadata"]["stations"]:
            self.add_station(station)
        
        self.data["metadata"]["stations"][station]["layers"][layer] = {
            "material": material,
            "thickness_mm": thickness_mm
        }
        self.data["metadata"]["stations"][station]["layers"][layer].update(kwargs)
    
    def add_quality(self, station, item, value, unit, status="ok"):
        """Add quality record"""
        if station not in self.data["metadata"]["stations"]:
            self.add_station(station)
        
        self.data["metadata"]["stations"][station]["quality"].append({
            "item": item,
            "value": value,
            "unit": unit,
            "status": status,
            "date": datetime.now().strftime("%Y-%m-%d")
        })
    
    # === Section Management ===
    def add_section(self, start, end, status="not_started", progress=0):
        """Add section"""
        self.data["metadata"]["sections"].append({
            "start": start,
            "end": end,
            "status": status,
            "progress_percent": progress,
            "start_date": None,
            "end_date": None
        })
    
    # === Export/Import ===
    def to_json(self, filepath=None):
        """Export to JSON"""
        json_str = json.dumps(self.data, ensure_ascii=False, indent=2)
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(json_str)
        return json_str
    
    @staticmethod
    def from_json(filepath):
        """Import from JSON"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        obj = RoadProjectData(data["project"]["name"], data["project"]["code"])
        obj.data = data
        return obj
    
    # === Query ===
    def get_station(self, station):
        """Get station data"""
        return self.data["metadata"]["stations"].get(station)
    
    def get_all_layers(self):
        """Get all layer data"""
        layers = []
        for station, data in self.data["metadata"]["stations"].items():
            for layer_name, layer_data in data.get("layers", {}).items():
                layers.append({
                    "station": station,
                    "layer": layer_name,
                    **layer_data
                })
        return layers


# Demo
print("="*60)
print("Road Project Data Format Demo")
print("="*60)

# Create project
project = RoadProjectData("351 Provincial Road", "351-2024")

# Add stations with layers
print("\n[Adding Station Data...]")

project.add_station("K5+800", 5.8)
project.set_layer("K5+800", "surface", "AC-13", 40, compaction=98)
project.set_layer("K5+800", "base", "CTSM", 180)
project.set_layer("K5+800", "subbase", "GAB", 300)
project.add_quality("K5+800", "compaction", 98, "%", "ok")
project.add_quality("K5+800", "temperature", 145, "C", "ok")

project.add_station("K6+000", 6.0)
project.set_layer("K6+000", "surface", "AC-16", 50, compaction=98)
project.set_layer("K6+000", "base", "CTSM", 200)
project.add_quality("K6+000", "compaction", 98, "%", "ok")

project.add_station("K6+500", 6.5)
project.set_layer("K6+500", "surface", "AC-16", 50)
project.set_layer("K6+500", "base", "CTSM", 180)
project.add_quality("K6+500", "compaction", 97, "%", "warning")

# Add sections
print("\n[Adding Sections...]")

project.add_section("K0+000", "K1+000", "completed", 100)
project.add_section("K1+000", "K2+000", "completed", 100)
project.add_section("K2+000", "K3+000", "completed", 100)
project.add_section("K3+000", "K4+000", "in_progress", 70)
project.add_section("K4+000", "K5+000", "in_progress", 40)
project.add_section("K5+000", "K6+000", "not_started", 0)

# Export
print("\n[Exporting JSON...]")
json_output = project.to_json()

# Show structure
print("\n[Data Structure Preview:]")
print("-"*60)

parsed = json.loads(json_output)
print(json.dumps(parsed, indent=2)[:1500])
print("...")

# Query
print("\n[Query Examples:]")

# All layers
print("\nAll Layers:")
for layer in project.get_all_layers():
    print(f"  {layer['station']} {layer['layer']}: {layer['material']} {layer['thickness_mm']}mm")

# Quality issues
print("\nQuality Warnings:")
for station, data in parsed["metadata"]["stations"].items():
    for q in data.get("quality", []):
        if q["status"] != "ok":
            print(f"  {station}: {q['item']} = {q['value']}{q['unit']} [{q['status']}]")

# Save to file
project.to_json("drawing_3d/project_data.json")
print("\n[Saved to: drawing_3d/project_data.json]")

print("\n" + "="*60)
print("Data Format Ready!")
print("="*60)
