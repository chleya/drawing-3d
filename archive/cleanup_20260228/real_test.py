"""
Real Test - Create a test drawing and process it
"""

import easyocr
from PIL import Image, ImageDraw, ImageFont
import os

print("="*60)
print("Real OCR Test")
print("="*60)

# Initialize OCR
print("\n[1] Loading OCR...")
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
print("    Ready!")

# Create a realistic engineering drawing
print("\n[2] Creating test drawing...")
img = Image.new('RGB', (600, 800), color='white')
d = ImageDraw.Draw(img)

# Title
d.text((200, 20), "Road Cross Section", fill='black')
d.text((180, 45), "K5+800 Section", fill='black')

# Table headers
d.text((30, 100), "Layer", fill='black')
d.text((150, 100), "Material", fill='black')
d.text((300, 100), "Thickness", fill='black')
d.text((420, 100), "Notes", fill='black')

# Data rows
d.text((30, 130), "Surface", fill='black')
d.text((150, 130), "AC-13", fill='black')
d.text((300, 130), "40mm", fill='black')
d.text((420, 130), "Asphalt", fill='black')

d.text((30, 155), "Base", fill='black')
d.text((150, 155), "CSM", fill='black')
d.text((300, 155), "180mm", fill='black')
d.text((420, 155), "Cement", fill='black')

d.text((30, 180), "Subbase", fill='black')
d.text((150, 180), "GAB", fill='black')
d.text((300, 180), "300mm", fill='black')
d.text((420, 180), "Granular", fill='black')

d.text((30, 205), "Subgrade", fill='black')
d.text((150, 205), "Soil", fill='black')
d.text((300, 205), "500mm", fill='black')
d.text((420, 205), "Compacted", fill='black')

# Requirements box
d.rectangle([30, 250, 550, 350], outline='black')
d.text((40, 260), "Requirements:", fill='black')
d.text((40, 285), "- Compaction: 98%", fill='black')
d.text((40, 305), "- Water Content: 5-8%", fill='black')
d.text((40, 325), "- Temperature: 140-160C", fill='black')

# Station info
d.text((30, 370), "Station: K5+800", fill='black')
d.text((30, 390), "Date: 2024-06-15", fill='black')
d.text((30, 410), "Inspector: Zhang", fill='black')

# Save
test_path = 'test_road_drawing.png'
img.save(test_path)
print(f"    Saved: {test_path}")

# OCR
print("\n[3] Running OCR...")
result = reader.readtext(test_path, detail=0)

print("\n[4] OCR Results:")
print("-"*50)
for i, line in enumerate(result):
    print(f"  {i+1:2d}: {line}")

# Extract structured data
print("\n[5] Extracted Data:")
print("-"*50)

knowledge = {}
for line in result:
    line_upper = line.upper()
    
    # Thickness
    if 'MM' in line_upper and any(x in line_upper for x in ['AC', 'CSM', 'GAB', 'SOIL']):
        parts = line.split()
        for p in parts:
            if 'MM' in p.upper():
                knowledge['thickness'] = p
                print(f"  Thickness: {p}")
    
    # Material
    if any(x in line.upper() for x in ['AC-13', 'CSM', 'GAB']):
        knowledge['material'] = line
        print(f"  Material: {line}")
    
    # Requirements
    if 'COMPACTION' in line_upper:
        knowledge['compaction'] = line
        print(f"  Compaction: {line}")
    if 'TEMPERATURE' in line_upper:
        knowledge['temperature'] = line
        print(f"  Temperature: {line}")

print("\n[6] Knowledge Base:")
print("-"*50)
for k, v in knowledge.items():
    print(f"  {k}: {v}")

# Cleanup
os.remove(test_path)

print("\n" + "="*60)
print("Real OCR Test Complete!")
print("="*60)
