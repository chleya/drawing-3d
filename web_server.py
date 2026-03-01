# -*- coding: utf-8 -*-
"""
Drawing 3D - Web Interface
Web界面
"""

from flask import Flask, render_template_string, request, jsonify, Response
import os
import json
import cv2
from datetime import datetime

app = Flask(__name__)

# 导入核心模块
from enhanced_core import Drawing3D, WeatherSystem, CostSystem, EquipmentSystem, ReportSystem, AIQAV2

# 初始化系统
system = Drawing3D()

# YOLO检测器
yolo_detector = None

def get_yolo():
    """获取YOLO检测器"""
    global yolo_detector
    if yolo_detector is None:
        from yolo_detector import YOLODetector
        yolo_detector = YOLODetector()
        yolo_detector.load_model()
    return yolo_detector

# 摄像头配置
CAMERA_URL = 0  # 默认使用摄像头0

# HTML模板
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
        .btn-danger { background: #ef4444; }
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
        }
        .status { 
            display: flex; 
            gap: 10px; 
            flex-wrap: wrap; 
        }
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
                <button class="btn" onclick="getWeather()">查询天气</button>
                <div id="weatherResult" class="result"></div>
            </div>
            
            <!-- 成本管理 -->
            <div class="card">
                <h2>💰 成本管理</h2>
                <input type="text" id="costName" placeholder="材料名称">
                <input type="number" id="costQty" placeholder="数量">
                <button class="btn btn-success" onclick="addCost()">添加成本</button>
                <button class="btn" onclick="getCostSummary()">查看汇总</button>
                <div id="costResult" class="result"></div>
            </div>
            
            <!-- 设备管理 -->
            <div class="card">
                <h2>🔧 设备管理</h2>
                <input type="text" id="deviceName" placeholder="设备名称">
                <input type="text" id="deviceType" placeholder="设备类型">
                <button class="btn btn-success" onclick="addDevice()">添加设备</button>
                <button class="btn" onclick="getDevices()">设备列表</button>
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
                <button class="btn" onclick="generateReport()">生成报告</button>
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
                    <span class="status-item {{'active' if weather else ''}}">天气: {{'✓' if weather else '✗'}}</span>
                    <span class="status-item {{'active' if cost else ''}}">成本: {{'✓' if cost else '✗'}}</span>
                    <span class="status-item {{'active' if equipment else ''}}">设备: {{'✓' if equipment else '✗'}}</span>
                    <span class="status-item {{'active' if report else ''}}">报告: {{'✓' if report else '✗'}}</span>
                    <span class="status-item {{'active' if ai_qa else ''}}">AI: {{'✓' if ai_qa else '✗'}}</span>
                </div>
            </div>
            
            <!-- 实时视频监控 -->
            <div class="card" style="grid-column: 1 / -1;">
                <h2>📹 实时视频监控 (YOLO)</h2>
                <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                    <div style="flex: 1; min-width: 400px;">
                        <img src="/video_feed" style="width: 100%; border-radius: 10px; border: 2px solid #667eea;">
                    </div>
                    <div style="flex: 0 0 250px;">
                        <h3>📊 实时统计</h3>
                        <div id="cameraStats" style="background: #f5f5f5; padding: 15px; border-radius: 10px; margin-top: 10px;">
                            <p>人员检测: <span id="personCount" style="font-size: 24px; color: #667eea; font-weight: bold;">0</span></p>
                            <p>总检测数: <span id="detectionCount" style="font-size: 24px; color: #764ba2; font-weight: bold;">0</span></p>
                            <p>帧数: <span id="frameCount">0</span></p>
                        </div>
                        <div id="alertBox" style="background: #ff4444; color: white; padding: 15px; border-radius: 10px; margin-top: 15px; display: none;">
                            <h4>⚠️ 安全提醒</h4>
                            <p id="alertMsg">检测到人员，请确认安全帽佩戴！</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // 定时获取摄像头统计
        setInterval(function() {
            fetch('/api/camera/stats')
                .then(r => r.json())
                .then(d => {
                    if (d.status === 'ok') {
                        const stats = d.detector_stats;
                        document.getElementById('personCount').textContent = stats.persons || 0;
                        document.getElementById('detectionCount').textContent = stats.total_detections || 0;
                        document.getElementById('frameCount').textContent = stats.total_frames || 0;
                        
                        // 显示报警
                        const alertBox = document.getElementById('alertBox');
                        if (stats.persons > 0) {
                            alertBox.style.display = 'block';
                            console.log('⚠️ 检测到工人，请确认安全帽');
                        } else {
                            alertBox.style.display = 'none';
                        }
                    }
                });
        }, 1000);
        
        function getWeather() {
            const location = document.getElementById('weatherLocation').value;
            fetch('/api/weather?location=' + encodeURIComponent(location))
                .then(r => r.json())
                .then(d => {
                    document.getElementById('weatherResult').textContent = JSON.stringify(d, null, 2);
                });
        }
        
        function addCost() {
            const name = document.getElementById('costName').value;
            const qty = parseFloat(document.getElementById('costQty').value);
            fetch('/api/cost/add', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name, quantity: qty})
            }).then(r => r.json()).then(d => {
                document.getElementById('costResult').textContent = JSON.stringify(d, null, 2);
            });
        }
        
        function getCostSummary() {
            fetch('/api/cost/summary').then(r => r.json()).then(d => {
                document.getElementById('costResult').textContent = JSON.stringify(d, null, 2);
            });
        }
        
        function addDevice() {
            const name = document.getElementById('deviceName').value;
            const device_type = document.getElementById('deviceType').value;
            fetch('/api/device/add', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name, device_type})
            }).then(r => r.json()).then(d => {
                document.getElementById('deviceResult').textContent = JSON.stringify(d, null, 2);
            });
        }
        
        function getDevices() {
            fetch('/api/devices').then(r => r.json()).then(d => {
                document.getElementById('deviceResult').textContent = JSON.stringify(d, null, 2);
            });
        }
        
        function generateReport() {
            const report_type = document.getElementById('reportType').value;
            fetch('/api/report/generate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({report_type})
            }).then(r => r.json()).then(d => {
                document.getElementById('reportResult').textContent = JSON.stringify(d, null, 2);
            });
        }
        
        function askAI() {
            const question = document.getElementById('aiQuestion').value;
            fetch('/api/ai/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({question})
            }).then(r => r.json()).then(d => {
                document.getElementById('aiResult').textContent = d.answer;
            });
        }
    </script>
