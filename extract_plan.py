# -*- coding: utf-8 -*-
"""
六维时空企划书知识提取器
"""

import re
import json

def extract_knowledge(content):
    """从六维时空企划书提取知识"""
    
    knowledge = {
        "dimensions": [],  # 六维
        "modules": [],      # 模块
        "capabilities": [], # 能力
        "targets": [],      # 目标
        "technologies": [], # 技术
        "scenarios": []    # 场景
    }
    
    # 提取六维
    dimensions = re.findall(r'第[一二三四五六]维[：:]\s*([^\\n]+)', content)
    knowledge["dimensions"] = [d.strip() for d in dimensions]
    
    # 提取模块
    modules = re.findall(r'[感知认知决策执行应用]层|知识库|调度引擎|积分系统|本地数据库', content)
    knowledge["modules"] = list(set(modules))
    
    # 提取能力 (AI能...)
    capabilities = re.findall(r'AI[能可][^。，]+', content)
    knowledge["capabilities"] = [c.strip()[:50] for c in capabilities[:10]]
    
    # 提取目标 (百分之X...%)
    targets = re.findall(r'百分之(\d+)[以]+', content)
    knowledge["targets"] = [f"{t}%" for t in targets]
    
    # 提取技术
    techs = re.findall(r'知识图谱|强化学习|优化算法|CAD|BIM|OCR|CPUT|RT|三维建模|GIS|计算机视觉|深度学习', content)
    knowledge["technologies"] = list(set(techs))
    
    # 提取场景
    scenarios = re.findall(r'场景[一二三四]?[：:]\s*([^\\n]+)', content)
    knowledge["scenarios"] = [s.strip()[:30] for s in scenarios[:5]]
    
    return knowledge


if __name__ == "__main__":
    # 读取文档
    with open('F:/drawing_3d/data/六维时空企划书.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取
    result = extract_knowledge(content)
    
    print("=== 六维时空企划书知识 ===")
    print(f"\n维度: {result['dimensions']}")
    print(f"\n模块: {result['modules']}")
    print(f"\n能力: {result['capabilities']}")
    print(f"\n目标: {result['targets']}")
    print(f"\n技术: {result['technologies']}")
    print(f"\n场景: {result['scenarios']}")
