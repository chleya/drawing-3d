# -*- coding: utf-8 -*-
"""
Drawing 3D - YOLO 安全检测器 (完整版)
YOLO Safety Detector - Complete Version
"""

import os
import cv2
import time
from datetime import datetime


class YOLODetector:
    """YOLO目标检测器 - 完整版"""
    
    DEFAULT_MODEL = 'yolov8n.pt'
    
    # COCO数据集类别 (YOLOv8预训练)
    COCO_CLASSES = {
        0: 'person',      # 人员
        1: 'bicycle',    # 自行车
        2: 'car',        # 汽车
        3: 'motorcycle', # 摩托车
        5: 'bus',        # 公交车
        7: 'truck',      # 卡车
    }
    
    # 安全相关类别
    SAFETY_CLASSES = {
        'person': '人员',
        'helmet': '安全帽',
        'no_helmet': '未戴安全帽',
        'vest': '反光衣',
        'vehicle': '车辆',
    }
    
    def __init__(self, model_path=None):
        """初始化检测器"""
        self.model_path = model_path or self.DEFAULT_MODEL
        self.model = None
        self.loaded = False
        self.stats = {
            'total_frames': 0,
            'total_detections': 0,
            'start_time': None,
            'persons': 0,
            'vehicles': 0,
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
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                
                # 类别名称
                cls_name = self.model.names.get(cls, 'unknown')
                
                detection = {
                    'bbox': [float(x1), float(y1), float(x2), float(y2)],
                    'confidence': conf,
                    'class_id': cls,
                    'class_name': cls_name,
                }
                detections.append(detection)
                
                # 统计
                if cls == 0:  # person
                    self.stats['persons'] += 1
                elif cls in [2, 3, 5, 7]:  # vehicle
                    self.stats['vehicles'] += 1
        
        self.stats['total_frames'] += 1
        self.stats['total_detections'] += len(detections)
        
        return detections
    
    def process_video(self, video_path, output_path=None, max_frames=None):
        """处理视频文件"""
        if not self.loaded:
            self.load_model()
        
        if not os.path.exists(video_path):
            return {'error': f'Video file not found: {video_path}'}
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return {'error': 'Failed to open video'}
        
        # 视频信息
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # 写入器
        writer = None
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
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
            
            # 绘制
            annotated_frame = self.draw_detections(frame, detections)
            
            # 写入
            if writer:
                writer.write(annotated_frame)
            
            # 记录
            results.append({
                'frame': frame_idx,
                'detections': detections,
                'timestamp': datetime.now().isoformat()
            })
            
            frame_idx += 1
            
            # 限制
            if max_frames and frame_idx >= max_frames:
                break
            
            # 进度
            if frame_idx % 30 == 0:
                print(f"Processed {frame_idx}/{total_frames} frames...")
        
        cap.release()
        if writer:
            writer.release()
        
        process_time = time.time() - start_time
        
        return {
            'video_path': video_path,
            'output_path': output_path,
            'frames_processed': frame_idx,
            'total_frames': total_frames,
            'fps': frame_idx / process_time if process_time > 0 else 0,
            'results': results,
            'stats': self.get_stats(),
        }
    
    def process_camera(self, camera_id=0, max_frames=100):
        """处理摄像头实时流"""
        if not self.loaded:
            self.load_model()
        
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
            
            # 退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            if max_frames and frame_idx >= max_frames:
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        return {
            'frames_processed': frame_idx,
            'results': results,
            'stats': self.get_stats(),
        }
    
    def draw_detections(self, frame, detections):
        """绘制检测框"""
        annotated = frame.copy()
        
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            conf = det['confidence']
            cls_name = det['class_name']
            
            # 颜色: 绿色person, 蓝色vehicle, 红色其他
            if cls_name == 'person':
                color = (0, 255, 0)  # 绿色
            elif cls_name in ['car', 'truck', 'bus', 'motorcycle']:
                color = (255, 0, 0)  # 蓝色
            else:
                color = (0, 0, 255)  # 红色
            
            # 绘制框
            cv2.rectangle(annotated, 
                         (int(x1), int(y1)), 
                         (int(x2), int(y2)), 
                         color, 2)
            
            # 标签
            label = f"{cls_name}: {conf:.2f}"
            cv2.putText(annotated, label, 
                       (int(x1), int(y1) - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 
                       0.5, color, 2)
        
        return annotated
    
    def get_stats(self):
        """获取统计信息"""
        return self.stats.copy()
    
    def reset_stats(self):
        """重置统计"""
        self.stats = {
            'total_frames': 0,
            'total_detections': 0,
            'persons': 0,
            'vehicles': 0,
            'start_time': datetime.now().isoformat(),
        }
    
    def fine_tune_helmet(self, dataset_yaml='helmet_dataset.yaml', epochs=20):
        """Fine-tune 安全帽模型"""
        if not self.loaded:
            self.load_model()
        
        if self.model is None:
            return {'error': 'Model not loaded'}
        
        print(f"Starting fine-tune with {epochs} epochs...")
        
        try:
            # 训练模型
            self.model.train(data=dataset_yaml, epochs=epochs, imgsz=640, verbose=True)
            
            # 导出模型
            self.model.export(format='pt', path='helmet_yolov8.pt')
            
            # 更新路径
            self.model_path = 'helmet_yolov8.pt'
            self.loaded = False  # 下次使用新模型
            
            print("Fine-tune completed! New model: helmet_yolov8.pt")
            return {'status': 'success', 'model': 'helmet_yolov8.pt'}
        except Exception as e:
            return {'error': str(e)}


# ==================== 测试 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("YOLO Safety Detector - Complete Version Test")
    print("=" * 60)
    
    detector = YOLODetector()
    
    # 加载模型
    print("\n[1] Loading model...")
    if detector.load_model():
        print("Model loaded!")
        
        # 统计
        stats = detector.get_stats()
        print(f"Stats: {stats}")
        
        print("\n[SUCCESS] YOLO detector ready!")
    else:
        print("Failed to load model")
