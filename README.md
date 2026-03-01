# Drawing 3D - NeuralSite Light

Road Engineering Management System (Light Version)

## 阶段1 完成 (2026-03-01)

**全视之眼 - 感知基础设施** ✅

### Demo视频

> 阶段1最终Demo录制中...
> 视频将展示：地面实时监控 + 无人机视角 + 全链路数据流

### 访问

- **地面视图**: http://localhost:5000
- **无人机视图**: http://localhost:5000/drone

---

## Features

- **Weather System**: Real-time weather, construction impact analysis
- **Cost Management**: Material, labor, equipment costs
- **Equipment Scheduling**: Device tracking, utilization
- **Report Generation**: Daily, weekly, monthly reports
- **AI Q&A**: Intelligent Q&A with context understanding
- **Web Interface**: Browser-based management UI
- **Data Persistence**: Save and load project data

## Quick Start

```bash
cd F:\drawing_3d
python main_improved.py      # Basic version
python cli.py                # Command line interface
python web_server.py         # Web interface (http://localhost:5000)
python enhanced_core.py      # Enhanced core modules
```

## Modules

| Module | File | Description |
|--------|------|-------------|
| Enhanced Core | enhanced_core.py | All core systems |
| Web Interface | web_server.py | Flask web UI |
| CLI | cli.py | Command line interface |
| Persistence | persistence_enhanced.py | Data storage |
| Config | config.json | Configuration |

## Architecture

```
Drawing 3D
├── enhanced_core.py     # Core systems
│   ├── WeatherSystem    # Weather & impact
│   ├── CostSystem      # Cost tracking
│   ├── EquipmentSystem # Device management
│   ├── ReportSystem    # Report generation
│   └── AIQAV2          # Intelligent Q&A
├── web_server.py        # Flask web UI
├── cli.py              # CLI interface
├── persistence_enhanced.py  # Data persistence
└── config.json         # Configuration
```

## Web Interface

Start web server:
```bash
python web_server.py
```

Then open: http://localhost:5000

## Configuration

Edit `config.json` to enable/disable features:

```json
{
  "features": {
    "weather": true,
    "cost": true,
    "equipment": true,
    "report": true,
    "ai_qa": true
  }
}
```

## Testing

```bash
python tests/test_all.py
```

## Data Directory

```
data/
├── weather/          # Weather cache
├── cost/             # Cost records
├── equipment/        # Device data
└── reports/          # Generated reports
```

---

*Updated: 2026-02-28*
