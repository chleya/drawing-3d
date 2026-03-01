# -*- coding: utf-8 -*-
"""
NeuralSite Light - 压力测试
Stress Test for Long-Run Stability & Concurrency
"""

import threading
import time
import random
import os

# 确保目录存在
os.makedirs("data", exist_ok=True)

from multi_camera_manager import MultiCameraManager
from drone_simulator import DroneSimulator
from mock_cloud_sync import MockCloudSync


def ground_stress(duration=60):
    """地面多摄像头压力测试"""
    print(f"[Ground-Stress] Starting ({duration}s)...")
    
    manager = MultiCameraManager()
    manager.add_camera(0, url=0)
    # 第二路用同一摄像头模拟
    manager.add_camera(1, url=0)
    
    manager.start_all(max_frames=200)
    
    print(f"[Ground-Stress] Finished")


def drone_stress(duration=60):
    """无人机压力测试"""
    print(f"[Drone-Stress] Starting ({duration}s)...")
    
    drone = DroneSimulator()
    drone.run_drone_loop(max_frames=300)
    
    print(f"[Drone-Stress] Finished")


def cloud_sync_stress(duration=60):
    """云同步压力测试"""
    print(f"[Cloud-Stress] Starting ({duration}s)...")
    
    sync = MockCloudSync()
    iterations = 0
    
    start = time.time()
    while time.time() - start < duration:
        sync.sync_alerts_to_cloud()
        iterations += 1
        wait = random.uniform(5, 15)
        print(f"[Cloud-Stress] Iteration {iterations}, waiting {wait:.1f}s")
        time.sleep(wait)
    
    print(f"[Cloud-Stress] Finished ({iterations} iterations)")


def run_stress_test(duration=180):
    """运行压力测试
    
    Args:
        duration: 持续时间（秒）
    """
    
    print("\n" + "="*50)
    print("NeuralSite Light - Stress Test")
    print("="*50)
    print(f"Duration: {duration} seconds")
    print("="*50 + "\n")
    
    # 记录初始状态
    import sqlite3
    conn = sqlite3.connect("data/edge.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM edge_frames")
    initial_edge = c.fetchone()[0]
    conn.close()
    
    with open("data/cloud_sync.jsonl", "r") as f:
        initial_cloud = len(f.readlines())
    
    print(f"Initial state:")
    print(f"  Edge DB: {initial_edge} records")
    print(f"  Cloud sync: {initial_cloud} records\n")
    
    # 启动线程
    threads = [
        threading.Thread(target=ground_stress, args=(duration,), name="Ground-Stress"),
        threading.Thread(target=drone_stress, args=(duration,), name="Drone-Stress"),
        threading.Thread(target=cloud_sync_stress, args=(duration,), name="Cloud-Stress"),
    ]
    
    print("Starting stress test threads...\n")
    
    for t in threads:
        t.start()
    
    # 等待
    for t in threads:
        t.join()
    
    # 检查最终状态
    print("\n" + "="*50)
    print("Stress Test Results")
    print("="*50)
    
    conn = sqlite3.connect("data/edge.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM edge_frames")
    final_edge = c.fetchone()[0]
    conn.close()
    
    with open("data/cloud_sync.jsonl", "r") as f:
        final_cloud = len(f.readlines())
    
    print(f"  Edge DB: {initial_edge} -> {final_edge} (+{final_edge - initial_edge})")
    print(f"  Cloud sync: {initial_cloud} -> {final_cloud} (+{final_cloud - initial_cloud})")
    print(f"  Duration: {duration}s")
    print("="*50 + "\n")
    
    print("[SUCCESS] Stress test completed!")
    
    return {
        'duration': duration,
        'edge_added': final_edge - initial_edge,
        'cloud_added': final_cloud - initial_cloud,
    }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='NeuralSite Stress Test')
    parser.add_argument('--duration', type=int, default=60, help='Test duration in seconds')
    args = parser.parse_args()
    
    run_stress_test(duration=args.duration)
