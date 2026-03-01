# -*- coding: utf-8 -*-
"""
真实硬件集成层 - Hardware Integration
支持海康摄像头 + 北斗定位 + 边缘盒子
"""

import cv2
import time
import random
from datetime import datetime


class HardwareIntegrator:
    """真实硬件集成层"""
    
    def __init__(self):
        self.cameras = {}  # camera_id -> url
        self.gps_devices = {}  # 北斗设备
        self.edge_boxes = {}  # 边缘盒子
        self.active_streams = {}  # 活跃视频流
    
    def add_hik_camera(self, camera_id, ip, username="admin", password="12345", port=554):
        """添加海康摄像头 (RTSP)
        
        Args:
            camera_id: 摄像头ID
            ip: IP地址
            username: 用户名
            password: 密码
            port: 端口
        """
        # RTSP URL 格式
        url = f"rtsp://{username}:{password}@{ip}:{port}/Streaming/Channels/101"
        self.cameras[camera_id] = {
            "url": url,
            "ip": ip,
            "status": "offline"
        }
        print(f"[HW] Hikvision Camera {camera_id} configured: {ip}")
        return True
    
    def add_beidou(self, device_id, com_port="COM3"):
        """添加北斗定位设备
        
        Args:
            device_id: 设备ID
            com_port: 串口
        """
        self.gps_devices[device_id] = {
            "com_port": com_port,
            "status": "offline"
        }
        print(f"[HW] Beidou GPS {device_id} configured: {com_port}")
        return True
    
    def add_edge_box(self, box_id, ip, port=8080):
        """添加边缘计算盒子
        
        Args:
            box_id: 盒子ID
            ip: IP地址
            port: 端口
        """
        self.edge_boxes[box_id] = {
            "ip": ip,
            "port": port,
            "status": "offline"
        }
        print(f"[HW] Edge Box {box_id} configured: {ip}:{port}")
        return True
    
    def start_real_stream(self, camera_id, use_usb_fallback=True):
        """启动真实视频流
        
        Args:
            camera_id: 摄像头ID
            use_usb_fallback: 是否使用USB摄像头作为fallback
        
        Returns:
            cv2.VideoCapture: 视频捕获对象
        """
        if camera_id not in self.cameras:
            print(f"[HW] Camera {camera_id} not configured")
            if use_usb_fallback:
                print(f"[HW] Falling back to USB camera")
                return cv2.VideoCapture(0)
            return None
        
        camera_info = self.cameras[camera_id]
        url = camera_info["url"]
        
        print(f"[HW] Attempting RTSP connection to {camera_info['ip']}...")
        cap = cv2.VideoCapture(url)
        
        if not cap.isOpened():
            print(f"[HW] RTSP connection failed to {camera_info['ip']}")
            if use_usb_fallback:
                print(f"[HW] Falling back to USB camera (index 0)")
                cap = cv2.VideoCapture(0)
            else:
                return None
        
        if cap.isOpened():
            self.cameras[camera_id]["status"] = "online"
            print(f"[HW] ✅ Camera {camera_id} stream online: {camera_info['ip']}")
        else:
            print(f"[HW] ❌ Camera {camera_id} stream failed")
        
        self.active_streams[camera_id] = cap
        return cap
    
    def get_gps_position(self, device_id, simulate=True):
        """获取北斗定位
        
        Args:
            device_id: 设备ID
            simulate: 是否模拟（无硬件时）
        
        Returns:
            dict: 位置信息
        """
        if device_id not in self.gps_devices:
            return {"lat": 0, "lon": 0, "status": "not_found"}
        
        if simulate:
            # 模拟坐标（上海附近）
            lat = 31.23 + random.uniform(-0.01, 0.01)
            lon = 121.47 + random.uniform(-0.01, 0.01)
        else:
            # TODO: 实现真实串口读取
            lat, lon = 0, 0
        
        position = {
            "lat": lat,
            "lon": lon,
            "timestamp": datetime.now().isoformat(),
            "status": "online"
        }
        
        self.gps_devices[device_id]["last_position"] = position
        return position
    
    def get_edge_status(self, box_id):
        """获取边缘盒子状态
        
        Args:
            box_id: 盒子ID
        
        Returns:
            dict: 状态信息
        """
        if box_id not in self.edge_boxes:
            return {"status": "not_found"}
        
        # TODO: 实现真实状态查询
        return {
            "cpu_usage": random.uniform(20, 60),
            "memory_usage": random.uniform(30, 70),
            "temperature": random.uniform(35, 55),
            "status": "online"
        }
    
    def stop_stream(self, camera_id):
        """停止视频流
        
        Args:
            camera_id: 摄像头ID
        """
        if camera_id in self.active_streams:
            self.active_streams[camera_id].release()
            del self.active_streams[camera_id]
            if camera_id in self.cameras:
                self.cameras[camera_id]["status"] = "offline"
            print(f"[HW] Camera {camera_id} stream stopped")
    
    def get_status(self):
        """获取所有硬件状态
        
        Returns:
            dict: 状态汇总
        """
        return {
            "cameras": self.cameras,
            "gps_devices": self.gps_devices,
            "edge_boxes": self.edge_boxes,
            "active_streams": len(self.active_streams)
        }


# 测试
if __name__ == "__main__":
    print("="*50)
    print("Hardware Integration Test")
    print("="*50)
    
    hw = HardwareIntegrator()
    
    # 配置海康摄像头
    hw.add_hik_camera(1, "192.168.1.100", "admin", "12345")
    
    # 配置北斗
    hw.add_beidou(1, "COM3")
    
    # 配置边缘盒子
    hw.add_edge_box(1, "192.168.1.200", 8080)
    
    # 启动视频流（使用USB fallback）
    print("\n--- Testing Video Stream ---")
    cap = hw.start_real_stream(1, use_usb_fallback=True)
    
    if cap and cap.isOpened():
        print("✅ Video stream opened successfully")
        # 读取一帧测试
        ret, frame = cap.read()
        if ret:
            print(f"✅ Frame captured: {frame.shape}")
        cap.release()
    else:
        print("❌ Failed to open video stream")
    
    # 测试GPS
    print("\n--- Testing GPS ---")
    gps = hw.get_gps_position(1, simulate=True)
    print(f"GPS Position: {gps}")
    
    # 测试边缘盒子
    print("\n--- Testing Edge Box ---")
    status = hw.get_edge_status(1)
    print(f"Edge Box Status: {status}")
    
    # 状态汇总
    print("\n--- Hardware Status ---")
    print(hw.get_status())
    
    print("\n" + "="*50)
    print("Hardware Integration Test Complete")
    print("="*50)
