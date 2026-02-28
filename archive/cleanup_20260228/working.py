"""
Drawing to Knowledge - Working Version

This demonstrates the complete flow:
1. Create engineering drawing (image)
2. OCR read text
3. Extract to knowledge base
4. Query

OCR has limitations - for production, would need:
- Better image quality
- Template-based extraction
- Post-processing correction
"""

import easyocr
from PIL import Image, ImageDraw
import re

print("="*60)
print("Drawing to Knowledge System")
print("="*60)

# Initialize
print("\n[1] Initializing OCR...")
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
print("    Done!")

# Create drawing
print("\n[2] Creating drawing...")
img = Image.new('RGB', (450, 350), 'white')
d = ImageDraw.Draw(img)
d.text((120, 10), "ROAD CROSS SECTION", fill='black')
d.text((150, 35), "Station K5+800", fill='black')

d.text((30, 80), "Surface: AC-13, 40mm", fill='black')
d.text((30, 105), "Base: CTSM, 180mm", fill='black')
d.text((30, 130), "Subbase: GAB, 300mm", fill='black')

d.text((30, 170), "Requirements:", fill='black')
d.text((30, 195), "Compaction: 98%", fill='black')
d.text((30, 215), "Temperature: 145C", fill='black')

d.text((30, 260), "Date: 2024-06-15", fill='black')
d.text((30, 280), "Inspector: Zhang", fill='black')

img.save('test.png')
print("    Saved: test.png")

# OCR
print("\n[3] Running OCR...")
result = reader.readtext('test.png', detail=0)
print(f"    Got {len(result)} lines")

# Extract - simplified
print("\n[4] Extracting...")
knowledge = {}

for line in result:
    # Station
    if 'K' in line and '+' in line:
        knowledge['station'] = line.strip()
        print(f"    Station: {line.strip()}")
    
    # Thickness (look for numbers + mm)
    line_clean = line.upper().replace('O', '0').replace('S', '5')
    match = re.search(r'(\d+)\s*MM', line_clean)
    if match and int(match.group(1)) >= 10:  # Filter noise
        knowledge['thickness'] = match.group(1) + 'mm'
        print(f"    Thickness: {knowledge['thickness']}")
    
    # Compaction
    if 'COMPACT' in line.upper():
        m = re.search(r'\d+', line)
        if m:
            knowledge['compaction'] = m.group() + '%'
            print(f"    Compaction: {knowledge['compaction']}")
    
    # Temperature
    if 'TEMP' in line.upper():
        m = re.search(r'\d+', line)
        if m:
            knowledge['temperature'] = m.group() + 'C'
            print(f"    Temperature: {knowledge['temperature']}")

# Query
print("\n[5] Query Test:")
print("-"*40)
queries = ["thickness", "compact", "temp", "station"]
for q in queries:
    found = False
    for k, v in knowledge.items():
        if q.lower() in k.lower():
            print(f"  {q}: {v}")
            found = True
    if not found:
        print(f"  {q}: (not found)")

# Summary
print("\n" + "="*60)
print("Summary:")
print("-"*40)
print(f"  Lines read: {len(result)}")
print(f"  Data extracted: {len(knowledge)} items")
for k, v in knowledge.items():
    print(f"    - {k}: {v}")

print("\nNote: OCR has ~10-20% error rate on engineering drawings.")
print("Production use needs: better images, templates, correction.")

import os
os.remove('test.png')

print("\n" + "="*60)
