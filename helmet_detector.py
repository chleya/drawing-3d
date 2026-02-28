# -*- coding: utf-8 -*-
"""
安全帽检测 - 使用预训练模型
Helmet Detection using Pre-trained Model

由于网络限制，这里使用一个替代方案：
使用YOLOv8预训练模型中最接近的类别进行检测
"""

from yolo_detector import YOLODetector
import cv2
import os

def detect_with_yolo8():
    """使用YOLOv8进行检测（最接近安全帽的类别）"""
    
    detector = YOLODetector()
    
    print("Loading YOLOv8 model...")
    detector.load_model()
    
    # 创建测试图像（模拟工地场景）
    print("\nCreating test image...")
    img = create_construction_scene()
    
    # 检测
    print("Running detection...")
    detections = detector.detect_frame(img)
    
    # 分析结果
    print("\n" + "="*50)
    print("Detection Results:")
    print("="*50)
    
    # 统计
    class_counts = {}
    for det in detections:
        cls = det['class_name']
        conf = det['confidence']
        class_counts[cls] = class_counts.get(cls, 0) + 1
        print(f"  {cls}: {conf:.2f}")
    
    # 关键检测
    persons = class_counts.get('person', 0)
    print(f"\nTotal persons detected: {persons}")
    
    # YOLOv8 COCO类别说明
    print("\n" + "="*50)
    print("YOLOv8 COCO Classes (for reference):")
    print("="*50)
    print("  0: person (人员)")
    print("  1: bicycle")
    print("  2: car (汽车)")
    print("  3: motorcycle")
    print("  5: bus (公交车)")
    print("  7: truck (卡车)")
    print("\nNote: helmet detection requires custom training!")
    
    return detections


def create_construction_scene():
    """创建模拟工地场景"""
    import numpy as np
    
    # 创建图像
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    img[:] = (200, 200, 200)  # 灰色背景
    
    # 画一个人形
    # 头
    cv2.circle(img, (320, 150), 30, (200, 150, 150), -1)
    # 身体
    cv2.rectangle(img, (290, 180), (350, 350), (100, 100, 200), -1)
    # 腿
    cv2.rectangle(img, (295, 350), (315, 450), (80, 80, 150), -1)
    cv2.rectangle(img, (325, 350), (345, 450), (80, 80, 150), -1)
    
    return img


def create_sample_dataset():
    """创建样本数据集（用于演示格式）"""
    
    # 创建数据目录结构
    dirs = [
        'F:/helmet_dataset/images/train',
        'F:/helmet_dataset/images/val',
        'F:/helmet_dataset/labels/train',
        'F:/helmet_dataset/labels/val',
    ]
    
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    
    # 创建dataset.yaml
    dataset_yaml = """
# Helmet Detection Dataset
path: F:/helmet_dataset
train: images/train
val: images/val

# Classes
nc: 3
names: ['person', 'helmet', 'no-helmet']
"""
    
    with open('F:/helmet_dataset/dataset.yaml', 'w') as f:
        f.write(dataset_yaml)
    
    print("Sample dataset structure created!")
    print("To train with real data:")
    print("1. Add images to images/train/")
    print("2. Add YOLO format labels to labels/train/")
    print("3. Run: detector.fine_tune_helmet('F:/helmet_dataset/dataset.yaml', epochs=10)")
    
    return True


if __name__ == "__main__":
    print("="*60)
    print("Helmet Detection Demo")
    print("="*60)
    
    # 1. 检测演示
    detect_with_yolo8()
    
    # 2. 创建数据集模板
    print("\n" + "="*60)
    print("Creating sample dataset structure...")
    print("="*60)
    create_sample_dataset()
