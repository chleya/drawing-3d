# -*- coding: utf-8 -*-
"""
图纸智能问答系统 - Blueprint Q&A
基于知识图谱的自然语言问答
"""

import re
from datetime import datetime


class BlueprintQA:
    """图纸智能问答系统"""
    
    def __init__(self, knowledge_graph):
        """初始化
        
        Args:
            knowledge_graph: BlueprintKnowledgeGraph实例
        """
        self.kg = knowledge_graph
        
        # 问答模板
        self.templates = {
            'structure': [
                r'(?:.*?)(?:路面)?结构(?:层)?(?:是|是什么|有哪些)',
                r'(?:K?\d+\+\d+).*?(?:路面|结构)',
            ],
            'material': [
                r'(?:需要|用|使用).*?材料',
                r'(?:材料|规格|要求)',
            ],
            'stake': [
                r'K\d+\+\d+.*?K\d+\+\d+',
                r'.*?至.*?路段',
            ],
            'standard': [
                r'(?:规范|标准|依据)',
                r'必须.*?遵循',
            ]
        }
        
        # 结构层信息缓存
        self.layer_templates = {
            '上面层': {
                'name': '上面层',
                'thickness': '4cm (40mm)',
                'material': 'AC-13C改性沥青混凝土',
                'temperature': '摊铺温度≥160℃，初压温度≥150℃',
                'standard': 'JTG F40-2004'
            },
            '中面层': {
                'name': '中面层', 
                'thickness': '6cm (60mm)',
                'material': 'AC-20中粒式沥青混凝土',
                'temperature': '摊铺温度≥150℃',
                'standard': 'JTG F40-2004'
            },
            '下面层': {
                'thickness': '8cm (80mm)',
                'material': 'AC-25粗粒式沥青混凝土',
                'name': '下面层',
                'temperature': '摊铺温度≥140℃',
                'standard': 'JTG F40-2004'
            },
            '上基层': {
                'name': '上基层',
                'thickness': '36cm',
                'material': '水泥稳定碎石',
                'standard': 'JTG/T F50-2011'
            },
            '下基层': {
                'name': '下基层',
                'thickness': '18cm',
                'material': '水泥稳定碎石',
                'standard': 'JTG/T F50-2011'
            },
            '底基层': {
                'name': '底基层',
                'thickness': '15cm',
                'material': '级配碎石',
                'standard': 'JTG/T F50-2011'
            }
        }
    
    def ask(self, question):
        """问答接口
        
        Args:
            question: 用户问题
        
        Returns:
            dict: 回答结果
        """
        question = question.strip()
        
        # 解析问题类型
        qtype = self._classify_question(question)
        
        # 提取关键信息
        stake = self._extract_stake(question)
        
        # 生成回答
        if qtype == 'structure':
            answer = self._answer_structure(question, stake)
        elif qtype == 'material':
            answer = self._answer_material(question, stake)
        elif qtype == 'stake_range':
            answer = self._answer_stake_range(question)
        elif qtype == 'standard':
            answer = self._answer_standard(question, stake)
        else:
            answer = self._answer_general(question)
        
        return {
            'question': question,
            'answer': answer,
            'type': qtype,
            'stake': stake,
            'timestamp': datetime.now().isoformat()
        }
    
    def _classify_question(self, question):
        """问题分类"""
        q = question.lower()
        
        if any(re.search(p, q) for p in self.templates['structure']):
            return 'structure'
        elif any(re.search(p, q) for p in self.templates['material']):
            return 'material'
        elif any(re.search(p, q) for p in self.templates['stake']):
            return 'stake_range'
        elif any(re.search(p, q) for p in self.templates['standard']):
            return 'standard'
        else:
            return 'general'
    
    def _extract_stake(self, question):
        """提取里程桩号"""
        # 匹配 K5+800 格式
        pattern = r'K(\d+)\+(\d+)'
        matches = re.findall(pattern, question)
        
        if matches:
            return [f"K{m[0]}+{m[1]}" for m in matches]
        return None
    
    def _extract_stake_range(self, question):
        """提取里程范围"""
        pattern = r'K(\d+)\+(\d+).*?K(\d+)\+(\d+)'
        match = re.search(pattern, question)
        
        if match:
            start = f"K{match.group(1)}+{match.group(2)}"
            end = f"K{match.group(3)}+{match.group(4)}"
            return start, end
        return None
    
    def _answer_structure(self, question, stake):
        """回答路面结构问题"""
        if not stake:
            stake = ['K5+800']  # 默认
        
        answers = []
        for s in stake:
            # 查知识图谱
            layers = self.kg.query_structure_layers(s)
            
            if layers:
                answer = f"根据设计图纸，{s}路段的路面结构为：\n\n"
                for i, layer in enumerate(layers):
                    props = layer.get('properties', {})
                    answer += f"**{layer.get('name', '结构层')}**：{props.get('thickness', '?')}mm {props.get('material', '')}\n"
                answers.append(answer)
            else:
                # 使用模板回答
                answer = f"根据设计图纸，{s}路段的路面结构为：\n\n"
                for name, info in self.layer_templates.items():
                    answer += f"**{name}**：{info['thickness']} {info['material']}\n"
                answers.append(answer)
        
        return '\n\n'.join(answers)
    
    def _answer_material(self, question, stake):
        """回答材料问题"""
        if not stake:
            stake = ['K5+800']
        
        answers = []
        for s in stake:
            # 查知识图谱
            elements = self.kg.query_by_location(s)
            
            answer = f"{s}路段的材料要求：\n\n"
            
            # 沥青材料
            answer += "**沥青材料**：\n"
            answer += "- 采用SBS改性沥青，针入度60-80\n"
            answer += "- 依据：JTG F40-2004\n\n"
            
            # 粗集料
            answer += "**粗集料**：\n"
            answer += "- 采用玄武岩，压碎值≤26%\n"
            answer += "- 粒径规格：9.5-19mm\n\n"
            
            # 细集料
            answer += "**细集料**：\n"
            answer += "- 采用机制砂，含泥量≤3%\n"
            answer += "- 粒径规格：0-4.75mm\n\n"
            
            answers.append(answer)
        
        return '\n\n'.join(answers)
    
    def _answer_stake_range(self, question):
        """回答里程范围问题"""
        stake_range = self._extract_stake_range(question)
        
        if not stake_range:
            return "请指定具体的里程范围，如 K5+800至K6+200"
        
        start, end = stake_range
        
        # 查知识图谱
        elements = self.kg.query_by_stake_range(start, end)
        
        if elements:
            answer = f"根据设计图纸，{start}至{end}路段：\n\n"
            for e in elements[:5]:  # 限制显示数量
                answer += f"- {e.get('name')} ({e.get('type')})\n"
        else:
            answer = f"{start}至{end}路段的信息：\n\n"
            answer += "该路段路面结构为标准结构：\n"
            for name, info in self.layer_templates.items():
                answer += f"- {name}：{info['thickness']} {info['material']}\n"
        
        return answer
    
    def _answer_standard(self, question, stake):
        """回答规范问题"""
        return ("**相关规范**：\n\n"
                "1. **JTG F40-2004**《公路沥青路面施工技术规范》\n"
                "2. **JTG/T F50-2011**《公路路面基层施工技术细则》\n"
                "3. **JTG E42-2005**《公路工程集料试验规程》\n\n"
                "更多规范请查询知识库。")
    
    def _answer_general(self, question):
        """通用回答"""
        q = question.lower()
        
        if '厚度' in question:
            return self._answer_structure(question, None)
        elif '材料' in question or '规格' in question:
            return self._answer_material(question, None)
        elif any(k in q for k in ['施工', '工艺', '方法']):
            return self._answer_construction(question)
        else:
            return ("抱歉，我不太理解您的问题。\n\n"
                    "您可以尝试问：\n"
                    "- K5+800至K6+200路段的路面结构是什么？\n"
                    "- 需要用什么材料？\n"
                    "- 施工温度要求？\n"
                    "- 有什么规范要求？")
    
    def _answer_construction(self, question):
        """施工工艺回答"""
        return ("**沥青路面施工要点**：\n\n"
                "**1. 温度控制**\n"
                "- 摊铺温度：≥160℃\n"
                "- 初压温度：≥150℃\n"
                "- 复压温度：≥130℃\n"
                "- 终压温度：≥90℃\n\n"
                "**2. 碾压遍数**\n"
                "- 初压：钢轮压路机1-2遍\n"
                "- 复压：钢轮压路机3-4遍 + 轮胎压路机2-3遍\n"
                "- 终压：钢轮压路机1-2遍\n\n"
                "**3. 压实度要求**\n"
                "- 上面层：≥96%\n"
                "- 中下面层：≥95%\n\n"
                "**依据**：JTG F40-2004")


# ========== 测试 ==========

if __name__ == "__main__":
    from blueprint_knowledge_graph import create_sample_knowledge_graph
    
    print("="*50)
    print("Blueprint Q&A Test")
    print("="*50)
    
    # 创建知识图谱
    kg = create_sample_knowledge_graph()
    
    # 创建问答系统
    qa = BlueprintQA(kg)
    
    # 测试问题
    test_questions = [
        "K5+800至K6+200路段的路面结构是什么？",
        "K5+800路面需要用什么材料？",
        "沥青路面施工有什么规范要求？",
        "路面结构层厚度是多少？",
    ]
    
    for q in test_questions:
        print(f"\n[Q] {q}")
        result = qa.ask(q)
        print(f"[A] {result['answer'][:200]}...")
        print("-" * 40)
    
    print("\n" + "="*50)
    print("Q&A Test Complete")
    print("="*50)
