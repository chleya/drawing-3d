# -*- coding: utf-8 -*-
"""
图纸知识图谱 - Blueprint Knowledge Graph
基于Neo4j的空间语义知识库
"""

import json
from datetime import datetime


class BlueprintKnowledgeGraph:
    """图纸知识图谱管理器"""
    
    def __init__(self, neo4j_uri=None, username=None, password=None):
        """初始化
        
        Args:
            neo4j_uri: Neo4j连接URI (可选，不传则使用内存模拟)
            username: Neo4j用户名
            password: Neo4j密码
        """
        self.neo4j_uri = neo4j_uri
        self.username = username
        self.password = password
        self.driver = None
        self.use_neo4j = neo4j_uri is not None
        
        # 内存模拟模式
        self.nodes = {}  # id -> node
        self.relationships = []  # [(from, to, type)]
        
        if self.use_neo4j:
            self._connect_neo4j()
        else:
            print("[INFO] BlueprintKnowledgeGraph initialized in simulation mode")
    
    def _connect_neo4j(self):
        """连接Neo4j"""
        try:
            from neo4j import GraphDatabase
            self.driver = GraphDatabase.driver(
                self.neo4j_uri,
                auth=(self.username, self.password)
            )
            print(f"[OK] Connected to Neo4j: {self.neo4j_uri}")
        except Exception as e:
            print(f"[WARN] Neo4j connection failed: {e}, using simulation mode")
            self.use_neo4j = False
    
    # ========== 节点操作 ==========
    
    def add_design_element(self, element_id, name, element_type, properties=None):
        """添加设计元素节点
        
        Args:
            element_id: 元素ID
            name: 元素名称
            element_type: 元素类型 (road_base/pavement_layer/bridge_pier/culvert等)
            properties: 其他属性 dict
        """
        node = {
            'id': element_id,
            'name': name,
            'type': element_type,
            'properties': properties or {},
            'created_at': datetime.now().isoformat()
        }
        
        if self.use_neo4j:
            self._neo4j_add_node('DesignElement', node)
        else:
            self.nodes[element_id] = node
        
        return node
    
    def add_location(self, location_id, stake, longitude=None, latitude=None, elevation=None):
        """添加位置节点
        
        Args:
            location_id: 位置ID
            stake: 里程桩号 (如 K5+800)
            longitude: 经度
            latitude: 纬度
            elevation: 高程
        """
        node = {
            'id': location_id,
            'stake': stake,
            'longitude': longitude,
            'latitude': latitude,
            'elevation': elevation,
            'created_at': datetime.now().isoformat()
        }
        
        if self.use_neo4j:
            self._neo4j_add_node('Location', node)
        else:
            self.nodes[location_id] = node
        
        return node
    
    def add_material(self, material_id, name, material_type, properties=None):
        """添加材料节点
        
        Args:
            material_id: 材料ID
            name: 材料名称
            material_type: 材料类型
            properties: 属性
        """
        node = {
            'id': material_id,
            'name': name,
            'type': material_type,
            'properties': properties or {},
            'created_at': datetime.now().isoformat()
        }
        
        if self.use_neo4j:
            self._neo4j_add_node('Material', node)
        else:
            self.nodes[material_id] = node
        
        return node
    
    def add_standard(self, standard_id, code, name, content=None):
        """添加规范节点
        
        Args:
            standard_id: 规范ID
            code: 规范编号 (如 JTG F40-2004)
            name: 规范名称
            content: 规范内容
        """
        node = {
            'id': standard_id,
            'code': code,
            'name': name,
            'content': content,
            'created_at': datetime.now().isoformat()
        }
        
        if self.use_neo4j:
            self._neo4j_add_node('Standard', node)
        else:
            self.nodes[standard_id] = node
        
        return node
    
    # ========== 关系操作 ==========
    
    def add_relationship(self, from_id, to_id, rel_type, properties=None):
        """添加关系
        
        Args:
            from_id: 起始节点ID
            to_id: 目标节点ID
            rel_type: 关系类型 (MADE_OF/LOCATED_AT/PROCESSED_BY/BELOW/ABOVE等)
            properties: 属性
        """
        rel = {
            'from': from_id,
            'to': to_id,
            'type': rel_type,
            'properties': properties or {},
            'created_at': datetime.now().isoformat()
        }
        
        if self.use_neo4j:
            self._neo4j_add_relationship(rel)
        else:
            self.relationships.append(rel)
        
        return rel
    
    # ========== 查询操作 ==========
    
    def query_by_location(self, stake, radius=None):
        """按位置查询
        
        Args:
            stake: 里程桩号
            radius: 范围 (米)
        
        Returns:
            list: 相关的设计元素
        """
        results = []
        
        if self.use_neo4j:
            results = self._neo4j_query_by_location(stake, radius)
        else:
            # 模拟查询
            for rel in self.relationships:
                if rel['type'] == 'LOCATED_AT':
                    to_node = self.nodes.get(rel['to'])
                    if to_node and to_node.get('stake') == stake:
                        from_node = self.nodes.get(rel['from'])
                        if from_node:
                            results.append(from_node)
        
        return results
    
    def query_by_stake_range(self, start_stake, end_stake):
        """按里程范围查询
        
        Args:
            start_stake: 起始桩号
            end_stake: 结束桩号
        
        Returns:
            list: 范围内的设计元素
        """
        results = []
        
        def stake_to_number(s):
            """桩号转数字"""
            s = s.replace('K', '').replace('+', '.')
            return float(s)
        
        start_num = stake_to_number(start_stake)
        end_num = stake_to_number(end_stake)
        
        for rel in self.relationships:
            if rel['type'] == 'LOCATED_AT':
                to_node = self.nodes.get(rel['to'])
                if to_node and 'stake' in to_node:
                    stake_num = stake_to_number(to_node['stake'])
                    if start_num <= stake_num <= end_num:
                        from_node = self.nodes.get(rel['from'])
                        if from_node:
                            results.append({
                                **from_node,
                                'stake': to_node['stake']
                            })
        
        return results
    
    def query_by_keyword(self, keyword):
        """关键词查询
        
        Args:
            keyword: 关键词
        
        Returns:
            list: 匹配的节点
        """
        results = []
        keyword = keyword.lower()
        
        for node in self.nodes.values():
            # 匹配名称、类型、属性
            if keyword in node.get('name', '').lower():
                results.append(node)
            elif keyword in node.get('type', '').lower():
                results.append(node)
            elif 'properties' in node:
                for k, v in node['properties'].items():
                    if keyword in str(v).lower():
                        results.append(node)
                        break
        
        return results
    
    def query_structure_layers(self, stake):
        """查询某位置的路面结构层
        
        Args:
            stake: 里程桩号
        
        Returns:
            list: 结构层列表 (从上到下)
        """
        # 找到该位置的设计元素
        elements = self.query_by_location(stake)
        
        # 找结构层
        layers = []
        for e in elements:
            if 'layer' in e.get('type', '').lower() or 'layer' in e.get('name', '').lower():
                layers.append(e)
        
        # 按厚度排序 (薄到厚 = 从上到下)
        layers.sort(key=lambda x: x.get('properties', {}).get('thickness', 0))
        
        return layers
    
    # ========== Neo4j 内部方法 ==========
    
    def _neo4j_add_node(self, label, node):
        """Neo4j添加节点"""
        with self.driver.session() as session:
            session.run(f"""
                CREATE (n:{label} $props)
            """, props=node)
    
    def _neo4j_add_relationship(self, rel):
        """Neo4j添加关系"""
        with self.driver.session() as session:
            session.run(f"""
                MATCH (a), (b)
                WHERE a.id = $from AND b.id = $to
                CREATE (a)-[r:$rel_type $props]->(b)
            """, from_=rel['from'], to_=rel['to'], rel_type=rel['type'], props=rel.get('properties', {}))
    
    def _neo4j_query_by_location(self, stake, radius):
        """Neo4j按位置查询"""
        # TODO: 实现Neo4j空间查询
        return []
    
    # ========== 工具方法 ==========
    
    def get_stats(self):
        """获取统计信息"""
        node_types = {}
        for node in self.nodes.values():
            t = node.get('type', 'unknown')
            node_types[t] = node_types.get(t, 0) + 1
        
        return {
            'total_nodes': len(self.nodes),
            'total_relationships': len(self.relationships),
            'node_types': node_types,
            'mode': 'neo4j' if self.use_neo4j else 'simulation'
        }
    
    def export_json(self, filepath):
        """导出JSON"""
        data = {
            'nodes': self.nodes,
            'relationships': self.relationships,
            'exported_at': datetime.now().isoformat()
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[OK] Exported to {filepath}")
    
    def close(self):
        """关闭连接"""
        if self.driver:
            self.driver.close()


# ========== 示例数据 ==========

def create_sample_knowledge_graph():
    """创建示例知识图谱"""
    kg = BlueprintKnowledgeGraph()
    
    # 添加路面结构层
    layers = [
        ('layer_1', '上面层', 'pavement_layer', {'thickness': 40, 'material': 'AC-13C'}),
        ('layer_2', '中面层', 'pavement_layer', {'thickness': 60, 'material': 'AC-20'}),
        ('layer_3', '下面层', 'pavement_layer', {'thickness': 80, 'material': 'AC-25'}),
        ('layer_4', '上基层', 'road_base', {'thickness': 360, 'material': '水泥稳定碎石'}),
        ('layer_5', '下基层', 'road_base', {'thickness': 180, 'material': '水泥稳定碎石'}),
        ('layer_6', '底基层', 'road_base', {'thickness': 150, 'material': '级配碎石'}),
    ]
    
    for lid, name, ltype, props in layers:
        kg.add_design_element(lid, name, ltype, props)
    
    # 添加材料
    materials = [
        ('mat_1', 'AC-13C沥青混凝土', 'asphalt_concrete', {'penetration': '60-80'}),
        ('mat_2', 'SBS改性沥青', 'binder', {'grade': 'I-D'}),
        ('mat_3', '玄武岩', 'aggregate', {'crush_value': '≤26%'}),
    ]
    
    for mid, name, mtype, props in materials:
        kg.add_material(mid, name, mtype, props)
    
    # 添加规范
    standards = [
        ('std_1', 'JTG F40-2004', '公路沥青路面施工技术规范'),
        ('std_2', 'JTG/T F50-2011', '公路路面基层施工技术细则'),
    ]
    
    for sid, code, name in standards:
        kg.add_standard(sid, code, name)
    
    # 添加位置
    locations = [
        ('loc_1', 'K5+800', 121.47, 31.23),
        ('loc_2', 'K6+000', 121.48, 31.24),
    ]
    
    for lid, stake, lon, lat in locations:
        kg.add_location(lid, stake, lon, lat)
    
    # 建立关系
    # 结构层Made Of 材料
    kg.add_relationship('layer_1', 'mat_1', 'MADE_OF')
    kg.add_relationship('layer_1', 'mat_2', 'USES')
    kg.add_relationship('layer_3', 'mat_3', 'USES')
    
    # 结构层Located At 位置
    kg.add_relationship('layer_1', 'loc_1', 'LOCATED_AT')
    kg.add_relationship('layer_2', 'loc_1', 'LOCATED_AT')
    
    # 结构层上下关系
    kg.add_relationship('layer_1', 'layer_2', 'BELOW')
    kg.add_relationship('layer_2', 'layer_3', 'BELOW')
    kg.add_relationship('layer_1', 'layer_3', 'BELOW')
    
    # 材料Follow规范
    kg.add_relationship('mat_1', 'std_1', 'MUST_FOLLOW')
    kg.add_relationship('mat_3', 'std_2', 'MUST_FOLLOW')
    
    return kg


# ========== 测试 ==========

if __name__ == "__main__":
    print("="*50)
    print("Blueprint Knowledge Graph Test")
    print("="*50)
    
    # 创建示例
    kg = create_sample_knowledge_graph()
    
    # 统计
    print("\n[Stats]")
    stats = kg.get_stats()
    print(f"Total nodes: {stats['total_nodes']}")
    print(f"Total relationships: {stats['total_relationships']}")
    print(f"Mode: {stats['mode']}")
    
    # 查询测试
    print("\n[Query by location: K5+800]")
    results = kg.query_by_location('K5+800')
    for r in results:
        print(f"  - {r.get('name')} ({r.get('type')})")
    
    print("\n[Query by keyword: 沥青]")
    results = kg.query_by_keyword('沥青')
    for r in results:
        print(f"  - {r.get('name')} ({r.get('type')})")
    
    print("\n[Query structure layers: K5+800]")
    layers = kg.query_structure_layers('K5+800')
    for l in layers:
        props = l.get('properties', {})
        print(f"  - {l.get('name')}: {props.get('thickness')}mm {props.get('material', '')}")
    
    print("\n" + "="*50)
    print("Knowledge Graph Test Complete")
    print("="*50)
