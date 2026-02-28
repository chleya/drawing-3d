"""
Drawing 3D - Advanced Features

More Features:
1. Cost Tracking
2. Resource Management
3. Issue Tracking
4. Document Management
5. Team Collaboration

Run: python drawing_3d/advanced.py
"""

from datetime import datetime
import json

class AdvancedRoadProject:
    """Advanced Road Project Management"""
    
    def __init__(self, name):
        self.name = name
        # Core data
        self.progress = []
        self.quality = []
        self.photos = []
        self.knowledge = {}
        
        # New features
        self.costs = []
        self.resources = []
        self.issues = []
        self.documents = []
        self.team = []
    
    # === Cost Tracking ===
    def add_cost(self, category, amount, description=""):
        self.costs.append({
            'category': category,
            'amount': amount,
            'description': description,
            'date': datetime.now().isoformat()
        })
    
    def get_total_cost(self):
        return sum(c['amount'] for c in self.costs)
    
    def get_cost_by_category(self):
        by_cat = {}
        for c in self.costs:
            cat = c['category']
            by_cat[cat] = by_cat.get(cat, 0) + c['amount']
        return by_cat
    
    # === Resource Management ===
    def add_resource(self, name, quantity, unit, status="available"):
        self.resources.append({
            'name': name,
            'quantity': quantity,
            'unit': unit,
            'status': status
        })
    
    def get_resource_summary(self):
        summary = {}
        for r in self.resources:
            name = r['name']
            summary[name] = summary.get(name, 0) + r['quantity']
        return summary
    
    # === Issue Tracking ===
    def add_issue(self, title, description, priority="medium", status="open"):
        self.issues.append({
            'title': title,
            'description': description,
            'priority': priority,
            'status': status,
            'created': datetime.now().isoformat()
        })
    
    def resolve_issue(self, title):
        for issue in self.issues:
            if issue['title'] == title:
                issue['status'] = 'resolved'
    
    # === Document Management ===
    def add_document(self, name, doc_type, path):
        self.documents.append({
            'name': name,
            'type': doc_type,
            'path': path,
            'uploaded': datetime.now().isoformat()
        })
    
    # === Team ===
    def add_team_member(self, name, role):
        self.team.append({
            'name': name,
            'role': role,
            'joined': datetime.now().isoformat()
        })
    
    # === Dashboard ===
    def generate_dashboard(self):
        total_progress = sum(p['percent'] for p in self.progress) / len(self.progress) if self.progress else 0
        total_cost = self.get_total_cost()
        open_issues = sum(1 for i in self.issues if i['status'] == 'open')
        quality_ok = sum(1 for q in self.quality if q['status'] == 'ok')
        
        dashboard = f"""
============================================================
DASHBOARD: {self.name}
============================================================

[PROGRESS]
  Overall: {total_progress:.1f}%
  Sections: {len(self.progress)}

[COSTS]
  Total: ${total_cost:,.0f}
  By Category:
"""
        for cat, amount in self.get_cost_by_category().items():
            dashboard += f"    - {cat}: ${amount:,.0f}\n"
        
        dashboard += f"""
[QUALITY]
  Records: {len(self.quality)}
  OK: {quality_ok}

[ISSUES]
  Open: {open_issues}
  Total: {len(self.issues)}

[RESOURCES]
  Types: {len(self.resources)}
"""
        
        dashboard += f"""
[TEAM]
  Members: {len(self.team)}

[DOCUMENTS]
  Files: {len(self.documents)}

============================================================
"""
        return dashboard


# Demo
print("="*60)
print("Advanced Features Demo")
print("="*60)

# Create project
project = AdvancedRoadProject("351 Highway Project")

# Progress
project.progress = [
    {'start': 0, 'end': 1, 'status': 'completed', 'percent': 100},
    {'start': 1, 'end': 2, 'status': 'completed', 'percent': 100},
    {'start': 2, 'end': 3, 'status': 'in_progress', 'percent': 70},
]

# Quality
project.quality = [
    {'mileage': 1.5, 'item': 'compaction', 'result': '98%', 'status': 'ok'},
    {'mileage': 2.3, 'item': 'temperature', 'result': '145C', 'status': 'ok'},
]

# Costs
project.add_cost("Materials", 500000, "Asphalt")
project.add_cost("Labor", 200000, "Workers")
project.add_cost("Equipment", 150000, "Machines")
project.add_cost("Materials", 300000, "Concrete")

# Resources
project.add_resource("Excavator", 5, "units")
project.add_resource("Dump Truck", 10, "units")
project.add_resource("Worker", 50, "persons")

# Issues
project.add_issue("Delay at K2+500", "Weather delay", "high")
project.add_issue("Equipment maintenance", "Need repair", "medium")

# Documents
project.add_document("design_drawing.pdf", "drawing", "/docs/")
project.add_document("contract.pdf", "contract", "/docs/")

# Team
project.add_team_member("Zhang San", "Project Manager")
project.add_team_member("Li Si", "Site Engineer")

# Dashboard
print(project.generate_dashboard())

# Issue Summary
print("\n[Issues]")
for issue in project.issues:
    print(f"  [{issue['priority'].upper()}] {issue['title']} - {issue['status']}")

print("\n" + "="*60)
print("Advanced Features Complete!")
print("="*60)
