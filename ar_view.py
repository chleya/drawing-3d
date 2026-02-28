# -*- coding: utf-8 -*-
"""
Drawing 3D - AR Visualization
现场增强现实

Features:
- 3D model overlay
- Construction guidance
- Distance measurement
- Annotation system
"""

class ARViewer:
    """AR Visualization System"""
    
    def __init__(self, road_system):
        self.road = road_system
        
        # AR markers
        self.markers = []
        
        # Annotations
        self.annotations = []
        
        # 3D models
        self.models = {
            'pipeline': {'name': '管道', 'color': 'blue'},
            'cable': {'name': '电缆', 'color': 'yellow'},
            'structure': {'name': '结构', 'color': 'gray'}
        }
    
    def add_marker(self, mileage, x, y, z, label):
        """Add AR marker at location"""
        marker = {
            'id': len(self.markers) + 1,
            'mileage': mileage,
            'position': (x, y, z),
            'label': label,
            'visible': True
        }
        self.markers.append(marker)
        return marker
    
    def add_annotation(self, mileage, text, author):
        """Add annotation at location"""
        annotation = {
            'id': len(self.annotations) + 1,
            'mileage': mileage,
            'text': text,
            'author': author,
            'timestamp': '2026-02-28'
        }
        self.annotations.append(annotation)
        return annotation
    
    def add_3d_model(self, model_type, mileage, position):
        """Add 3D model overlay"""
        if model_type not in self.models:
            return {'error': f'Unknown model: {model_type}'}
        
        model = {
            'type': model_type,
            'name': self.models[model_type]['name'],
            'mileage': mileage,
            'position': position,
            'color': self.models[model_type]['color']
        }
        
        return model
    
    def get_nearby_markers(self, mileage, radius_km=0.5):
        """Get markers near a location"""
        nearby = []
        for m in self.markers:
            if abs(m['mileage'] - mileage) <= radius_km:
                nearby.append(m)
        return nearby
    
    def generate_guide(self, mileage):
        """Generate AR construction guide for location"""
        guide = []
        guide.append("="*50)
        guide.append(f"AR Construction Guide - K{mileage}")
        guide.append("="*50)
        
        # Nearby markers
        markers = self.get_nearby_markers(mileage)
        if markers:
            guide.append(f"\n[Markers] ({len(markers)} found)")
            for m in markers:
                guide.append(f"  - {m['label']} at {m['position']}")
        
        # Annotations
        annotations = [a for a in self.annotations if abs(a['mileage'] - mileage) < 0.1]
        if annotations:
            guide.append(f"\n[Annotations] ({len(annotations)} found)")
            for a in annotations:
                guide.append(f"  - {a['text']} (by {a['author']})")
        
        # Available 3D models
        guide.append("\n[Available Overlays]")
        for model_type, model_info in self.models.items():
            guide.append(f"  - {model_info['name']} ({model_type})")
        
        return "\n".join(guide)


# Demo
if __name__ == "__main__":
    import sys
    sys.path.insert(0, '.')
    from main import Road3D
    
    road = Road3D()
    ar = ARViewer(road)
    
    print("="*50)
    print("AR Visualization Demo")
    print("="*50)
    
    # Add markers
    ar.add_marker(1.5, 100, 50, 0, 'Pipeline Entry')
    ar.add_marker(1.5, 120, 60, 0, 'Cable Cross')
    ar.add_marker(2.0, 200, 100, 0, 'Structure')
    
    # Add annotations
    ar.add_annotation(1.5, 'Check pipeline depth', 'Zhang San')
    ar.add_annotation(1.5, 'Warning: Cable above', 'Li Si')
    
    # Get guide
    print(ar.generate_guide(1.5))
