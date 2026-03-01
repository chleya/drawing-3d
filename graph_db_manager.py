# -*- coding: utf-8 -*-
"""
图数据库管理器 - 支持Neo4j和文件存储
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

try:
    from neo4j import GraphDatabase
    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False


class GraphDBManager:
    """图数据库管理器 - 支持Neo4j和本地JSON文件"""
    
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password=None, 
                 storage_path=None):
        """
        初始化图数据库
        
        Args:
            uri: Neo4j连接URI
            user: Neo4j用户名
            password: Neo4j密码
            storage_path: 本地文件存储路径 (当Neo4j不可用时使用)
        """
        self.uri = uri
        self.user = user
        self.password = password or os.environ.get('NEO4J_PASSWORD', 'neo4j')
        self.storage_path = storage_path or "data/graph_storage.json"
        self.driver = None
        self.connected = False
        self._use_file = not NEO4J_AVAILABLE
        
        # 尝试连接Neo4j
        if NEO4J_AVAILABLE:
            try:
                self.driver = GraphDatabase.driver(
                    self.uri, 
                    auth=(self.user, self.password)
                )
                # 测试连接
                with self.driver.session() as session:
                    session.run("RETURN 1")
                self.connected = True
                print(f"[OK] Connected to Neo4j: {self.uri}")
            except Exception as e:
                print(f"[WARN] Neo4j connection failed: {e}")
                self._use_file = True
        else:
            print("[INFO] Neo4j driver not available, using file storage")
        
        # 初始化文件存储
        if self._use_file:
            self._init_file_storage()
    
    def _init_file_storage(self):
        """初始化文件存储"""
        storage_dir = os.path.dirname(self.storage_path)
        if storage_dir:
            os.makedirs(storage_dir, exist_ok=True)
        if not os.path.exists(self.storage_path):
            self._save_data({"nodes": [], "relationships": []})
        print(f"[OK] Using file storage: {self.storage_path}")
    
    def _load_data(self) -> Dict:
        """加载数据"""
        if not self._use_file:
            return {}
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"nodes": [], "relationships": []}
    
    def _save_data(self, data: Dict):
        """保存数据"""
        if self._use_file:
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
    
    # ========== 节点操作 ==========
    
    def create_node(self, label: str, properties: Dict) -> Optional[str]:
        """创建节点"""
        if self._use_file:
            data = self._load_data()
            node_id = f"{label}_{len(data['nodes'])}"
            node = {"id": node_id, "label": label, "properties": properties}
            data['nodes'].append(node)
            self._save_data(data)
            return node_id
        
        # Neo4j实现
        query = f"CREATE (n:{label} $props) RETURN id(n) as nid"
        with self.driver.session() as session:
            result = session.run(query, props=properties)
            record = result.single()
            return str(record['nid']) if record else None
    
    def create_nodes_batch(self, nodes: List[Dict]) -> int:
        """批量创建节点"""
        if self._use_file:
            data = self._load_data()
            for node in nodes:
                node_id = f"{node['label']}_{len(data['nodes'])}"
                data['nodes'].append({
                    "id": node_id,
                    "label": node['label'],
                    "properties": node['properties']
                })
            self._save_data(data)
            return len(nodes)
        
        # Neo4j实现
        count = 0
        with self.driver.session() as session:
            for node in nodes:
                query = f"CREATE (n:{node['label']} $props)"
                session.run(query, props=node['properties'])
                count += 1
        return count
    
    def find_node(self, label: str, property_key: str, property_value: Any) -> List[Dict]:
        """查找节点"""
        if self._use_file:
            data = self._load_data()
            results = []
            for node in data['nodes']:
                if node['label'] == label and node['properties'].get(property_key) == property_value:
                    results.append(node)
            return results
        
        # Neo4j实现
        query = f"MATCH (n:{label}) WHERE n.{property_key} = $value RETURN n"
        with self.driver.session() as session:
            result = session.run(query, value=property_value)
            return [{"properties": dict(record['n'])} for record in result]
    
    def find_nodes_by_label(self, label: str) -> List[Dict]:
        """按标签查找所有节点"""
        if self._use_file:
            data = self._load_data()
            return [n for n in data['nodes'] if n['label'] == label]
        
        query = f"MATCH (n:{label}) RETURN n"
        with self.driver.session() as session:
            result = session.run(query)
            return [{"properties": dict(record['n'])} for record in result]
    
    # ========== 关系操作 ==========
    
    def create_relationship(self, from_id: str, to_id: str, 
                          rel_type: str, properties: Dict = None) -> bool:
        """创建关系"""
        if self._use_file:
            data = self._load_data()
            rel = {
                "from": from_id,
                "to": to_id,
                "type": rel_type,
                "properties": properties or {}
            }
            data['relationships'].append(rel)
            self._save_data(data)
            return True
        
        # Neo4j实现
        query = f"""
        MATCH (a), (b) 
        WHERE id(a) = $from_id AND id(b) = $to_id 
        CREATE (a)-[r:{rel_type} $props]->(b)
        RETURN r
        """
        with self.driver.session() as session:
            session.run(query, from_id=int(from_id), to_id=int(to_id), 
                       props=properties or {})
        return True
    
    def find_relationships(self, node_id: str = None, rel_type: str = None) -> List[Dict]:
        """查找关系"""
        if self._use_file:
            data = self._load_data()
            results = []
            for rel in data['relationships']:
                if node_id and rel['from'] != node_id and rel['to'] != node_id:
                    continue
                if rel_type and rel['type'] != rel_type:
                    continue
                results.append(rel)
            return results
        
        # Neo4j实现
        if node_id:
            query = f"MATCH (a)-[r:{rel_type or '*'}]->(b) WHERE id(a) = $node_id RETURN r"
            with self.driver.session() as session:
                result = session.run(query, node_id=int(node_id))
        else:
            query = f"MATCH (a)-[r:{rel_type or '*'}]->(b) RETURN r"
            with self.driver.session() as session:
                result = session.run(query)
        
        return [dict(record['r']) for record in result]
    
    # ========== 查询 ==========
    
    def execute_query(self, cypher: str, params: Dict = None) -> List[Dict]:
        """执行Cypher查询"""
        if self._use_file:
            print("[WARN] Cypher queries not supported in file mode")
            return []
        
        with self.driver.session() as session:
            result = session.run(cypher, params or {})
            return [dict(record) for record in result]
    
    # ========== 统计 ==========
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        if self._use_file:
            data = self._load_data()
            labels = {}
            for node in data['nodes']:
                label = node['label']
                labels[label] = labels.get(label, 0) + 1
            
            rel_types = {}
            for rel in data['relationships']:
                rtype = rel['type']
                rel_types[rtype] = rel_types.get(rtype, 0) + 1
            
            return {
                "total_nodes": len(data['nodes']),
                "total_relationships": len(data['relationships']),
                "node_labels": labels,
                "relationship_types": rel_types,
                "storage_mode": "file"
            }
        
        # Neo4j实现
        stats = {}
        with self.driver.session() as session:
            # 节点统计
            result = session.run("CALL db.labels()")
            labels = [record['label'] for record in result]
            for label in labels:
                result = session.run(f"MATCH (n:{label}) RETURN count(n) as count")
                stats[label] = result.single()['count']
            
            # 关系统计
            result = session.run("CALL db.relationshipTypes()")
            rel_types = [record['relationshipType'] for record in result]
            for rtype in rel_types:
                result = session.run(f"MATCH ()-[r:{rtype}]->() RETURN count(r) as count")
                stats[rtype] = result.single()['count']
        
        return {
            "total_nodes": sum(v for k, v in stats.items() if not k.startswith('_')),
            "total_relationships": sum(v for k, v in stats.items() if k.startswith('_')),
            "storage_mode": "neo4j"
        }
    
    # ========== 导入导出 ==========
    
    def import_from_dict(self, data: Dict) -> bool:
        """从字典导入数据"""
        if self._use_file:
            nodes = data.get('nodes', [])
            rels = data.get('relationships', [])
            
            storage_data = self._load_data()
            storage_data['nodes'].extend(nodes)
            storage_data['relationships'].extend(rels)
            self._save_data(storage_data)
            return True
        
        # Neo4j实现
        with self.driver.session() as session:
            for node in data.get('nodes', []):
                query = f"CREATE (n:{node['label']} $props)"
                session.run(query, props=node['properties'])
            
            for rel in data.get('relationships', []):
                query = f"""
                MATCH (a), (b) 
                WHERE a.{rel.get('from_key', 'id')} = $from_val 
                AND b.{rel.get('to_key', 'id')} = $to_val
                CREATE (a)-[r:{rel['type']}]->(b)
                """
                session.run(query, 
                           from_val=rel['from'], 
                           to_val=rel['to'])
        return True
    
    def export_to_dict(self) -> Dict:
        """导出为字典"""
        if self._use_file:
            return self._load_data()
        
        data = {"nodes": [], "relationships": []}
        with self.driver.session() as session:
            # 导出节点
            result = session.run("MATCH (n) RETURN labels(n) as labels, properties(n) as props, id(n) as nid")
            for record in result:
                data["nodes"].append({
                    "label": record['labels'][0] if record['labels'] else "Node",
                    "properties": dict(record['props']),
                    "id": str(record['nid'])
                })
            
            # 导出关系
            result = session.run("MATCH (a)-[r]->(b) RETURN id(a) as from_id, id(b) as to_id, type(r) as type, properties(r) as props")
            for record in result:
                data["relationships"].append({
                    "from": str(record['from_id']),
                    "to": str(record['to_id']),
                    "type": record['type'],
                    "properties": dict(record['props'])
                })
        
        return data
    
    def clear(self):
        """清空所有数据"""
        if self._use_file:
            self._save_data({"nodes": [], "relationships": []})
        else:
            with self.driver.session() as session:
                session.run("MATCH (n) DETACH DELETE n")
    
    def close(self):
        """关闭连接"""
        if self.driver:
            self.driver.close()


# ========== 便捷函数 ==========

def create_graph_db(uri="bolt://localhost:7687", user="neo4j", password=None):
    """创建图数据库连接"""
    return GraphDBManager(uri, user, password)


# ========== 测试 ==========

if __name__ == "__main__":
    print("="*50)
    print("GraphDB Manager Test")
    print("="*50)
    
    # 创建数据库
    db = GraphDBManager(storage_path="test_graph.json")
    
    # 测试创建节点
    print("\n[1] Creating nodes...")
    db.create_node("Road", {"stake": "K5+800", "type": "structure"})
    db.create_node("Road", {"stake": "K6+200", "type": "structure"})
    db.create_node("Material", {"name": "AC-13C", "thickness": "40mm"})
    print("[OK] Nodes created")
    
    # 测试查找
    print("\n[2] Finding nodes...")
    roads = db.find_nodes_by_label("Road")
    print(f"Found {len(roads)} roads")
    
    # 测试统计
    print("\n[3] Statistics:")
    stats = db.get_stats()
    print(stats)
    
    # 导出
    print("\n[4] Exporting data...")
    data = db.export_to_dict()
    print(f"Exported {len(data['nodes'])} nodes, {len(data['relationships'])} relationships")
    
    # 清理
    db.clear()
    print("\n[OK] Test complete!")
