# -*- coding: utf-8 -*-
"""
智能合约模拟 - Smart Contract Simulator
区块链进度触发支付原型
"""

from datetime import datetime
import json
import os


class SmartContractSimulator:
    """智能合约模拟：进度确认 → 自动支付触发"""
    
    def __init__(self, payment_log="data/payment_log.jsonl"):
        self.contract_state = "pending"
        self.payment_log = payment_log
        self.milestones = {
            "milestone1": {"progress": 0, "amount": 100000, "paid": False, "name": "基础施工完成"},
            "milestone2": {"progress": 0, "amount": 200000, "paid": False, "name": "主体结构完成"},
            "milestone3": {"progress": 0, "amount": 300000, "paid": False, "name": "竣工验收"},
        }
        
        # 确保目录存在
        os.makedirs(os.path.dirname(payment_log) if os.path.dirname(payment_log) else "data", exist_ok=True)
    
    def update_progress(self, milestone_id, current_progress):
        """更新里程碑进度
        
        Args:
            milestone_id: 里程碑ID
            current_progress: 当前进度 (0-100)
        
        Returns:
            dict: 更新结果
        """
        if milestone_id not in self.milestones:
            return {"status": "error", "msg": "Invalid milestone"}
        
        self.milestones[milestone_id]["progress"] = current_progress
        
        # 检查是否触发支付
        if current_progress >= 100 and not self.milestones[milestone_id]["paid"]:
            self.trigger_payment(milestone_id)
        
        return {
            "status": "updated",
            "milestone": milestone_id,
            "progress": current_progress,
            "paid": self.milestones[milestone_id]["paid"]
        }
    
    def trigger_payment(self, milestone_id):
        """模拟支付触发（区块链事件）
        
        Args:
            milestone_id: 里程碑ID
        """
        amount = self.milestones[milestone_id]["amount"]
        self.milestones[milestone_id]["paid"] = True
        self.contract_state = "payment_executed"
        
        # 生成模拟交易哈希
        tx_hash = f"0x{hash(datetime.now().isoformat()) % 100000000:08x}"
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "milestone": milestone_id,
            "milestone_name": self.milestones[milestone_id]["name"],
            "amount": amount,
            "status": "paid",
            "tx_hash": tx_hash
        }
        
        with open(self.payment_log, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        
        print(f"[PAYMENT] Smart contract triggered payment:")
        print(f"  Milestone: {milestone_id} ({self.milestones[milestone_id]['name']})")
        print(f"  Amount: {amount} CNY")
        print(f"  TX: {tx_hash}")
        
        return log_entry
    
    def get_contract_state(self):
        """获取合约状态
        
        Returns:
            dict: 合约状态
        """
        return {
            "state": self.contract_state,
            "milestones": self.milestones,
            "total_paid": sum(m["amount"] for m in self.milestones.values() if m["paid"]),
            "last_payment": self._get_last_payment()
        }
    
    def _get_last_payment(self):
        """获取最近支付记录"""
        if not os.path.exists(self.payment_log):
            return None
        
        with open(self.payment_log, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        if lines:
            return json.loads(lines[-1].strip())
        return None
    
    def get_payment_history(self, limit=10):
        """获取支付历史"""
        if not os.path.exists(self.payment_log):
            return []
        
        with open(self.payment_log, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        history = []
        for line in lines[-limit:]:
            if line.strip():
                history.append(json.loads(line.strip()))
        
        return history


# 全局实例
_contract = None

def get_smart_contract():
    """获取全局智能合约实例"""
    global _contract
    if _contract is None:
        _contract = SmartContractSimulator()
    return _contract


# 测试
if __name__ == "__main__":
    print("="*50)
    print("Smart Contract Simulator Test")
    print("="*50)
    
    contract = SmartContractSimulator()
    
    # 测试进度更新
    print("\n[1] Update milestone progress...")
    result = contract.update_progress("milestone1", 50)
    print(f"    Result: {result}")
    
    result = contract.update_progress("milestone1", 100)
    print(f"    Result: {result}")
    
    # 合约状态
    print("\n[2] Contract state:")
    state = contract.get_contract_state()
    print(f"    State: {state['state']}")
    print(f"    Total paid: {state['total_paid']} CNY")
    
    # 支付历史
    print("\n[3] Payment history:")
    history = contract.get_payment_history()
    for h in history:
        print(f"    {h['milestone']}: {h['amount']} CNY - {h['tx_hash']}")
    
    # 第二个里程碑
    print("\n[4] Second milestone:")
    contract.update_progress("milestone2", 100)
    state = contract.get_contract_state()
    print(f"    Total paid: {state['total_paid']} CNY")
    
    print("\n[SUCCESS] Smart Contract Simulator working!")
