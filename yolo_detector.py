# -*- coding: utf-8 -*-
"""
Drawing 3D - YOLO 安全检测器
YOLO Safety Detector
"""

import os
import cv2
import time
from datetime import datetime


class YOLODetector:
    """YOLO目标检测器"""
    
    # 预训练模型路径
    DEFAULT_MODEL = 'yolov8n.pt'
    
    # 安全相关类别 (COCO数据集)
    SAFETY_CLASSES = {
        0: 'person',           # 人员
        1: 'bicycle',         # 自行车
        2: 'car',             # 汽车
        3: 'motorcycle',      # 摩托车
        5: 'bus',             # 公交车
        7: 'truck',           # 卡车
    }
    
    # 工地安全检测类别 (自定义)
    SITE_CLASSES = {
        'helmet': '安全帽',
        'person': '人员',
        'vehicle': '车辆',
        'hardhat': '安全帽(黄)',
        'vest': '反光衣',
    }
    
    def __init__(self, model_path=None):
        """初始化检测器"""
        self.model_path = model_path or self.DEFAULT_MODEL
        self.model = None
        self.loaded = False
        
        # 检测统计
        self.stats = {
            'total_frames': 0,
            'total_detections': 0,
            'start_time': None,
        }
    
    def load_model(self):
        """加载模型"""
        if self.loaded:
            return True
        
        try:
            from ultralytics import YOLO
            print(f"Loading YOLO model: {self.model_path}")
            self.model = YOLO(self.model_path)
            self.loaded = True
            self.stats['start_time'] = datetime.now().isoformat()
            print("YOLO model loaded successfully!")
            return True
        except Exception as e:
            print(f"Failed to load YOLO model: {e}")
            return False
    
    def detect_frame(self, frame):
        """检测单帧"""
        if not self.loaded:
            self.load_model()
        
        if self.model is None:
            return None
        
        # YOLO推理
        results = self.model(frame, verbose=False)
        
        # 解析结果
        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # 获取边界框
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                
                detection = {
                    'bbox': [float(x1), float(y1), float(x2), float(y2)],
                    'confidence': conf,
                    'class_id': cls,
                    'class_name': self.model.names.get(cls, 'unknown'),
                }
                detections.append(detection)
        
        self.stats['total_frames'] += 1
        self.stats['total_detections'] += len(detections)
        
        return detections
    
    def process_video(self, video_path, output_path=None, max_frames=None):
        """处理视频文件"""
        if not os.path.exists(video_path):
            return {'error': f'Video file not found: {video_path}'}
        
        # 打开视频
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return {'error': 'Failed to open video'}
        
        # 获取视频信息
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # 输出视频写入器
        writer = None
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        # 处理每一帧
        results = []
        frame_idx = 0
        start_time = time.time()
        
        print(f"Processing video: {video_path}")
        print(f"Resolution: {width}x{height}, FPS: {fps}, Frames: {total_frames}")
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # 检测
            detections = self.detect_frame(frame)
            
            # 绘制检测框
            annotated_frame = self.draw_detections(frame, detections)
            
            # 写入输出视频
            if writer:
                writer.write(annotated_frame)
            
            # 记录结果
            results.append({
                'frame': frame_idx,
                'detections': detections,
                'timestamp': datetime.now().isoformat()
            })
            
            frame_idx += 1
            
            # 限制处理帧数
            if max_frames and frame_idx >= max_frames:
                break
            
            # 进度显示
            if frame_idx % 30 == 0:
                print(f"Processed {frame_idx}/{total_frames} frames...")
        
        # 释放资源
        cap.release()
        if writer:
            writer.release()
        
        # 统计信息
        process_time = time.time() - start_time
        
        return {
            'video_path': video_path,
            'output_path': output_path,
            'frames_processed': frame_idx,
            'total_frames': total_frames,
            'fps': frame_idx / process_time if process_time > 0 else 0,
            'results': results,
            'stats': self.stats,
        }
    
    def process_camera(self, camera_id=0, max_frames=100):
        """处理摄像头实时流"""
        cap = cv2.VideoCapture(camera_id)
        if not cap.isOpened():
            return {'error': f'Failed to open camera {camera_id}'}
        
        print(f"Camera {camera_id} opened. Press 'q' to quit.")
        
        results = []
        frame_idx = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # 检测
            detections = self.detect_frame(frame)
            
            # 绘制
            annotated_frame = self.draw_detections(frame, detections)
            
            # 显示
            cv2.imshow('YOLO Detection', annotated_frame)
            
            # 记录
            results.append({
                'frame': frame_idx,
                'detections': detections,
            })
            
            frame_idx += 1
            
            # 退出条件
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            if max_frames and frame_idx >= max_frames:
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        return {
            'frames_processed': frame_idx,
            'results': results,
        }
    
    def draw_detections(self, frame, detections):
        """绘制检测框"""
        annotated = frame.copy()
        
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            conf = det['confidence']
            cls_name = det['class_name']
            
            # 颜色 (根据类别)
            color = (0, 255, 0)  # 绿色
            
            # 绘制框
            cv2.rectangle(annotated, 
                         (int(x1), int(y1)), 
                         (int(x2), int(y2)), 
                         color, 2)
            
            # 绘制标签
            label = f"{cls_name}: {conf:.2f}"
            cv2.putText(annotated, label, 
                       (int(x1), int(y1) - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 
                       0.5, color, 2)
        
        return annotated
    
    def get_stats(self):
        """获取统计信息"""
        return self.stats
    
    def reset_stats(self):
        """重置统计"""
        self.stats = {
            'total_frames': 0,
            'total_detections': 0,
            'start_time': datetime.now().isoformat(),
        }


# ==================== 测试 ====================

if __name__ == "__main__":
    # 测试检测器
    detector = YOLODetector()
    
    print("=" * 50)
    print("YOLO Safety Detector Test")
    print("=" * 50)
    
    # 尝试加载模型
    if detector.load_model():
        print("Model loaded successfully!")
        
        # 创建测试图像
        import numpy as np
        test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # 测试检测
        detections = detector.detect_frame(test_frame)
        print(f"Test detection result: {len(detections)} objects")
        
        # 统计
        stats = detector.get_stats()
        print(f"Stats: {stats}")
    else:
        print("Failed to load model. Please install ultralytics.")
        print("Run: pip install ultralytics")
