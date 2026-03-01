# -*- coding: utf-8 -*-
"""
文档解析器 - 支持多种格式
用于从AIGC文档中提取结构化知识
"""

import os
import re
import json
from typing import Dict, List, Tuple


class DocumentParser:
    """文档解析器基类"""
    
    def parse(self, file_path: str) -> Dict:
        """解析文档"""
        raise NotImplementedError


class TextParser(DocumentParser):
    """纯文本解析器"""
    
    def parse(self, file_path: str) -> Dict:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return self._extract_knowledge(content)
    
    def _extract_knowledge(self, content: str) -> Dict:
        """提取知识"""
        knowledge = {
            "entities": [],
            "relationships": [],
            "raw_text": content
        }
        
        # 提取桩号 (K\d+\+\d+)
        stakes = re.findall(r'K(\d+)\+(\d+)', content)
        for k, pos in stakes:
            knowledge["entities"].append({
                "type": "stake",
                "id": f"K{k}+{pos}",
                "k": int(k),
                "position": int(pos)
            })
        
        # 提取材料 (AC-\d+, 水泥, 沥青)
        materials = re.findall(r'AC-\d+[A-Z]?|SBS|\w*沥青\w*|\w*水泥\w*', content)
        for m in materials:
            if m.strip():
                knowledge["entities"].append({
                    "type": "material",
                    "id": m.strip()
                })
        
        # 提取厚度 ((\d+)cm|(\d+)mm)
        thicknesses = re.findall(r'(\d+)\s*cm|(\d+)\s*mm', content)
        for tc, tm in thicknesses:
            val = tc or tm
            knowledge["entities"].append({
                "type": "thickness",
                "id": f"{val}mm"
            })
        
        # 提取温度 ((\d+)-(\d+)℃)
        temps = re.findall(r'(\d+)\s*[-~]\s*(\d+)\s*℃', content)
        for t1, t2 in temps:
            knowledge["entities"].append({
                "type": "temperature",
                "min": int(t1),
                "max": int(t2)
            })
        
        # 提取规范 (JTG[\s\-]?F?\d+-\d+)
        standards = re.findall(r'JTG[\s\-]?F?\d+[\-\d]*', content)
        for s in standards:
            knowledge["entities"].append({
                "type": "standard",
                "id": s.strip()
            })
        
        return knowledge


class JSONParser(DocumentParser):
    """JSON解析器"""
    
    def parse(self, file_path: str) -> Dict:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return self._extract_knowledge(data)
    
    def _extract_knowledge(self, data: Dict) -> Dict:
        """从JSON提取知识"""
        knowledge = {
            "entities": [],
            "relationships": [],
            "raw_data": data
        }
        
        def recursive_extract(obj, path=""):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    recursive_extract(v, f"{path}.{k}")
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    recursive_extract(item, f"{path}[{i}]")
            else:
                # 提取关键字段
                if "桩号" in path or "stake" in path.lower():
                    knowledge["entities"].append({
                        "type": "stake",
                        "value": str(obj)
                    })
                if "材料" in path or "material" in path.lower():
                    knowledge["entities"].append({
                        "type": "material",
                        "value": str(obj)
                    })
        
        recursive_extract(data)
        return knowledge


class KnowledgeExtractor:
    """知识提取器 - 从文档到知识图谱"""
    
    def __init__(self):
        self.parsers = {
            '.txt': TextParser(),
            '.json': JSONParser(),
            '.md': TextParser()
        }
    
    def parse_document(self, file_path: str) -> Dict:
        """解析文档"""
        ext = os.path.splitext(file_path)[1].lower()
        parser = self.parsers.get(ext, TextParser())
        return parser.parse(file_path)
    
    def to_kg_format(self, knowledge: Dict) -> List[Dict]:
        """转换为知识图谱格式"""
        nodes = []
        
        # 添加实体
        for entity in knowledge.get("entities", []):
            nodes.append({
                "id": entity.get("id", entity.get("value", "")),
                "type": entity.get("type", "unknown"),
                "data": entity
            })
        
        return nodes
    
    def extract_structures(self, content: str) -> Dict:
        """提取路面结构信息"""
        structures = {}
        
        # 匹配所有桩号
        stake_pattern = r'K(\d+)\+(\d+)'
        stakes = re.findall(stake_pattern, content)
        
        for k, pos in stakes:
            stake_id = f"K{k}+{pos}"
            structures[stake_id] = {}
            
            # 简化：直接返回桩号，让后续处理更精细
            structures[stake_id]["exists"] = True
        
        return structures
    
    def extract_all_entities(self, content: str) -> Dict:
        """提取所有实体"""
        entities = {
            "stakes": [],      # 桩号
            "materials": [],   # 材料
            "thicknesses": [], # 厚度
            "temperatures": [], # 温度
            "standards": []    # 规范
        }
        
        # 桩号
        for m in re.finditer(r'K(\d+)\+(\d+)', content):
            entities["stakes"].append(f"K{m.group(1)}+{m.group(2)}")
        
        # 材料
        for m in re.finditer(r'AC-\d+[A-Z]?|SBS|\w*沥青\w*|\w*水泥\w*', content):
            if m.group().strip():
                entities["materials"].append(m.group().strip())
        
        # 厚度
        for m in re.finditer(r'(\d+)\s*mm|(\d+)\s*cm', content):
            val = m.group(1) or m.group(2)
            entities["thicknesses"].append(f"{val}mm")
        
        # 温度
        for m in re.finditer(r'(\d+)\s*[-~至]\s*(\d+)\s*℃', content):
            entities["temperatures"].append(f"{m.group(1)}-{m.group(2)}℃")
        
        # 规范
        for m in re.finditer(r'JTG[\s\-]?F?\d+[\-\d]*', content):
            entities["standards"].append(m.group().strip())
        
        return entities


# ========== 使用示例 ==========

if __name__ == "__main__":
    extractor = KnowledgeExtractor()
    
    # 测试
    test_text = """
    K5+800路面结构：
    上面层：AC-13C，4cm
    中面层：AC-20，6cm
    下面层：AC-25，8cm
    上基层：水泥稳定碎石，36cm
    
    施工温度：160-180℃
    压实度：≥96%
    
    规范：JTG F40-2004
    """
    
    result = extractor.extract_structures(test_text)
    print("Extracted structures:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
