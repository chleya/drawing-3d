# Drawing 3D - API Documentation

## Overview

Drawing 3D REST API provides interfaces for road engineering management.

Base URL: `http://localhost:5000`

---

## Authentication

Currently no authentication required.

---

## Endpoints

### Weather

#### GET /api/weather

Get current weather for a location.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| location | string | No | City name (default: Beijing) |

**Response:**
```json
{
  "weather": {
    "location": "北京",
    "temp": 25,
    "condition": "sunny",
    "humidity": 60,
    "wind": 12
  },
  "impact": ["天气适宜施工"]
}
```

---

### Cost Management

#### POST /api/cost/add

Add cost record.

**Request Body:**
```json
{
  "name": "水泥",
  "quantity": 100
}
```

**Response:**
```json
{
  "type": "material",
  "name": "水泥",
  "quantity": 100,
  "price": 520,
  "total": 52000,
  "timestamp": "2026-02-28T17:00:00"
}
```

#### GET /api/cost/summary

Get cost summary.

**Response:**
```json
{
  "total": 52000,
  "by_type": {
    "material": 52000
  },
  "count": 1
}
```

---

### Equipment Management

#### POST /api/device/add

Add new device.

**Request Body:**
```json
{
  "name": "挖掘机",
  "device_type": "excavator"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "挖掘机",
  "type": "excavator",
  "status": "idle",
  "add_time": "2026-02-28T17:00:00"
}
```

#### GET /api/devices

Get all devices.

**Response:**
```json
[
  {
    "id": 1,
    "name": "挖掘机",
    "type": "excavator",
    "status": "idle"
  }
]
```

---

### Report Generation

#### POST /api/report/generate

Generate report.

**Request Body:**
```json
{
  "report_type": "daily"
}
```

**Response:**
```json
{
  "type": "daily",
  "title": "日报",
  "sections": ["施工进度", "材料使用", "人员安排", "问题汇总"],
  "data": {},
  "generate_time": "2026-02-28T17:00:00"
}
```

**Report Types:**
- `daily` - Daily report
- `weekly` - Weekly report
- `monthly` - Monthly report

---

### AI Q&A

#### POST /api/ai/ask

Ask AI question.

**Request Body:**
```json
{
  "question": "项目进度如何？"
}
```

**Response:**
```json
{
  "answer": "项目整体进度正常，已完成65%"
}
```

---

## Error Responses

All endpoints may return:

```json
{
  "error": "Error message",
  "code": 500
}
```

---

## Web Interface

Access the web interface at: `http://localhost:5000`

Features:
- Weather query
- Cost management
- Equipment tracking
- Report generation
- AI Q&A
- System status

---

## Rate Limits

No rate limits currently.

---

## Example Usage

### cURL

```bash
# Get weather
curl "http://localhost:5000/api/weather?location=北京"

# Add cost
curl -X POST "http://localhost:5000/api/cost/add" \
  -H "Content-Type: application/json" \
  -d '{"name": "水泥", "quantity": 100}'

# Ask AI
curl -X POST "http://localhost:5000/api/ai/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "项目进度如何？"}'
```

### Python

```python
import requests

# Get weather
r = requests.get("http://localhost:5000/api/weather?location=北京")
print(r.json())

# Add cost
r = requests.post("http://localhost:5000/api/cost/add", json={
    "name": "水泥",
    "quantity": 100
})
print(r.json())
```

---

*Generated: 2026-02-28*
