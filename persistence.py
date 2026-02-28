# -*- coding: utf-8 -*-
"""
Drawing 3D - Data Persistence
Save and load project data
"""

import json
import os


class DataManager:
    """Data save/load manager"""
    
    @staticmethod
    def save(road, filepath='project_data.json'):
        """Save project data to JSON"""
        data = {
            'name': road.name,
            'points': road.points,
            'knowledge': road.knowledge,
            'photos': road.photos,
            'quality': road.quality,
            'progress': road.progress
        }
        
        # Get module data
        try:
            data['cost'] = {
                'materials': road.cost.materials,
                'labor': road.cost.labor,
                'equipment': road.cost.equipment
            }
        except:
            pass
        
        try:
            data['equipment'] = road.equipment.equipment
        except:
            pass
        
        try:
            data['report'] = {
                'daily': road.report.data.get('daily', []),
                'quality': road.report.data.get('quality', []),
                'issues': road.report.data.get('issues', [])
            }
        except:
            pass
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Project saved to {filepath}")
        return filepath
    
    @staticmethod
    def load(road, filepath='project_data.json'):
        """Load project data from JSON"""
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            return False
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Restore basic data
        road.name = data.get('name', 'Road Project')
        road.points = data.get('points', [])
        road.knowledge = data.get('knowledge', {})
        road.photos = data.get('photos', [])
        road.quality = data.get('quality', [])
        road.progress = data.get('progress', [])
        
        # Restore cost data
        if 'cost' in data:
            cost_data = data['cost']
            road.cost.materials = cost_data.get('materials', [])
            road.cost.labor = cost_data.get('labor', [])
            road.cost.equipment = cost_data.get('equipment', [])
        
        # Restore equipment data
        if 'equipment' in data:
            road.equipment.equipment = data['equipment']
        
        print(f"Project loaded from {filepath}")
        return True


# Demo
if __name__ == "__main__":
    import sys
    sys.path.insert(0, '.')
    from main import Road3D
    
    # Create test project
    road = Road3D()
    for i in range(5):
        road.add_point(i, i*100, i*30)
    
    road.add_knowledge("test_key", "test_value")
    road.add_progress(0, 1, "completed", 100)
    road.add_material_cost('沥青', 100)
    
    # Save
    print("Saving...")
    DataManager.save(road, 'test_project.json')
    
    # Load into new instance
    print("\nLoading...")
    road2 = Road3D()
    DataManager.load(road2, 'test_project.json')
    
    print(f"Name: {road2.name}")
    print(f"Points: {len(road2.points)}")
    print(f"Knowledge: {road2.knowledge}")
    print(f"Progress: {road2.progress}")
    
    # Clean up
    os.remove('test_project.json')
