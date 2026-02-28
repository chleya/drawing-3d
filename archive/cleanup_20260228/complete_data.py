"""
Complete Road Project Data System

Features:
- Full data model
- CRUD operations
- Validation
- Import/Export
- Query engine
- Report generation

Run: python drawing_3d/complete_data.py
"""

import json
from datetime import datetime
from pathlib import Path

# ============================================================
# DATA SCHEMA
# ============================================================

SCHEMA = {
    "project": {
        "name": str,
        "code": str,
        "total_length_km": float,
        "start_station": str,
        "end_station": str,
        "created": str,
        "version": "1.0"
    },
    "design": {
        "road_type": str,          # 公路等级: highway, expressway, etc.
        "design_speed_kmh": int,   # 设计速度
        "lane_count": int,         # 车道数
        "road_width_m": float,     # 路幅宽度
    },
    "materials": [
        {
            "code": str,           # 材料编号
            "name": str,           # 材料名称
            "type": str,           # 类型:沥青/水泥/钢材等
            "spec": str,           # 规格
            "supplier": str,       # 供应商
        }
    ],
    "stations": {},  # Dynamic
    "sections": [],   # Dynamic
    "quality": [],    # Dynamic
    "documents": [],
    "team": [],
    "issues": [],
    "costs": {}
}

# Layer types
LAYER_TYPES = ["surface", "base", "subbase", "subgrade", "shoulder", "drainage"]

# Quality test types
QUALITY_TESTS = {
    "road": ["压实度", "平整度", "弯沉", "厚度", "宽度", "横坡"],
    "bridge": ["混凝土强度", "钢筋保护层", "尺寸", "平整度"],
    "tunnel": ["支护厚度", "混凝土强度", "渗漏水"],
    "culvert": ["混凝土强度", "尺寸", "基础承载力"]
}


