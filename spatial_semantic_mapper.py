# -*- coding: utf-8 -*-
"""
空间语义映射器 - Spatial-Semantic Mapper
连接三维空间坐标与知识图谱语义
"""

import math
from datetime import datetime


class SpatialSemanticMapper:
    """空间语义映射器"""
    
    def __init__(self, knowledge_graph=None):
        """初始化
        
        Args:
            knowledge_graph: BlueprintKnowledgeGraph实例
        """
        self.kg = knowledge_graph
        
        # 坐标系转换参数
        self.origin = {
            'lat': 31.23,    # 基准纬度
            'lon': 121.47    # 基准经度
        }
        
        # 道路中心线 (简化：直线)
        self.center_line = {
            'start': {'stake': 'K0+000', 'lat': 31.23, 'lon': 121.47},
            'end': {'stake': 'K20+000', 'lat': 31.43, 'lon': 121.67},
        }
        
        # 已映射的点位
        self.mapped_points = {}
    
    # ========== 坐标转换 ==========
    
    def stake_to_coords(self, stake):
        """里程桩号转坐标
        
        Args:
            stake: 里程桩号 (如 K5+800)
        
        Returns:
            dict: {lat, lon}
        """
        # 解析桩号
        stake_num = self._stake_to_number(stake)
        
        # 线性插值
        total_length = 20000  # 20km
        ratio = stake_num / total_length
        
        lat = self.center_line['start']['lat'] + ratio * (self.center_line['end']['lat'] - self.center_line['start']['lat'])
        lon = self.center_line['start']['lon'] + ratio * (self.center_line['end']['lon'] - self.center_line['start']['lon'])
        
        return {'lat': lat, 'lon': lon}
    
    def coords_to_stake(self, lat, lon):
        """坐标转里程桩号
        
        Args:
            lat: 纬度
            lon: 经度
        
        Returns:
            str: 里程桩号
        """
        # 简化为直线距离
        dx = lon - self.center_line['start']['lon']
        dy = lat - self.center_line['start']['lat']
        
        total_dx = self.center_line['end']['lon'] - self.center_line['start']['lon']
        total_dy = self.center_line['end']['lat'] - self.center_line['start']['lat']
        
        if total_dx == 0 and total_dy == 0:
            ratio = 0
        else:
            # 使用欧氏距离近似
            distance = math.sqrt(dx**2 + dy**2)
            total_distance = math.sqrt(total_dx**2 + total_dy**2)
            ratio = distance / total_distance
        
        stake_num = ratio * 20000  # 20km
        return self._number_to_stake(stake_num)
    
    def _stake_to_number(self, stake):
        """桩号转数字"""
        # K5+800 -> 5800
        stake = stake.replace('K', '').replace('k', '')
        parts = stake.split('+')
        if len(parts) == 2:
            return int(parts[0]) * 1000 + int(parts[1])
        return 0
    
    def _number_to_stake(self, num):
        """数字转桩号"""
        km = int(num // 1000)
        m = int(num % 1000)
        return f"K{km}+{m:03d}"
    
    # ========== 空间查询 ==========
    
    def query_nearby(self, lat, lon, radius_meters=100):
        """查询附近的设计元素
        
        Args:
            lat: 纬度
            lon: 经度
            radius_meters: 半径(米)
        
        Returns:
            list: 附近的设计元素
        """
        # 转换为桩号
        stake = self.coords_to_stake(lat, lon)
        
        # 查知识图谱
        if self.kg:
            elements = self.kg.query_by_location(stake)
        else:
            elements = []
        
        # 添加GPS位置信息
        for e in elements:
            e['gps'] = {'lat': lat, 'lon': lon}
        
        return elements
    
    def query_by_stake_range(self, start_stake, end_stake):
        """按里程范围查询
        
        Args:
            start_stake: 起始桩号
            end_stake: 结束桩号
        
        Returns:
            list: 范围内的设计元素
        """
        if self.kg:
            return self.kg.query_by_stake_range(start_stake, end_stake)
        return []
    
    # ========== 照片关联 ==========
    
    def map_photo_to_location(self, photo_gps, photo_content=None):
        """照片GPS映射到工程位置
        
        Args:
            photo_gps: 照片GPS {'lat': float, 'lon': float}
            photo_content: 照片内容描述 (可选，用于AI识别)
        
        Returns:
            dict: 映射结果
        """
        lat = photo_gps.get('lat')
        lon = photo_gps.get('lon')
        
        if not lat or not lon:
            return {
                'status': 'error',
                'message': 'GPS坐标无效'
            }
        
        # 转换为桩号
        stake = self.coords_to_stake(lat, lon)
        
        # 计算偏移
        coords = self.stake_to_coords(stake)
        offset_meters = self._calculate_distance(
            lat, lon, coords['lat'], coords['lon']
        )
        
        # 查询该位置的设计元素
        elements = []
        if self.kg:
            elements = self.kg.query_by_location(stake)
        
        # 生成结果
        result = {
            'status': 'success',
            'gps': {'lat': lat, 'lon': lon},
            'stake': stake,
            'offset_meters': offset_meters,
            'design_elements': elements,
            'mapped_at': datetime.now().isoformat()
        }
        
        # 如果有照片内容，进行语义分析
        if photo_content:
            result['semantic_analysis'] = self._analyze_photo_content(photo_content, stake)
        
        return result
    
    def _calculate_distance(self, lat1, lon1, lat2, lon2):
        """计算两点距离(米) - 简化版"""
        # 1度 ≈ 111km
        dlat = abs(lat1 - lat2) * 111000
        dlon = abs(lon1 - lon2) * 111000 * math.cos(math.radians(lat1))
        return math.sqrt(dlat**2 + dlon**2)
    
    def _analyze_photo_content(self, content, stake):
        """分析照片内容语义"""
        # 简单的关键词匹配
        content = content.lower()
        
        analysis = {
            'construction_type': None,
            'status': None,
            'issues': []
        }
        
        # 施工类型识别
        if any(k in content for k in ['摊铺', '铺设', '沥青']):
            analysis['construction_type'] = '沥青摊铺'
        elif any(k in content for k in ['碾压', '压实']):
            analysis['construction_type'] = '碾压施工'
        elif any(k in content for k in ['钢筋', '绑扎']):
            analysis['construction_type'] = '钢筋施工'
        elif any(k in content for k in ['混凝土', '浇筑']):
            analysis['construction_type'] = '混凝土施工'
        
        # 状态识别
        if any(k in content for k in ['完成', '完工', '结束']):
            analysis['status'] = 'completed'
        elif any(k in content for k in ['进行', '正在', '施工中']):
            analysis['status'] = 'in_progress'
        elif any(k in content for k in ['准备', '开始']):
            analysis['status'] = 'pending'
        
        # 问题识别
        if any(k in content for k in ['裂缝', '裂纹', '破损']):
            analysis['issues'].append('表面裂缝')
        if any(k in content for k in ['沉降', '下沉', '不平']):
            analysis['issues'].append('不均匀沉降')
        if any(k in content for k in ['松散', '石子', '脱落']):
            analysis['issues'].append('集料松散')
        
        return analysis
    
    # ========== 三维场景集成 ==========
    
    def generate_3d_annotations(self, stake_range=None):
        """生成三维场景标注数据
        
        Args:
            stake_range: (start_stake, end_stake) 可选
        
        Returns:
            list: 三维标注列表
        """
        annotations = []
        
        # 确定范围
        if stake_range:
            start, end = stake_range
        else:
            start, end = 'K0+000', 'K20+000'
        
        # 查询所有元素
        elements = self.query_by_stake_range(start, end)
        
        for e in elements:
            stake = e.get('stake')
            if not stake:
                continue
            
            coords = self.stake_to_coords(stake)
            
            annotation = {
                'id': e.get('id'),
                'name': e.get('name'),
                'type': e.get('type'),
                'position': {
                    'lat': coords['lat'],
                    'lon': coords['lon'],
                    'elevation': e.get('properties', {}).get('elevation', 0)
                },
                'properties': e.get('properties', {}),
                'info': self._generate_info_popup(e)
            }
            
            annotations.append(annotation)
        
        return annotations
    
    def _generate_info_popup(self, element):
        """生成信息弹窗内容"""
        name = element.get('name', '')
        props = element.get('properties', {})
        
        info = f"**{name}**\n\n"
        
        if 'thickness' in props:
            info += f"厚度: {props['thickness']}mm\n"
        if 'material' in props:
            info += f"材料: {props['material']}\n"
        if 'stake' in element:
            info += f"桩号: {element['stake']}\n"
        
        return info
    
    # ========== 进度映射 ==========
    
    def map_progress_to_3d(self, progress_data):
        """将进度数据映射到三维场景
        
        Args:
            progress_data: [{stake, progress, status, date}, ...]
        
        Returns:
            list: 带进度颜色的三维点位
        """
        result = []
        
        for item in progress_data:
            stake = item.get('stake')
            progress = item.get('progress', 0)
            status = item.get('status', 'pending')
            
            # 坐标
            coords = self.stake_to_coords(stake)
            
            # 颜色 (根据状态)
            color = self._get_status_color(status, progress)
            
            result.append({
                'stake': stake,
                'position': coords,
                'progress': progress,
                'status': status,
                'color': color,
                'date': item.get('date')
            })
        
        return result
    
    def _get_status_color(self, status, progress):
        """获取状态颜色"""
        if status == 'completed' or progress >= 100:
            return '#00FF00'  # 绿色 - 完成
        elif status == 'in_progress' or progress > 0:
            return '#00BFFF'  # 蓝色 - 进行中
        else:
            return '#808080'  # 灰色 - 未开工


# ========== 测试 ==========

if __name__ == "__main__":
    from blueprint_knowledge_graph import create_sample_knowledge_graph
    
    print("="*50)
    print("Spatial-Semantic Mapper Test")
    print("="*50)
    
    # 创建知识图谱
    kg = create_sample_knowledge_graph()
    
    # 创建映射器
    mapper = SpatialSemanticMapper(kg)
    
    # 测试坐标转换
    print("\n[Stake to Coords]")
    coords = mapper.stake_to_coords('K5+800')
    print(f"K5+800 -> lat:{coords['lat']:.4f}, lon:{coords['lon']:.4f}")
    
    print("\n[Coords to Stake]")
    stake = mapper.coords_to_stake(31.23, 121.47)
    print(f"31.23, 121.47 -> {stake}")
    
    # 测试照片映射
    print("\n[Photo Mapping]")
    photo_gps = {'lat': 31.235, 'lon': 121.475}
    result = mapper.map_photo_to_location(photo_gps)
    print(f"GPS: {photo_gps}")
    print(f"Stake: {result['stake']}")
    print(f"Offset: {result['offset_meters']:.1f}m")
    
    # 测试三维标注
    print("\n[3D Annotations]")
    annotations = mapper.generate_3d_annotations('K5+000', 'K6+000')
    for a in annotations[:3]:
        print(f"  - {a['name']} @ {a['position']}")
    
    # 测试进度映射
    print("\n[Progress Mapping]")
    progress_data = [
        {'stake': 'K5+000', 'progress': 100, 'status': 'completed'},
        {'stake': 'K5+500', 'progress': 50, 'status': 'in_progress'},
        {'stake': 'K6+000', 'progress': 0, 'status': 'pending'},
    ]
    progress = mapper.map_progress_to_3d(progress_data)
    for p in progress:
        print(f"  - {p['stake']}: {p['progress']}% ({p['color']})")
    
    print("\n" + "="*50)
    print("Mapper Test Complete")
    print("="*50)
