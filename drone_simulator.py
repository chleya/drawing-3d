# -*- coding: utf-8 -*-
"""
无人机RTSP模拟 + 宏观进度识别 - Drone Simulator
"""

import cv2
from yolo_detector import YOLODetector
from datetime import datetime
import json
import os


class DroneSimulator:
    """无人机RTSP模拟 + 宏观进度识别"""
    
    def __init__(self, source="data/test_video.mp4"):
        # 默认本地视频，实际可换RTSP
        self.source = source
        self.detector = YOLODetector()
        self.detector.load_model()
        self.progress_log = "data/drone_progress.jsonl"
        
        os.makedirs("data", exist_ok=True)
    
    def run_drone_loop(self, max_frames=300):
        """运行无人机模拟循环"""
        
        cap = cv2.VideoCapture(self.source)
        
        if not cap.isOpened():
            print(f"[WARN] Cannot open video source: {self.source}")
            return
        
        print(f"\n{'='*50}")
        print(f"Drone Simulator Started - Source: {self.source}")
        print(f"{'='*50}\n")
        
        frame_count = 0
        total_persons = 0
        total_vehicles = 0
        
        while frame_count < max_frames:
            ret, frame = cap.read()
            if not ret:
                break
            
            # YOLO检测
            detections = self.detector.detect_frame(frame)
            
            # 统计
            persons = len([d for d in detections if d['class_name'] == 'person'])
            vehicles = len([d for d in detections if d['class_name'] in ['car', 'truck', 'bus', 'motorcycle']])
            
            total_persons += persons
            total_vehicles += vehicles
            
            # 进度估算 (简单公式)
            progress_estimate = round((persons + vehicles * 5) / 50, 2)
            
            # 记录
            if persons > 0 or vehicles > 0:
                entry = {
                    "frame": frame_count,
                    "timestamp": datetime.now().isoformat(),
                    "persons": persons,
                    "vehicles": vehicles,
                    "total_persons": total_persons,
                    "total_vehicles": total_vehicles,
                    "progress_estimate": progress_estimate
                }
                
                with open(self.progress_log, "a", encoding="utf-8") as f:
                    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
                
                print(f"[DRONE] Frame {frame_count}: persons={persons} | vehicles={vehicles} | progress={progress_estimate}")
            
            frame_count += 1
            
            if frame_count % 50 == 0:
                print(f"[DRONE] Progress: {frame_count}/{max_frames} frames processed")
        
        cap.release()
        
        print(f"\n{'='*50}")
        print(f"Drone Simulator Finished")
        print(f"  Total frames: {frame_count}")
        print(f"  Total persons: {total_persons}")
        print(f"  Total vehicles: {total_vehicles}")
        print(f"  Log file: {self.progress_log}")
        print(f"{'='*50}\n")
        
        return {
            'frames': frame_count,
            'persons': total_persons,
            'vehicles': total_vehicles,
            'log_file': self.progress_log
        }
    
    def get_progress_logs(self, limit=10):
        """获取进度日志"""
        if not os.path.exists(self.progress_log):
            return []
        
        logs = []
        with open(self.progress_log, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    logs.append(json.loads(line))
        
        return logs[-limit:]


# 测试
if __name__ == "__main__":
    print("="*50)
    print("Drone Simulator Test")
    print("="*50)
    
    # 使用本地测试视频
    simulator = DroneSimulator(source="data/test_video.mp4")
    
    # 运行短测试
    result = simulator.run_drone_loop(max_frames=50)
    
    # 查看日志
    print("\n[Progress Logs]")
    logs = simulator.get_progress_logs(limit=5)
    for log in logs:
        print(f"  {log}")
    
    print("\n[SUCCESS] Drone Simulator working!")
