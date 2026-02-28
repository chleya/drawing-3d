"""
Complete Flow - From Drawing to Knowledge to Query
"""

import easyocr
from PIL import Image, ImageDraw
import os

class DrawingProcessor:
    """Process engineering drawings to knowledge base"""
    
    def __init__(self):
        print("Initializing OCR...")
        self.reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
        self.knowledge = {}
        print("Ready!")
    
    def create_sample_drawing(self, filename="sample_drawing.png"):
        """Create a realistic road drawing"""
        img = Image.new('RGB', (500, 600), color='white')
        d = ImageDraw.Draw(img)
        
        # Header
        d.text((150, 10), "ROAD SECTION DRAWING", fill='black')
        d.text((180, 35), "K6+500", fill='black')
        
        # Table
        y = 80
        d.text((50, y), "Layer", fill='black')
        d.text((200, y), "Material", fill='black')
        d.text((350, y), "Thickness", fill='black')
        
        # Data
        layers = [
            ("Surface", "AC-16", "50mm"),
            ("Base", "CTSM", "200mm"),
            ("Subbase", "GAB", "350mm"),
            ("Subgrade", "Soil", "600mm"),
        ]
        
        for i, (layer, mat, thick) in enumerate(layers):
            y = 120 + i * 40
            d.text((50, y), layer, fill='black')
            d.text((200, y), mat, fill='black')
            d.text((350, y), thick, fill='black')
        
        # Specs
        d.text((50, 300), "Specs:", fill='black')
        d.text((50, 325), "Compaction: 98%", fill='black')
        d.text((50, 345), "Water: 5-8%", fill='black')
        d.text((50, 365), "Temp: 140-160C", fill='black')
        
        # Info
        d.text((50, 420), "Date: 2024-06-20", fill='black')
        d.text((50, 440), "Engineer: Wang", fill='black')
        
        img.save(filename)
        return filename
    
    def ocr_drawing(self, filepath):
        """OCR a drawing file"""
        result = self.reader.readtext(filepath, detail=0)
        return result
    
    def extract_knowledge(self, ocr_results):
        """Extract structured knowledge from OCR text"""
        knowledge = {}
        
        # Find station
        for line in ocr_results:
            if 'K' in line and '+' in line:
                knowledge['station'] = line.strip()
                break
        
        # Find thickness values - OCR makes mistakes, be flexible
        import re
        for line in ocr_results:
            line_clean = line.upper().replace('O', '0').replace('S', '5').replace('I', '1')
            # Look for mm values (50mm, 200mm, etc)
            match = re.search(r'(\d+)\s*MM', line_clean)
            if match:
                thickness = match.group(1) + "mm"
                # Find layer name
                layer = "unknown"
                line_upper = line.upper()
                if 'SURFACE' in line_upper or 'SURTACE' in line_upper:
                    layer = "surface"
                elif 'BASE' in line_upper or 'BSE' in line_upper:
                    layer = "base"
                elif 'SUBBASE' in line_upper or 'SUBBUS' in line_upper:
                    layer = "subbase"
                elif 'SUBGRADE' in line_upper:
                    layer = "subgrade"
                
                key = f"thickness_{layer}"
                knowledge[key] = thickness
                print(f"    Found {layer} thickness: {thickness}")
        
        # Find compaction
        for line in ocr_results:
            if 'COMPACTION' in line.upper():
                import re
                match = re.search(r'\d+', line)
                if match:
                    knowledge['compaction'] = match.group() + "%"
        
        # Find temperature
        for line in ocr_results:
            if 'TEMP' in line.upper():
                import re
                match = re.search(r'\d+-\d+', line)
                if match:
                    knowledge['temperature'] = match.group() + "C"
        
        return knowledge
    
    def query(self, keyword):
        """Query knowledge base"""
        keyword = keyword.lower()
        results = []
        for k, v in self.knowledge.items():
            if keyword in k.lower():
                results.append(f"{k}: {v}")
        return results


# Demo
print("="*60)
print("Complete Flow Demo")
print("="*60)

# Create processor
processor = DrawingProcessor()

# Step 1: Create drawing
print("\n[Step 1] Create sample drawing...")
filepath = processor.create_sample_drawing()
print(f"  Created: {filepath}")

# Step 2: OCR
print("\n[Step 2] Run OCR...")
ocr_results = processor.ocr_drawing(filepath)
print(f"  Got {len(ocr_results)} lines")

# Step 3: Extract
print("\n[Step 3] Extract knowledge...")
knowledge = processor.extract_knowledge(ocr_results)
processor.knowledge = knowledge
print(f"  Extracted {len(knowledge)} items")
for k, v in knowledge.items():
    print(f"    {k}: {v}")

# Step 4: Query
print("\n[Step 4] Query demo...")
queries = ["thickness", "compaction", "temperature", "station"]
for q in queries:
    results = processor.query(q)
    if results:
        print(f"  '{q}': {results[0]}")
    else:
        print(f"  '{q}': Not found")

# Cleanup
os.remove(filepath)

print("\n" + "="*60)
print("Flow Complete!")
print("="*60)
