"""
PDF Drawing Parser
Try to parse real engineering drawings
"""

import PyPDF2
import re
import os

class PDFParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.text = ""
        self.pages = 0
    
    def read(self):
        """Read PDF"""
        try:
            with open(self.filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                self.pages = len(reader.pages)
                
                # Extract text from key pages
                # Usually: page 1 = overview, middle = details
                texts = []
                
                # First few pages
                for i in range(min(10, self.pages)):
                    try:
                        text = reader.pages[i].extract_text()
                        if text:
                            texts.append(text)
                    except:
                        pass
                
                self.text = "\n\n".join(texts)
                return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def extract_info(self):
        """Extract structured info"""
        info = {
            'project_name': '',
            'length': '',
            'pages': self.pages,
            'dimensions': [],
            'materials': [],
            'coordinates': [],
        }
        
        # Project name (usually on first page)
        lines = self.text.split('\n')
        for line in lines[:10]:
            if '公路' in line or '道路' in line or '工程' in line:
                info['project_name'] = line.strip()
                break
        
        # Length (look for numbers with km or 米)
        for match in re.finditer(r'(\d+\.?\d*)\s*(?:km|公里|米|m)', self.text, re.I):
            info['length'] = match.group()
            break
        
        # Dimensions (look for numbers with mm, cm)
        dims = re.findall(r'(\d+\.?\d*)\s*(?:mm|厘米|cm)', self.text)
        info['dimensions'] = dims[:20]
        
        # Materials (common road materials)
        materials = ['沥青', '混凝土', '水泥', '钢筋', '碎石', '级配', '水稳']
        for mat in materials:
            if mat in self.text:
                info['materials'].append(mat)
        
        # Coordinates (look for numbers like XXXXX.XX)
        coords = re.findall(r'\d{5,}\.?\d*', self.text)
        info['coordinates'] = coords[:10]
        
        return info
    
    def extract_by_page(self, page_num):
        """Extract text from specific page"""
        try:
            with open(self.filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                if page_num < len(reader.pages):
                    return reader.pages[page_num].extract_text()
        except:
            pass
        return ""


# Find PDF files
def find_pdfs(path='E:\\'):
    pdfs = []
    try:
        for root, dirs, files in os.walk(path):
            for f in files:
                if f.endswith('.pdf') and 'recycle' not in root.lower():
                    full_path = os.path.join(root, f)
                    pdfs.append(full_path)
    except:
        pass
    return pdfs

# Demo
print("="*60)
print("PDF Drawing Parser")
print("="*60)

# Find PDFs
pdfs = find_pdfs()
print(f"\nFound {len(pdfs)} PDF files")

# Try first valid PDF
for pdf in pdfs[:5]:
    print(f"\nTrying: {os.path.basename(pdf)[:40]}")
    
    parser = PDFParser(pdf)
    if parser.read():
        print(f"  Pages: {parser.pages}")
        
        info = parser.extract_info()
        
        print(f"  Project: {info['project_name'][:30] if info['project_name'] else 'N/A'}")
        print(f"  Length: {info['length']}")
        print(f"  Materials: {info['materials']}")
        print(f"  Dimensions: {info['dimensions'][:5]}")
        
        if parser.pages > 50:
            print("\n  Sample from middle page:")
            text = parser.extract_by_page(parser.pages // 2)
            print(text[:300])
            break
    else:
        print("  Failed to read")

print("\n" + "="*60)
print("Done!")
print("="*60)
