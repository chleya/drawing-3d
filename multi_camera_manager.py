# -*- coding: utf-8 -*-
"""
多摄像头管理器 - Multi Camera Manager
并行2+路摄像头 + 共享SQLite日志
"""

import threading
import time
import os

# 确保data目录存在
os.makedirs("data", exist_ok=True)

from edge_node import EdgeNode
from edge_filter import EdgeFilter


class MultiCameraManager:
    """多摄像头管理器"""
    
    def __init__(self):
        self.cameras = []  # 摄像头配置列表
        self.filter = EdgeFilter()  # 共享过滤器
        self.threads = []  # 线程列表
        self.running = False
    
    def add_camera(self, camera_id, url=0):
        """添加摄像头节点
        
        Args:
            camera_id: 摄像头ID
            url: 摄像头URL (0=USB, 或RTSP地址)
        """
        node = EdgeNode(camera_url=url)
        self.cameras.append({
            'id': camera_id,
            'url': url,
            'node': node
        })
        print(f"[OK] Added camera: ID {camera_id}, URL {url}")
    
    def start_all(self, max_frames=100):
        """启动所有摄像头线程
        
        Args:
            max_frames: 每个摄像头最大帧数
        """
        self.running = True
        print("\n" + "="*50)
        print(f"Starting {len(self.cameras)} cameras...")
        print("="*50 + "\n")
        
        # 启动线程
        for cam in self.cameras:
            thread = threading.Thread(
                target=self._run_camera,
                args=(cam['id'], cam['url'], max_frames),
                name=f"Cam-{cam['id']}"
            )
            thread.start()
            self.threads.append(thread)
            print(f"[START] Camera {cam['id']} thread started")
        
        # 监控线程
        while any(t.is_alive() for t in self.threads):
            active = sum(t.is_alive() for t in self.threads)
            print(f"[MONITOR] Active threads: {active}/{len(self.threads)}")
            time.sleep(2)
        
        # 结束
        self.running = False
        self._print_summary()
    
    def _run_camera(self, camera_id, url, max_frames):
        """运行单个摄像头"""
        print(f"[RUN] Camera {camera_id} processing...")
        node = EdgeNode(camera_url=url)
        node.edge_filter = self.filter  # 共享过滤器
        node.run_edge_loop(max_frames=max_frames)
        print(f"[DONE] Camera {camera_id} finished")
    
    def _print_summary(self):
        """打印汇总"""
        print("\n" + "="*50)
        print("Multi-Camera Manager Summary")
        print("="*50)
        
        # 查询数据库
        stats = self.filter.get_stats()
        print(f"Total frames processed: {stats['total_frames']}")
        print(f"Alert frames: {stats['alert_frames']}")
        print(f"Total persons detected: {stats['total_persons']}")
        
        # 最近报警
        recent = self.filter.get_recent_alerts(limit=5)
        print(f"\nRecent alerts: {len(recent)}")
        for row in recent:
            print(f"  Camera {row[2]}: {row[3]} persons at {row[1]}")
        
        print("="*50 + "\n")
    
    def get_status(self):
        """获取状态"""
        return {
            'cameras': len(self.cameras),
            'active_threads': sum(t.is_alive() for t in self.threads),
            'running': self.running
        }


# 测试
if __name__ == "__main__":
    print("="*50)
    print("Multi-Camera Manager Test")
    print("="*50)
    
    manager = MultiCameraManager()
    
    # 添加摄像头
    manager.add_camera(camera_id=0, url=0)  # USB摄像头
    
    # 启动（每个跑30帧测试）
    manager.start_all(max_frames=30)
    
    # 状态
    status = manager.get_status()
    print(f"\nFinal status: {status}")
    
    print("\n[SUCCESS] Multi-Camera Manager test completed!")
