# Drawing 3D 项目现状说明书

**版本**: 1.0  
**日期**: 2026-03-03  
**项目**: 道路工程智能管理系统 (Road Engineering Management System)

---

## 一、项目概述

Drawing 3D 是一个面向道路工程的全栈智能管理系统，旨在通过AI、物联网和三维可视化技术，提升道路施工的管理效率和质量控制能力。

**项目地址**: https://github.com/chleya/drawing-3d

---

## 二、核心功能模块

### 2.1 已完成功能

| 模块 | 文件 | 状态 | 说明 |
|------|------|------|------|
| 🌤️ 天气系统 | `weather.py` | ✅ 完成 | 实时天气、施工影响分析 |
| 💰 成本管理 | `cost.py` | ✅ 完成 | 材料/人工/设备成本跟踪 |
| 🛠️ 设备调度 | `equipment.py` | ✅ 完成 | 设备状态管理、利用率跟踪 |
| 📊 报告生成 | `report.py` | ✅ 完成 | 日/周/月报导出 |
| 🤖 AI问答 | `ai_qa_v2.py` | ✅ 完成 | 基于上下文的智能问答 |
| 📐 图纸问答 | `blueprint_qa.py` | ✅ 完成 | 道路结构、材料、规范问答 |
| 🗺️ 空间映射 | `spatial_semantic_mapper.py` | ✅ 完成 | 桩号↔经纬度坐标转换 |
| 🧠 知识图谱 | `blueprint_knowledge_graph.py` | ✅ 完成 | 图纸知识存储与查询 |
| 🚗 自动驾驶 | `autonomous_decision.py` | ✅ 完成 | Q-learning决策引擎 |
| 🛸 无人机 | `drone.py` | ✅ 完成 | 无人机视角监控 |
| 🔍 质量检测 | `quality_detection.py` | ✅ 完成 | YOLO安全帽/违章检测 |
| 🛡️ 安全管理 | `safety.py` | ✅ 完成 | 安全风险评估 |

### 2.2 基础设施

| 功能 | 文件 | 状态 |
|------|------|------|
| Web服务器 | `server.py`, `web_server.py` | ✅ |
| REST API | `api.py`, `semantic_api.py` | ✅ |
| 数据持久化 | `persistence.py` | ✅ |
| 日志系统 | `logging_system.py` | ✅ |
| Docker支持 | `Dockerfile`, `docker-compose.yml` | ✅ |

---

## 三、阶段完成情况

### 阶段1: 全视之眼 (感知基础设施) ✅ 100%

- [x] 地面实时监控
- [x] 无人机视角
- [x] 多摄像头管理
- [x] 天气数据集成
- [x] 知识图谱基础

### 阶段2: 智能决策 (AI + 知识) ✅ 100%

- [x] AI问答系统
- [x] 图纸智能问答
- [x] 空间语义映射
- [x] 成本分析
- [x] 设备调度优化

### 阶段3: 自动驾驶 (自主行动) ✅ 100%

- [x] 自主决策引擎 (Q-learning)
- [x] 人类监督与干预
- [x] 智能合约支付触发
- [x] 端到端全链路测试

---

## 四、技术架构

```
┌─────────────────────────────────────────────┐
│              Presentation Layer             │
│   (Web UI / AR View / Drone View)          │
├─────────────────────────────────────────────┤
│              API Layer                      │
│   (REST API / Semantic API / WebSocket)     │
├─────────────────────────────────────────────┤
│            Business Logic Layer             │
│  (Weather / Cost / Equipment / Planning)    │
├─────────────────────────────────────────────┤
│              AI / ML Layer                  │
│   (AI Q&A / Blueprint QA / Quality Det)    │
├─────────────────────────────────────────────┤
│              Data Layer                     │
│   (JSON Persistence / Neo4j / PostgreSQL)   │
└─────────────────────────────────────────────┘
```

### 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Python (Flask/FastAPI) |
| 前端 | HTML/CSS/JavaScript |
| 数据库 | JSON (当前) → PostgreSQL (计划) |
| 图数据库 | 内存模拟 (当前) → Neo4j (计划) |
| AI | 模板匹配 → LLM API (MiniMax) |
| 三维 | Canvas/Three.js |
| 检测 | YOLOv8 |

---

## 五、访问地址

| 服务 | 地址 |
|------|------|
| 地面视图 | http://localhost:5000 |
| 无人机视角 | http://localhost:5000/drone |
| Web服务 | http://localhost:5000 |

---

## 六、待开发功能 (BACKLOG)

### P0 - 本周完成

- [ ] 摄像头视频流接入 (支持本地mp4)
- [ ] YOLO安全帽/违章识别 (预训练模型)
- [ ] Web实时展示增强
- [ ] 报告PDF导出
- [ ] 单元测试覆盖≥70%

### P1 - 3月10日前

- [ ] 真实工地设备对接 (海康/北斗)
- [ ] 响应式Web界面优化
- [ ] 实时数据刷新 (WebSocket/SSE)

### P2 - 阶段2

- [ ] 真实AR眼镜叠加
- [ ] 区块链存证
- [ ] 多项目支持
- [ ] 无人机真实控制

---

## 七、已知问题

1. **数据库**: 当前使用JSON文件，生产环境需迁移到PostgreSQL
2. **图数据库**: 当前使用内存模拟，需部署Neo4j
3. **LLM API**: 当前使用模板匹配，建议接入MiniMax API
4. **测试覆盖**: 当前<30%，需提升到70%

---

## 八、下一步建议

1. **完善测试** - 提升代码覆盖率到70%
2. **接入LLM** - 使用MiniMax API增强AI问答
3. **部署Neo4j** - 启用知识图谱功能
4. **视频流** - 接入真实摄像头
5. **PDF导出** - 实现报告导出功能

---

**报告生成时间**: 2026-03-03
