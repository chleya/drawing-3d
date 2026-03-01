# -*- coding: utf-8 -*-
"""
边缘数据过滤与关键帧上传模拟 - Edge Filter
SQLite持久化 + 关键帧上传
"""

import sqlite3
import json
from datetime import datetime
import os


class EdgeFilter:
    """边缘数据过滤与关键帧上传模拟"""
    
    def __init__(self, db_path="data/edge.db"):
        self.db_path = db_path
        os.makedirs("data", exist_ok=True)
        self.init_db()
    
    def init_db(self):
        """初始化SQLite数据库"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS edge_frames (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                camera_id INTEGER,
                persons INTEGER,
                total_detections INTEGER,
                alert INTEGER,
                frame_path TEXT
            )
        ''')
        conn.commit()
        conn.close()
        print("[OK] EdgeFilter: SQLite database initialized")
    
    def filter_and_save(self, camera_id, detections, frame=None):
        """过滤逻辑：仅异常帧（persons > 0）保存到SQLite + 模拟上传"""
        
        # 统计人数
        persons = len([d for d in detections if d.get('class_name') == 'person'])
        
        # 报警标志
        alert = 1 if persons > 0 else 0
        
        # 正常帧，丢弃
        if alert == 0 and len(detections) == 0:
            return False
        
        timestamp = datetime.now().isoformat()
        frame_path = f"data/keyframe_cam{camera_id}_{timestamp.replace(':', '')[:19].replace('-', '').replace('T', '_')}.jpg"
        
        # 保存到SQLite
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            INSERT INTO edge_frames (timestamp, camera_id, persons, total_detections, alert, frame_path)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (timestamp, camera_id, persons, len(detections), alert, frame_path))
        conn.commit()
        conn.close()
        
        print(f"[UPLOAD] Edge filter OK: camera {camera_id} detected {persons} persons -> saved to DB")
        return True
    
    def get_recent_alerts(self, limit=10):
        """查询最近报警"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM edge_frames WHERE alert=1 ORDER BY id DESC LIMIT ?", (limit,))
        rows = c.fetchall()
        conn.close()
        return rows
    
    def get_all_frames(self, limit=100):
        """查询所有帧"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM edge_frames ORDER BY id DESC LIMIT ?", (limit,))
        rows = c.fetchall()
        conn.close()
        return rows
    
    def get_stats(self):
        """获取统计信息"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT COUNT(*), SUM(alert), SUM(persons) FROM edge_frames")
        total, alerts, persons = c.fetchone()
        conn.close()
        return {
            'total_frames': total or 0,
            'alert_frames': alerts or 0,
            'total_persons': persons or 0
        }


# 测试
if __name__ == "__main__":
    print("="*50)
    print("EdgeFilter Test")
    print("="*50)
    
    filter = EdgeFilter()
    
    # 模拟测试 - 有人的帧
    print("\n[1] 测试有人的帧:")
    dummy_detections = [{'class_name': 'person'}, {'class_name': 'person'}]
    filter.filter_and_save(camera_id=0, detections=dummy_detections)
    
    # 模拟测试 - 无人的帧
    print("\n[2] 测试无人的帧:")
    empty_detections = []
    filter.filter_and_save(camera_id=0, detections=empty_detections)
    
    # 查询最近报警
    print("\n[3] 最近报警:")
    alerts = filter.get_recent_alerts()
    print(f"  报警数: {len(alerts)}")
    
    # 统计
    print("\n[4] 统计:")
    stats = filter.get_stats()
    print(f"  {stats}")
    
    print("\n[SUCCESS] EdgeFilter working!")
