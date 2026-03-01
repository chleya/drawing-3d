# -*- coding: utf-8 -*-
"""
边缘节点模块 - Edge Node
本地毫秒级处理 + 只上传关键帧
"""

import cv2
from yolo_detector import YOLODetector
from datetime import datetime
import json
import os

# 导入边缘过滤模块
from edge_filter import EdgeFilter


class EdgeNode:
    """边缘计算节点"""
    
    def __init__(self, camera_url=0, log_file="data/edge_logs.jsonl"):
        self.camera_url = camera_url
        self.detector = YOLODetector()
        self.detector.load_model()
        self.log_file = log_file
        
        # 初始化边缘过滤
        self.edge_filter = EdgeFilter()
        
        # 确保目录存在
        os.makedirs(os.path.dirname(log_file) if os.path.dirname(log_file) else "data", exist_ok=True)
    
    def run_edge_loop(self, max_frames=500):
        """运行边缘检测循环"""
        cap = cv2.VideoCapture(self.camera_url)
        
        if not cap.isOpened():
            print(f"无法打开摄像头: {self.camera_url}")
            return
        
        frame_count = 0
        alert_count = 0
        
        print(f"\n{'='*50}")
        print(f"Edge Node Started - Camera {self.camera_url}")
        print(f"{'='*50}\n")
        
        while frame_count < max_frames:
            ret, frame = cap.read()
            if not ret:
                break
            
            # YOLO检测
            detections = self.detector.detect_frame(frame)
            
            # 统计人数
            persons = len([d for d in detections if d['class_name'] == 'person'])
            
            # 边缘过滤：使用EdgeFilter进行持久化
            if persons > 0:
                alert_count += 1
                
                # 使用EdgeFilter保存到SQLite
                self.edge_filter.filter_and_save(
                    camera_id=self.camera_url,
                    detections=detections,
                    frame=frame
                )
                
                print(f"[ALERT] Edge node detected {persons} persons (frame {frame_count})")
            
            frame_count += 1
            
            if frame_count % 30 == 0:
                # 显示统计
                stats = self.edge_filter.get_stats()
                print(f"边缘节点已处理 {frame_count} 帧, 报警 {alert_count} 次 | DB: {stats}")
        
        cap.release()
        print(f"\n{'='*50}")
        print(f"边缘节点结束 - 共处理 {frame_count} 帧, 报警 {alert_count} 次")
        print(f"日志文件: {self.log_file}")
        print(f"{'='*50}\n")
        
        return {
            'total_frames': frame_count,
            'alerts': alert_count,
            'log_file': self.log_file
        }


def run_edge_with_camera(camera_id=0):
    """运行边缘节点（指定摄像头）"""
    edge = EdgeNode(camera_url=camera_id)
    return edge.run_edge_loop(max_frames=100)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='边缘节点')
    parser.add_argument('--camera', type=int, default=0, help='摄像头ID')
    parser.add_argument('--frames', type=int, default=100, help='最大帧数')
    args = parser.parse_args()
    
    edge = EdgeNode(camera_url=args.camera)
    edge.run_edge_loop(max_frames=args.frames)
