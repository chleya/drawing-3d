# -*- coding: utf-8 -*-
"""
施工风险预测模型 - Risk Predictor
副驾驶模式核心模块
"""

import pandas as pd
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
import numpy as np


class RiskPredictor:
    """施工风险预测模型（副驾驶核心）"""
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False
        self.data_history = []  # 缓存实时数据
        self.risk_thresholds = {
            'high': {'persons': 10, 'violations': 1},
            'medium': {'persons': 5, 'violations': 0},
        }
    
    def add_data_point(self, timestamp=None, persons=0, violations=0, weather="normal"):
        """实时添加数据点
        
        Args:
            timestamp: 时间戳
            persons: 当前人数
            violations: 违章次数
            weather: 天气状况
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        risk_level = self._label_risk(persons, violations)
        
        self.data_history.append({
            "timestamp": timestamp,
            "persons": persons,
            "violations": violations,
            "weather": weather,
            "risk_level": risk_level
        })
        
        return len(self.data_history)
    
    def _label_risk(self, persons, violations):
        """简单标签规则"""
        if violations > 0:
            return "high"
        if persons > 10:
            return "high"
        if persons > 5:
            return "medium"
        return "low"
    
    def train_from_history(self):
        """从历史数据训练"""
        if len(self.data_history) < 20:
            print(f"[WARN] 数据不足，无法训练 (当前: {len(self.data_history)}条)")
            return False
        
        df = pd.DataFrame(self.data_history)
        
        # 特征
        X = df[['persons', 'violations']].values
        
        # 标签转换为数值
        label_map = {'low': 0, 'medium': 1, 'high': 2}
        y = df['risk_level'].map(label_map).values
        
        self.model.fit(X, y)
        self.is_trained = True
        
        print(f"[OK] Risk prediction model trained! Data: {len(df)} samples")
        return True
    
    def predict_risk(self, current_persons, current_violations):
        """实时预测
        
        Args:
            current_persons: 当前人数
            current_violations: 当前违章次数
        
        Returns:
            dict: 预测结果
        """
        if not self.is_trained:
            # 未训练时使用规则预测
            risk_level = self._label_risk(current_persons, current_violations)
            return {
                "risk_level": risk_level,
                "confidence": 0.5,
                "advice": self._generate_advice(risk_level),
                "mode": "rule-based"
            }
        
        # 模型预测
        X = np.array([[current_persons, current_violations]])
        pred = self.model.predict(X)[0]
        prob = self.model.predict_proba(X)[0]
        
        # 数值转标签
        label_map = {0: 'low', 1: 'medium', 2: 'high'}
        risk_level = label_map[pred]
        
        return {
            "risk_level": risk_level,
            "confidence": float(max(prob)),
            "advice": self._generate_advice(risk_level),
            "mode": "ml-based"
        }
    
    def _generate_advice(self, risk_level):
        """根据风险等级生成建议"""
        if risk_level == "high":
            return "[ALERT] High risk! Stop work immediately, check helmet compliance!"
        elif risk_level == "medium":
            return "[WARNING] Medium risk: Increase patrol, remind workers to wear PPE"
        else:
            return "[OK] Normal: Continue construction"
    
    def get_risk_trend(self, window=10):
        """获取风险趋势
        
        Args:
            window: 窗口大小
        
        Returns:
            dict: 趋势统计
        """
        if len(self.data_history) < window:
            window = len(self.data_history)
        
        recent = self.data_history[-window:]
        
        counts = {'low': 0, 'medium': 0, 'high': 0}
        for d in recent:
            counts[d['risk_level']] = counts.get(d['risk_level'], 0) + 1
        
        return {
            'window': window,
            'counts': counts,
            'dominant_risk': max(counts, key=counts.get),
            'avg_persons': sum(d['persons'] for d in recent) / window
        }
    
    def get_stats(self):
        """获取统计信息"""
        return {
            'total_data_points': len(self.data_history),
            'is_trained': self.is_trained,
            'risk_trend': self.get_risk_trend()
        }


# 测试
if __name__ == "__main__":
    print("="*50)
    print("Risk Predictor Test")
    print("="*50)
    
    predictor = RiskPredictor()
    
    # 模拟实时数据
    print("\n[1] Adding simulated data...")
    for i in range(25):
        persons = i % 15  # 0-14人
        violations = 1 if i % 10 == 0 else 0  # 每10次1次违章
        predictor.add_data_point(persons=persons, violations=violations)
    
    print(f"    Total data points: {len(predictor.data_history)}")
    
    # 训练模型
    print("\n[2] Training model...")
    predictor.train_from_history()
    
    # 预测
    print("\n[3] Testing predictions...")
    
    test_cases = [
        (3, 0),   # 3人，无违章
        (6, 0),   # 6人，无违章
        (8, 1),   # 8人，有违章
        (12, 2),  # 12人，严重违章
    ]
    
    for persons, violations in test_cases:
        result = predictor.predict_risk(persons, violations)
        print(f"    Persons={persons}, Violations={violations} -> {result}")
    
    # 趋势
    print("\n[4] Risk trend:")
    trend = predictor.get_risk_trend()
    print(f"    {trend}")
    
    # 统计
    print("\n[5] Stats:")
    stats = predictor.get_stats()
    print(f"    {stats}")
    
    print("\n[SUCCESS] Risk Predictor working!")
