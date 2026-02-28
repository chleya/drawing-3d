"""
Drawing OCR - Read engineering drawings with EasyOCR

Run: python drawing_3d/draw_ocr.py
"""

import easyocr
from PIL import Image, ImageDraw, ImageFont
import os

# Initialize OCR (one time)
print("Initializing EasyOCR...")
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
print("Ready!")

def create_test_drawing(filename="test_drawing.png"):
    """Create a test engineering drawing image"""
    
    img = Image.new('RGB', (400, 300), color='white')
    d = ImageDraw.Draw(img)
    
    # Title
    d.text((150, 10), "Road Section Drawing", fill='black')
    
    # K Station
    d.text((20, 50), "K5+800", fill='black')
    
    # Dimensions
    d.text((20, 80), "Surface: 40mm AC-13", fill='black')
    d.text((20, 100), "Base: 180mm CSM", fill='black')
    d.text((20, 120), "Subbase: 300mm", fill='black')
    d.text((20, 140), "Subgrade: 500mm", fill='black')
    
    # Materials
    d.text((20, 170), "Materials:", fill='black')
    d.text((20, 190), "AC-13 Asphalt Concrete", fill='black')
    d.text((20, 210), "Cement Stabilized Macadam", fill='black')
    
    # Requirements
    d.text((20, 240), "Compaction: 98%", fill='black')
    d.text((20, 260), "Water Content: 5-8%", fill='black')
    
    # Save
    img.save(filename)
    return filename

def read_drawing(filename):
    """Read drawing with OCR"""
    if not os.path.exists(filename):
        return None
    
    result = reader.readtext(filename, detail=0)
    return result

# Demo
print("\n" + "="*50)
print("Drawing OCR Demo")
print("="*50)

# Create test drawing
print("\n[1] Creating test drawing...")
test_file = create_test_drawing()
print("    Saved: " + test_file)

# Read with OCR
print("\n[2] Reading with OCR...")
texts = read_drawing(test_file)

print("\n=== OCR Results ===")
for i, text in enumerate(texts):
    print(f"  {i+1}. {text}")

# Clean up
os.remove(test_file)

print("\n" + "="*50)
print("OCR Demo Complete!")
print("="*50)
