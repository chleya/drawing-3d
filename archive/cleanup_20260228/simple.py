"""
Drawing 3D - Simple Working Version

Keep it simple:
1. OCR reads text
2. Store all text
3. Search in text

Run: python drawing_3d/simple.py
"""

import easyocr
from PIL import Image, ImageDraw
import os

print("="*60)
print("Simple Drawing System")
print("="*60)

# Init
print("\n[1] Loading OCR...")
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
print("    Done!")

# Create sample drawings
print("\n[2] Creating drawings...")
drawings = [
    ("K5+800", "Surface AC-13 40mm Base CTSM 180mm Subbase GAB 300mm Compaction 98% Temperature 145C"),
    ("K6+000", "Surface AC-16 50mm Base CTSM 200mm Subbase GAB 350mm Compaction 98% Temperature 150C"),
    ("K6+500", "Surface AC-16 50mm Base CTSM 180mm Subbase GAB 300mm Compaction 97% Temperature 148C"),
]

data = {}

for station, content in drawings:
    img = Image.new('RGB', (400, 80), 'white')
    d = ImageDraw.Draw(img)
    d.text((10, 30), content, fill='black')
    path = f"temp_{station.replace('+', '_')}.png"
    img.save(path)
    
    # OCR
    result = reader.readtext(path, detail=0)
    text = ' '.join(result)
    data[station] = text
    print(f"    {station}: {text[:50]}...")
    
    os.remove(path)

# Search
print("\n[3] Search Test:")
print("-"*40)

searches = [
    "40mm",
    "50mm", 
    "98%",
    "97%",
    "AC-13",
    "AC-16",
    "145C"
]

for term in searches:
    print(f"\n'{term}':")
    for station, text in data.items():
        if term in text:
            # Show context
            idx = text.find(term)
            start = max(0, idx - 20)
            end = min(len(text), idx + 30)
            context = text[start:end]
            print(f"  {station}: ...{context}...")

# Summary
print("\n" + "="*60)
print("Summary:")
print("-"*40)
print(f"  Drawings: {len(data)}")
print(f"  Total text: {sum(len(t) for t in data.values())} chars")
print("\nSimple approach works!")
print("="*60)
