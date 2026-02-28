# -*- coding: utf-8 -*-
"""
Drawing 3D - Integrated Server
集成服务器 (完整版)
"""

from flask import Flask, render_template_string, request, jsonify
import os
import json

# 导入模块
from enhanced_core import Drawing3D
from logging_system import logger, log_request, log_response, log_error
from middleware import (
    handle_errors, request_logger, 
    validate_params, rate_limit, performance_monitor
)

# 创建Flask应用
app = Flask(__name__)

# 初始化系统
system = Drawing3D()

# 应用中间件
handle_errors(app)
request_logger(app)

# ==================== 前端页面 ====================

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Drawing 3D - 道路工程管理系统</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { color: white; text-align: center; margin-bottom: 30px; font-size: 2.5em; }
        .grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
            gap: 20px;
        }
        .card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .card h2 { 
            color: #333; 
            margin-bottom: 20px; 
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }
        .btn {
            display: inline-block;
            padding: 10px 20px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            margin: 5px;
            transition: all 0.3s;
        }
        .btn:hover { background: #764ba2; transform: translateY(-2px); }
        .btn-success { background: #10b981; }
        input, select {
            width: 100%;
            padding: 10px;
            margin: 5px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        .result { 
            margin-top: 15px; 
            padding: 15px; 
            background: #f3f4f6; 
            border-radius: 8px;
            white-space: pre-wrap;
            font-size: 0.9em;
        }
        .status { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 20px; }
        .status-item {
            padding: 5px 15px;
            background: #e5e7eb;
            border-radius: 20px;
            font-size: 0.9em;
        }
        .status-item.active { background: #10b981; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🛣️ Drawing 3D - 道路工程管理系统</h1>
        
        <div class="grid">
            <!-- 天气系统 -->
            <div class="card">
                <h2>🌤️ 天气查询</h2>
                <input type="text" id="weatherLocation" placeholder="地点" value="北京">
                <button class="btn" onclick="getWeather()">查询</button>
                <div id="weatherResult" class="result"></div>
            </div>
            
            <!-- 成本管理 -->
            <div class="card">
                <h2>💰 成本管理</h2>
                <input type="text" id="costName" placeholder="材料名称">
                <input type="number" id="costQty" placeholder="数量">
                <button class="btn btn-success" onclick="addCost()">添加</button>
                <button class="btn" onclick="getCostSummary()">汇总</button>
                <div id="costResult" class="result"></div>
            </div>
            
            <!-- 设备管理 -->
            <div class="card">
                <h2>🔧 设备管理</h2>
                <input type="text" id="deviceName" placeholder="设备名称">
                <input type="text" id="deviceType" placeholder="设备类型">
                <button class="btn btn-success" onclick="addDevice()">添加</button>
                <button class="btn" onclick="getDevices()">列表</button>
                <div id="deviceResult" class="result"></div>
            </div>
            
            <!-- 报告生成 -->
            <div class="card">
                <h2>📊 报告生成</h2>
                <select id="reportType">
                    <option value="daily">日报</option>
                    <option value="weekly">周报</option>
                    <option value="monthly">月报</option>
                </select>
                <button class="btn" onclick="generateReport()">生成</button>
                <div id="reportResult" class="result"></div>
            </div>
            
            <!-- AI问答 -->
            <div class="card">
                <h2>🤖 AI问答</h2>
                <input type="text" id="aiQuestion" placeholder="请输入问题">
                <button class="btn" onclick="askAI()">提问</button>
                <div id="aiResult" class="result"></div>
            </div>
            
            <!-- 系统状态 -->
            <div class="card">
                <h2>⚙️ 系统状态</h2>
                <div class="status">
                    <span class="status-item {{'active' if weather else ''}}">天气</span>
                    <span class="status-item {{'active' if cost else ''}}">成本</span>
                    <span class="status-item {{'active' if equipment else ''}}">设备</span>
                    <span class="status-item {{'active' if report else ''}}">报告</span>
                    <span class="status-item {{'active' if ai_qa else ''}}">AI</span>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function getWeather() {
            fetch('/api/weather?location=' + encodeURIComponent(document.getElementById('weatherLocation').value))
                .then(r => r.json()).then(d => document.getElementById('weatherResult').textContent = JSON.stringify(d, null, 2));
        }
        function addCost() {
            fetch('/api/cost/add', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    name: document.getElementById('costName').value,
                    quantity: parseFloat(document.getElementById('costQty').value)
                })
            }).then(r => r.json()).then(d => document.getElementById('costResult').textContent = JSON.stringify(d, null, 2));
        }
        function getCostSummary() {
            fetch('/api/cost/summary').then(r => r.json()).then(d => document.getElementById('costResult').textContent = JSON.stringify(d, null, 2));
        }
        function addDevice() {
            fetch('/api/device/add', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    name: document.getElementById('deviceName').value,
                    device_type: document.getElementById('deviceType').value
                })
            }).then(r => r.json()).then(d => document.getElementById('deviceResult').textContent = JSON.stringify(d, null, 2));
        }
        function getDevices() {
            fetch('/api/devices').then(r => r.json()).then(d => document.getElementById('deviceResult').textContent = JSON.stringify(d, null, 2));
        }
        function generateReport() {
            fetch('/api/report/generate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({report_type: document.getElementById('reportType').value})
            }).then(r => r.json()).then(d => document.getElementById('reportResult').textContent = JSON.stringify(d, null, 2));
        }
        function askAI() {
            fetch('/api/ai/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({question: document.getElementById('aiQuestion').value})
            }).then(r => r.json()).then(d => document.getElementById('aiResult').textContent = d.answer);
        }
    </script>
