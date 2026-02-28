"""
Improved OCR with Image Pre-processing

Try to improve OCR accuracy with:
1. Grayscale conversion
2. Contrast enhancement
3. Binarization
4. Noise removal

Run: python drawing_3d/improved_ocr.py
"""

import easyocr
from PIL import Image, ImageEnhance
import os

print("="*60)
print("Improved OCR with Pre-processing")
print("="*60)

# Init
print("\n[1] Loading OCR...")
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
print("    Done!")

def preprocess_image(input_path, output_path):
    """Preprocess image for better OCR"""
    img = Image.open(input_path)
    
    # Convert to grayscale
    img = img.convert('L')
    
    # Increase contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)
    
    # Increase sharpness
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(2.0)
    
    img.save(output_path)
    return output_path

# Create test drawings with better quality
print("\n[2] Creating test images...")

test_cases = [
    ("K5+800", "AC-13 40mm CTSM 180mm GAB 300mm 98% 145C"),
    ("K6+000", "AC-16 50mm CTSM 200mm GAB 350mm 98% 150C"),
]

results = {}

for station, content in test_cases:
    # Create cleaner image (larger, clearer text)
    img = Image.new('RGB', (600, 100), 'white')
    from PIL import ImageDraw
    d = ImageDraw.Draw(img)
    d.text((50, 35), content, fill='black')
    
    raw_path = f"raw_{station.replace('+', '_')}.png"
    img.save(raw_path)
    
    # Pre-process
    proc_path = f"proc_{station.replace('+', '_')}.png"
    preprocess_image(raw_path, proc_path)
    
    # OCR on both
    print(f"\n[3] Processing {station}...")
    
    raw_result = reader.readtext(raw_path, detail=0)
    raw_text = ' '.join(raw_result)
    print(f"    Raw:     {raw_text[:60]}")
    
    proc_result = reader.readtext(proc_path, detail=0)
    proc_text = ' '.join(proc_result)
    print(f"    Processed: {proc_text[:60]}")
    
    results[station] = {
        'raw': raw_text,
        'processed': proc_text
    }
    
    # Cleanup
    os.remove(raw_path)
    os.remove(proc_path)

# Try fuzzy matching
print("\n[4] Fuzzy Search Test:")
print("-"*40)

def fuzzy_search(text, target):
    """Simple fuzzy search"""
    # Normalize
    text = text.upper().replace('O', '0').replace('S', '5').replace('I', '1')
    target = target.upper()
    return target in text

searches = ["40", "50", "180", "300", "98", "145", "AC"]

for term in searches:
    print(f"\n'{term}':")
    for station, texts in results.items():
        for version, text in texts.items():
            if fuzzy_search(text, term):
                print(f"  {station} ({version}): FOUND")
                break

print("\n" + "="*60)
print("Done!")
print("="*60)
