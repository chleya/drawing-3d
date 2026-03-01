# -*- coding: utf-8 -*-
"""
风险预测与现有检测集成 - Risk Integrator
桥接摄像头检测与风险预测
"""

from risk_predictor import RiskPredictor
from yolo_detector import YOLODetector
from datetime import datetime
import cv2


class RiskIntegrator:
    """风险预测与现有检测集成"""
    
    def __init__(self):
        self.predictor = RiskPredictor()
        self.detector = YOLODetector()
        self.detector.load_model()
        self.frame_count = 0
        self.last_risk = None
    
    def process_frame(self, frame):
        """处理单帧：检测 → 风险预测 → 建议
        
        Args:
            frame: 视频帧
        
        Returns:
            dict: 处理结果
        """
        # YOLO检测
        detections = self.detector.detect_frame(frame)
        
        # 统计人数
        persons = len([d for d in detections if d['class_name'] == 'person'])
        
        # 违章统计 (当前COCO无helmet，后续fine-tune后替换)
        violations = 0  # 预留
        
        # 添加到历史
        self.predictor.add_data_point(
            timestamp=datetime.now(),
            persons=persons,
            violations=violations
        )
        
        # 每10帧训练一次（模拟在线学习）
        self.frame_count += 1
        if self.frame_count % 10 == 0 and len(self.predictor.data_history) >= 20:
            self.predictor.train_from_history()
        
        # 预测风险
        risk = self.predictor.predict_risk(persons, violations)
        self.last_risk = risk
        
        return {
            "persons": persons,
            "violations": violations,
            "risk": risk,
            "detections": detections,
            "frame_count": self.frame_count
        }
    
    def annotate_frame(self, frame, result):
        """在帧上叠加风险信息
        
        Args:
            frame: 原始帧
            result: process_frame的结果
        
        Returns:
            annotated: 标注后的帧
        """
        annotated = frame.copy()
        
        risk = result.get('risk', {})
        risk_level = risk.get('risk_level', 'unknown')
        confidence = risk.get('confidence', 0)
        advice = risk.get('advice', '')
        
        # 颜色根据风险等级
        if risk_level == 'high':
            color = (0, 0, 255)  # 红色
        elif risk_level == 'medium':
            color = (0, 165, 255)  # 橙色
        else:
            color = (0, 255, 0)  # 绿色
        
        # 绘制风险等级
        text1 = f"Risk: {risk_level.upper()} ({confidence:.0%})"
        cv2.putText(annotated, text1, (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        # 绘制建议
        if advice:
            cv2.putText(annotated, advice[:50], (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # 绘制人数
        cv2.putText(annotated, f"Persons: {result['persons']}", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        return annotated
    
    def get_current_advice(self):
        """获取当前最新建议"""
        if not self.predictor.data_history:
            return "No data yet"
        
        latest = self.predictor.data_history[-1]
        return self.predictor._generate_advice(latest.get("risk_level", "low"))
    
    def get_risk_stats(self):
        """获取风险统计"""
        return self.predictor.get_stats()


# 全局实例（用于Web API）
_integrator = None

def get_integrator():
    """获取全局集成器"""
    global _integrator
    if _integrator is None:
        _integrator = RiskIntegrator()
    return _integrator


# 测试
if __name__ == "__main__":
    print("="*50)
    print("Risk Integrator Test")
    print("="*50)
    
    integrator = RiskIntegrator()
    
    # 模拟处理几帧
    print("\n[1] Processing simulated frames...")
    import numpy as np
    
    for i in range(25):
        # 创建模拟帧
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        result = integrator.process_frame(frame)
        
        if i % 10 == 0:
            print(f"    Frame {i}: persons={result['persons']}, risk={result['risk']['risk_level']}")
    
    # 获取建议
    print("\n[2] Current advice:")
    advice = integrator.get_current_advice()
    print(f"    {advice}")
    
    # 统计
    print("\n[3] Risk stats:")
    stats = integrator.get_risk_stats()
    print(f"    {stats}")
    
    # 测试帧标注
    print("\n[4] Frame annotation test:")
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    result = integrator.process_frame(frame)
    annotated = integrator.annotate_frame(frame, result)
    print(f"    Annotated frame shape: {annotated.shape}")
    
    print("\n[SUCCESS] Risk Integrator working!")
