# -*- coding: utf-8 -*-
"""
AI建议反馈循环 - Feedback Loop
人工确认/拒绝 → 数据回流 → 模型改进
"""

import json
import os
from datetime import datetime
from risk_predictor import RiskPredictor


class FeedbackLoop:
    """AI建议反馈循环（人工确认 → 数据回流 → 模型改进）"""
    
    def __init__(self, feedback_file="data/feedback.jsonl"):
        self.feedback_file = feedback_file
        self.predictor = RiskPredictor()
        
        # 确保目录存在
        os.makedirs(os.path.dirname(feedback_file) if os.path.dirname(feedback_file) else "data", exist_ok=True)
    
    def record_feedback(self, suggestion_id, original_risk, original_strategy, 
                       user_action, user_comment=""):
        """记录用户反馈
        
        Args:
            suggestion_id: 建议ID
            original_risk: 原始风险等级
            original_strategy: 原始策略
            user_action: 用户操作 (accept/reject/modify)
            user_comment: 用户评论
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "suggestion_id": suggestion_id,
            "original_risk": original_risk,
            "original_strategy": original_strategy,
            "user_action": user_action,
            "user_comment": user_comment,
            "adjusted_risk": None
        }
        
        with open(self.feedback_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        
        print(f"[FEEDBACK] Recorded: {user_action} - {original_strategy}")
        
        return entry
    
    def get_recent_feedback(self, limit=10):
        """获取最近反馈"""
        if not os.path.exists(self.feedback_file):
            return []
        
        with open(self.feedback_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        feedbacks = []
        for line in lines[-limit:]:
            if line.strip():
                feedbacks.append(json.loads(line.strip()))
        
        return feedbacks
    
    def retrain_with_feedback(self):
        """用反馈数据微调模型
        
        Returns:
            str: 训练结果信息
        """
        if not os.path.exists(self.feedback_file):
            return "No feedback data"
        
        with open(self.feedback_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        if not lines:
            return "No feedback data"
        
        # 分析反馈
        accept_count = 0
        reject_count = 0
        modify_count = 0
        
        feedback_data = []
        
        for line in lines:
            fb = json.loads(line.strip())
            action = fb.get("user_action", "")
            
            if action == "accept":
                accept_count += 1
            elif action == "reject":
                reject_count += 1
            elif action == "modify":
                modify_count += 1
                
                # 修改建议：添加新的训练样本
                comment = fb.get("user_comment", "")
                if "lower" in comment.lower() or "降低" in comment:
                    # 用户认为风险过高，调整为低
                    feedback_data.append({
                        "persons": 3,
                        "violations": 0,
                        "risk_level": "low"
                    })
                elif "higher" in comment.lower() or "提高" in comment:
                    # 用户认为风险过低，调整为高
                    feedback_data.append({
                        "persons": 8,
                        "violations": 2,
                        "risk_level": "high"
                    })
        
        # 如果有有效反馈，添加到训练数据
        if feedback_data:
            self.predictor.data_history.extend(feedback_data)
            self.predictor.train_from_history()
            return f"Model retrained with {len(feedback_data)} feedback samples. Accepts: {accept_count}, Rejects: {reject_count}, Modifies: {modify_count}"
        
        return f"Feedback analyzed. Accepts: {accept_count}, Rejects: {reject_count}, Modifies: {modify_count}. No retraining needed."
    
    def get_feedback_stats(self):
        """获取反馈统计"""
        feedbacks = self.get_recent_feedback(limit=100)
        
        if not feedbacks:
            return {"total": 0}
        
        stats = {"accept": 0, "reject": 0, "modify": 0}
        
        for fb in feedbacks:
            action = fb.get("user_action", "")
            if action in stats:
                stats[action] += 1
        
        stats["total"] = len(feedbacks)
        
        return stats


# 全局实例
_feedback_loop = None

def get_feedback_loop():
    """获取全局反馈循环实例"""
    global _feedback_loop
    if _feedback_loop is None:
        _feedback_loop = FeedbackLoop()
    return _feedback_loop


# 测试
if __name__ == "__main__":
    print("="*50)
    print("Feedback Loop Test")
    print("="*50)
    
    loop = FeedbackLoop()
    
    # 记录反馈
    print("\n[1] Recording feedback...")
    loop.record_feedback("sug-001", "high", "STOP: Pause high-risk work", "reject", "weather is fine")
    loop.record_feedback("sug-002", "medium", "PATROL: Increase frequency", "accept")
    loop.record_feedback("sug-003", "low", "OK: Continue normal", "modify", "risk should be higher")
    
    # 查看反馈
    print("\n[2] Recent feedback:")
    recent = loop.get_recent_feedback(limit=3)
    for fb in recent:
        print(f"    {fb['user_action']}: {fb['original_strategy'][:40]}")
    
    # 统计
    print("\n[3] Stats:")
    stats = loop.get_feedback_stats()
    print(f"    {stats}")
    
    # 微调
    print("\n[4] Retrain with feedback:")
    result = loop.retrain_with_feedback()
    print(f"    {result}")
    
    print("\n[SUCCESS] Feedback Loop working!")
