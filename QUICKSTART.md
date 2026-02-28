# Drawing 3D - Quick Start Guide

## 5-Minute Quick Start

### 1. Install Dependencies
```bash
cd F:\drawing_3d
pip install -r requirements.txt
```

### 2. Start Server
```bash
python server.py
```

### 3. Open Browser
Navigate to: http://localhost:5000

---

## Running Options

### Option 1: Web Server (Recommended)
```bash
python server.py
```
- Full features
- Web UI at http://localhost:5000
- API at http://localhost:5000/api/*

### Option 2: Simple Web
```bash
python web_server.py
```
- Basic web interface

### Option 3: Command Line
```bash
python cli.py
```
- Interactive terminal interface

### Option 4: Demo
```bash
python enhanced_core.py
```
- Run demo directly

---

## Docker Deployment

### Build & Run
```bash
# Build
docker build -t drawing3d .

# Run
docker-compose up -d

# Stop
docker-compose down
```

---

## API Examples

### Get Weather
```bash
curl "http://localhost:5000/api/weather?location=北京"
```

### Add Cost
```bash
curl -X POST "http://localhost:5000/api/cost/add" \
  -H "Content-Type: application/json" \
  -d '{"name": "水泥", "quantity": 100}'
```

### Ask AI
```bash
curl -X POST "http://localhost:5000/api/ai/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "项目进度如何？"}'
```

---

## Configuration

Edit `config.json` to customize:

```json
{
  "features": {
    "weather": true,
    "cost": true,
    "equipment": true,
    "report": true,
    "ai_qa": true
  },
  "debug": false,
  "log_level": "INFO"
}
```

---

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process
taskkill /PID <PID> /F
```

### Module Not Found
```bash
pip install -r requirements.txt
```

### Check Logs
```bash
tail -f logs/drawing3d_*.log
```

---

## Next Steps

1. Read [README.md](README.md) for overview
2. Check [API.md](API.md) for API docs
3. Review [CHANGELOG.md](CHANGELOG.md) for version history

---

*Quick Start Guide v1.0 - 2026-02-28*
