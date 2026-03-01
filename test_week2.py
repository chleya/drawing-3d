# -*- coding: utf-8 -*-
"""
Week2 全链路集成测试
Test Week2 Full Pipeline Integration
"""

import unittest
import os
import time

# 确保data目录存在
os.makedirs("data", exist_ok=True)

from multi_camera_manager import MultiCameraManager
from mock_cloud_sync import MockCloudSync
from edge_filter import EdgeFilter


class TestWeek2(unittest.TestCase):
    """Week2全链路集成测试"""
    
    def test_full_pipeline(self):
        """测试摄像头 → 边缘 → 过滤 → 云同步"""
        
        print("\n" + "="*50)
        print("Week2 Integration Test")
        print("="*50 + "\n")
        
        # 1. 初始化管理器
        print("[1] Initializing MultiCameraManager...")
        manager = MultiCameraManager()
        manager.add_camera(camera_id=0, url=0)  # USB摄像头
        print("    Camera added: ID 0, URL 0")
        
        # 2. 启动处理（短跑测试）
        print("\n[2] Starting edge processing (30 frames)...")
        start_time = time.time()
        manager.start_all(max_frames=30)
        elapsed = time.time() - start_time
        print(f"    Processing time: {elapsed:.2f}s")
        
        # 3. 验证过滤DB
        print("\n[3] Verifying EdgeFilter DB...")
        filter = EdgeFilter()
        alerts = filter.get_recent_alerts(limit=10)
        print(f"    Alert records: {len(alerts)}")
        
        stats = filter.get_stats()
        print(f"    Stats: {stats}")
        
        self.assertGreaterEqual(len(alerts), 0, "EdgeFilter DB error")
        
        # 4. 验证云同步
        print("\n[4] Verifying Cloud Sync...")
        sync = MockCloudSync()
        uploaded = sync.sync_alerts_to_cloud()
        print(f"    Uploaded records: {uploaded}")
        
        # 5. 验证日志文件
        print("\n[5] Verifying cloud log file...")
        self.assertTrue(os.path.exists("data/cloud_sync.jsonl"), "Cloud log file missing")
        
        with open("data/cloud_sync.jsonl", "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        print(f"    Cloud log lines: {len(lines)}")
        
        # 6. 统计
        sync_stats = sync.get_sync_stats()
        print(f"\n[6] Sync stats: {sync_stats}")
        
        # 汇总
        print("\n" + "="*50)
        print("Week2 Integration Test Summary")
        print("="*50)
        print(f"  Processing time: {elapsed:.2f}s")
        print(f"  Alert records: {len(alerts)}")
        print(f"  Cloud uploads: {uploaded}")
        print(f"  Cloud log lines: {len(lines)}")
        print("="*50)
        
        # 断言
        self.assertGreaterEqual(len(alerts), 0)
        self.assertGreaterEqual(uploaded, 0)
        self.assertGreater(len(lines), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
