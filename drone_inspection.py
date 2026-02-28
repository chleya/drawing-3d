# -*- coding: utf-8 -*-
"""
Drawing 3D - 无人机巡检系统
Drone Inspection System
"""

import random
from datetime import datetime


class DroneInspection:
    """无人机巡检"""
    
    def __init__(self):
        self.flights = []  # 飞行记录
        self.inspections = []  # 检查记录
        self.alerts = []  # 告警记录
    
    def start_flight(self, location, altitude=100, duration=30):
        """开始飞行"""
        flight = {
            'id': len(self.flights) + 1,
            'location': location,
            'altitude': altitude,
            'duration': duration,
            'start_time': datetime.now().isoformat(),
            'status': 'flying'
        }
        self.flights.append(flight)
        return flight
    
    def end_flight(self, flight_id):
        """结束飞行"""
        for f in self.flights:
            if f['id'] == flight_id:
                f['status'] = 'completed'
                f['end_time'] = datetime.now().isoformat()
                return f
        return None
    
    def capture_image(self, flight_id, position):
        """拍摄照片"""
        image = {
            'flight_id': flight_id,
            'position': position,
            'timestamp': datetime.now().isoformat(),
            'type': 'photo',
            # 模拟图片URL
            'url': f'/images/inspection_{len(self.inspections)}.jpg'
        }
        self.inspections.append(image)
        return image
    
    def record_video(self, flight_id, duration=60):
        """录制视频"""
        video = {
            'flight_id': flight_id,
            'duration': duration,
            'timestamp': datetime.now().isoformat(),
            'type': 'video',
            'url': f'/videos/inspection_{len(self.inspections)}.mp4'
        }
        self.inspections.append(video)
        return video
    
    def detect_issue(self, flight_id, issue_type, description, severity='medium'):
        """发现问题"""
        issue = {
            'id': len(self.alerts) + 1,
            'flight_id': flight_id,
            'issue_type': issue_type,  # 安全隐患/质量问题/设备故障
            'description': description,
            'severity': severity,  # high/medium/low
            'status': 'open',  # open/resolved
            'timestamp': datetime.now().isoformat()
        }
        self.alerts.append(issue)
        return issue
    
    def resolve_issue(self, issue_id, solution=''):
        """解决问题"""
        for issue in self.alerts:
            if issue['id'] == issue_id:
                issue['status'] = 'resolved'
                issue['solution'] = solution
                issue['resolve_time'] = datetime.now().isoformat()
                return issue
        return None
    
    def get_flights(self):
        """获取飞行记录"""
        return self.flights
    
    def get_alerts(self, status=None):
        """获取告警"""
        if status:
            return [a for a in self.alerts if a['status'] == status]
        return self.alerts
    
    def get_inspections(self):
        """获取检查记录"""
        return self.inspections
    
    def generate_report(self):
        """生成巡检报告"""
        total_flights = len(self.flights)
        completed_flights = sum(1 for f in self.flights if f['status'] == 'completed')
        
        open_alerts = len([a for a in self.alerts if a['status'] == 'open'])
        resolved_alerts = len([a for a in self.alerts if a['status'] == 'resolved'])
        
        high_severity = len([a for a in self.alerts if a['severity'] == 'high' and a['status'] == 'open'])
        
        return {
            'total_flights': total_flights,
            'completed_flights': completed_flights,
            'total_inspections': len(self.inspections),
            'total_alerts': len(self.alerts),
            'open_alerts': open_alerts,
            'resolved_alerts': resolved_alerts,
            'high_severity_alerts': high_severity,
            'timestamp': datetime.now().isoformat()
        }


# ==================== 模拟检测 ====================

class IssueDetector:
    """问题检测器 (简化版)"""
    
    # 预定义问题类型
    ISSUE_TYPES = {
        '安全隐患': ['未戴安全帽', '高空作业未系安全带', '临边无防护', '用电不规范'],
        '质量问题': ['混凝土裂缝', '钢筋外露', '防水层破损', '墙面不平整'],
        '设备故障': ['设备漏油', '电线裸露', '支架松动', '仪表失灵'],
        '环境问题': ['积水', '扬尘', '杂物堆积', '道路损坏']
    }
    
    @classmethod
    def detect_from_image(cls):
        """模拟图像识别检测"""
        # 随机选择一个类型
        category = random.choice(list(cls.ISSUE_TYPES.keys()))
        issue = random.choice(cls.ISSUE_TYPES[category])
        severity = random.choice(['high', 'medium', 'low'])
        
        return {
            'category': category,
            'issue': issue,
            'severity': severity,
            'confidence': round(random.uniform(0.7, 0.99), 2),
            'timestamp': datetime.now().isoformat()
        }


# ==================== 运行测试 ====================

if __name__ == "__main__":
    drone = DroneInspection()
    
    # 开始飞行
    print("=== 无人机巡检 ===")
    flight = drone.start_flight('K100+500', altitude=50, duration=30)
    print(f"飞行开始: #{flight['id']} - {flight['location']}")
    
    # 拍摄照片
    for i in range(3):
        img = drone.capture_image(flight['id'], f'K100+{500+i*10}')
        print(f"拍照: {img['position']}")
    
    # 检测问题
    for _ in range(2):
        detection = IssueDetector.detect_from_image()
        issue = drone.detect_issue(
            flight['id'],
            detection['category'],
            detection['issue'],
            detection['severity']
        )
        print(f"发现问题: [{detection['severity']}] {detection['issue']}")
    
    # 结束飞行
    drone.end_flight(flight['id'])
    print("飞行结束")
    
    # 报告
    print("\n=== 巡检报告 ===")
    report = drone.generate_report()
    for k, v in report.items():
        print(f"{k}: {v}")
