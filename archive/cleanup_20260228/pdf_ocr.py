"""
PDF OCR - Use EasyOCR to read engineering drawings

Run: python drawing_3d/pdf_ocr.py
"""

import os
import easyocr

# Initialize OCR (one time)
print("Initializing EasyOCR...")
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
print("Ready!")

# Find PDF
pdfs = []
for root, dirs, files in os.walk('E:\\'):
    for f in files:
        if f.endswith('.pdf') and 'recycle' not in root.lower():
            pdfs.append(os.path.join(root, f))
    if len(pdfs) >= 3:
        break

print(f"\nFound {len(pdfs)} PDFs")

# Note: Converting PDF to images requires poppler
# For now, let's just show that OCR is available
print("\nOCR Engine Ready!")
print("To fully work with PDFs, we need:")
print("1. poppler (for pdf2image)")
print("2. Or use screenshots of drawings")
print("\nLet's try reading an image instead...")

# Try to find any image files
images = []
for root, dirs, files in os.walk('E:\\'):
    for f in files:
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            images.append(os.path.join(root, f))
    if len(images) >= 1:
        break

if images:
    print(f"\nFound image: {os.path.basename(images[0])}")
    print("Running OCR...")
    
    result = reader.readtext(images[0], detail=0)
    
    print("\n=== OCR Result ===")
    for line in result[:20]:  # First 20 lines
        print(line)
else:
    print("\nNo images found")
    print("\nDemo text:")
    test_texts = [
        "K5+800 沥青路面 厚度40mm",
        "压实度要求98%以上",
        "材料: AC-13沥青混凝土",
    ]
    for t in test_texts:
        print(f"  {t}")
