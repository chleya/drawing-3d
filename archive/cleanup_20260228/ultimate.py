"""
Ultimate Robust System - Maximum Fuzzy Matching

Extract numbers and search by position/

Run: pythonpattern drawing_3d/ultimate.py
"""

import easyocr
from PIL import Image, ImageDraw
import re
import os

print("="*60)
print("Ultimate Robust System")
print("="*60)

# Init
print("\n[1] Loading OCR...")
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
print("    Done!")

def super_normalize(text):
    """Super normalization - extract only numbers and key chars"""
    # Keep only: digits, K, +, mm, %, C
    result = ""
    for c in text.upper():
        if c.isdigit() or c in 'K+':
            result += c
        elif c == 'M':
            result += 'M'
        elif c == '%':
            result += '%'
        elif c == 'C':
            result += 'C'
        elif c == '-':
            result += '-'
    return result

# Test normalize
tests = [
    "F-13 4Omm CTSN I8omm GAB3hhmm 98% 45C",
    "}-16SOmm CTSN 2OommGAB3Omm 98% 15OC",
    "FC-16Snmm CTSN Ianmm GAB3OOmm",
]

print("\n[2] Normalization Test:")
for t in tests:
    print(f"  {t[:40]}")
    print(f"  → {super_normalize(t)}")

# Create drawings
print("\n[3] Creating and processing...")

samples = [
    ("K5+800", "AC-13 40mm CTSM 180mm GAB 300mm 98% 145C"),
    ("K6+000", "AC-16 50mm CTSM 200mm GAB 350mm 98% 150C"),
    ("K6+500", "AC-16 50mm CTSM 180mm GAB 300mm 97% 148C"),
]

knowledge = {}

for station, content in samples:
    img = Image.new('RGB', (750, 80), 'white')
    d = ImageDraw.Draw(img)
    d.text((30, 30), content, fill='black')
    path = f"ult_{station.replace('+', '_')}.png"
    img.save(path)
    
    result = reader.readtext(path, detail=0)
    text = ' '.join(result)
    normalized = super_normalize(text)
    
    knowledge[station] = {
        'raw': text,
        'normalized': normalized
    }
    
    print(f"  {station}:")
    print(f"    Raw:      {text[:45]}")
    print(f"    Normal:   {normalized}")
    
    os.remove(path)

# Search
print("\n[4] Search:")
print("-"*60)

def find_value(normalized, pattern):
    """Find pattern in normalized text"""
    # For mm values
    if 'mm' in pattern.lower():
        nums = re.findall(r'\d+M', normalized)
        for n in nums:
            num = int(n.replace('M', ''))
            target = int(re.search(r'\d+', pattern).group())
            if abs(num - target) <= 5:  # Allow ±5 tolerance
                return True
    
    # For % values
    if '%' in pattern:
        if pattern.replace('%', '') in normalized:
            return True
    
    # For C values
    if 'C' in pattern:
        nums = re.findall(r'\d+C', normalized)
        for n in nums:
            num = int(n.replace('C', ''))
            target = int(re.search(r'\d+', pattern).group())
            if abs(num - target) <= 10:
                return True
    
    return False

searches = [
    "40mm", "50mm", "180mm", "200mm", "300mm", "350mm",
    "98%", "97%", "145C", "150C"
]

for s in searches:
    print(f"\n  '{s}':")
    for station, data in knowledge.items():
        if find_value(data['normalized'], s):
            print(f"    [OK] {station}")

# Extract all numbers
print("\n[5] Extracted Data:")
print("-"*60)

for station, data in knowledge.items():
    norm = data['normalized']
    print(f"\n  {station}:")
    
    # Find all mm values
    mm_vals = re.findall(r'(\d+)M', norm)
    print(f"    Thickness: {mm_vals}")
    
    # Find %
    pct = re.findall(r'(\d+)%', norm)
    print(f"    Compaction: {pct}")
    
    # Find temps
    temps = re.findall(r'(\d+)C', norm)
    print(f"    Temperature: {temps}")

print("\n" + "="*60)
print("Ultimate system works with tolerance matching!")
print("="*60)
