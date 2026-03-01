# -*- coding: utf-8 -*-
"""
安全帽检测模型 Fine-Tune
基于Ultralytics YOLOv8
"""

import os
import sys
from datetime import datetime


class HelmetFineTuner:
    """安全帽模型fine-tune"""
    
    def __init__(self, base_model='yolov8n.pt'):
        """初始化
        
        Args:
            base_model: 基础模型（yolov8n.pt, yolov8s.pt, yolov8m.pt）
        """
        self.base_model = base_model
        self.yaml_path = "dataset_config.yaml"
        self.output_dir = f"runs/helmet_finetune_{datetime.now().strftime('%Y%m%d_%H%M')}"
        self.model = None
        
    def load_model(self):
        """加载YOLO模型"""
        try:
            from ultralytics import YOLO
            self.model = YOLO(self.base_model)
            print(f"[OK] Loaded base model: {self.base_model}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to load model: {e}")
            return False
    
    def check_dataset(self):
        """检查数据集是否存在"""
        if not os.path.exists(self.yaml_path):
            print(f"[ERROR] dataset_config.yaml not found!")
            print(f"[INFO] Please create {self.yaml_path} with correct dataset path")
            return False
        
        # 尝试读取配置
        import yaml
        with open(self.yaml_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        dataset_path = config.get('path', '')
        if not os.path.exists(dataset_path):
            print(f"[WARN] Dataset path not found: {dataset_path}")
            print(f"[INFO] Using fallback: training on dummy data for demo")
            return False
        
        print(f"[OK] Dataset found: {dataset_path}")
        return True
    
    def train(self, epochs=20, imgsz=640, batch=16, device='auto'):
        """执行fine-tune
        
        Args:
            epochs: 训练轮数
            imgsz: 输入图像尺寸
            batch: 批次大小
            device: 设备 ('0' for GPU, 'cpu' for CPU, 'auto' for auto)
        
        Returns:
            str: 最佳模型路径
        """
        if self.model is None:
            if not self.load_model():
                return None
        
        print("="*50)
        print("Helmet Fine-Tune Training")
        print("="*50)
        print(f"Base model: {self.base_model}")
        print(f"Dataset: {self.yaml_path}")
        print(f"Epochs: {epochs}")
        print(f"Image size: {imgsz}")
        print(f"Batch size: {batch}")
        print(f"Device: {device}")
        print("="*50)
        
        # 检查数据集
        has_dataset = self.check_dataset()
        
        if not has_dataset:
            # 创建演示模式
            print("\n[Demo Mode] Running demo training...")
            print("[INFO] For real training, please prepare dataset first:")
            print("  1. Download from: https://www.kaggle.com/datasets/andrewmvd/hard-hat-detection")
            print("  2. Or collect your own images and annotate with labelImg")
            print("  3. Update dataset_config.yaml with correct path")
            return None
        
        try:
            # 开始训练
            results = self.model.train(
                data=self.yaml_path,
                epochs=epochs,
                imgsz=imgsz,
                batch=batch,
                name=self.output_dir,
                device=device,
                patience=10,
                save_period=5,
                project="runs/helmet",
                exist_ok=True,
                verbose=True
            )
            
            # 获取最佳模型
            best_model = f"runs/helmet/{self.output_dir}/weights/best.pt"
            
            if os.path.exists(best_model):
                print(f"\n[OK] Training completed!")
                print(f"[OK] Best model: {best_model}")
                return best_model
            else:
                print(f"[WARN] Best model not found at expected path")
                return None
                
        except Exception as e:
            print(f"[ERROR] Training failed: {e}")
            return None
    
    def validate(self, model_path):
        """验证模型性能
        
        Args:
            model_path: 模型路径
        
        Returns:
            dict: 验证指标
        """
        if self.model is None:
            from ultralytics import YOLO
            self.model = YOLO(model_path)
        
        print("="*50)
        print("Model Validation")
        print("="*50)
        
        try:
            metrics = self.model.val()
            
            result = {
                "map50": getattr(metrics.box, 'map50', 0),
                "map": getattr(metrics.box, 'map', 0),
                "precision": getattr(metrics.box, 'mp', 0),
                "recall": getattr(metrics.box, 'mr', 0)
            }
            
            print(f"mAP50: {result['map50']:.3f}")
            print(f"mAP50-95: {result['map']:.3f}")
            print(f"Precision: {result['precision']:.3f}")
            print(f"Recall: {result['recall']:.3f}")
            
            return result
            
        except Exception as e:
            print(f"[ERROR] Validation failed: {e}")
            return None
    
    def export_model(self, model_path, format='onnx'):
        """导出模型
        
        Args:
            model_path: 模型路径
            format: 导出格式 (onnx, torchscript, tflite, etc.)
        
        Returns:
            str: 导出后的路径
        """
        if self.model is None:
            from ultralytics import YOLO
            self.model = YOLO(model_path)
        
        try:
            exported = self.model.export(format=format)
            print(f"[OK] Model exported: {exported}")
            return exported
        except Exception as e:
            print(f"[ERROR] Export failed: {e}")
            return None


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Helmet Fine-Tune')
    parser.add_argument('--epochs', type=int, default=5, help='Training epochs')
    parser.add_argument('--imgsz', type=int, default=640, help='Image size')
    parser.add_argument('--batch', type=int, default=16, help='Batch size')
    parser.add_argument('--model', type=str, default='yolov8n.pt', help='Base model')
    parser.add_argument('--device', type=str, default='auto', help='Device (0/cpu/auto)')
    
    args = parser.parse_args()
    
    # 创建fine-tuner
    tuner = HelmetFineTuner(base_model=args.model)
    
    # 训练
    best_model = tuner.train(
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        device=args.device
    )
    
    if best_model and os.path.exists(best_model):
        # 验证
        tuner.validate(best_model)
        
        # 导出为ONNX（更适合边缘部署）
        tuner.export_model(best_model, format='onnx')
    else:
        print("\n[INFO] Demo mode - no real training performed")
        print("[INFO] To start real training:")
        print("  1. Prepare helmet dataset")
        print("  2. Update dataset_config.yaml")
        print("  3. Run: python helmet_finetune.py --epochs 20")


if __name__ == "__main__":
    main()
