# NeuralSite Light 阶段1 技术文档 v0.1

**文档标题**: 全视之眼 - 感知基础设施实现
**完成日期**: 2026年3月1日
**项目阶段**: 阶段1（全视之眼）
**负责人**: chleya（开发） + Grok（PM）

---

## 1. 阶段目标回顾

- ✅ 7×24h自动"看见"施工现场
- ✅ 数据零人工输入雏形
- ✅ 云边端一体化基础
- ✅ 真实摄像头接入 + 多路管理 + 边缘过滤 + 云同步 + 无人机模拟 + Web统一面板

---

## 2. 系统架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                     NeuralSite Light v0.1                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│  │   感知层    │    │   边缘层     │    │   云层       │        │
│  │             │    │             │    │             │        │
│  │ USB摄像头   │───▶│ EdgeNode    │───▶│ EdgeFilter  │        │
│  │ IP摄像头    │    │ 本地YOLO    │    │ SQLite      │        │
│  │ 无人机视频  │    │ 实时检测    │    │ 过滤持久化  │        │
│  └─────────────┘    └─────────────┘    └──────┬──────┘        │
│                                                │               │
│  ┌─────────────────────────────────────────────┼─────────────┐  │
│  │                     云边端数据流                           │  │
│  │                                                        │  │
│  │ 摄像头 → 边缘检测 → 关键帧过滤 → SQLite → 云同步日志   │  │
│  │                                        ↓                 │  │
│  │                              MockCloudSync (模拟上传)    │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                      展示层 ()                         │ Web │
│  │                                                          │  │
│  │  http://localhost:5000        http://localhost:5000/drone│  │
│  │  地面实时监控 + 统计            无人机视角 + 进度          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. 核心组件清单

| 组件 | 文件 | 功能描述 |
|------|------|----------|
| YOLO核心 | `yolo_detector.py` | 人员/车辆检测 + 绘制框 |
| 地面边缘节点 | `edge_node.py` | 本地检测 + 异常帧记录 |
| 数据过滤 & 持久化 | `edge_filter.py` | SQLite存储 + 关键帧模拟上传 |
| 多摄像头管理 | `multi_camera_manager.py` | 线程并行 + 共享日志 |
| 云同步模拟 | `mock_cloud_sync.py` | 边缘→云报警上传 |
| 无人机模拟 | `drone_simulator.py` | RTSP + 宏观进度估算 |
| Web面板 | `web_server.py` | 实时流 + 双视图 + 统计 + 报警 |
| 端到端测试 | `end_to_end_test.py` | 全链路验证 |
| 压力测试 | `stress_test.py` | 长时间并发稳定性 |
| 最终巡检 | `final_stability_check.py` | 自动总结报告 |

---

## 4. 测试总结

| 指标 | 结果 |
|------|------|
| Edge DB记录 | 1条 |
| Cloud Sync记录 | 5条 |
| Drone Progress | 0条 (测试视频无对象) |
| 压力测试 | 30秒多线程无崩溃 |
| 整体状态 | WARNING (Drone日志空，符合预期) |

---

## 5. 部署指南

### 5.1 本地运行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动Web服务
python web_server.py

# 3. 访问
# 地面视图: http://localhost:5000
# 无人机视图: http://localhost:5000/drone
```

### 5.2 Docker部署

```bash
# 构建并运行
docker-compose up --build

# 访问
# 地面视图: http://localhost:5000
# 无人机视图: http://localhost:5000/drone
```

---

## 6. API端点

| 端点 | 方法 | 功能 |
|------|------|------|
| `/` | GET | 主页面 |
| `/video_feed` | GET | 实时摄像头流 + YOLO检测 |
| `/drone` | GET | 无人机监控页面 |
| `/drone_feed` | GET | 无人机视频流 |
| `/api/safety` | POST | 安全检测 |
| `/api/camera/stats` | GET | 摄像头统计 |
| `/api/drone_progress` | GET | 无人机进度 |
| `/api/scrape` | POST | 网页爬取 |
| `/api/search` | POST | 网页搜索 |

---

## 7. 下一步（阶段2准备）

- 副驾驶模式：风险预测 + AI建议
- 安全帽fine-tune（待数据集）
- 真实工地数据采集
- 真实云API集成（AWS S3 / 阿里云OSS）

---

## 8. Git提交记录

| Commit | Message |
|--------|---------|
| 3618a8c | feat(stage1-week2-day1): launch edge node simulation |
| 02ff669 | feat(stage1-week2-day2): add edge_filter with SQLite |
| 5a61fc3 | feat(stage1-week2-day3): add multi_camera_manager |
| 6083506 | feat(stage1-week2-day4): add mock_cloud_sync |
| ac311d3 | feat(stage1-week2-day5-6): integrated tests + Week2 report |
| 601e34d | feat(stage1-week3-day1): add drone RTSP simulator |
| ab97938 | feat(stage1-week3-day2): integrate drone into Web panel |
| 50e0511 | feat(stage1-week3-day3): end-to-end integration test |
| f5e1160 | feat(stage1-week3-day4): stress test |
| bc306c4 | feat(stage1-week3-day5): final stability check |

---

## 9. 附录

- 架构图: 详见上文
- Demo视频: 待录制

---

*文档版本: v0.1*
*生成时间: 2026-03-01 10:24 HKT*
