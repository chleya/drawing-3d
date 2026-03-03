# -*- coding: utf-8 -*-
"""
CAD图纸解析器 - 使用ezdxf
支持DWG/DXF文件解析，提取道路工程关键信息
"""

import os
import re
from typing import Dict, List, Optional, Tuple

try:
    import ezdxf
    from ezdxf.enums import TextEntityAlignment
    EZDXF_AVAILABLE = True
except ImportError:
    EZDXF_AVAILABLE = False
    print("警告: ezdxf未安装，将使用备用解析方式")


class CADParser:
    """CAD图纸解析器"""
    
    def __init__(self):
        self.entities = {
            'texts': [],        # 文字实体
            'mileages': [],      # 桩号
            'structures': [],    # 结构物
            'layers': {},        # 图层信息
            'blocks': [],        # 块定义
            'polylines': [],     # 多段线
        }
        
        # 道路工程关键字
        self.keywords = {
            'mileage': ['K', 'K+', '桩号', '里程', 'm'],
            'structure': {
                '桥梁': ['桥'],
                '涵洞': ['涵'],
                '隧道': ['隧道'],
                '互通': ['互通', '立交'],
                '通道': ['通道'],
            },
            'elevation': ['标高', '高程', '设计高', '地面高'],
            'width': ['宽度', '路基', '路面', '车道'],
        }
    
    def parse_file(self, filepath: str) -> Dict:
        """解析CAD文件
        
        Args:
            filepath: DWG/DXF文件路径
            
        Returns:
            解析结果字典
        """
        if not os.path.exists(filepath):
            return {'error': f'文件不存在: {filepath}'}
        
        if not EZDXF_AVAILABLE:
            return self._parse_fallback(filepath)
        
        try:
            # 读取DXF文件（DWG需先用CAD转换）
            doc = ezdxf.readfile(filepath)
            
            # 提取各类实体
            self._extract_texts(doc)
            self._extract_mileages()
            self._extract_structures()
            self._extract_layers(doc)
            self._extract_blocks(doc)
            
            return {
                'status': 'success',
                'file': os.path.basename(filepath),
                'entities': self.entities,
                'summary': self._generate_summary()
            }
            
        except Exception as e:
            return {'error': f'解析失败: {str(e)}'}
    
    def _extract_texts(self, doc):
        """提取所有文字实体"""
        msp = doc.modelspace()
        
        for text in msp.query('TEXT'):
            self.entities['texts'].append({
                'text': text.dxf.text,
                'layer': text.dxf.layer,
                'insert': tuple(text.dxf.insert) if hasattr(text.dxf, 'insert') else None,
                'height': text.dxf.height if hasattr(text.dxf, 'height') else None,
            })
        
        # MTEXT (多行文字)
        for mtext in msp.query('MTEXT'):
            self.entities['texts'].append({
                'text': mtext.text,
                'layer': mtext.dxf.layer,
                'insert': tuple(mtext.dxf.insert) if hasattr(mtext.dxf, 'insert') else None,
            })
    
    def _extract_mileages(self):
        """提取桩号信息"""
        mileage_pattern = re.compile(r'K(\d+)\+(\d+)')
        
        for text in self.entities['texts']:
            content = text['text']
            matches = mileage_pattern.findall(content.upper())
            
            for m in matches:
                km = int(m[0])
                m_val = int(m[1])
                total_m = km * 1000 + m_val
                
                self.entities['mileages'].append({
                    'km': km,
                    'meter': m_val,
                    'total': total_m,
                    'layer': text['layer'],
                    'position': text['insert'],
                    'raw_text': content
                })
    
    def _extract_structures(self):
        """提取结构物信息"""
        for text in self.entities['texts']:
            content = text['text']
            
            for struct_type, keywords in self.keywords['structure']:
                if any(kw in content for kw in keywords):
                    self.entities['structures'].append({
                        'type': struct_type,
                        'name': content,
                        'layer': text['layer'],
                        'position': text['insert']
                    })
                    break
    
    def _extract_layers(self, doc):
        """提取图层信息"""
        for layer in doc.layers:
            self.entities['layers'][layer.dxf.name] = {
                'name': layer.dxf.name,
                'color': layer.dxf.color if hasattr(layer.dxf, 'color') else None,
                'linetype': layer.dxf.linetype if hasattr(layer.dxf, 'linetype') else None,
            }
    
    def _extract_blocks(self, doc):
        """提取块定义"""
        for block in doc.blocks:
            if block.name.startswith('*'):
                continue  # 跳过系统块
            
            self.entities['blocks'].append({
                'name': block.name,
                'base_point': tuple(block.base_point) if block.base_point else None,
                'entities_count': len(block)
            })
    
    def _generate_summary(self) -> str:
        """生成解析摘要"""
        return f"""
解析完成:
- 文字实体: {len(self.entities['texts'])} 个
- 桩号: {len(self.entities['mileages'])} 个
- 结构物: {len(self.entities['structures'])} 个
- 图层: {len(self.entities['layers'])} 个
- 块: {len(self.entities['blocks'])} 个
        """.strip()
    
    def _parse_fallback(self, filepath: str) -> Dict:
        """备用解析方式（无ezdxf时）"""
        # 尝试读取文件内容（仅对DXF文本格式有效）
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # 简单提取K+桩号
            mileage_pattern = re.compile(r'K(\d+)\+(\d+)')
            mileages = mileage_pattern.findall(content.upper())
            
            return {
                'status': 'fallback',
                'file': os.path.basename(filepath),
                'mileages_found': len(mileages),
                'mileages': mileages[:20],  # 最多20个
                'note': '使用备用模式，建议安装ezdxf: pip install ezdxf'
            }
        except Exception as e:
            return {'error': f'备用解析失败: {str(e)}'}
    
    def export_to_neo4j_format(self) -> List[Dict]:
        """导出为Neo4j导入格式"""
        nodes = []
        
        # 桩号节点
        for m in self.entities['mileages']:
            nodes.append({
                'type': 'MileagePoint',
                'properties': {
                    'chainage': m['total'],
                    'km': m['km'],
                    'meter': m['meter'],
                    'layer': m['layer'],
                    'source': 'cad_parser'
                }
            })
        
        # 结构物节点
        for s in self.entities['structures']:
            nodes.append({
                'type': 'Structure',
                'properties': {
                    'name': s['name'],
                    'category': s['type'],
                    'layer': s['layer'],
                    'source': 'cad_parser'
                }
            })
        
        return nodes


# 测试
if __name__ == '__main__':
    parser = CADParser()
    
    # 测试解析
    test_file = 'test.dxf'
    if os.path.exists(test_file):
        result = parser.parse_file(test_file)
        print(result)
    else:
        print(f"测试文件不存在: {test_file}")
        print("\nezdxf解析器已就绪")
        print("使用方法:")
        print("  parser = CADParser()")
        print("  result = parser.parse_file('your_drawing.dxf')")
        print("  nodes = parser.export_to_neo4j_format()  # 导出到图数据库")
