# -*- coding: utf-8 -*-
"""
LLM问答集成 - LLM Q&A Integration
支持 OpenAI / MiniMax / 本地模型
"""

import os
import json
from datetime import datetime


class LLMQASystem:
    """LLM智能问答系统"""
    
    def __init__(self, provider='minimax', api_key=None):
        """初始化
        
        Args:
            provider: 'openai' / 'minimax' / 'local'
            api_key: API密钥
        """
        self.provider = provider
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY') or os.environ.get('MINIMAX_API_KEY')
        
        # 知识库
        self.knowledge_base = self._init_knowledge_base()
        
        print(f"[OK] LLM QA System initialized: {provider}")
    
    def _init_knowledge_base(self):
        """初始化知识库"""
        return {
            "路面结构": {
                "上面层": "AC-13C改性沥青混凝土，厚度4cm",
                "中面层": "AC-20中粒式沥青混凝土，厚度6cm", 
                "下面层": "AC-25粗粒式沥青混凝土，厚度8cm",
                "上基层": "水泥稳定碎石，厚度36cm",
                "下基层": "水泥稳定碎石，厚度18cm",
                "底基层": "级配碎石，厚度15cm"
            },
            "材料要求": {
                "沥青": "SBS改性沥青，针入度60-80",
                "粗集料": "玄武岩，压碎值≤26%",
                "细集料": "机制砂，含泥量≤3%",
                "水泥": "普通硅酸盐水泥，强度等级42.5"
            },
            "施工温度": {
                "摊铺温度": "≥160℃",
                "初压温度": "≥150℃",
                "复压温度": "≥130℃",
                "终压温度": "≥90℃"
            },
            "压实度要求": {
                "上面层": "≥96%",
                "中下面层": "≥95%",
                "基层": "≥97%"
            },
            "规范标准": {
                "JTG F40-2004": "公路沥青路面施工技术规范",
                "JTG/T F50-2011": "公路路面基层施工技术细则",
                "JTG E42-2005": "公路工程集料试验规程"
            }
        }
    
    def ask(self, question, use_rag=True):
        """问答接口
        
        Args:
            question: 用户问题
            use_rag: 是否使用RAG增强
        
        Returns:
            dict: 回答结果
        """
        # 1. RAG - 检索相关知识
        context = ""
        if use_rag:
            context = self._retrieve_context(question)
        
        # 2. 构建prompt
        prompt = self._build_prompt(question, context)
        
        # 3. 调用LLM
        if self.provider == 'local':
            answer = self._local_generate(prompt)
        else:
            answer = self._api_generate(prompt)
        
        return {
            'question': question,
            'answer': answer,
            'context': context if use_rag else None,
            'provider': self.provider,
            'timestamp': datetime.now().isoformat()
        }
    
    def _retrieve_context(self, question):
        """检索相关上下文"""
        question_lower = question.lower()
        context_parts = []
        
        # 遍历知识库找相关内容
        for category, items in self.knowledge_base.items():
            if any(k in question_lower for k in category.lower()):
                context_parts.append(f"【{category}】")
                for key, value in items.items():
                    if any(k in question_lower for k in key.lower()):
                        context_parts.append(f"- {key}: {value}")
        
        if not context_parts:
            # 返回全部知识作为上下文
            context_parts.append("【路面结构】")
            for k, v in self.knowledge_base['路面结构'].items():
                context_parts.append(f"- {k}: {v}")
        
        return '\n'.join(context_parts[:10])  # 限制长度
    
    def _build_prompt(self, question, context):
        """构建Prompt"""
        system_prompt = """你是一个专业的道路工程AI助手，专门回答关于路面施工、结构、材料等方面的问题。

要求：
1. 根据提供的知识回答问题
2. 如果知识库中没有相关信息，如实说明
3. 回答要准确、简洁
4. 可以适当补充相关规范要求

"""
        
        if context:
            system_prompt += f"\n参考知识：\n{context}\n"
        
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    
    def _api_generate(self, messages):
        """API调用"""
        if self.provider == 'minimax':
            return self._minimax_generate(messages)
        elif self.provider == 'openai':
            return self._openai_generate(messages)
        else:
            return "请配置有效的API Key"
    
    def _minimax_generate(self, messages):
        """MiniMax API调用"""
        try:
            import requests
            
            # 提取用户问题
            user_msg = messages[-1]['content']
            
            # 构建prompt
            prompt = f"""你是一个专业的道路工程AI助手。请回答以下问题：

问题：{user_msg}

请根据道路施工规范回答，要求准确、简洁。"""
            
            # API调用
            url = "https://api.minimax.chat/v1/text/chatcompletion_v2"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "abab6.5s-chat",
                "messages": [{"role": "user", "content": prompt}]
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"API调用失败: {response.status_code}"
                
        except Exception as e:
            return f"LLM调用出错: {str(e)}"
    
    def _openai_generate(self, messages):
        """OpenAI API调用"""
        try:
            import openai
            openai.api_key = self.api_key
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"OpenAI调用出错: {str(e)}"
    
    def _local_generate(self, prompt):
        """本地模型调用"""
        # TODO: 支持本地模型如 ChatGLM
        return "本地模型暂未实现，请配置API Key"
    
    def add_knowledge(self, category, key, value):
        """添加知识"""
        if category not in self.knowledge_base:
            self.knowledge_base[category] = {}
        self.knowledge_base[category][key] = value
        print(f"[OK] Added: {category}.{key}")


