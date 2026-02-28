# -*- coding: utf-8 -*-
"""
Drawing 3D - Web Interface
Simple HTTP server for remote access
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# Import the main system
import sys
sys.path.insert(0, '.')
from main import Road3D

# Global road instance
road = Road3D()

# Setup demo data
for i in range(8):
    road.add_point(i, i * 100, i * 30)

road.add_knowledge("asphalt_temp", "150-170C")
road.add_knowledge("compaction", "95-98%")

road.add_progress(0, 1, "completed", 100)
road.add_progress(1, 2, "completed", 100)
road.add_progress(2, 3, "in_progress", 70)

road.add_material_cost('沥青', 500)
road.add_material_cost('水泥', 200)

road.add_device('压路机1', 'CAT', '压路机')
road.add_device('摊铺机1', 'VOGELE', '摊铺机')


class APIHandler(BaseHTTPRequestHandler):
    """HTTP API Handler"""
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(self.index_page().encode('utf-8'))
            
        elif self.path == '/api/progress':
            self.send_json({'progress': road.get_progress()})
            
        elif self.path == '/api/weather':
            w = road.get_weather()
            can, msg = road.can_construct_today()
            self.send_json({
                'weather': w['weather'],
                'temperature': w['temperature'],
                'can_construct': can,
                'message': msg
            })
            
        elif self.path == '/api/cost':
            c = road.get_cost_summary()
            self.send_json(c)
            
        elif self.path == '/api/equipment':
            e = road.get_device_utilization()
            self.send_json(e)
            
        elif self.path == '/api/report':
            self.send_json({
                'progress': road.get_progress(),
                'weather': road.get_weather(),
                'cost': road.get_cost_summary(),
                'equipment': road.get_device_utilization()
            })
            
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/api/ask':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode('utf-8')
            
            # Parse JSON
            try:
                data = json.loads(body)
                question = data.get('question', '')
                answer = road.ask(question)
                self.send_json({'answer': answer})
            except:
                self.send_error(400)
        else:
            self.send_error(404)
    
    def send_json(self, data):
        """Send JSON response"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def index_page(self):
        """Main page"""
        return """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Drawing 3D - NeuralSite Light</title>
    <style>
        body { font-family: Arial; margin: 40px; background: #f5f5f5; }
        h1 { color: #333; }
        .card { background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .stats { display: flex; gap: 20px; }
        .stat { flex: 1; text-align: center; padding: 20px; background: #f0f0f0; border-radius: 8px; }
        .stat-value { font-size: 32px; font-weight: bold; color: #4CAF50; }
        .stat-label { color: #666; }
        input, button { padding: 10px; font-size: 16px; }
        input { width: 60%; }
        button { background: #4CAF50; color: white; border: none; cursor: pointer; }
        button:hover { background: #45a049; }
        #answer { margin-top: 20px; padding: 20px; background: #e8f5e9; border-radius: 8px; }
    </style>
</head>
<body>
    <h1>Drawing 3D - NeuralSite Light</h1>
    
    <div class="card">
        <h2>Project Status</h2>
        <div class="stats">
            <div class="stat">
                <div class="stat-value" id="progress">--</div>
                <div class="stat-label">Progress %</div>
            </div>
            <div class="stat">
                <div class="stat-value" id="weather">--</div>
                <div class="stat-label">Weather</div>
            </div>
            <div class="stat">
                <div class="stat-value" id="cost">--</div>
                <div class="stat-label">Cost (K)</div>
            </div>
        </div>
    </div>
    
    <div class="card">
        <h2>AI Assistant</h2>
        <input type="text" id="question" placeholder="Ask something...">
        <button onclick="ask()">Ask</button>
        <div id="answer"></div>
    </div>
    
    <script>
        // Load initial data
        fetch('/api/progress').then(r=>r.json()).then(d=>{
            document.getElementById('progress').innerText = d.progress.toFixed(1) + '%';
        });
        
        fetch('/api/weather').then(r=>r.json()).then(d=>{
            document.getElementById('weather').innerText = d.temperature + 'C';
        });
        
        fetch('/api/cost').then(r=>r.json()).then(d=>{
            document.getElementById('cost').innerText = (d.total/1000).toFixed(0) + 'K';
        });
        
        function ask() {
            var q = document.getElementById('question').value;
            if (!q) return;
            
            fetch('/api/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({question: q})
            }).then(r=>r.json()).then(d=>{
                document.getElementById('answer').innerHTML = '<strong>AI:</strong> ' + d.answer.replace(/\\n/g, '<br>');
            });
        }
        
        // Enter key to ask
        document.getElementById('question').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') ask();
        });
    </script>
</body>
</html>"""


def run_server(port=8080):
    """Run the web server"""
    server = HTTPServer(('0.0.0.0', port), APIHandler)
    print(f"Server running at http://localhost:{port}")
    print("Press Ctrl+C to stop")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
