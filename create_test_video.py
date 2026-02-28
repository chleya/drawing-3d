# -*- coding: utf-8 -*-
"""
Create a simple test video for YOLO testing
创建测试视频
"""

import cv2
import numpy as np
import os

def create_test_video(output_path='data/test_video.mp4', num_frames=100):
    """创建测试视频"""
    
    # 创建data目录
    os.makedirs('data', exist_ok=True)
    
    # 视频参数
    width, height = 640, 480
    fps = 30
    
    # 创建视频写入器
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    print(f"Creating test video: {output_path}")
    print(f"Resolution: {width}x{height}, FPS: {fps}, Frames: {num_frames}")
    
    for frame_idx in range(num_frames):
        # 创建蓝色背景
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[:] = (200, 150, 100)  # 蓝绿色背景
        
        # 添加一些移动的"人" (用矩形模拟)
        x = int((frame_idx * 5) % (width - 100))
        
        # 模拟人 (蓝色矩形)
        cv2.rectangle(frame, (x, 200), (x + 60, 400), (255, 100, 50), -1)
        
        # 模拟头 (黄色圆形 = 安全帽)
        cv2.circle(frame, (x + 30, 180), 25, (0, 255, 255), -1)
        
        # 添加文字
        cv2.putText(frame, f"Frame {frame_idx+1}/{num_frames}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # 写入帧
        out.write(frame)
        
        if (frame_idx + 1) % 30 == 0:
            print(f"Progress: {frame_idx + 1}/{num_frames}")
    
    # 释放
    out.release()
    
    print(f"\nTest video created: {output_path}")
    print(f"File size: {os.path.getsize(output_path) / 1024:.1f} KB")
    
    return output_path


if __name__ == "__main__":
    # 创建测试视频
    video_path = create_test_video()
    print(f"\nVideo ready: {video_path}")
    print("\nNow run: python quality_detection.py")
