# -*- coding: utf-8 -*-
"""
Drawing 3D - 现场AR视图
AR View System (Simplified)
"""

from datetime import datetime
import random


class ARMarker:
    """AR标记点"""
    
    def __init__(self, marker_id, name, x, y, z, marker_type='info'):
        self.id = marker_id
        self.name = name
        self.position = {'x': x, 'y': y, 'z': z}
        self.marker_type = marker_type  # info/warning/safety/inspection
        self.content = ''
        self.visible = True
    
    def set_content(self, content):
        self.content = content


class ARScene:
    """AR场景"""
    
    def __init__(self, scene_id, name, location):
        self.id = scene_id
        self.name = name
        self.location = location
        self.markers = []
        self.models = []  # 3D模型
        self.annotations = []  # 标注
    
    def add_marker(self, marker):
        self.markers.append(marker)
        return marker
    
    def remove_marker(self, marker_id):
        self.markers = [m for m in self.markers if m.id != marker_id]
    
    def get_markers(self, marker_type=None):
        if marker_type:
            return [m for m in self.markers if m.marker_type == marker_type]
        return self.markers


class ARViewSystem:
    """AR视图系统"""
    
    def __init__(self):
        self.scenes = {}
        self.current_scene = None
        self.recordings = []  # 记录
        self.init_default_scenes()
    
    def init_default_scenes(self):
        """初始化默认场景"""
        scenes = [
            ('S001', 'K100+500 路段', 'K100+500'),
            ('S002', 'K101+000 桥梁', 'K101+000'),
            ('S003', 'K102+500 隧道', 'K102+500'),
        ]
        
        for sid, name, location in scenes:
            self.scenes[sid] = ARScene(sid, name, location)
    
    def create_scene(self, scene_id, name, location):
        """创建场景"""
        scene = ARScene(scene_id, name, location)
        self.scenes[scene_id] = scene
        return scene
    
    def set_current_scene(self, scene_id):
        """设置当前场景"""
        if scene_id in self.scenes:
            self.current_scene = self.scenes[scene_id]
            return True
        return False
    
    def add_marker_to_scene(self, scene_id, marker):
        """添加标记"""
        if scene_id in self.scenes:
            self.scenes[scene_id].add_marker(marker)
            return True
        return False
    
    def add_info_marker(self, scene_id, name, x, y, z, content):
        """添加信息标记"""
        marker = ARMarker(
            len(self.scenes.get(scene_id, ARScene('','','')).markers) + 1,
            name, x, y, z, 'info'
        )
        marker.set_content(content)
        
        if scene_id in self.scenes:
            self.scenes[scene_id].add_marker(marker)
            return marker
        return None
    
    def add_warning_marker(self, scene_id, name, x, y, z, warning):
        """添加警告标记"""
        marker = ARMarker(
            len(self.scenes.get(scene_id, ARScene('','','')).markers) + 1,
            name, x, y, z, 'warning'
        )
        marker.set_content(warning)
        
        if scene_id in self.scenes:
            self.scenes[scene_id].add_marker(marker)
            return marker
        return None
    
    def start_recording(self, scene_id):
        """开始录制"""
        recording = {
            'id': len(self.recordings) + 1,
            'scene_id': scene_id,
            'start_time': datetime.now().isoformat(),
            'status': 'recording',
            'markers': []
        }
        self.recordings.append(recording)
        return recording
    
    def stop_recording(self, recording_id):
        """停止录制"""
        for r in self.recordings:
            if r['id'] == recording_id:
                r['status'] = 'completed'
                r['stop_time'] = datetime.now().isoformat()
                return r
        return None
    
    def get_scenes(self):
        """获取场景列表"""
        return list(self.scenes.values())
    
    def get_scene_markers(self, scene_id):
        """获取场景标记"""
        if scene_id in self.scenes:
            return self.scenes[scene_id].markers
        return []
    
    def generate_overview(self, scene_id):
        """生成场景概览"""
        if scene_id not in self.scenes:
            return None
        
        scene = self.scenes[scene_id]
        markers = scene.markers
        
        overview = {
            'scene_id': scene.id,
            'scene_name': scene.name,
            'location': scene.location,
            'total_markers': len(markers),
            'marker_types': {},
            'markers': []
        }
        
        for m in markers:
            overview['marker_types'][m.marker_type] = overview['marker_types'].get(m.marker_type, 0) + 1
            overview['markers'].append({
                'id': m.id,
                'name': m.name,
                'position': m.position,
                'type': m.marker_type,
                'content': m.content[:50] + '...' if len(m.content) > 50 else m.content
            })
        
        return overview


# ==================== 运行测试 ====================

if __name__ == "__main__":
    ar = ARViewSystem()
    
    # 创建场景
    print("=== AR场景 ===")
    scene = ar.create_scene('S004', 'K103+000 施工现场', 'K103+000')
    print(f"创建场景: {scene.name}")
    
    # 设置当前场景
    ar.set_current_scene('S004')
    
    # 添加标记
    print("\n=== 添加标记 ===")
    m1 = ar.add_info_marker('S004', '进度', 100, 0, 50, '今日完成：基础浇筑80%，计划明天完成')
    print(f"添加信息标记: {m1.name}")
    
    m2 = ar.add_warning_marker('S004', '安全提醒', 150, 0, 50, '注意：临边作业，请系好安全带')
    print(f"添加警告标记: {m2.name}")
    
    # 添加更多标记
    ar.add_info_marker('S004', '材料', 120, 0, 50, '水泥：50吨，钢筋：20吨')
    ar.add_warning_marker('S004', '质量', 130, 0, 50, '混凝土养护期未到')
    
    # 概览
    print("\n=== 场景概览 ===")
    overview = ar.generate_overview('S004')
    print(f"场景: {overview['scene_name']}")
    print(f"位置: {overview['location']}")
    print(f"标记数: {overview['total_markers']}")
    print(f"类型分布: {overview['marker_types']}")
    
    # 标记列表
    print("\n标记列表:")
    for m in overview['markers']:
        print(f"  [{m['type']}] {m['name']}: {m['content'][:30]}...")
