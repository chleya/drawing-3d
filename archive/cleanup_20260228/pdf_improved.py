"""
Drawing 3D - PDF with OCR
Better text extraction from engineering drawings

Note: EasyOCR needs to download models first time (~200MB)
"""

# For now, let's use improved PDF text extraction
# OCR can be added when EasyOCR is ready

class ImprovedPDFParser:
    """Improved PDF parser with better extraction"""
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.text = ""
        self.pages = 0
    
    def read(self):
        """Read PDF"""
        try:
            import PyPDF2
            with open(self.filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                self.pages = len(reader.pages)
                
                # Extract from first few pages + some key pages
                texts = []
                
                # First 3 pages (project info)
                for i in range(min(3, self.pages)):
                    try:
                        texts.append(reader.pages[i].extract_text())
                    except:
                        pass
                
                # Middle pages (technical specs)
                if self.pages > 10:
                    for i in range(self.pages//2 - 2, self.pages//2 + 2):
                        try:
                            texts.append(reader.pages[i].extract_text())
                        except:
                            pass
                
                # Last few pages
                for i in range(max(3, self.pages - 3), self.pages):
                    try:
                        texts.append(reader.pages[i].extract_text())
                    except:
                        pass
                
                self.text = "\n\n======\n\n".join(texts)
                return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def extract_structured(self):
        """Extract structured information"""
        import re
        
        info = {
            'project': [],
            'length': [],
            'coordinates': [],
            'dimensions': [],
            'materials': [],
            'structures': [],
        }
        
        # Project name patterns
        project_patterns = [
            r'([^\s]+(?:高速|公路|道路|桥梁|隧道|涵洞)[^\s]*)',
            r'(?:项目|工程)[^\s]*([^\n]{5,20})',
        ]
        for p in project_patterns:
            matches = re.findall(p, self.text)
            info['project'].extend(matches)
        
        # Length
        length_patterns = [
            r'(?:全长|总长|长度)[^\d]*(\d+\.?\d*)\s*(?:km|公里|米|m)',
            r'(\d+\.?\d*)\s*公里',
        ]
        for p in length_patterns:
            matches = re.findall(p, self.text, re.I)
            info['length'].extend(matches)
        
        # Coordinates (X=, Y=, or numbers)
        coord_patterns = [
            r'X\s*[=:]\s*(\d+\.?\d*)',
            r'Y\s*[=:]\s*(\d+\.?\d*)',
            r'K\s*\d+\s*\+\s*(\d+)',  # K桩号
        ]
        for p in coord_patterns:
            matches = re.findall(p, self.text, re.I)
            info['coordinates'].extend(matches[:10])
        
        # Dimensions (mm, cm, m)
        dim_patterns = [
            r'(\d+\.?\d*)\s*mm',
            r'(\d+\.?\d*)\s*cm', 
            r'(\d+\.?\d*)\s*m[^a-z]',
        ]
        for p in dim_patterns:
            matches = re.findall(p, self.text, re.I)
            info['dimensions'].extend(matches[:20])
        
        # Materials
        material_keywords = [
            '沥青', '混凝土', '水泥', '钢筋', '碎石', '级配',
            '水稳', '二灰', '灰土', 'AC', 'SMA', 'C\d{2}', 'HRB',
        ]
        for kw in material_keywords:
            if kw in self.text:
                info['materials'].append(kw)
        
        # Structures
        structure_keywords = [
            '涵洞', '桥梁', '隧道', '挡土墙', '排水沟', '护坡',
            '路基', '路面', '基层', '面层', '底基层',
        ]
        for kw in structure_keywords:
            if kw in self.text:
                info['structures'].append(kw)
        
        return info


# Demo
print("="*60)
print("Improved PDF Parser")
print("="*60)

# Find PDF
import os
pdfs = []
for root, dirs, files in os.walk('E:\\'):
    for f in files:
        if f.endswith('.pdf') and 'recycle' not in root.lower():
            pdfs.append(os.path.join(root, f))
    if pdfs:
        break

if pdfs:
    path = pdfs[0]
    print(f"\nReading: {os.path.basename(path)}")
    
    parser = ImprovedPDFParser(path)
    if parser.read():
        print(f"Pages: {parser.pages}")
        
        info = parser.extract_structured()
        
        print("\n=== Extracted Info ===")
        print(f"Project: {info['project'][:3]}")
        print(f"Length: {info['length'][:3]}")
        print(f"Coordinates: {info['coordinates'][:5]}")
        print(f"Dimensions: {info['dimensions'][:10]}")
        print(f"Materials: {info['materials']}")
        print(f"Structures: {info['structures']}")
else:
    print("No PDFs found")

print("\n" + "="*60)
