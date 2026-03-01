# -*- coding: utf-8 -*-
"""
边缘→云传输模拟 - Mock Cloud Sync
异常帧数据上传到"云端"
"""

import json
import time
import os
from datetime import datetime
from edge_filter import EdgeFilter


class MockCloudSync:
    """边缘→云传输模拟"""
    
    def __init__(self, edge_db_path="data/edge.db", cloud_log_path="data/cloud_sync.jsonl"):
        self.edge_db_path = edge_db_path
        self.cloud_log_path = cloud_log_path
        self.sync_interval = 10  # 秒
        os.makedirs("data", exist_ok=True)
    
    def sync_alerts_to_cloud(self):
        """从边缘DB查询报警 → 模拟上传到云"""
        
        filter = EdgeFilter()
        alerts = filter.get_recent_alerts(limit=50)  # 查询最近50条
        
        uploaded = 0
        for row in alerts:
            entry = {
                "id": row[0],
                "timestamp": row[1],
                "camera_id": row[2],
                "persons": row[3],
                "total_detections": row[4],
                "alert": row[5],
                "frame_path": row[6],
                "synced_at": datetime.now().isoformat()
            }
            
            with open(self.cloud_log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            
            uploaded += 1
        
        print(f"[CLOUD] Sync complete: uploaded {uploaded} alert records")
        return uploaded
    
    def get_cloud_logs(self, limit=10):
        """获取云端日志"""
        if not os.path.exists(self.cloud_log_path):
            return []
        
        logs = []
        with open(self.cloud_log_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    logs.append(json.loads(line))
        
        return logs[-limit:]
    
    def run_sync_loop(self):
        """定时同步循环"""
        print(f"[CLOUD] Starting sync loop (interval: {self.sync_interval}s)")
        
        while True:
            try:
                self.sync_alerts_to_cloud()
                time.sleep(self.sync_interval)
            except KeyboardInterrupt:
                print("\n[CLOUD] Sync loop stopped")
                break
    
    def get_sync_stats(self):
        """获取同步统计"""
        logs = self.get_cloud_logs(limit=1000)
        
        # 统计
        total_uploads = len(logs)
        cameras = set(log.get('camera_id') for log in logs)
        total_persons = sum(log.get('persons', 0) for log in logs)
        
        return {
            'total_syncs': total_uploads,
            'cameras': len(cameras),
            'total_persons': total_persons,
            'cloud_log_file': self.cloud_log_path
        }


# 测试
if __name__ == "__main__":
    print("="*50)
    print("Mock Cloud Sync Test")
    print("="*50)
    
    sync = MockCloudSync()
    
    # 同步一次
    print("\n[1] Syncing alerts to cloud...")
    uploaded = sync.sync_alerts_to_cloud()
    print(f"    Uploaded: {uploaded} records")
    
    # 查看云端日志
    print("\n[2] Cloud logs:")
    logs = sync.get_cloud_logs(limit=3)
    for log in logs:
        print(f"    {log}")
    
    # 统计
    print("\n[3] Sync stats:")
    stats = sync.get_sync_stats()
    print(f"    {stats}")
    
    print("\n[SUCCESS] Mock Cloud Sync working!")
