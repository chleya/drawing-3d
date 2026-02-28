# -*- coding: utf-8 -*-
"""
Drawing 3D - Drone Inspection System
无人机巡检系统

Features:
- Drone mission planning
- Auto patrol routes
- Defect detection simulation
- Inspection reports
"""

class DroneInspector:
    """Drone Inspection System"""
    
    def __init__(self, road_system):
        self.road = road_system
        
        # Drone fleet
        self.drones = []
        
        # Inspection missions
        self.missions = []
        
        # Defect categories
        self.defect_types = {
            'crack': {'name': '裂缝', 'severity': 'high'},
            'pothole': {'name': '坑洞', 'severity': 'high'},
            'damage': {'name': '破损', 'severity': 'medium'},
            '杂物': {'name': '杂物', 'severity': 'low'},
            'water': {'name': '积水', 'severity': 'medium'}
        }
    
    def add_drone(self, name, model, capability='mapping'):
        """Add drone to fleet"""
        drone = {
            'id': len(self.drones) + 1,
            'name': name,
            'model': model,
            'capability': capability,
            'status': 'idle'
        }
        self.drones.append(drone)
        return drone
    
    def plan_mission(self, start_km, end_km, mission_type='patrol'):
        """Plan inspection mission"""
        if not self.drones:
            return {'error': 'No drones available'}
        
        # Find idle drone
        drone = next((d for d in self.drones if d['status'] == 'idle'), None)
        
        if not drone:
            return {'error': 'No idle drones'}
        
        mission = {
            'id': len(self.missions) + 1,
            'drone_id': drone['id'],
            'start_km': start_km,
            'end_km': end_km,
            'type': mission_type,
            'status': 'planned',
            'distance': end_km - start_km,
            'estimated_time': (end_km - start_km) * 10  # minutes
        }
        
        self.missions.append(mission)
        
        # Mark drone as busy
        drone['status'] = 'mission'
        
        return mission
    
    def execute_mission(self, mission_id):
        """Execute mission (simulated)"""
        mission = next((m for m in self.missions if m['id'] == mission_id), None)
        
        if not mission:
            return {'error': 'Mission not found'}
        
        # Simulate defects found
        import random
        defects = []
        
        if random.random() > 0.5:
            defect_type = random.choice(list(self.defect_types.keys()))
            defects.append({
                'type': defect_type,
                'name': self.defect_types[defect_type]['name'],
                'severity': self.defect_types[defect_type]['severity'],
                'location': f"K{random.uniform(mission['start_km'], mission['end_km']):.1f}",
                'image': f"defect_{mission_id}_{len(defects)}.jpg"
            })
        
        mission['status'] = 'completed'
        mission['defects'] = defects
        
        # Free drone
        drone = next((d for d in self.drones if d['id'] == mission['drone_id']), None)
        if drone:
            drone['status'] = 'idle'
        
        return mission
    
    def generate_report(self):
        """Generate inspection report"""
        report = []
        report.append("="*50)
        report.append("Drone Inspection Report")
        report.append("="*50)
        
        # Fleet status
        report.append("\n[Fleet Status]")
        for drone in self.drones:
            report.append(f"  {drone['name']} ({drone['model']}): {drone['status']}")
        
        # Missions
        report.append(f"\n[Missions] ({len(self.missions)} total)")
        for m in self.missions:
            status_icon = '[DONE]' if m['status'] == 'completed' else '[PLANNED]'
            defects = len(m.get('defects', []))
            report.append(f"  {status_icon} Mission {m['id']}: K{m['start_km']}-K{m['end_km']}, Defects: {defects}")
            
            # List defects
            for d in m.get('defects', []):
                severity_icon = {'high': '!!!', 'medium': '!!', 'low': '!'}.get(d['severity'], '-')
                report.append(f"      {severity_icon} {d['name']} at {d['location']}")
        
        return "\n".join(report)


# Demo
if __name__ == "__main__":
    import sys
    sys.path.insert(0, '.')
    from main import Road3D
    
    road = Road3D()
    inspector = DroneInspector(road)
    
    print("="*50)
    print("Drone Inspection Demo")
    print("="*50)
    
    # Add drones
    inspector.add_drone('UAV-01', 'DJI Mavic 3', 'mapping')
    inspector.add_drone('UAV-02', 'DJI Matrice 300', 'thermal')
    
    # Plan missions
    print("\n[Plan Mission: K1-K3]")
    mission = inspector.plan_mission(1, 3, 'patrol')
    print(f"  Mission ID: {mission.get('id')}")
    print(f"  Drone: {mission.get('drone_id')}")
    print(f"  Time: {mission.get('estimated_time')} min")
    
    # Execute
    print("\n[Execute Mission]")
    result = inspector.execute_mission(1)
    print(f"  Status: {result.get('status')}")
    print(f"  Defects found: {len(result.get('defects', []))}")
    
    # Report
    print(inspector.generate_report())
