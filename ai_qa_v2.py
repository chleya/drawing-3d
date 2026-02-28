# -*- coding: utf-8 -*-
"""
Drawing 3D - AI Q&A System V2
With Intent Recognition + Reasoning
"""


class AIQAV2:
    """Enhanced AI Q&A with understanding"""
    
    def __init__(self, road_system):
        self.road = road_system
        self.conversation_history = []
        
        # Intent patterns
        self.intents = {
            'query': {
                'keywords': ['什么', '多少', '进度', '状态', '查看', '查询', 'what', 'how', 'is'],
                'description': '查询信息'
            },
            'analysis': {
                'keywords': ['分析', '是否', '正常', '为什么', '原因', 'analyze', 'why'],
                'description': '分析情况'
            },
            'suggestion': {
                'keywords': ['建议', '应该', '怎么办', '如何', 'should', 'what to do'],
                'description': '获取建议'
            },
            'prediction': {
                'keywords': ['什么时候', '预测', '预计', 'when', 'predict', 'will', '完工', '完成', '结束', '多久'],
                'description': '预测未来'
            },
            'comparison': {
                'keywords': ['比较', '对比', '差别', '区别', 'compare', 'vs', 'versus'],
                'description': '比较分析'
            }
        }
        
        # Entity patterns
        self.entities = {
            'progress': ['进度', '完成', 'percent', 'progress', '完成了多少'],
            'cost': ['成本', '费用', '钱', 'cost', '花费', '多少钱'],
            'weather': ['天气', '温度', 'weather', '下雨', '晴天'],
            'quality': ['质量', '压实度', '厚度', 'quality', '平整度'],
            'equipment': ['设备', '机械', 'equipment', '压路机', '摊铺机'],
            'material': ['材料', '沥青', '水泥', 'material'],
            'time': ['时间', '工期', '什么时候', 'time', 'when'],
            'plan': ['计划', '规划', '方案', 'plan', '安排'],
            'quality_check': ['质量', '检测', '压实度', '厚度', 'quality', '检测'],
            'safety': ['安全', '风险', '预警', 'safety', '危险']
        }
    
    # === Intent Recognition ===
    def recognize_intent(self, question):
        """Recognize user intent"""
        q = question.lower()
        
        for intent_name, intent_data in self.intents.items():
            for keyword in intent_data['keywords']:
                if keyword in q:
                    return intent_name
        
        return 'query'  # default
    
    # === Entity Extraction ===
    def extract_entities(self, question):
        """Extract entities from question"""
        q = question.lower()
        found = []
        
        for entity_name, keywords in self.entities.items():
            for keyword in keywords:
                if keyword in q:
                    found.append(entity_name)
                    break
        
        return found if found else ['general']
    
    # === Reasoning Engine ===
    def reason(self, intent, entities, question):
        """Multi-step reasoning"""
        
        # Query + Progress
        if intent == 'query' and 'progress' in entities:
            return self._query_progress()
        
        # Query + Cost
        if intent == 'query' and 'cost' in entities:
            return self._query_cost()
        
        # Query + Weather
        if intent == 'query' and 'weather' in entities:
            return self._query_weather()
        
        # Query + Quality
        if intent == 'query' and 'quality' in entities:
            return self._query_quality()
        
        # Query + Equipment
        if intent == 'query' and 'equipment' in entities:
            return self._query_equipment()
        
        # Analysis + Progress
        if intent == 'analysis' and 'progress' in entities:
            return self._analyze_progress()
        
        # Analysis + Weather + Impact
        if 'weather' in entities and ('影响' in question or 'impact' in question.lower()):
            return self._analyze_weather_impact()
        
        # Suggestion + Weather
        if intent == 'suggestion' and 'weather' in entities:
            return self._suggest_weather()
        
        # Prediction + Time (or explicit completion question)
        if intent == 'prediction' and 'time' in entities:
            return self._predict_time()
        
        # Quality check
        if 'quality_check' in entities or '质量' in question:
            return self._query_quality_check()
        
        # Safety check
        if 'safety' in entities or '安全' in question or '风险' in question:
            return self._query_safety()
        
        # Also check for completion questions directly
        if '完工' in question or '结束' in question:
            return self._predict_time()
        
        # Query + Plan
        if 'plan' in entities or '计划' in question or '方案' in question:
            return self._query_plan()
        
        # Default: general query
        return self._general_query(question)
    
    # === Query Handlers ===
    def _query_progress(self):
        """Query progress"""
        prog = self.road.get_progress()
        
        details = []
        for p in self.road.progress:
            status_map = {"completed": "[Done]", "in_progress": "[Doing]", "not_started": "[Todo]"}
            status = status_map.get(p['status'], "[Unknown]")
            details.append(f"  K{p['start']:.0f}-K{p['end']:.0f}: {status} {p['percent']}%")
        
        return f"[Progress] Total: {prog:.1f}%\n" + "\n".join(details)
    
    def _query_cost(self):
        """Query cost"""
        cost = self.road.get_cost_summary()
        return (f"[Cost] Summary\n"
                f"  Total: {cost['total']:,.0f} Yuan\n"
                f"  Material: {cost['material']:,.0f} Yuan\n"
                f"  Labor: {cost['labor']:,.0f} Yuan\n"
                f"  Equipment: {cost['equipment']:,.0f} Yuan")
    
    def _query_weather(self):
        """Query weather"""
        w = self.road.get_weather()
        can, msg = self.road.can_construct_today()
        
        weather_map = {'sunny': 'Sunny', 'cloudy': 'Cloudy', 'rainy': 'Rainy', 'stormy': 'Stormy'}
        weather = weather_map.get(w['weather'], w['weather'])
        
        return (f"[Weather] {weather}, {w['temperature']}C\n"
                f"  Humidity: {w['humidity']}%, Wind: {w['wind_speed']} m/s\n"
                f"  Construction: {'OK' if can else 'NO'} - {msg}")
    
    def _query_quality(self):
        """Query quality"""
        if not self.road.quality:
            return "[Quality] No records"
        
        results = ["[Quality] Records:"]
        for q in self.road.quality:
            status = "[OK]" if q['status'] == 'ok' else "[WARN]"
            results.append(f"  K{q['mileage']}: {status} {q['item']} = {q['result']}")
        
        return "\n".join(results)
    
    def _query_equipment(self):
        """Query equipment"""
        util = self.road.get_device_utilization()
        
        return (f"[Equipment] Status\n"
                f"  Total: {util['total']}, Running: {util['running']}, "
                f"Idle: {util['idle']}, Maintenance: {util['maintenance']}\n"
                f"  Utilization: {util['utilization_rate']:.1f}%")
    
    def _query_plan(self):
        """Query construction plan"""
        try:
            plan = self.road.generate_plan(1, 'asphalt')
            
            result = [f"[Construction Plan]"]
            result.append(f"  Method: {plan.get('method', 'N/A')}")
            result.append(f"  Est. Days: {plan.get('estimated_days', 'N/A')}")
            result.append(f"  Layers: {', '.join(plan.get('layers', []))}")
            result.append(f"  Equipment: {', '.join(plan.get('equipment_needed', []))}")
            
            if plan.get('risks'):
                result.append("\n  Risks:")
                for risk in plan['risks'][:3]:
                    result.append(f"    [{risk['level']}] {risk['message']}")
            
            if plan.get('recommendations'):
                result.append("\n  Recommendations:")
                for rec in plan['recommendations'][:3]:
                    result.append(f"    - {rec}")
            
            return "\n".join(result)
        except Exception as e:
            return f"[Plan] Error: {str(e)}"
    
    def _query_quality_check(self):
        """Query quality check"""
        try:
            report = self.road.quality_report()
            return report
        except Exception as e:
            return f"[Quality] Error: {str(e)}"
    
    def _query_safety(self):
        """Query safety status"""
        try:
            report = self.road.safety_report()
            return report
        except Exception as e:
            return f"[Safety] Error: {str(e)}"
    
    # === Analysis Handlers ===
    def _analyze_progress(self):
        """Analyze progress status"""
        prog = self.road.get_progress()
        
        if prog >= 80:
            return f"[Analysis] Progress is GOOD! {prog:.0f}% completed, ahead of schedule"
        elif prog >= 50:
            return f"[Analysis] Progress is NORMAL. {prog:.0f}% completed, keep going"
        else:
            return f"[Analysis] Progress is SLOW. {prog:.0f}% completed, need to speed up"
    
    def _analyze_weather_impact(self):
        """Analyze weather impact"""
        w = self.road.get_weather()
        impacts = self.road.get_weather_impact(w)
        
        result = [f"[Weather Impact] ({w['weather']}, {w['temperature']}C)"]
        for impact in impacts:
            status = {"good": "[OK]", "medium": "[WARN]", "high": "[STOP]"}.get(impact['level'], "[--]")
            result.append(f"  {status} {impact['message']}")
        
        return "\n".join(result)
    
    # === Suggestion Handlers ===
    def _suggest_weather(self):
        """Suggest based on weather"""
        w = self.road.get_weather()
        can, msg = self.road.can_construct_today()
        
        if can:
            return ("[Suggestion] Weather is good for construction. Recommended:\n"
                    "  - Asphalt paving\n"
                    "  - Water-stable layer\n"
                    "  - Equipment maintenance")
        else:
            return ("[Suggestion] Weather is NOT suitable. Recommended:\n"
                    "  - Indoor work\n"
                    "  - Equipment maintenance\n"
                    "  - Material storage")
    
    # === Prediction Handlers ===
    def _predict_time(self):
        """Predict completion time"""
        prog = self.road.get_progress()
        
        if prog == 0:
            return "[Prediction] Not started yet"
        
        remaining = 100 - prog
        rate = prog / 10
        
        if rate > 0:
            days_left = remaining / rate
            return f"[Prediction] Estimated {days_left:.0f} more days (based on {prog:.0f}% progress)"
        else:
            return "[Prediction] Not enough data"
    
    # === General Query ===
    def _general_query(self, question):
        """General knowledge base query"""
        results = self.road.query(question)
        
        if results:
            return "[Knowledge]\n" + "\n".join(f"  - {r}" for r in results[:5])
        
        return ("[Help] You can ask me:\n"
                "  - How's the progress?\n"
                "  - What's the cost?\n"
                "  - What's the weather?\n"
                "  - Equipment status?\n"
                "  - Quality records?\n"
                "  - What if it rains?\n"
                "  - When will we finish?")
    
    # === Main Understand ===
    def understand(self, question):
        """Main understanding pipeline"""
        
        # 1. Intent recognition
        intent = self.recognize_intent(question)
        
        # 2. Entity extraction
        entities = self.extract_entities(question)
        
        # 3. Reasoning
        answer = self.reason(intent, entities, question)
        
        # 4. Save to history
        self.conversation_history.append({
            'question': question,
            'intent': intent,
            'entities': entities,
            'answer': answer
        })
        
        return answer


