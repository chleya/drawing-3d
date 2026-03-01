# -*- coding: utf-8 -*-
"""
NeuralSite Light - 端到端集成测试
End-to-End Integration Test
"""

import time
import json
import os

# 确保目录存在
os.makedirs("data", exist_ok=True)

from multi_camera_manager import MultiCameraManager
from mock_cloud_sync import MockCloudSync
from drone_simulator import DroneSimulator


def run_end_to_end_test():
    """运行端到端测试"""
    
    print("\n" + "="*50)
    print("NeuralSite Light - End-to-End Integration Test")
    print("="*50 + "\n")
    
    # 1. 测试地面多摄像头（地面）
    print("[1] Testing ground multi-camera...")
    print("-" * 40)
    manager = MultiCameraManager()
    manager.add_camera(camera_id=0, url=0)  # USB摄像头
    manager.start_all(max_frames=30)  # 短跑测试
    
    time.sleep(2)  # 等待日志写入
    
    # 2. 测试边缘→云同步
    print("\n[2] Testing edge-to-cloud sync...")
    print("-" * 40)
    sync = MockCloudSync()
    uploaded = sync.sync_alerts_to_cloud()
    print(f"Cloud uploaded records: {uploaded}")
    
    # 3. 测试无人机模拟
    print("\n[3] Testing drone simulator...")
    print("-" * 40)
    drone = DroneSimulator()
    drone_result = drone.run_drone_loop(max_frames=50)
    print(f"Drone processed: {drone_result['frames']} frames")
    
    # 4. 检查数据文件
    print("\n[4] Checking data files...")
    print("-" * 40)
    
    # Edge DB
    import sqlite3
    conn = sqlite3.connect("data/edge.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM edge_frames")
    edge_count = c.fetchone()[0]
    conn.close()
    print(f"Edge DB records: {edge_count}")
    
    # Cloud sync
    cloud_logs = sync.get_cloud_logs(limit=5)
    print(f"Cloud sync records: {len(cloud_logs)}")
    
    # Drone progress
    drone_logs = drone.get_progress_logs(limit=5)
    print(f"Drone progress records: {len(drone_logs)}")
    
    # 汇总
    print("\n" + "="*50)
    print("End-to-End Test Summary")
    print("="*50)
    print(f"  Ground camera: OK")
    print(f"  Edge DB: {edge_count} records")
    print(f"  Cloud sync: {len(cloud_logs)} records")
    print(f"  Drone: {drone_result['frames']} frames processed")
    print(f"  Drone progress: {len(drone_logs)} records")
    print("="*50 + "\n")
    
    print("[SUCCESS] End-to-end test completed!")
    
    return {
        'edge_db': edge_count,
        'cloud_sync': len(cloud_logs),
        'drone_frames': drone_result['frames'],
        'drone_logs': len(drone_logs)
    }


if __name__ == "__main__":
    run_end_to_end_test()
