# -*- coding: utf-8 -*-
"""
NeuralSite Light - 阶段1最终稳定性巡检
Final Stability Check for Stage 1
"""

import os
import json
import sqlite3
from datetime import datetime


def check_edge_db():
    """检查边缘数据库"""
    db_path = "data/edge.db"
    if not os.path.exists(db_path):
        return {"status": "error", "msg": "edge.db not found"}
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM edge_frames")
    count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM edge_frames WHERE alert=1")
    alerts = c.fetchone()[0]
    
    conn.close()
    
    return {"status": "ok", "total_records": count, "alert_records": alerts}


def check_cloud_log():
    """检查云同步日志"""
    log_path = "data/cloud_sync.jsonl"
    if not os.path.exists(log_path):
        return {"status": "error", "msg": "cloud_sync.jsonl not found"}
    
    with open(log_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    return {"status": "ok", "total_records": len(lines)}


def check_drone_log():
    """检查无人机进度日志"""
    log_path = "data/drone_progress.jsonl"
    if not os.path.exists(log_path):
        return {"status": "error", "msg": "drone_progress.jsonl not found"}
    
    with open(log_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    return {"status": "ok", "total_records": len(lines)}


def check_data_files():
    """检查所有数据文件"""
    files = {
        "edge.db": "data/edge.db",
        "cloud_sync.jsonl": "data/cloud_sync.jsonl",
        "drone_progress.jsonl": "data/drone_progress.jsonl",
    }
    
    results = {}
    for name, path in files.items():
        results[name] = {
            "exists": os.path.exists(path),
            "path": path
        }
        if os.path.exists(path):
            results[name]["size"] = os.path.getsize(path)
    
    return results


def generate_summary():
    """生成巡检总结"""
    
    print("\n" + "="*50)
    print("NeuralSite Light - Stage 1 Final Stability Check")
    print("="*50 + "\n")
    
    # 检查各模块
    print("[1] Checking Edge DB...")
    edge = check_edge_db()
    print(f"    Status: {edge.get('status')}")
    if edge.get('status') == 'ok':
        print(f"    Total records: {edge.get('total_records')}")
        print(f"    Alert records: {edge.get('alert_records')}")
    
    print("\n[2] Checking Cloud Sync...")
    cloud = check_cloud_log()
    print(f"    Status: {cloud.get('status')}")
    if cloud.get('status') == 'ok':
        print(f"    Total records: {cloud.get('total_records')}")
    
    print("\n[3] Checking Drone Progress...")
    drone = check_drone_log()
    print(f"    Status: {drone.get('status')}")
    if drone.get('status') == 'ok':
        print(f"    Total records: {drone.get('total_records')}")
    
    print("\n[4] Checking Data Files...")
    files = check_data_files()
    for name, info in files.items():
        print(f"    {name}: {'OK' if info['exists'] else 'MISSING'}")
        if info.get('size'):
            print(f"      Size: {info['size']} bytes")
    
    # 生成总结
    all_ok = all(v.get("status") == "ok" for v in [edge, cloud, drone])
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "overall_status": "healthy" if all_ok else "warning",
        "edge_db": edge,
        "cloud_sync": cloud,
        "drone_progress": drone,
        "data_files": files
    }
    
    # 保存报告
    report_path = "data/stage1_final_summary.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*50)
    print("Summary")
    print("="*50)
    print(f"Overall Status: {summary['overall_status'].upper()}")
    print(f"Report saved to: {report_path}")
    print("="*50 + "\n")
    
    return summary


if __name__ == "__main__":
    generate_summary()
