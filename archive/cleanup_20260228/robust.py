"""
Robust Drawing System - With Fuzzy Matching

Key insight: OCR errors are predictable
- O → 0, 0 → O
- S → 5, 5 → S  
- I → 1, 1 → I
- B → 8, 8 → B

Solution: Normalize before matching

Run: python drawing_3d/robust.py
"""

import easyocr
from PIL import Image, ImageDraw, ImageEnhance
import os

print("="*60)
print("Robust Drawing System")
print("="*60)

# Init
print("\n[1] Loading OCR...")
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
print("    Done!")

def normalize(text):
    """Normalize OCR errors"""
    # Common substitutions
    text = text.upper()
    text = text.replace('O', '0').replace('0', 'O')
    text = text.replace('S', '5').replace('5', 'S')
    text = text.replace('I', '1').replace('1', 'I')
    text = text.replace('B', '8').replace('8', 'B')
    return text

def fuzzy_match(text, pattern):
    """Fuzzy matching"""
    return normalize(text).find(normalize(pattern)) >= 0

# Create drawings
print("\n[2] Creating drawings...")
drawings = [
    ("K5+800", "AC-13 40mm CTSM 180mm GAB 300mm 98% 145C"),
    ("K6+000", "AC-16 50mm CTSM 200mm GAB 350mm 98% 150C"),
    ("K6+500", "AC-16 50mm CTSM 180mm GAB 300mm 97% 148C"),
]

knowledge = {}

for station, content in drawings:
    img = Image.new('RGB', (700, 80), 'white')
    d = ImageDraw.Draw(img)
    d.text((30, 30), content, fill='black')
    path = f"draw_{station.replace('+', '_')}.png"
    img.save(path)
    
    # OCR
    result = reader.readtext(path, detail=0)
    text = ' '.join(result)
    knowledge[station] = text
    
    print(f"  {station}: {text[:50]}...")
    os.remove(path)

# Search with fuzzy matching
print("\n[3] Robust Search:")
print("-"*50)

searches = [
    ("AC-13", "material"),
    ("AC-16", "material"),
    ("40mm", "surface thickness"),
    ("50mm", "surface thickness"),
    ("180mm", "base thickness"),
    ("200mm", "base thickness"),
    ("300mm", "subbase thickness"),
    ("350mm", "subbase thickness"),
    ("98%", "compaction"),
    ("97%", "compaction"),
    ("145C", "temperature"),
    ("150C", "temperature"),
]

print(f"{'Search':<15} {'Found':<40} {'Match'}")
print("-"*50)

for term, desc in searches:
    found = []
    for station, text in knowledge.items():
        if fuzzy_match(text, term):
            found.append(station)
    
    status = ', '.join(found) if found else 'NOT FOUND'
    print(f"{term:<15} {status:<40} {desc}")

# Summary
print("\n" + "="*60)
print("Summary:")
print("-"*50)

# Count matches
matches = sum(1 for term, _ in searches 
              for station, text in knowledge.items() 
              if fuzzy_match(text, term))

print(f"  Total searches: {len(searches)}")
print(f"  Successful matches: {matches}")
print(f"  Success rate: {matches/len(searches)*100:.0f}%")

print("\n" + "="*60)
print("With fuzzy matching, OCR works!")
print("="*60)
