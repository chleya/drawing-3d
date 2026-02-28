# -*- coding: utf-8 -*-
"""
Drawing 3D - 完整集成系统
Complete Integration System
整合所有模块
"""

from flask import Flask, render_template_string, request, jsonify
import os
import json

# 导入所有模块
from enhanced_core import Drawing3D
from logging_system import logger
from middleware import handle_errors, request_logger
from compliance_assistant import ComplianceSystem
from drone_inspection import DroneInspection, IssueDetector
from material_scheduling import Inventory, Scheduler
from ar_view_system import ARViewSystem

# 创建Flask应用
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# 初始化所有系统
drawing3d = Drawing3D()
compliance = ComplianceSystem()
drone = DroneInspection()
inventory = Inventory()
scheduler = Scheduler(inventory)
ar_view = ARViewSystem()

# 应用中间件
handle_errors(app)
request_logger(app)

# ==================== HTML模板 ====================

HTML = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Drawing 3D - 道路工程管理系统</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, sans-serif; background: #f5f5f5; }
        .header { background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 20px; text-align: center; }
        .header h1 { font-size: 2em; }
        .nav { background: #333; padding: 10px; text-align: center; }
        .nav a { color: white; margin: 0 15px; text-decoration: none; padding: 8px 16px; border-radius: 4px; }
        .nav a:hover, .nav a.active { background: #667eea; }
        .container { max-width: 1400px; margin: 20px auto; padding: 0 20px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; }
        .card { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .card h2 { color: #333; border-bottom: 2px solid #667eea; padding-bottom: 10px; margin-bottom: 15px; }
        .btn { display: inline-block; padding: 8px 16px; background: #667eea; color: white; border: none; border-radius: 6px; cursor: pointer; margin: 3px; }
        .btn:hover { background: #764ba2; }
        .btn-success { background: #10b981; }
        .btn-danger { background: #ef4444; }
        .btn-warning { background: #f59e0b; }
        input, select { width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 6px; }
        .result { margin-top: 15px; padding: 15px; background: #f9fafb; border-radius: 8px; white-space: pre-wrap; font-size: 0.9em; max-height: 300px; overflow-y: auto; }
        .status { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 10px; }
        .status-item { padding: 5px 12px; background: #e5e7eb; border-radius: 20px; font-size: 0.85em; }
        .status-item.active { background: #10b981; color: white; }
        .badge { display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 0.8em; }
        .badge-high { background: #ef4444; color: white; }
        .badge-medium { background: #f59e0b; color: white; }
        .badge-low { background: #10b981; color: white; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🛣️ Drawing 3D - 道路工程管理系统</h1>
        <p>集成所有功能的完整版本</p>
    </div>
    <div class="nav">
        <a href="#weather" class="active" onclick="showSection('weather')">🌤️ 天气</a>
        <a href="#cost" onclick="showSection('cost')">💰 成本</a>
        <a href="#equipment" onclick="showSection('equipment')">🔧 设备</a>
        <a href="#compliance" onclick="showSection('compliance')">📋 合规</a>
        <a href="#drone" onclick="showSection('drone')">🚁 无人机</a>
        <a href="#material" onclick="showSection('material')">📦 材料</a>
        <a href="#ar" onclick="showSection('ar')">📱 AR</a>
        <a href="#report" onclick="showSection('report')">📊 报告</a>
    </div>
    
    <div class="container">
        <div class="grid">
            <!-- 天气系统 -->
            <div class="card" id="weather-section">
                <h2>🌤️ 天气查询</h2>
                <input type="text" id="weatherLocation" placeholder="地点" value="北京">
                <button class="btn" onclick="getWeather()">查询天气</button>
                <button class="btn" onclick="getWeatherImpact()">影响分析</button>
                <div id="weatherResult" class="result"></div>
            </div>
            
            <!-- 成本管理 -->
            <div class="card" id="cost-section">
                <h2>💰 成本管理</h2>
                <input type="text" id="costName" placeholder="材料名称">
                <input type="number" id="costQty" placeholder="数量">
                <button class="btn btn-success" onclick="addCost()">添加成本</button>
                <button class="btn" onclick="getCostSummary()">成本汇总</button>
                <div id="costResult" class="result"></div>
            </div>
            
            <!-- 设备管理 -->
            <div class="card" id="equipment-section">
                <h2>🔧 设备管理</h2>
                <input type="text" id="deviceName" placeholder="设备名称">
                <input type="text" id="deviceType" placeholder="设备类型">
                <button class="btn btn-success" onclick="addDevice()">添加设备</button>
                <button class="btn" onclick="getDevices()">设备列表</button>
                <div id="deviceResult" class="result"></div>
            </div>
            
            <!-- 合规助手 -->
            <div class="card" id="compliance-section">
                <h2>📋 合规助手</h2>
                <button class="btn" onclick="getComplianceRules()">查看规则</button>
                <button class="btn btn-warning" onclick="checkCompliance()">合规检查</button>
                <button class="btn" onclick="getComplianceRate()">合规率</button>
                <div id="complianceResult" class="result"></div>
            </div>
            
            <!-- 无人机巡检 -->
            <div class="card" id="drone-section">
                <h2>🚁 无人机巡检</h2>
                <button class="btn btn-success" onclick="startDroneFlight()">开始飞行</button>
                <button class="btn" onclick="droneDetect()">问题检测</button>
                <button class="btn" onclick="getDroneReport()">巡检报告</button>
                <div id="droneResult" class="result"></div>
            </div>
            
            <!-- 材料调度 -->
            <div class="card" id="material-section">
                <h2>📦 材料调度</h2>
                <button class="btn" onclick="getMaterialStock()">库存查询</button>
                <button class="btn btn-success" onclick="suggestOrder()">推荐采购</button>
                <button class="btn" onclick="createAllocation()">创建配送</button>
                <div id="materialResult" class="result"></div>
            </div>
            
            <!-- AR视图 -->
            <div class="card" id="ar-section">
                <h2>📱 AR视图</h2>
                <button class="btn btn-success" onclick="createARScene()">创建场景</button>
                <button class="btn" onclick="addARMarker()">添加标记</button>
                <button class="btn" onclick="getAROverview()">场景概览</button>
                <div id="arResult" class="result"></div>
            </div>
            
            <!-- 报告系统 -->
            <div class="card" id="report-section">
                <h2>📊 报告中心</h2>
                <select id="reportType">
                    <option value="daily">日报</option>
                    <option value="weekly">周报</option>
                    <option value="monthly">月报</option>
                </select>
                <button class="btn" onclick="generateReport()">生成报告</button>
                <button class="btn" onclick="getAllStats()">综合统计</button>
                <div id="reportResult" class="result"></div>
            </div>
        </div>
    </div>
    
    <script>
        function showSection(id) {
            document.querySelectorAll('.card').forEach(c => c.style.display = 'none');
            document.getElementById(id + '-section').style.display = 'block';
            event.target.classList.add('active');
        }
        
        // Weather
        function getWeather() {
            fetch('/api/weather?location=' + encodeURIComponent(document.getElementById('weatherLocation').value))
                .then(r => r.json()).then(d => document.getElementById('weatherResult').textContent = JSON.stringify(d, null, 2));
        }
        function getWeatherImpact() {
            fetch('/api/weather/impact?location=' + encodeURIComponent(document.getElementById('weatherLocation').value))
                .then(r => r.json()).then(d => document.getElementById('weatherResult').textContent = JSON.stringify(d, null, 2));
        }
        
        // Cost
        function addCost() {
            fetch('/api/cost/add', { method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name: document.getElementById('costName').value, quantity: parseFloat(document.getElementById('costQty').value)})})
                .then(r => r.json()).then(d => document.getElementById('costResult').textContent = JSON.stringify(d, null, 2));
        }
        function getCostSummary() {
            fetch('/api/cost/summary').then(r => r.json()).then(d => document.getElementById('costResult').textContent = JSON.stringify(d, null, 2));
        }
        
        // Equipment
        function addDevice() {
            fetch('/api/device/add', { method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name: document.getElementById('deviceName').value, device_type: document.getElementById('deviceType').value)})})
                .then(r => r.json()).then(d => document.getElementById('deviceResult').textContent = JSON.stringify(d, null, 2));
        }
        function getDevices() {
            fetch('/api/devices').then(r => r.json()).then(d => document.getElementById('deviceResult').textContent = JSON.stringify(d, null, 2));
        }
        
        // Compliance
        function getComplianceRules() {
            fetch('/api/compliance/rules').then(r => r.json()).then(d => document.getElementById('complianceResult').textContent = JSON.stringify(d, null, 2));
        }
        function checkCompliance() {
            fetch('/api/compliance/check', { method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({check_item: '高空作业', check_point: '安全带'})})
                .then(r => r.json()).then(d => document.getElementById('complianceResult').textContent = JSON.stringify(d, null, 2));
        }
        function getComplianceRate() {
            fetch('/api/compliance/rate').then(r => r.json()).then(d => document.getElementById('complianceResult').textContent = JSON.stringify(d, null, 2));
        }
        
        // Drone
        let currentFlight = null;
        function startDroneFlight() {
            fetch('/api/drone/flight/start', { method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({location: 'K100+500', altitude: 50})})
                .then(r => r.json()).then(d => { currentFlight = d.id; document.getElementById('droneResult').textContent = JSON.stringify(d, null, 2); });
        }
        function droneDetect() {
            fetch('/api/drone/detect', { method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({flight_id: currentFlight || 1})})
                .then(r => r.json()).then(d => document.getElementById('droneResult').textContent = JSON.stringify(d, null, 2));
        }
        function getDroneReport() {
            fetch('/api/drone/report').then(r => r.json()).then(d => document.getElementById('droneResult').textContent = JSON.stringify(d, null, 2));
        }
        
        // Material
        function getMaterialStock() {
            fetch('/api/material/stock').then(r => r.json()).then(d => document.getElementById('materialResult').textContent = JSON.stringify(d, null, 2));
        }
        function suggestOrder() {
            fetch('/api/material/suggest').then(r => r.json()).then(d => document.getElementById('materialResult').textContent = JSON.stringify(d, null, 2));
        }
        function createAllocation() {
            fetch('/api/material/allocation', { method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({material_id: 'M001', quantity: 10, location: 'K100+500'})})
                .then(r => r.json()).then(d => document.getElementById('materialResult').textContent = JSON.stringify(d, null, 2));
        }
        
        // AR
        let currentScene = null;
        function createARScene() {
            fetch('/api/ar/scene', { method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name: 'K100+500施工现场', location: 'K100+500'})})
                .then(r => r.json()).then(d => { currentScene = d.id; document.getElementById('arResult').textContent = JSON.stringify(d, null, 2); });
        }
        function addARMarker() {
            fetch('/api/ar/marker', { method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({scene_id: currentScene || 'S001', name: '进度', content: '完成80%', marker_type: 'info'})})
                .then(r => r.json()).then(d => document.getElementById('arResult').textContent = JSON.stringify(d, null, 2));
        }
        function getAROverview() {
            fetch('/api/ar/overview?scene_id=' + (currentScene || 'S001'))
                .then(r => r.json()).then(d => document.getElementById('arResult').textContent = JSON.stringify(d, null, 2));
        }
        
        // Report
        function generateReport() {
            fetch('/api/report/generate', { method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({report_type: document.getElementById('reportType').value})})
                .then(r => r.json()).then(d => document.getElementById('reportResult').textContent = JSON.stringify(d, null, 2));
        }
        function getAllStats() {
            fetch('/api/stats/all').then(r => r.json()).then(d => document.getElementById('reportResult').textContent = JSON.stringify(d, null, 2));
        }
    </script>
</body>
</html>
'''


# ==================== API路由 ====================

@app.route('/')
def index():
    return render_template_string(HTML)


# 天气API
@app.route('/api/weather')
def api_weather():
    location = request.args.get('location', '北京')
    weather = drawing3d.weather.get_current(location)
    return jsonify(weather)


@app.route('/api/weather/impact')
def api_weather_impact():
    location = request.args.get('location', '北京')
    weather = drawing3d.weather.get_current(location)
    impact = drawing3d.weather.analyze_impact(weather)
    return jsonify({'weather': weather, 'impact': impact})


# 成本API
@app.route('/api/cost/add', methods=['POST'])
def api_cost_add():
    data = request.json
    record = drawing3d.cost.add_material(data.get('name', ''), data.get('quantity', 0))
    return jsonify(record)


@app.route('/api/cost/summary')
def api_cost_summary():
    return jsonify(drawing3d.cost.get_summary())


# 设备API
@app.route('/api/device/add', methods=['POST'])
def api_device_add():
    data = request.json
    device = drawing3d.equipment.add_device(data.get('name', ''), data.get('device_type', ''))
    return jsonify(device)


@app.route('/api/devices')
def api_devices():
    return jsonify(drawing3d.equipment.devices)


# 合规API
@app.route('/api/compliance/rules')
def api_compliance_rules():
    rules = compliance.get_rules()
    return jsonify([{
        'id': r.id, 'category': r.category, 'title': r.title,
        'severity': r.severity, 'content': r.content
    } for r in rules])


@app.route('/api/compliance/check', methods=['POST'])
def api_compliance_check():
    data = request.json
    result = compliance.check_compliance(
        data.get('check_item', ''),
        data.get('check_point', '')
    )
    return jsonify(result)


@app.route('/api/compliance/rate')
def api_compliance_rate():
    return jsonify({'compliance_rate': compliance.get_compliance_rate()})


# 无人机API
@app.route('/api/drone/flight/start', methods=['POST'])
def api_drone_start():
    data = request.json
    flight = drone.start_flight(
        data.get('location', 'K100+500'),
        data.get('altitude', 50),
        data.get('duration', 30)
    )
    return jsonify(flight)


@app.route('/api/drone/detect', methods=['POST'])
def api_drone_detect():
    data = request.json
    detection = IssueDetector.detect_from_image()
    issue = drone.detect_issue(
        data.get('flight_id', 1),
        detection['category'],
        detection['issue'],
        detection['severity']
    )
    return jsonify({'detection': detection, 'issue': issue})


@app.route('/api/drone/report')
def api_drone_report():
    return jsonify(drone.generate_report())


# 材料API
@app.route('/api/material/stock')
def api_material_stock():
    stocks = inventory.get_stock()
    return jsonify({mid: {
        'name': info['material'].name,
        'quantity': info['quantity'],
        'unit': info['material'].unit,
        'status': info['status']
    } for mid, info in stocks.items()})


@app.route('/api/material/suggest')
def api_material_suggest():
    return jsonify(scheduler.suggest_orders())


@app.route('/api/material/allocation', methods=['POST'])
def api_material_allocation():
    data = request.json
    allocation = scheduler.create_allocation(
        data.get('material_id', 'M001'),
        data.get('quantity', 10),
        data.get('location', ''),
        data.get('purpose', '')
    )
    return jsonify(allocation)


# AR API
@app.route('/api/ar/scene', methods=['POST'])
def api_ar_scene():
    data = request.json
    scene = ar_view.create_scene(
        f"S{len(ar_view.scenes) + 1:03d}",
        data.get('name', '新场景'),
        data.get('location', '')
    )
    return jsonify({'id': scene.id, 'name': scene.name, 'location': scene.location})


@app.route('/api/ar/marker', methods=['POST'])
def api_ar_marker():
    data = request.json
    marker = ar_view.add_info_marker(
        data.get('scene_id', 'S001'),
        data.get('name', '标记'),
        data.get('x', 0), data.get('y', 0), data.get('z', 0),
        data.get('content', '')
    )
    return jsonify({'id': marker.id, 'name': marker.name})


@app.route('/api/ar/overview')
def api_ar_overview():
    scene_id = request.args.get('scene_id', 'S001')
    overview = ar_view.generate_overview(scene_id)
    return jsonify(overview or {'error': 'Scene not found'})


# 报告API
@app.route('/api/report/generate', methods=['POST'])
def api_report_generate():
    data = request.json
    report = drawing3d.report.generate(data.get('report_type', 'daily'))
    return jsonify(report)


@app.route('/api/stats/all')
def api_stats_all():
    return jsonify({
        'weather': 'ok' if drawing3d.weather else 'disabled',
        'cost': drawing3d.cost.get_summary(),
        'equipment': drawing3d.equipment.get_status(),
        'compliance': compliance.generate_report(),
        'drone': drone.generate_report(),
        'material': {
            'total_types': len(inventory.materials),
            'pending_orders': len(scheduler.get_pending_orders())
        }
    })


# ==================== 运行 ====================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Drawing 3D - Complete Integration System")
    print("All modules integrated")
    print("="*60)
    print("\nOpen: http://localhost:5000\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
