"""
Drawing 3D - AI Question Answering
Natural Language Interface

Run: python drawing_3d/ai_qa.py
"""

class AIQA:
    """AI-powered Q&A for road project"""
    
    def __init__(self, road_system):
        self.road = road_system
        self.understanders = {
            "thickness": self._query_thickness,
            "厚度": self._query_thickness,
            "material": self._query_material,
            "材料": self._query_material,
            "compaction": self._query_compaction,
            "压实度": self._query_compaction,
            "temperature": self._query_temp,
            "温度": self._query_temp,
            "progress": self._query_progress,
            "进度": self._query_progress,
            "photo": self._query_photo,
            "照片": self._query_photo,
            "quality": self._query_quality,
            "质量": self._query_quality,
        }
    
    def _query_thickness(self, keywords):
        """Query thickness info"""
        results = self.road.query("thickness")
        if results:
            return "路面结构厚度:\n" + "\n".join(results)
        return "未找到厚度信息"
    
    def _query_material(self, keywords):
        """Query material info"""
        results = self.road.query("material")
        if results:
            return "材料信息:\n" + "\n".join(results)
        return "未找到材料信息"
    
    def _query_compaction(self, keywords):
        """Query compaction info"""
        results = self.road.query("compaction")
        if results:
            return "压实度信息:\n" + "\n".join(results)
        
        # Also check quality records
        for q in self.road.quality:
            if 'compact' in q.get('item', '').lower():
                return f"K{q['mileage']}: {q['item']} = {q['result']} ({q['status']})"
        return "未找到压实度信息"
    
    def _query_temp(self, keywords):
        """Query temperature info"""
        for q in self.road.quality:
            if 'temp' in q.get('item', '').lower():
                return f"K{q['mileage']}: {q['item']} = {q['result']}"
        return "未找到温度信息"
    
    def _query_progress(self, keywords):
        """Query progress"""
        prog = self.road.get_progress()
        details = []
        for p in self.road.progress:
            details.append(f"K{p['start']:.0f}-K{p['end']:.0f}: {p['percent']}%")
        return f"总体进度: {prog:.0f}%\n" + "\n".join(details)
    
    def _query_photo(self, keywords):
        """Query photos"""
        if not self.road.photos:
            return "暂无照片"
        
        results = ["现场照片:"]
        for p in self.road.photos:
            results.append(f"  K{p['mileage']:.1f}: {p['file']} - {p['description']}")
        return "\n".join(results)
    
    def _query_quality(self, keywords):
        """Query quality records"""
        if not self.road.quality:
            return "暂无质量记录"
        
        results = ["质量检查记录:"]
        for q in self.road.quality:
            status = "✓" if q['status'] == 'ok' else "⚠"
            results.append(f"  K{q['mileage']}: {status} {q['item']} = {q['result']}")
        return "\n".join(results)
    
    def understand(self, question):
        """Understand question and route to handler"""
        q_lower = question.lower()
        
        # Try to match keywords
        for key, handler in self.understanders.items():
            if key in q_lower:
                return handler([])
        
        # Fallback to knowledge base
        results = self.road.query(question)
        if results:
            return "找到相关信息:\n" + "\n".join(results[:5])
        
        return "抱歉，我不太理解这个问题。你可以问:\n- 路面厚度\n- 材料类型\n- 压实度\n- 施工进度\n- 现场照片\n- 质量记录"
    
    def chat(self):
        """Interactive chat"""
        print("\n" + "="*50)
        print("AI QA Assistant - Type 'exit' to quit")
        print("="*50)
        
        while True:
            try:
                q = input("\nYou: ").strip()
                if not q:
                    continue
                if q.lower() in ['exit', 'quit', 'q']:
                    break
                
                answer = self.understand(q)
                print(f"\nAI: {answer}")
            except KeyboardInterrupt:
                break
        
        print("\nGoodbye!")


# Demo
print("="*50)
print("Drawing 3D - AI Question Answering")
print("="*50)

# Import from main
import sys
sys.path.insert(0, 'drawing_3d')
from main import Road3D

# Create road with demo data
road = Road3D()

# Setup
for i in range(8):
    road.add_point(i, i * 100, i * 30)

# Knowledge
road.add_knowledge("road_K5_thickness_40", "40 mm (surface)")
road.add_knowledge("road_K5_thickness_180", "180 mm (base)")
road.add_knowledge("road_K5_thickness_300", "300 mm (subbase)")
road.add_knowledge("road_K5_material_asphalt", "AC-13")
road.add_knowledge("road_K5_material_stone", "水泥稳定碎石")
road.add_knowledge("road_K5_compaction", "98%")
road.add_knowledge("bridge_K6_concrete", "C50")
road.add_knowledge("bridge_K6_rebar", "HRB400")

# Photos
road.add_photo(1.5, "K1+500.jpg", "水稳层施工")
road.add_photo(2.3, "K2+300.jpg", "沥青摊铺")
road.add_photo(3.8, "K3+800.jpg", "碾压施工")

# Quality
road.add_quality(1.5, "compaction", "98%", "ok")
road.add_quality(2.3, "temperature", "145C", "ok")
road.add_quality(3.8, "compaction", "96%", "warning")

# Progress
road.add_progress(0, 1, "completed", 100)
road.add_progress(1, 2, "completed", 100)
road.add_progress(2, 3, "completed", 100)
road.add_progress(3, 4, "in_progress", 70)
road.add_progress(4, 5, "in_progress", 40)

# AI QA
print("\n[AI Q&A Test]")
qa = AIQA(road)

questions = [
    "路面厚度多少?",
    "用什么材料?",
    "压实度怎么样?",
    "施工进度如何?",
    "有哪些照片?",
    "质量记录?",
    "今天天气怎么样?",  # Unknown
]

for q in questions:
    print(f"\nYou: {q}")
    a = qa.understand(q)
    print(f"AI: {a}")

print("\n" + "="*50)
print("AI Q&A Module Complete!")
print("="*50)
