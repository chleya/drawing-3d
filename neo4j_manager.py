# -*- coding: utf-8 -*-
"""
语义化知识图谱 - Neo4j管理器
基于graph_db_manager.py，支持Neo4j和文件存储
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

# 导入图数据库管理器
from graph_db_manager import GraphDBManager


class Neo4jKnowledgeGraph:
    """知识图谱管理器 - 支持Neo4j和本地存储"""
    
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password=None,
                 storage_path="data/knowledge_graph.json"):
        """
        初始化知识图谱
        
        Args:
            uri: Neo4j连接URI
            user: Neo4j用户名
            password: Neo4j密码
            storage_path: 本地文件存储路径
        """
        # 初始化图数据库
        self.db = GraphDBManager(
            uri=uri,
            user=user,
            password=password,
            storage_path=storage_path
        )
        
        self.connected = self.db.connected
        self.storage_mode = "neo4j" if self.db.connected else "file"
        
        print(f"[INFO] Knowledge Graph initialized in {self.storage_mode} mode")
    
    # ========== 道路工程实体 ==========
    
    def add_road_structure(self, stake: str, structure: Dict) -> str:
        """添加道路结构"""
        properties = {
            "stake": stake,
            "type": "road_structure",
            "surface": structure.get("surface", ""),
            "base": structure.get("base", ""),
            "subbase": structure.get("subbase", ""),
            "total_thickness": structure.get("total_thickness", ""),
            "timestamp": datetime.now().isoformat()
        }
        return self.db.create_node("RoadStructure", properties)
    
    def add_material(self, name: str, properties: Dict) -> str:
        """添加材料"""
        props = {
            "name": name,
            "category": properties.get("category", ""),
            "spec": properties.get("spec", ""),
            "thickness": properties.get("thickness", ""),
            "standard": properties.get("standard", ""),
            "timestamp": datetime.now().isoformat()
        }
        return self.db.create_node("Material", props)
    
    def add_construction_standard(self, name: str, requirements: Dict) -> str:
        """添加施工规范"""
        props = {
            "name": name,
            "temperature": requirements.get("temperature", ""),
            "compaction": requirements.get("compaction", ""),
            "standard": requirements.get("standard", ""),
            "timestamp": datetime.now().isoformat()
        }
        return self.db.create_node("ConstructionStandard", props)
    
    # ========== 关系创建 ==========
    
    def link_stake_to_material(self, stake: str, material: str, rel_type="USES"):
        """连接桩号到材料"""
        stake_node = self.db.find_node("RoadStructure", "stake", stake)
        material_node = self.db.find_node("Material", "name", material)
        
        if stake_node and material_node:
            self.db.create_relationship(
                stake_node[0]['id'],
                material_node[0]['id'],
                rel_type
            )
    
    # ========== 查询 ==========
    
    def query_by_stake(self, stake: str) -> List[Dict]:
        """按桩号查询"""
        return self.db.find_node("RoadStructure", "stake", stake)
    
    def query_by_material(self, material_name: str) -> List[Dict]:
        """按材料查询"""
        return self.db.find_node("Material", "name", material_name)
    
    def get_all_structures(self) -> List[Dict]:
        """获取所有道路结构"""
        return self.db.find_nodes_by_label("RoadStructure")
    
    def get_all_materials(self) -> List[Dict]:
        """获取所有材料"""
        return self.db.find_nodes_by_label("Material")
    
    # ========== 统计 ==========
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return self.db.get_stats()
    
    # ========== 同步方法 ==========
    
    def sync_from_knowledge_graph(self, kg):
        """从内存知识图谱同步数据"""
        nodes_data = {
            "nodes": [],
            "relationships": []
        }
        
        # 同步节点
        for node_id, node_data in kg.nodes.items():
            label = node_data.get("type", "Concept")
            nodes_data["nodes"].append({
                "label": label,
                "properties": {
                    "id": node_id,
                    "name": node_data.get("name", ""),
                    "data": json.dumps(node_data)
                }
            })
        
        # 同步关系
        for rel in kg.relationships:
            nodes_data["relationships"].append({
                "from": rel.get("from"),
                "to": rel.get("to"),
                "type": rel.get("type", "RELATED")
            })
        
        self.db.import_from_dict(nodes_data)
    
    def close(self):
        """关闭连接"""
        self.db.close()


# ========== 创建示例知识图谱 ==========

def create_sample_kg():
    """创建示例知识图谱"""
    kg = Neo4jKnowledgeGraph(storage_path="data/sample_kg.json")
    
    # 添加道路结构
    print("\n[1] Adding road structures...")
    kg.add_road_structure("K5+800", {
        "surface": "40mm AC-13C",
        "base": "60mm AC-20",
        "subbase": "36cm"
    })
    kg.add_road_structure("K6+200", {
        "surface": "40mm AC-13C",
        "base": "60mm AC-20",
        "subbase": "80mm AC-25",
        "total_thickness": "36cm"
    })
    
    # 添加材料
    print("[2] Adding materials...")
    kg.add_material("AC-13C", {
        "category": "沥青混凝土",
        "spec": "上面层",
        "thickness": "40mm"
    })
    kg.add_material("AC-20", {
        "category": "沥青混凝土", 
        "spec": "中面层",
        "thickness": "60mm"
    })
    
    # 添加施工规范
    print("[3] Adding construction standards...")
    kg.add_construction_standard("SMA-13", {
        "temperature": "160-180℃",
        "compaction": "26%",
        "standard": "JTG F40-2004"
    })
    
    # 统计
    print("\n[4] Statistics:")
    stats = kg.get_stats()
    print(f"  Nodes: {stats.get('total_nodes', 0)}")
    print(f"  Relationships: {stats.get('total_relationships', 0)}")
    
    return kg


# ========== 测试 ==========

if __name__ == "__main__":
    print("="*50)
    print("Neo4j Knowledge Graph Test")
    print("="*50)
    
    kg = create_sample_kg()
    
    # 查询
    print("\n[Query] K5+800:")
    result = kg.query_by_stake("K5+800")
    print(result)
    
    print("\n[OK] Test complete!")
    kg.close()
