# -*- coding: utf-8 -*-
"""
Blueprint Q&A - 集成MiniMax API增强版
基于知识图谱的自然语言问答 + LLM增强
"""

import re
from datetime import datetime

# MiniMax API
try:
    from src.utils.llm_client import MiniMaxClient
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False
    print("警告: MiniMax客户端未集成，将使用模板匹配模式")


class BlueprintQAv2:
    """图纸智能问答系统 v2 - LLM增强版"""
    
    def __init__(self, knowledge_graph=None):
        """初始化
        
        Args:
            knowledge_graph: BlueprintKnowledgeGraph实例
        """
        self.kg = knowledge_graph
        self.llm = MiniMaxClient() if LLM_AVAILABLE else None
        
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
        
        # 结构层信息
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
                'material': 'AC-20C沥青混凝土',
                'temperature': '摊铺温度≥150℃',
                'standard': 'JTG F40-2004'
            },
            '下面层': {
                'name': '下面层',
                'thickness': '8cm (80mm)',
                'material': 'AC-25C沥青混凝土',
                'standard': 'JTG F40-2004'
            },
            '基层 {
                'name':': '水泥稳定碎石基层',
                'thickness': '36cm',
                'material': '水泥剂量4-6%',
                'standard': 'JTG/T F20-2015'
            },
            '底基层': {
                'name': '水泥稳定碎石底基层',
                'thickness': '18cm',
                'material': '水泥剂量3-5%',
                'standard': 'JTG/T F20-2015'
            }
        }
    
    def ask(self, question: str) -> str:
        """问答入口
        
        Args:
            question: 用户问题
            
        Returns:
            回答内容
        """
        question = question.strip()
        
        # 判断问题类型
        qtype = self._classify_question(question)
        
        # 先尝试知识图谱/模板回答
        template_answer = self._template_answer(question, qtype)
        
        # 如果LLM可用，用LLM增强回答
        if self.llm and LLM_AVAILABLE:
            return self._llm_enhance(question, template_answer)
        else:
            return template_answer
    
    def _classify_question(self, question: str) -> str:
        """分类问题类型"""
        for qtype, patterns in self.templates.items():
            for p in patterns:
                if re.search(p, question, re.IGNORECASE):
                    return qtype
        return 'general'
    
    def _template_answer(self, question: str, qtype: str) -> str:
        """模板匹配回答"""
        if qtype == 'structure':
            return self._answer_structure(question)
        elif qtype == 'material':
            return self._answer_material(question)
        elif qtype == 'stake':
            return self._answer_stake(question)
        elif qtype == 'standard':
            return self._answer_standard(question)
        else:
            return self._answer_general(question)
    
    def _answer_structure(self, question: str) -> str:
        """回答路面结构问题"""
        # 提取桩号
        stake_match = re.search(r'K(\d+)\+(\d+)', question, re.IGNORECASE)
        
        if stake_match:
            km = stake_match.group(1)
            m = stake_match.group(2)
            return f"K{km}+{m}路段路面结构为：\n" + self._format_layers()
        
        return "路面结构层从上到下依次为：\n" + self._format_layers()
    
    def _format_layers(self) -> str:
        """格式化结构层信息"""
        lines = []
        for layer, info in self.layer_templates.items():
            lines.append(f"- **{layer}**: {info['thickness']} ({info['material']})")
        return '\n'.join(lines)
    
    def _answer_material(self, question: str) -> str:
        """回答材料问题"""
        for layer, info in self.layer_templates.items():
            if layer in question or '上面层' in question:
                return f"推荐材料: {info['material']}\n遵循规范: {info['standard']}"
        
        return "请明确具体结构层名称"
    
    def _answer_stake(self, question: str) -> str:
        """回答桩号区段问题"""
        stakes = re.findall(r'K(\d+)\+(\d+)', question, re.IGNORECASE)
        
        if len(stakes) >= 2:
            s1 = int(stakes[0][0]) * 1000 + int(stakes[0][1])
            s2 = int(stakes[1][0]) * 1000 + int(stakes[1][1])
            length = abs(s2 - s1)
            return f"路段长度: {length}米"
        
        return "请提供完整桩号区段"
    
    def _answer_standard(self, question: str) -> str:
        """回答规范问题"""
        standards = [
            "JTG F40-2004《公路沥青路面施工技术规范》",
            "JTG/T F20-2015《公路路面基层施工技术细则》",
            "JTG D50-2017《公路沥青路面设计规范》"
        ]
        return "相关规范：\n" + '\n'.join([f"- {s}" for s in standards])
    
    def _answer_general(self, question: str) -> str:
        """通用回答"""
        return "我是道路工程图纸问答助手，可以回答关于路面结构、材料、规范等问题。请具体说明您想查询的内容。"
    
    def _llm_enhance(self, question: str, template_answer: str) -> str:
        """LLM增强回答"""
        if not self.llm:
            return template_answer
        
        try:
            # 构建增强提示
            prompt = f"""
问题: {question}

模板回答:
{template_answer}

知识图谱信息:
{self._get_kg_context(question)}

请作为道路工程专家，基于以上信息给出更准确、更详细的回答。
"""
            
            enhanced = self.llm.generate(
                prompt,
                system_prompt="你是道路工程专家，精通公路设计、施工、规范。给出专业、准确、简洁的回答。",
                temperature=0.7
            )
            
            return enhanced
            
        except Exception as e:
            return f"{template_answer}\n\n💡 补充: {str(e)[:100]}"
    
    def _get_kg_context(self, question: str) -> str:
        """获取知识图谱相关上下文"""
        if not self.kg:
            return "无知识图谱数据"
        
        # 简单关键词匹配
        context = []
        
        # 桩号
        stakes = re.findall(r'K(\d+)\+(\d+)', question, re.IGNORECASE)
        for s in stakes:
            chainage = int(s[0]) * 1000 + int(s[1])
            context.append(f"桩号K{s[0]}+{s[1]}相关数据")
        
        # 关键词
        keywords = ['路面', '基层', '结构', '材料', '桥', '涵']
        for kw in keywords:
            if kw in question:
                context.append(f"包含'{kw}'的工程数据")
        
        return '\n'.join(context) if context else "根据问题分析"

    def query_with_llm(self, question: str) -> str:
        """纯LLM问答（不依赖模板）"""
        if not self.llm:
            return "LLM未集成，请先配置MiniMax API"
        
        try:
            response = self.llm.generate(
                question,
                system_prompt="""你是道路工程图纸专家，精通:
- 公路路面结构（上面层、中面层、下面层、基层、底基层）
- 工程材料（沥青混凝土、水稳碎石）
- 设计规范（JTG F40、JTG D50等）
- 图纸识读（桩号、结构物、坐标）

请用中文回答专业问题。如果不确定，请明确说明。""",
                temperature=0.7
            )
            return response
        except Exception as e:
            return f"LLM调用失败: {str(e)}"


# 测试
if __name__ == '__main__':
    qa = BlueprintQAv2()
    
    # 测试问题
    test_questions = [
        "K5+200的路面结构是什么？",
        "上面层用什么材料？",
        "K0+000到K1+000有多长？",
        "沥青路面施工依据什么规范？",
    ]
    
    print("=== Blueprint Q&A v2 测试 ===\n")
    for q in test_questions:
        print(f"问题: {q}")
        print(f"回答: {qa.ask(q)}")
        print()
