# -*- coding: utf-8 -*-
"""
语义化API服务 - Semantic API Server
提供RESTful API接口
"""

import os
from flask import, jsonify
 Flask, requestfrom datetime import datetime

# 导入核心模块
from blueprint_knowledge_graph import BlueprintKnowledgeGraph, create_sample_knowledge_graph
from blueprint_qa import BlueprintQA
from llm_qa import LLMQASystem, SemanticQA
from neo4j_manager import Neo4jManager
from spatial_semantic_mapper import SpatialSemanticMapper

app = Flask(__name__)

# 全局变量
kg = None          # 知识图谱
qa = None          # 问答系统
llm = None         # LLM系统
mapper = None      # 空间映射器
neo4j = None       # Neo4j管理器


def init_services():
    """初始化服务"""
    global kg, qa, llm, mapper, neo4j
    
    print("="*50)
    print("Initializing Semantic Services...")
    print("="*50)
    
    # 1. 尝试连接Neo4j
    neo4j = Neo4jManager()
    
    # 2. 创建知识图谱
    print("\n[1] Creating Knowledge Graph...")
    kg = create_sample_knowledge_graph()
    
    # 如果Neo4j可用，尝试同步
    if neo4j.connected:
        print("[OK] Neo4j connected, syncing data...")
        # TODO: 同步数据到Neo4j
    else:
        print("[INFO] Running in simulation mode")
    
    # 3. 创建问答系统
    print("\n[2] Initializing Q&A Systems...")
    
    # 传统模板问答
    qa = BlueprintQA(kg)
    print("[OK] Template-based QA ready")
    
    # LLM问答 (需要API Key)
    llm_api_key = os.environ.get('MINIMAX_API_KEY') or os.environ.get('OPENAI_API_KEY')
    if llm_api_key:
        try:
            llm = LLMQASystem(provider='minimax', api_key=llm_api_key)
            print("[OK] LLM QA ready")
        except Exception as e:
            print(f"[WARN] LLM init failed: {e}")
            llm = None
    else:
        print("[INFO] No API Key, LLM QA unavailable")
    
    # 语义问答 (结合KG + LLM)
    semantic_qa = SemanticQA(kg)
    print("[OK] Semantic QA ready")
    
    # 4. 创建空间映射器
    print("\n[3] Initializing Spatial Mapper...")
    mapper = SpatialSemanticMapper(kg)
    print("[OK] Spatial mapper ready")
    
    print("\n" + "="*50)
    print("All Services Initialized!")
    print("="*50)


# ========== API 路由 ==========

@app.route('/')
def index():
    """首页"""
    return {
        'service': 'NeuralSite Semantic API',
        'version': '1.0',
        'status': 'running',
        'endpoints': [
            '/api/qa - 问答接口',
            '/api/kg/query - 知识图谱查询',
            '/api/spatial/query - 空间查询',
            '/api/kg/stats - 统计信息'
        ]
    }


@app.route('/api/qa', methods=['POST'])
def qa_endpoint():
    """问答接口
    
    Request:
    {
        "question": "K5+800路面结构是什么？",
        "use_llm": false  // 是否使用LLM
    }
    
    Response:
    {
        "answer": "...",
        "type": "structure",
        "timestamp": "..."
    }
    """
    data = request.get_json() or {}
    question = data.get('question', '')
    use_llm = data.get('use_llm', False)
    
    if not question:
        return jsonify({'error': 'question is required'}), 400
    
    try:
        if use_llm and llm:
            result = llm.ask(question)
            answer = result.get('answer', 'No response')
        else:
            answer = qa.ask(question)['answer']
        
        return jsonify({
            'answer': answer,
            'question': question,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/kg/query', methods=['GET'])
def kg_query():
    """知识图谱查询
    
    Query params:
        - type: 'location' | 'keyword' | 'stake_range'
        - value: 查询值
    """
    query_type = request.args.get('type', 'location')
    value = request.args.get('value', '')
    
    if not value:
        return jsonify({'error': 'value is required'}), 400
    
    try:
        if query_type == 'location':
            results = kg.query_by_location(value)
        elif query_type == 'keyword':
            results = kg.query_by_keyword(value)
        elif query_type == 'stake_range':
            parts = value.split('-')
            if len(parts) == 2:
                results = kg.query_by_stake_range(parts[0], parts[1])
            else:
                results = []
        else:
            results = []
        
        return jsonify({
            'results': results,
            'count': len(results),
            'type': query_type
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/kg/stats', methods=['GET'])
def kg_stats():
    """知识图谱统计"""
    return jsonify(kg.get_stats())


@app.route('/api/spatial/query', methods=['GET'])
def spatial_query():
    """空间查询
    
    Query params:
        - type: 'stake' | 'coords' | 'range'
        - value: 查询值
    """
    query_type = request.args.get('type', 'stake')
    value = request.args.get('value', '')
    
    try:
        if query_type == 'stake':
            # 桩号查元素
            elements = kg.query_by_location(value)
            coords = mapper.stake_to_coords(value)
            return jsonify({
                'stake': value,
                'coords': coords,
                'elements': elements
            })
        
        elif query_type == 'coords':
            # 坐标查桩号
            parts = value.split(',')
            if len(parts) == 2:
                lat, lon = float(parts[0]), float(parts[1])
                stake = mapper.coords_to_stake(lat, lon)
                elements = mapper.query_nearby(lat, lon)
                return jsonify({
                    'coords': {'lat': lat, 'lon': lon},
                    'stake': stake,
                    'elements': elements
                })
        
        elif query_type == 'range':
            parts = value.split('-')
            if len(parts) == 2:
                results = mapper.query_by_stake_range(parts[0], parts[1])
                return jsonify({
                    'range': value,
                    'results': results,
                    'count': len(results)
                })
        
        return jsonify({'error': 'invalid query'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/spatial/photo', methods=['POST'])
def photo_map():
    """照片GPS映射
    
    Request:
    {
        "lat": 31.235,
        "lon": 121.475,
        "content": "可选，照片内容描述"
    }
    """
    data = request.get_json() or {}
    gps = {'lat': data.get('lat'), 'lon': data.get('lon')}
    content = data.get('content')
    
    if not gps.get('lat') or not gps.get('lon'):
        return jsonify({'error': 'lat and lon required'}), 400
    
    result = mapper.map_photo_to_location(gps, content)
    return jsonify(result)


# ========== 启动 ==========

def run_server(host='0.0.0.0', port=5001):
    """启动服务器"""
    init_services()
    print(f"\n[OK] Starting server on http://{host}:{port}")
    app.run(host=host, port=port, debug=False)


if __name__ == '__main__':
    run_server()