# ========== 封装版本 - 结合知识图谱 ==========

class SemanticQA:
    """语义问答系统 - 结合知识图谱 + LLM"""
    
    def __init__(self, knowledge_graph=None, llm_provider='minimax'):
        self.kg = knowledge_graph
        self.llm = LLMQASystem(provider=llm_provider)
        
        # 注册知识图谱数据到LLM
        self._sync_from_kg()
    
    def _sync_from_kg(self):
        """从知识图谱同步数据"""
        if not self.kg:
            return
        
        # 同步结构层
        stats = self.kg.get_stats()
        print(f"[OK] Synced {stats['total_nodes']} nodes from knowledge graph")
    
    def ask(self, question):
        """问答"""
        # 优先用知识图谱回答
        stake = self._extract_stake(question)
        
        if stake:
            # 知识图谱查询
            layers = self.kg.query_structure_layers(stake)
            if layers:
                return self._format_kg_answer(question, layers, stake)
        
        # 使用LLM回答
        result = self.llm.ask(question)
        return result['answer']
    
    def _extract_stake(self, question):
        """提取桩号"""
        import re
        pattern = r'K(\d+)\+(\d+)'
        matches = re.findall(pattern, question)
        if matches:
            return f"K{matches[0][0]}+{matches[0][1]}"
        return None
    
    def _format_kg_answer(self, question, layers, stake):
        """格式化知识图谱回答"""
        answer = f"根据设计图纸，{stake}路段的路面结构为：\n\n"
        
        for layer in layers:
            props = layer.get('properties', {})
            answer += f"• **{layer.get('name', '结构层')}**：{props.get('thickness', '?')}mm {props.get('material', '')}\n"
        
        return answer


# ========== 测试 ==========

if __name__ == "__main__":
    print("="*50)
    print("LLM QA System Test")
    print("="*50)
    
    # 创建系统
    llm = LLMQASystem(provider='minimax')
    
    # 测试问题
    test_questions = [
        "K5+800路面结构是什么？",
        "沥青路面施工温度要求是多少？",
        "压实度标准是多少？",
        "SBS改性沥青的要求？",
    ]
    
    for q in test_questions:
        print(f"\n[Q] {q}")
        result = llm.ask(q)
        answer = result.get('answer', str(result)) if isinstance(result, dict) else str(result)
        print(f"[A] {answer[:200]}...")
    
    print("\n" + "="*50)
    print("Test Complete")
    print("="*50)
