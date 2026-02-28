# -*- coding: utf-8 -*-
"""
Drawing 3D - 智能合规助手
Compliance Assistant
"""

from datetime import datetime


class ComplianceRule:
    """合规规则"""
    
    def __init__(self, rule_id, category, title, content, severity='high'):
        self.id = rule_id
        self.category = category  # 施工安全/质量标准/环保要求
        self.title = title
        self.content = content
        self.severity = severity  # high/medium/low
        self.timestamp = datetime.now().isoformat()


class ComplianceSystem:
    """智能合规助手"""
    
    # 内置法规库
    DEFAULT_RULES = [
        # 施工安全
        ComplianceRule('S001', '施工安全', '高空作业安全', '高空作业必须系安全带，配备安全网', 'high'),
        ComplianceRule('S002', '施工安全', '临边防护', '临边洞口必须设置防护栏杆，高度不低于1.2m', 'high'),
        ComplianceRule('S003', '施工安全', '用电安全', '临时用电必须采用TN-S系统，PE线必须可靠连接', 'high'),
        ComplianceRule('S004', '施工安全', '机械安全', '机械设备必须定期检修，操作人员必须持证上岗', 'medium'),
        
        # 质量标准
        ComplianceRule('Q001', '质量标准', '混凝土强度', '混凝土试块留置数量不少于3组/100m³', 'high'),
        ComplianceRule('Q002', '质量标准', '钢筋绑扎', '钢筋间距允许偏差±10mm，保护层厚度偏差±3mm', 'medium'),
        ComplianceRule('Q003', '质量标准', '防水工程', '防水层施工完成后必须进行24小时闭水试验', 'high'),
        
        # 环保要求
        ComplianceRule('E001', '环保要求', '扬尘控制', '施工现场必须采取洒水、覆盖等措施控制扬尘', 'medium'),
        ComplianceRule('E002', '环保要求', '噪声控制', '施工噪声不得超过70dB(A)，夜间禁止高噪声作业', 'high'),
        ComplianceRule('E003', '环保要求', '污水排放', '施工污水必须经过沉淀处理后方可排放', 'medium'),
    ]
    
    def __init__(self):
        self.rules = {r.id: r for r in self.DEFAULT_RULES}
        self.records = []  # 检查记录
    
    def add_rule(self, rule_id, category, title, content, severity='medium'):
        """添加规则"""
        rule = ComplianceRule(rule_id, category, title, content, severity)
        self.rules[rule_id] = rule
        return rule
    
    def get_rules(self, category=None):
        """获取规则列表"""
        if category:
            return [r for r in self.rules.values() if r.category == category]
        return list(self.rules.values())
    
    def search_rules(self, keyword):
        """搜索规则"""
        results = []
        for r in self.rules.values():
            if keyword in r.title or keyword in r.content:
                results.append(r)
        return results
    
    def check_compliance(self, check_item, check_point):
        """合规检查"""
        # 简单的关键词匹配检查
        for r in self.rules.values():
            if r.title in check_item or r.title in check_point:
                return {
                    'rule': r,
                    'compliant': True,
                    'suggestion': f'符合{r.title}要求'
                }
        
        return {
            'rule': None,
            'compliant': None,
            'suggestion': '未找到相关规则，请手动检查'
        }
    
    def add_record(self, rule_id, status, remark=''):
        """添加检查记录"""
        record = {
            'rule_id': rule_id,
            'status': status,  # pass/fail/na
            'remark': remark,
            'timestamp': datetime.now().isoformat()
        }
        self.records.append(record)
        return record
    
    def get_records(self):
        """获取检查记录"""
        return self.records
    
    def get_compliance_rate(self):
        """计算合规率"""
        if not self.records:
            return 0
        
        passed = sum(1 for r in self.records if r['status'] == 'pass')
        total = len(self.records)
        
        return round(passed / total * 100, 1)
    
    def generate_report(self):
        """生成合规报告"""
        return {
            'total_rules': len(self.rules),
            'total_checks': len(self.records),
            'compliance_rate': self.get_compliance_rate(),
            'categories': list(set(r.category for r in self.rules.values())),
            'timestamp': datetime.now().isoformat()
        }


# ==================== 运行测试 ====================

if __name__ == "__main__":
    cs = ComplianceSystem()
    
    # 查看规则
    print("=== 合规规则 ===")
    for r in cs.get_rules('施工安全'):
        print(f"[{r.id}] {r.title} ({r.severity})")
    
    # 合规检查
    print("\n=== 合规检查 ===")
    result = cs.check_compliance('高空作业', '安全带')
    print(f"检查项: 高空作业安全")
    print(f"结果: {result}")
    
    # 添加记录
    cs.add_record('S001', 'pass', '检查通过')
    cs.add_record('S002', 'pass', '检查通过')
    cs.add_record('S003', 'fail', '发现违规')
    
    # 合规率
    print(f"\n合规率: {cs.get_compliance_rate()}%")
    
    # 报告
    print("\n=== 合规报告 ===")
    print(cs.generate_report())
