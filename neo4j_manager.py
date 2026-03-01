# -*- coding: utf-8 -*-
"""
Neo4j图数据库管理器 - Neo4j Manager
提供连接池、查询、备份等功能
"""

import os
from datetime import datetime


class Neo4jManager:
    """Neo4j图数据库管理器"""
    
    def __init__(self, uri=None, username=None, password=None):
        """初始化
        
        Args:
            uri: Neo4j URI (如 neo4j://localhost:7687)
            username: 用户名
            password: 密码
        """
        # 从环境变量或参数获取
        self.uri = uri or os.environ.get('NEO4J_URI', 'bolt://localhost:7687')
        self.username = username or os.environ.get('NEO4J_USER', 'neo4j')
        self.password = password or os.environ.get('NEO4J_PASSWORD', 'password')
        
        self.driver = None
        self.connected = False
        
        # 尝试连接
        self.connect()
    
    def connect(self):
        """连接Neo4j"""
        try:
            from neo4j import GraphDatabase
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.username, self.password)
            )
            # 测试连接
            with self.driver.session() as session:
                result = session.run("RETURN 1 as n")
                result.single()
            self.connected = True
            print(f"[OK] Connected to Neo4j: {self.uri}")
            return True
        except Exception as e:
            print(f"[WARN] Neo4j connection failed: {e}")
            print(f"[INFO] Using simulation mode instead")
            self.connected = False
            return False
    
    def close(self):
        """关闭连接"""
        if self.driver:
            self.driver.close()
            print("[OK] Neo4j connection closed")
    
    # ========== 图谱操作 ==========
    
    def create_node(self, label, properties):
        """创建节点
        
        Args:
            label: 节点标签
            properties: 节点属性
        
        Returns:
            dict: 创建的节点
        """
        if not self.connected:
            return {"status": "simulation_mode"}
        
        query = f"CREATE (n:{label} $props) RETURN n"
        
        with self.driver.session() as session:
            result = session.run(query, props=properties)
            record = result.single()
            return dict(record['n'])
    
    def create_relationship(self, from_id, to_id, rel_type, properties=None):
        """创建关系
        
        Args:
            from_id: 起始节点ID
            to_id: 目标节点ID
            rel_type: 关系类型
            properties: 关系属性
        """
        if not self.connected:
            return {"status": "simulation_mode"}
        
        props = properties or {}
        
        query = f"""
        MATCH (a), (b)
        WHERE a.id = $from_id AND b.id = $to_id
        CREATE (a)-[r:{rel_type} $props]->(b)
        RETURN r
        """
        
        with self.driver.session() as session:
            result = session.run(
                query,
                from_id=from_id,
                to_id=to_id,
                props=props
            )
            return result.single()
    
    def query(self, cypher):
        """执行Cypher查询
        
        Args:
            cypher: Cypher语句
        
        Returns:
            list: 查询结果
        """
        if not self.connected:
            return []
        
        with self.driver.session() as session:
            result = session.run(cypher)
            return [dict(record) for record in result]
    
    def query_by_stake(self, stake):
        """按桩号查询
        
        Args:
            stake: 里程桩号
        
        Returns:
            list: 相关节点
        """
        if not self.connected:
            return []
        
        cypher = f"""
        MATCH (l:Location {{stake: '{stake}'}})<-[:LOCATED_AT]-(e)
        RETURN e
        """
        
        return self.query(cypher)
    
    def query_by_keyword(self, keyword):
        """关键词查询"""
        if not self.connected:
            return []
        
        cypher = f"""
        MATCH (n)
        WHERE n.name CONTAINS '{keyword}' OR n.type CONTAINS '{keyword}'
        RETURN n
        """
        
        return self.query(cypher)
    
    # ========== 批量操作 ==========
    
    def batch_import(self, nodes, relationships):
        """批量导入
        
        Args:
            nodes: 节点列表
            relationships: 关系列表
        """
        if not self.connected:
            print(f"[SIM] Would import {len(nodes)} nodes, {len(relationships)} relationships")
            return
        
        # 批量创建节点
        for node in nodes:
            label = node.get('label', 'Entity')
            props = {k: v for k, v in node.items() if k != 'label'}
            self.create_node(label, props)
        
        # 批量创建关系
        for rel in relationships:
            self.create_relationship(
                rel['from'],
                rel['to'],
                rel['type'],
                rel.get('properties')
            )
        
        print(f"[OK] Imported {len(nodes)} nodes, {len(relationships)} relationships")
    
    # ========== 数据库管理 ==========
    
    def get_stats(self):
        """获取数据库统计"""
        if not self.connected:
            return {"mode": "simulation"}
        
        stats = {}
        
        # 节点数量
        result = self.query("MATCH (n) RETURN count(n) as count")
        stats['nodes'] = result[0]['count'] if result else 0
        
        # 关系数量
        result = self.query("MATCH ()-[r]->() RETURN count(r) as count")
        stats['relationships'] = result[0]['count'] if result else 0
        
        # 标签分布
        result = self.query("""
            MATCH (n)
            RETURN labels(n)[0] as label, count(*) as count
            ORDER BY count DESC
        """)
        stats['labels'] = {r['label']: r['count'] for r in result}
        
        return stats
    
    def clear_all(self):
        """清空数据库"""
        if not self.connected:
            print("[SIM] Would clear all data")
            return
        
        self.query("MATCH (n) DETACH DELETE n")
        print("[OK] Database cleared")
    
    def export_json(self, filepath):
        """导出JSON"""
        if not self.connected:
            print("[SIM] Would export to file")
            return
        
        # 导出所有节点
        nodes = self.query("MATCH (n) RETURN n")
        
        # 导出所有关系
        rels = self.query("MATCH (a)-[r]->(b) RETURN a.id as from, b.id as to, type(r) as type")
        
        import json
        data = {
            'nodes': nodes,
            'relationships': rels,
            'exported_at': datetime.now().isoformat()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"[OK] Exported to {filepath}")


# ========== 快速开始 ==========

def quick_start(uri=None, user=None, password=None):
    """快速启动Neo4j连接
    
    Args:
        uri: Neo4j URI
        user: 用户名
        password: 密码
    
    Returns:
        Neo4jManager实例
    """
    manager = Neo4jManager(uri, user, password)
    
    if manager.connected:
        print(f"[OK] Neo4j connected: {manager.uri}")
    else:
        print("[INFO] Running in simulation mode")
    
    return manager


# ========== 测试 ==========

if __name__ == "__main__":
    print("="*50)
    print("Neo4j Manager Test")
    print("="*50)
    
    # 尝试连接
    manager = quick_start()
    
    # 获取统计
    print("\n[Stats]")
    stats = manager.get_stats()
    print(f"Mode: {stats.get('mode', 'neo4j')}")
    if 'nodes' in stats:
        print(f"Nodes: {stats['nodes']}")
        print(f"Relationships: {stats['relationships']}")
        print(f"Labels: {stats.get('labels', {})}")
    
    # 关闭
    manager.close()
    
    print("\n" + "="*50)
    print("Test Complete")
    print("="*50)