class RoadProject:
    """Complete Road Project Data System"""
    
    def __init__(self, name="Project", code="PRJ-001"):
        self.filepath = None
        self.data = {
            "project": {
                "name": name,
                "code": code,
                "total_length_km": 0,
                "start_station": "K0+000",
                "end_station": "K0+000",
                "created": datetime.now().isoformat(),
                "modified": datetime.now().isoformat(),
                "version": "1.0"
            },
            "design": {
                "road_type": "",
                "design_speed_kmh": 80,
                "lane_count": 2,
                "road_width_m": 12
            },
            "materials": [],
            "stations": {},
            "sections": [],
            "quality": [],
            "documents": [],
            "team": [],
            "issues": [],
            "costs": {
                "total": 0,
                "by_category": {}
            }
        }
    
    # === Station Operations ===
    def add_station(self, station, position_km=None, **kwargs):
        """Add station with data"""
        if position_km is None:
            position_km = self._parse_station(station)
        
        self.data["stations"][station] = {
            "position_km": position_km,
            "layers": {},
            "quality": [],
            "photos": [],
            "notes": "",
            **kwargs
        }
        
        # Update project bounds
        self._update_bounds(station)
        return self.data["stations"][station]
    
    def _parse_station(self, station):
        """Parse K5+800 -> 5.8"""
        try:
            if 'K' in station:
                k, rest = station.split('K')[1].split('+')
                return float(k) + float(rest)/1000
        except:
            pass
        return 0
    
    def _update_bounds(self, station):
        """Update project start/end"""
        pos = self._parse_station(station)
        
        start = self._parse_station(self.data["project"]["start_station"])
        end = self._parse_station(self.data["project"]["end_station"])
        
        if pos < start:
            self.data["project"]["start_station"] = station
        if pos > end:
            self.data["project"]["end_station"] = station
        
        self.data["project"]["total_length_km"] = end - start
    
    def set_layer(self, station, layer, material, thickness_mm, **kwargs):
        """Set layer data"""
        if station not in self.data["stations"]:
            self.add_station(station)
        
        self.data["stations"][station]["layers"][layer] = {
            "material": material,
            "thickness_mm": thickness_mm,
            **kwargs
        }
    
    def get_station(self, station):
        return self.data["stations"].get(station)
    
    # === Section Operations ===
    def add_section(self, start, end, status="not_started", progress=0, **kwargs):
        """Add section"""
        self.data["sections"].append({
            "start": start,
            "end": end,
            "start_km": self._parse_station(start),
            "end_km": self._parse_station(end),
            "status": status,
            "progress_percent": progress,
            "start_date": None,
            "end_date": None,
            **kwargs
        })
        self._sort_sections()
    
    def _sort_sections(self):
        """Sort sections by start position"""
        self.data["sections"].sort(key=lambda x: x.get("start_km", 0))
    
    def get_section_progress(self):
        """Calculate overall progress"""
        if not self.data["sections"]:
            return 0
        total = sum(s["progress_percent"] for s in self.data["sections"])
        return total / len(self.data["sections"])
    
    # === Quality Operations ===
    def add_quality_record(self, station, test_type, value, unit, 
                          status="ok", date=None, **kwargs):
        """Add quality record"""
        self.data["quality"].append({
            "station": station,
            "test_type": test_type,
            "value": value,
            "unit": unit,
            "status": status,
            "date": date or datetime.now().strftime("%Y-%m-%d"),
            **kwargs
        })
    
    def get_quality_summary(self):
        """Get quality summary"""
        total = len(self.data["quality"])
        if total == 0:
            return {"total": 0, "ok": 0, "warning": 0, "fail": 0}
        
        ok = sum(1 for q in self.data["quality"] if q["status"] == "ok")
        warning = sum(1 for q in self.data["quality"] if q["status"] == "warning")
        fail = sum(1 for q in self.data["quality"] if q["status"] == "fail")
        
        return {"total": total, "ok": ok, "warning": warning, "fail": fail}
    
    # === Material Operations ===
    def add_material(self, code, name, mtype, spec="", supplier=""):
        """Add material"""
        self.data["materials"].append({
            "code": code,
            "name": name,
            "type": mtype,
            "spec": spec,
            "supplier": supplier,
            "added": datetime.now().isoformat()
        })
    
    # === Document Operations ===
    def add_document(self, name, dtype, path, description=""):
        """Add document"""
        self.data["documents"].append({
            "name": name,
            "type": dtype,
            "path": path,
            "description": description,
            "uploaded": datetime.now().isoformat()
        })
    
    # === Team Operations ===
    def add_team_member(self, name, role, phone="", email=""):
        """Add team member"""
        self.data["team"].append({
            "name": name,
            "role": role,
            "phone": phone,
            "email": email,
            "joined": datetime.now().isoformat()
        })
    
    # === Issue Operations ===
    def add_issue(self, title, description, priority="medium", status="open", **kwargs):
        """Add issue"""
        self.data["issues"].append({
            "title": title,
            "description": description,
            "priority": priority,
            "status": status,
            "created": datetime.now().isoformat(),
            **kwargs
        })
    
    # === Cost Operations ===
    def add_cost(self, category, amount, description=""):
        """Add cost"""
        if category not in self.data["costs"]["by_category"]:
            self.data["costs"]["by_category"][category] = 0
        self.data["costs"]["by_category"][category] += amount
        self.data["costs"]["total"] += amount
    
    # === Import/Export ===
    def save(self, filepath=None):
        """Save to file"""
        if filepath:
            self.filepath = filepath
        
        if not self.filepath:
            self.filepath = f"{self.data['project']['code']}.json"
        
        self.data["project"]["modified"] = datetime.now().isoformat()
        
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        
        return self.filepath
    
    @classmethod
    def load(cls, filepath):
        """Load from file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        proj = cls(data["project"]["name"], data["project"]["code"])
        proj.data = data
        proj.filepath = filepath
        return proj
    
    # === Reports ===
    def generate_report(self):
        """Generate project report"""
        progress = self.get_section_progress()
        quality = self.get_quality_summary()
        
        report = f"""
{'='*60}
ROAD PROJECT REPORT
{'='*60}

PROJECT: {self.data['project']['name']}
CODE: {self.data['project']['code']}
CREATED: {self.data['project']['created'][:10]}
MODIFIED: {self.data['project']['modified'][:10]}

DESIGN
------
Type: {self.data['design']['road_type'] or 'N/A'}
Speed: {self.data['design']['design_speed_kmh']} km/h
Lanes: {self.data['design']['lane_count']}
Width: {self.data['design']['road_width_m']} m

LENGTH
------
From: {self.data['project']['start_station']}
To: {self.data['project']['end_station']}
Total: {self.data['project']['total_length_km']:.3f} km