</body>
</html>
'''


# ==================== 路由 ====================

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE,
        weather=system.weather is not None,
        cost=system.cost is not None,
        equipment=system.equipment is not None,
        report=system.report is not None,
        ai_qa=system.ai_qa is not None
    )


@app.route('/api/weather')
@performance_monitor
def api_weather():
    location = request.args.get('location', '北京')
    weather = system.weather.get_current(location)
    impact = system.weather.analyze_impact(weather)
    return jsonify({'weather': weather, 'impact': impact})


@app.route('/api/cost/add', methods=['POST'])
@validate_params(['name', 'quantity'])
@performance_monitor
def api_cost_add():
    data = request.json
    record = system.cost.add_material(data['name'], data['quantity'])
    return jsonify(record)


@app.route('/api/cost/summary')
@performance_monitor
def api_cost_summary():
    return jsonify(system.cost.get_summary())


@app.route('/api/device/add', methods=['POST'])
@validate_params(['name', 'device_type'])
@performance_monitor
def api_device_add():
    data = request.json
    device = system.equipment.add_device(data['name'], data['device_type'])
    return jsonify(device)


@app.route('/api/devices')
@performance_monitor
def api_devices():
    return jsonify(system.equipment.devices)


@app.route('/api/report/generate', methods=['POST'])
@validate_params(['report_type'])
@performance_monitor
def api_report_generate():
    data = request.json
    report = system.report.generate(data['report_type'])
    return jsonify(report)


@app.route('/api/ai/ask', methods=['POST'])
@validate_params(['question'])
@performance_monitor
def api_ai_ask():
    data = request.json
    answer = system.ai_qa.ask(data['question'])
    return jsonify({'answer': answer})


# ==================== 运行 ====================

def run_server(host='0.0.0.0', port=5000):
    """运行服务器"""
    logger.info(f"Starting Drawing 3D Server on {host}:{port}")
    
    print(f"\n{'='*50}")
    print(f"Drawing 3D - Integrated Server")
    print(f"Web: http://localhost:{port}")
    print(f"API Docs: http://localhost:{port}/api.md")
    print(f"{'='*50}\n")
    
    app.run(host=host, port=port, debug=False)


if __name__ == '__main__':
    run_server()
