"""
Drawing 3D - Phase 2: Drawing Parser + Knowledge Base

Run: python drawing_3d/parser.py
"""

import re

class DrawingParser:
    """Parse CAD/PDF drawings"""
    
    def __init__(self):
        self.drawings = {}  # name -> data
        self.entities = {}   # entity -> properties
    
    def parse_text(self, name, text):
        """Parse text content (from PDF/OCR)"""
        data = {
            'name': name,
            'layers': [],
            'dimensions': [],
            'materials': [],
            'notes': [],
            'structures': []
        }
        
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Layer
            if 'LAYER' in line or '图层' in line:
                data['layers'].append(line)
            
            # Dimension (e.g., "厚度=40mm")
            dims = re.findall(r'(\w+)\s*[=:]\s*(\d+(?:\.\d+)?)\s*(mm|m|cm)?', line, re.I)
            for d in dims:
                data['dimensions'].append({
                    'name': d[0],
                    'value': float(d[1]),
                    'unit': d[2] or 'mm'
                })
            
            # Material (e.g., "材料: 沥青混凝土")
            mats = re.findall(r'材料[:\s]*(\S+)', line, re.I)
            for m in mats:
                data['materials'].append(m)
            
            # Note
            if 'NOTE' in line or '注' in line or '说明' in line:
                data['notes'].append(line)
            
            # Structure
            if any(kw in line for kw in ['路基', '路面', '基层', '面层', '结构', 'layer']):
                data['structures'].append(line)
        
        self.drawings[name] = data
        return data
    
    def extract_all(self):
        """Extract all entities"""
        for name, data in self.drawings.items():
            # Dimensions
            for dim in data['dimensions']:
                key = dim['name']
                if key not in self.entities:
                    self.entities[key] = []
                self.entities[key].append({
                    'drawing': name,
                    'value': dim['value'],
                    'unit': dim['unit']
                })
            
            # Materials
            for mat in data['materials']:
                if mat not in self.entities:
                    self.entities[mat] = []
                self.entities[mat].append({
                    'drawing': name,
                    'type': 'material'
                })


class KnowledgeBase:
    """Knowledge base for QA"""
    
    def __init__(self):
        self.data = {}
        self.index = {}  # keyword -> keys
    
    def add(self, key, value):
        """Add knowledge"""
        self.data[key] = value
        
        # Index
        words = re.findall(r'[\w\u4e00-\u9fa5]+', key.lower())
        for w in words:
            if len(w) >= 2:
                if w not in self.index:
                    self.index[w] = []
                if key not in self.index[w]:
                    self.index[w].append(key)
    
    def query(self, question):
        """Query by keyword"""
        words = re.findall(r'[\w\u4e00-\u9fa5]+', question.lower())
        
        candidates = []
        for w in words:
            if w in self.index:
                candidates.extend(self.index[w])
        
        if not candidates:
            return None
        
        # Return best match
        best = max(candidates, key=len)
        return self.data.get(best)


# ===== Demo =====
print("="*50)
print("Drawing 3D - Phase 2: Parser + Knowledge")
print("="*50)

# Sample drawing data
SAMPLE_DRAWINGS = {
    "road_section_K5+800": """
LAYER: 路面结构
厚度 = 40 mm
厚度 = 180 mm
厚度 = 300 mm
材料: 沥青混凝土 AC-13
材料: 水泥稳定碎石
材料: 级配碎石
注: 压实度 98%
注: 养护 7天
""",
    
    "bridge_girder_K6+000": """
LAYER: 上部结构
直径 = 25 mm
间距 = 150 mm
长度 = 30000 mm
材料: C50混凝土
材料: HRB400钢筋
注: 保护层 30mm
注: 锚固 40d
""",
    
    "culvert_K6+500": """
LAYER: 主体
壁厚 = 500 mm
内径 = 2000 mm
材料: C30混凝土
注: 砂垫层
注: 闭水试验 24h
""",
}

# Parse drawings
print("\n[1] Parsing drawings...")
parser = DrawingParser()

for name, content in SAMPLE_DRAWINGS.items():
    data = parser.parse_text(name, content)
    print(f"    Parsed: {name}")
    print(f"      Layers: {len(data['layers'])}")
    print(f"      Dimensions: {len(data['dimensions'])}")
    print(f"      Materials: {len(data['materials'])}")

# Extract entities
print("\n[2] Extracting entities...")
parser.extract_all()
print(f"    Total entities: {len(parser.entities)}")

# Build knowledge base
print("\n[3] Building knowledge base...")
kb = KnowledgeBase()

for name, data in parser.drawings.items():
    # Add dimensions
    for dim in data['dimensions']:
        key = f"{dim['name']} {name}"
        value = f"{dim['value']} {dim['unit']}"
        kb.add(key, value)
    
    # Add materials
    for mat in data['materials']:
        key = f"{mat} {name}"
        value = f"Material: {mat}"
        kb.add(key, value)
    
    # Add notes
    for note in data['notes']:
        key = f"{note[:10]} {name}"
        value = note
        kb.add(key, value)

print(f"    Knowledge entries: {len(kb.data)}")

# QA Test
print("\n[4] QA Test:")
questions = [
    "thickness road",
    "material bridge",
    "K6+500 culvert",
    "compaction",
    "rebar",
]

for q in questions:
    answer = kb.query(q)
    print(f"    Q: {q}")
    print(f"    A: {answer or 'Not found'}")
    print()

print("="*50)
print("Phase 2 Complete!")
print("="*50)