</body>
</html>
'''


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
def api_weather():
    location = request.args.get('location', '北京')
    weather = system.weather.get_current(location)
    impact = system.weather.analyze_impact(weather)
    return jsonify({'weather': weather, 'impact': impact})


@app.route('/api/cost/add', methods=['POST'])
def api_cost_add():
    data = request.json
    record = system.cost.add_material(data['name'], data['quantity'])
    return jsonify(record)


@app.route('/api/cost/summary')
def api_cost_summary():
    return jsonify(system.cost.get_summary())


@app.route('/api/device/add', methods=['POST'])
def api_device_add():
    data = request.json
    device = system.equipment.add_device(data['name'], data['device_type'])
    return jsonify(device)


@app.route('/api/devices')
def api_devices():
    return jsonify(system.equipment.devices)


@app.route('/api/report/generate', methods=['POST'])
def api_report_generate():
    data = request.json
    report = system.report.generate(data['report_type'])
    return jsonify(report)


@app.route('/api/ai/ask', methods=['POST'])
def api_ai_ask():
    data = request.json
    answer = system.ai_qa.ask(data['question'])
    return jsonify({'answer': answer})


# ==================== YOLO 安全检测API ====================

@app.route('/api/safety', methods=['POST'])
def api_safety():
    """YOLO安全检测API"""
    data = request.json
    source = data.get('source', 'data/test_video.mp4')
    is_video = data.get('is_video', False)
    
    try:
        # 导入YOLO检测器
        from yolo_detector import YOLODetector
        
        detector = YOLODetector()
        detector.load_model()
        
        if is_video:
            # 视频检测
            result = detector.process_video(source, max_frames=100)
        else:
            # 图像检测
            import cv2
            frame = cv2.imread(source)
            if frame is None:
                return jsonify({'error': f'Cannot read image: {source}'}), 400
            
            detections = detector.detect_frame(frame)
            
            # 统计
            class_counts = {}
            for det in detections:
                cls = det.get('class_name', 'unknown')
                class_counts[cls] = class_counts.get(cls, 0) + 1
            
            result = {
                'source': source,
                'detections': detections,
                'count': len(detections),
                'class_counts': class_counts,
                'persons': class_counts.get('person', 0),
            }
        
        return jsonify({
            'status': 'success',
            'result': result,
            'stats': detector.get_stats()
        })
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/safety/stats')
def api_safety_stats():
    """获取安全检测统计"""
    return jsonify({
        'status': 'ok',
        'message': 'YOLO detector ready'
    })


# ==================== Firecrawl Web Scraper API ====================

@app.route('/api/scrape', methods=['POST'])
def api_scrape():
    """网页爬取API"""
    data = request.json
    url = data.get('url', '')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        from web_scraper import WebScraper
        scraper = WebScraper()
        result = scraper.scrape(url)
        return jsonify(result)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/search', methods=['POST'])
def api_search():
    """网页搜索API"""
    data = request.json
    query = data.get('query', '')
    limit = data.get('limit', 5)
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    try:
        from web_scraper import WebScraper
        scraper = WebScraper()
        result = scraper.search(query, limit=limit)
        return jsonify(result)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ==================== Real-time Camera Feed ====================

@app.route('/video_feed')
def video_feed():
    """实时摄像头流 + YOLO检测"""
    def gen_frames():
        camera_url = CAMERA_URL
        cap = cv2.VideoCapture(camera_url)
        
        if not cap.isOpened():
            # 发送错误帧
            error_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(error_frame, "Camera not available", (150, 240), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            ret, buffer = cv2.imencode('.jpg', error_frame)
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            return
        
        detector = get_yolo()
        
        while True:
            success, frame = cap.read()
            if not success:
                break
            
            # YOLO实时检测
            try:
                detections = detector.detect_frame(frame)
                annotated = detector.draw_detections(frame, detections)
            except:
                annotated = frame
            
            # 转为JPEG流
            ret, buffer = cv2.imencode('.jpg', annotated)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
        cap.release()
    
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/api/start_camera', methods=['POST'])
def start_camera():
    """启动摄像头检测"""
    data = request.json
    camera_url = data.get('camera_url', CAMERA_URL)
    
    # 可以在这里添加后台处理逻辑
    return jsonify({
        "status": "camera_started",
        "url": str(camera_url),
        "video_feed": "/video_feed"
    })


@app.route('/api/camera/stats')
def camera_stats():
    """获取摄像头统计"""
    detector = get_yolo()
    stats = detector.get_stats()
    return jsonify({
        'status': 'ok',
        'camera_url': str(CAMERA_URL),
        'detector_stats': stats
    })


# ==================== Drone Routes ====================

@app.route('/drone')
def drone_view():
    """无人机视角页面"""
    return '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NeuralSite - 无人机视角</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            padding: 20px;
            color: white;
        }
        h1 { text-align: center; margin-bottom: 30px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .grid { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; }
        .card {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
        }
        img { width: 100%; border-radius: 10px; }
        #progressLog {
            background: rgba(0,0,0,0.3);
            padding: 15px;
            border-radius: 10px;
            max-height: 400px;
            overflow-y: auto;
            font-family: monospace;
            font-size: 12px;
        }
        .log-item { padding: 5px 0; border-bottom: 1px solid rgba(255,255,255,0.1); }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚁 NeuralSite - 无人机视角监控</h1>
        <div class="grid">
            <div class="card">
                <h2>📹 实时视频流</h2>
                <img src="/drone_feed" />
            </div>
            <div class="card">
                <h2>📊 宏观进度识别</h2>
                <div id="progressLog">加载中...</div>
            </div>
        </div>
    </div>
    <script>
        setInterval(function() {
            fetch('/api/drone_progress')
                .then(r => r.json())
                .then(data => {
                    const log = document.getElementById('progressLog');
                    if (data.length > 0) {
                        log.innerHTML = data.slice(-10).map(d => 
                            `<div class="log-item">帧${d.frame}: ${d.persons}人, ${d.vehicles}车, 进度${d.progress_estimate}</div>`
                        ).join('');
                    }
                });
        }, 3000);
    </script>
</body>
</html>
'''


@app.route('/drone_feed')
def drone_feed():
    """无人机视频流"""
    def gen_frames():
        cap = cv2.VideoCapture("data/test_video.mp4")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 循环播放
                continue
            
            # YOLO检测
            try:
                detector = get_yolo()
                detections = detector.detect_frame(frame)
                annotated = detector.draw_detections(frame, detections)
            except:
                annotated = frame
            
            # 转为JPEG流
            ret, buffer = cv2.imencode('.jpg', annotated)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
        cap.release()
    
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/api/drone_progress')
def api_drone_progress():
    """获取无人机进度"""
    import json
    try:
        with open("data/drone_progress.jsonl", "r", encoding="utf-8") as f:
            lines = f.readlines()[-10:]  # 最近10条
        data = [json.loads(line.strip()) for line in lines if line.strip()]
        return jsonify(data)
    except:
        return jsonify([])


import numpy as np

def run_server(host='0.0.0.0', port=5000):
    """运行服务器"""
    print(f"\n{'='*50}")
    print(f"Drawing 3D Web Interface")
    print(f"http://localhost:{port}")
    print(f"{'='*50}\n")
    app.run(host=host, port=port, debug=True)


if __name__ == '__main__':
    run_server()
