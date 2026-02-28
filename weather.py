"""天气集成模块
功能：
1. 天气数据获取
2. 施工天气影响分析
3. 施工建议生成
4. 天气预报查询
"""

import random
from datetime import datetime, timedelta

class WeatherSystem:
    """施工天气管理系统"""
    
    def __init__(self):
        self.weather_data = {}
        self.constraints = {
            'rain': {'max': 0, 'name': '降雨'},
            'temp_min': {'min': 5, 'name': '最低温度'},
            'temp_max': {'max': 35, 'name': '最高温度'},
            'wind': {'max': 6, 'name': '风速'},
            'humidity': {'max': 85, 'name': '湿度'}
        }
    
    def get_weather(self, date=None):
        """获取天气数据（模拟）"""
        if date is None:
            date = datetime.now()
        
        # 模拟天气数据
        weather_types = ['sunny', 'cloudy', 'rainy', 'stormy']
        weather = random.choice(weather_types)
        
        temps = {
            'sunny': (20, 32),
            'cloudy': (15, 25),
            'rainy': (12, 20),
            'stormy': (10, 18)
        }
        
        temp_range = temps.get(weather, (15, 25))
        temp = random.randint(temp_range[0], temp_range[1])
        
        data = {
            'date': date.strftime('%Y-%m-%d'),
            'weather': weather,
            'temperature': temp,
            'humidity': random.randint(40, 90),
            'wind_speed': random.randint(0, 8),
            'precipitation': random.randint(0, 50) if weather in ['rainy', 'stormy'] else 0
        }
        
        return data
    
    def analyze_impact(self, weather):
        """分析天气对施工的影响"""
        issues = []
        
        # 降雨影响
        if weather['precipitation'] > 10:
            issues.append({
                'level': 'high',
                'type': 'rain',
                'message': '大雨不宜沥青摊铺'
            })
        elif weather['precipitation'] > 0:
            issues.append({
                'level': 'medium',
                'type': 'rain',
                'message': '小雨可施工，需注意排水'
            })
        
        # 温度影响
        if weather['temperature'] > 35:
            issues.append({
                'level': 'high',
                'type': 'temperature',
                'message': '高温预警，需注意防暑'
            })
        elif weather['temperature'] < 5:
            issues.append({
                'level': 'high',
                'type': 'temperature',
                'message': '低温不宜施工'
            })
        
        # 风速影响
        if weather['wind_speed'] > 6:
            issues.append({
                'level': 'medium',
                'type': 'wind',
                'message': '大风天气，摊铺需谨慎'
            })
        
        return issues if issues else [{'level': 'good', 'type': 'normal', 'message': '天气良好，适合施工'}]
    
    def get_suggestion(self, weather):
        """生成施工建议"""
        issues = self.analyze_impact(weather)
        suggestions = []
        
        for issue in issues:
            if issue['level'] == 'high':
                suggestions.append(f"⚠️ {issue['message']}")
            elif issue['level'] == 'medium':
                suggestions.append(f"🔔 {issue['message']}")
            else:
                suggestions.append(f"✅ {issue['message']}")
        
        # 天气良好时的建议
        if 15 <= weather['temperature'] <= 28:
            suggestions.append("📋 适合沥青摊铺作业")
        
        if weather['humidity'] < 60:
            suggestions.append("💨 湿度适中，适合施工")
        
        return suggestions
    
    def forecast(self, days=7):
        """天气预报"""
        forecast_data = []
        for i in range(days):
            date = datetime.now() + timedelta(days=i)
            weather = self.get_weather(date)
            impact = self.analyze_impact(weather)
            forecast_data.append({
                'date': weather['date'],
                'weather': weather['weather'],
                'temperature': weather['temperature'],
                'impact': impact[0]['message']
            })
        return forecast_data
    
    def can_construct(self, weather):
        """判断是否可以施工"""
        issues = self.analyze_impact(weather)
        for issue in issues:
            if issue['level'] == 'high':
                return False, issue['message']
        return True, "天气条件允许施工"


# 测试
if __name__ == "__main__":
    ws = WeatherSystem()
    
    print("="*50)
    print("天气集成模块测试")
    print("="*50)
    
    # 获取当前天气
    w = ws.get_weather()
    print(f"\n当前天气: {w['weather']}")
    print(f"温度: {w['temperature']}°C")
    print(f"湿度: {w['humidity']}%")
    print(f"风速: {w['wind_speed']}级")
    
    # 分析影响
    print("\n天气影响分析:")
    for issue in ws.analyze_impact(w):
        print(f"  {issue['level']}: {issue['message']}")
    
    # 施工建议
    print("\n施工建议:")
    for s in ws.get_suggestion(w):
        print(f"  {s}")
    
    # 天气预报
    print("\n7天天气预报:")
    for f in ws.forecast(3):
        print(f"  {f['date']}: {f['weather']} {f['temperature']}°C - {f['impact']}")
    
    # 是否可以施工
    can, msg = ws.can_construct(w)
    print(f"\n施工状态: {'可以' if can else '不可以'} - {msg}")