# Demo
if __name__ == "__main__":
    import sys
    sys.path.insert(0, '.')
    from main import Road3D
    
    road = Road3D()
    
    # Setup demo data
    for i in range(8):
        road.add_point(i, i * 100, i * 30)
    
    road.add_knowledge("asphalt_temp", "150-170C")
    road.add_knowledge("compaction", "95-98%")
    road.add_knowledge("layer_thickness", "50-80mm")
    
    road.add_progress(0, 1, "completed", 100)
    road.add_progress(1, 2, "completed", 100)
    road.add_progress(2, 3, "in_progress", 70)
    road.add_progress(3, 4, "in_progress", 40)
    
    road.add_material_cost('沥青', 500)
    road.add_material_cost('水泥', 200)
    road.add_labor_cost('技工', 30)
    road.add_equipment_cost('压路机', 15)
    
    # Add devices for testing
    road.add_device('压路机1', 'CAT', '压路机')
    road.add_device('摊铺机1', 'VOGELE', '摊铺机')
    road.add_device('挖掘机1', 'CAT', '挖掘机')
    road.update_device_status(1, 'RUNNING')
    road.update_device_status(2, 'IDLE')
    
    # Test Q&A
    qa = AIQAV2(road)
    
    print("\n" + "="*50)
    print("Testing AI Q&A V2")
    print("="*50)
    
    test_questions = [
        "进度怎么样？",
        "成本多少？",
        "今天天气如何？",
        "天气有影响吗？",
        "如果下雨怎么办？",
        "什么时候完工？",
        "设备状态？",
        "质量记录？"
    ]
    
    for q in test_questions:
        print(f"\n>>> {q}")
        print(qa.understand(q))