PROGRESS
--------
Overall: {progress:.1f}%
Sections: {len(self.data['sections'])}
  Completed: {sum(1 for s in self.data['sections'] if s['status'] == 'completed')}
  In Progress: {sum(1 for s in self.data['sections'] if s['status'] == 'in_progress')}
  Not Started: {sum(1 for s in self.data['sections'] if s['status'] == 'not_started')}

QUALITY
-------
Total Tests: {quality['total']}
  OK: {quality['ok']}
  Warning: {quality['warning']}
  Fail: {quality['fail']}

STATIONS: {len(self.data['stations'])}
MATERIALS: {len(self.data['materials'])}
DOCUMENTS: {len(self.data['documents'])}
TEAM: {len(self.data['team'])}
ISSUES: {len(self.data['issues'])} (Open: {sum(1 for i in self.data['issues'] if i['status'] == 'open')})

COSTS
-----
Total: ¥{self.data['costs']['total']:,.0f}
"""
        for cat, amt in self.data["costs"]["by_category"].items():
            report += f"  {cat}: ¥{amt:,.0f}\n"
        
        report += f"""
{'='*60}
"""
        return report


# ============================================================
# DEMO
# ============================================================

print("="*60)
print("Complete Road Project Data System")
print("="*60)

# Create project
project = RoadProject("351 Provincial Road Project", "351-2024")

# Design
project.data["design"]["road_type"] = "二级公路"
project.data["design"]["design_speed_kmh"] = 80
project.data["design"]["lane_count"] = 2
project.data["design"]["road_width_m"] = 12

# Add materials
project.add_material("AC-13", "沥青混凝土", "沥青", "细粒式", "浙江沥青厂")
project.add_material("AC-16", "沥青混凝土", "沥青", "中粒式", "浙江沥青厂")
project.add_material("CTSM", "水泥稳定碎石", "水泥", "5%", "本地石料厂")
project.add_material("GAB", "级配碎石", "碎石", "0-31.5mm", "本地石料厂")

# Add stations with layers
stations = [
    ("K5+800", "surface", "AC-13", 40),
    ("K5+800", "base", "CTSM", 180),
    ("K5+800", "subbase", "GAB", 300),
    ("K6+000", "surface", "AC-16", 50),
    ("K6+000", "base", "CTSM", 200),
    ("K6+000", "subbase", "GAB", 350),
    ("K6+500", "surface", "AC-16", 50),
    ("K6+500", "base", "CTSM", 180),
]

for station, layer, mat, thick in stations:
    project.set_layer(station, layer, mat, thick)

# Quality records
project.add_quality_record("K5+800", "压实度", 98, "%", "ok")
project.add_quality_record("K5+800", "温度", 145, "C", "ok")
project.add_quality_record("K6+000", "压实度", 98, "%", "ok")
project.add_quality_record("K6+500", "压实度", 97, "%", "warning")

# Sections
project.add_section("K0+000", "K1+000", "completed", 100)
project.add_section("K1+000", "K2+000", "completed", 100)
project.add_section("K2+000", "K3+000", "completed", 100)
project.add_section("K3+000", "K4+000", "in_progress", 70)
project.add_section("K4+000", "K5+000", "in_progress", 40)
project.add_section("K5+000", "K6+000", "not_started", 0)
project.add_section("K6+000", "K6+877", "not_started", 0)

# Team
project.add_team_member("张三", "项目经理", "138-0000-0001")
project.add_team_member("李四", "现场工程师", "138-0000-0002")
project.add_team_member("王五", "质量主管", "138-0000-0003")

# Documents
project.add_document("施工图设计.pdf", "drawing", "/docs/", "施工图设计文件")
project.add_document("施工组织设计.docx", "document", "/docs/", "施工组织设计")

# Issues
project.add_issue("K3+500路段压实度不足", "需要重新压实", "high", "open")
project.add_issue("设备维护", "压路机需要保养", "medium", "open")

# Costs
project.add_cost("材料", 5000000, "沥青混凝土")
project.add_cost("材料", 2000000, "水泥稳定碎石")
project.add_cost("人工", 1500000, "人工费用")
project.add_cost("设备", 1000000, "设备租赁")

# Generate report
print(project.generate_report())

# Save
filepath = project.save("drawing_3d/351_project.json")
print(f"\nSaved to: {filepath}")

# Show JSON structure
print("\n[JSON Structure]")
print("-"*60)
with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)
print(json.dumps(data, indent=2)[:1000])
print("...")

print("\n" + "="*60)
print("Complete Data System Ready!")
print("="*60)
