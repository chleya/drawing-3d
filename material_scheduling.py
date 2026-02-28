# -*- coding: utf-8 -*-
"""
Drawing 3D - 智能材料调度系统
Material Scheduling System
"""

from datetime import datetime, timedelta
import random


class Material:
    """材料"""
    
    def __init__(self, material_id, name, category, unit, unit_price, min_stock=0, max_stock=1000):
        self.id = material_id
        self.name = name
        self.category = category  # 钢材/水泥/砂石/其他
        self.unit = unit  # 吨/立方米/个
        self.unit_price = unit_price
        self.min_stock = min_stock  # 最小库存
        self.max_stock = max_stock  # 最大库存


class Inventory:
    """库存"""
    
    def __init__(self):
        self.materials = {}  # material_id -> Material
        self.stocks = {}  # material_id -> quantity
        self.transactions = []  # 入库/出库记录
        
        # 初始化默认材料
        self._init_default_materials()
    
    def _init_default_materials(self):
        """初始化默认材料"""
        defaults = [
            Material('M001', '水泥', '建材', '吨', 520, 50, 500),
            Material('M002', '钢筋', '钢材', '吨', 4800, 20, 200),
            Material('M003', '碎石', '砂石', '立方米', 85, 100, 1000),
            Material('M004', '沙子', '砂石', '立方米', 65, 50, 500),
            Material('M005', '沥青', '建材', '吨', 4500, 10, 100),
            Material('M006', '柴油', '燃料', '升', 7, 1000, 5000),
        ]
        
        for m in defaults:
            self.materials[m.id] = m
            self.stocks[m.id] = random.randint(m.min_stock, m.max_stock)
    
    def add_material(self, material):
        """添加材料"""
        self.materials[material.id] = material
        self.stocks[material.id] = 0
    
    def stock_in(self, material_id, quantity, operator='system'):
        """入库"""
        if material_id not in self.materials:
            return None
        
        self.stocks[material_id] = self.stocks.get(material_id, 0) + quantity
        
        transaction = {
            'type': 'in',
            'material_id': material_id,
            'quantity': quantity,
            'operator': operator,
            'timestamp': datetime.now().isoformat()
        }
        self.transactions.append(transaction)
        
        return transaction
    
    def stock_out(self, material_id, quantity, operator='system'):
        """出库"""
        if material_id not in self.materials:
            return None
        
        current = self.stocks.get(material_id, 0)
        if current < quantity:
            return {'error': '库存不足', 'available': current}
        
        self.stocks[material_id] = current - quantity
        
        transaction = {
            'type': 'out',
            'material_id': material_id,
            'quantity': quantity,
            'operator': operator,
            'timestamp': datetime.now().isoformat()
        }
        self.transactions.append(transaction)
        
        return transaction
    
    def get_stock(self, material_id=None):
        """获取库存"""
        if material_id:
            m = self.materials.get(material_id)
            if m:
                return {
                    'material': m,
                    'quantity': self.stocks.get(material_id, 0),
                    'status': self._get_stock_status(material_id)
                }
            return None
        
        return {
            m.id: {
                'material': m,
                'quantity': self.stocks.get(m.id, 0),
                'status': self._get_stock_status(m.id)
            }
            for m in self.materials.values()
        }
    
    def _get_stock_status(self, material_id):
        """获取库存状态"""
        m = self.materials[material_id]
        qty = self.stocks.get(material_id, 0)
        
        if qty <= m.min_stock:
            return 'low'  # 库存不足
        elif qty >= m.max_stock:
            return 'high'  # 库存充足
        else:
            return 'normal'  # 正常
    
    def get_transactions(self, material_id=None, limit=10):
        """获取交易记录"""
        if material_id:
            return [t for t in self.transactions if t['material_id'] == material_id][-limit:]
        return self.transactions[-limit:]


class Scheduler:
    """调度器"""
    
    def __init__(self, inventory):
        self.inventory = inventory
        self.orders = []  # 采购订单
        selfallocations = []  # 配送计划
    
    def create_order(self, material_id, quantity, urgency='normal', notes=''):
        """创建采购订单"""
        m = self.inventory.materials.get(material_id)
        if not m:
            return None
        
        order = {
            'id': len(self.orders) + 1,
            'material_id': material_id,
            'material_name': m.name,
            'quantity': quantity,
            'unit_price': m.unit_price,
            'total_price': quantity * m.unit_price,
            'urgency': urgency,  # urgent/normal/low
            'status': 'pending',  # pending/approved/arrived/cancelled
            'notes': notes,
            'create_time': datetime.now().isoformat()
        }
        self.orders.append(order)
        return order
    
    def approve_order(self, order_id):
        """审批订单"""
        for o in self.orders:
            if o['id'] == order_id:
                o['status'] = 'approved'
                o['approve_time'] = datetime.now().isoformat()
                return o
        return None
    
    def arrive_order(self, order_id):
        """订单到达入库"""
        for o in self.orders:
            if o['id'] == order_id and o['status'] == 'approved':
                o['status'] = 'arrived'
                o['arrive_time'] = datetime.now().isoformat()
                
                # 入库
                self.inventory.stock_in(o['material_id'], o['quantity'], f'order_{order_id}')
                return o
        return None
    
    def create_allocation(self, material_id, quantity, location, purpose=''):
        """创建配送计划"""
        # 检查库存
        available = self.inventory.stocks.get(material_id, 0)
        if available < quantity:
            return {'error': '库存不足', 'available': available}
        
        allocation = {
            'id': len(self.allocations) + 1,
            'material_id': material_id,
            'material_name': self.inventory.materials[material_id].name,
            'quantity': quantity,
            'location': location,
            'purpose': purpose,
            'status': 'pending',  # pending/delivering/completed
            'create_time': datetime.now().isoformat()
        }
        self.allocations.append(allocation)
        
        # 预留库存
        self.inventory.stock_out(material_id, quantity, f'allocation_{allocation["id"]}')
        
        return allocation
    
    def complete_allocation(self, allocation_id):
        """完成配送"""
        for a in self.allocations:
            if a['id'] == allocation_id:
                a['status'] = 'completed'
                a['complete_time'] = datetime.now().isoformat()
                return a
        return None
    
    def get_pending_orders(self):
        """获取待处理订单"""
        return [o for o in self.orders if o['status'] == 'pending']
    
    def get_pending_allocations(self):
        """获取待配送计划"""
        return [a for a in self.allocations if a['status'] == 'pending']
    
    def suggest_orders(self):
        """智能推荐采购"""
        suggestions = []
        
        for m in self.inventory.materials.values():
            qty = self.inventory.stocks.get(m.id, 0)
            
            if qty <= m.min_stock:
                # 库存不足，建议采购
                suggested_qty = m.max_stock - qty
                suggestions.append({
                    'material_id': m.id,
                    'material_name': m.name,
                    'current_stock': qty,
                    'suggested_quantity': suggested_qty,
                    'estimated_cost': suggested_qty * m.unit_price,
                    'priority': 'high' if qty < m.min_stock * 0.5 else 'normal'
                })
        
        return suggestions


# ==================== 运行测试 ====================

if __name__ == "__main__":
    inventory = Inventory()
    scheduler = Scheduler(inventory)
    
    # 查看库存
    print("=== 当前库存 ===")
    stocks = inventory.get_stock()
    for mid, info in stocks.items():
        m = info['material']
        print(f"{m.name}: {info['quantity']} {m.unit} [{info['status']}]")
    
    # 智能推荐采购
    print("\n=== 智能推荐 ===")
    suggestions = scheduler.suggest_orders()
    for s in suggestions:
        print(f"[{s['priority']}] {s['material_name']}: 建议采购{s['suggested_quantity']}吨, 约{s['estimated_cost']}元")
    
    # 创建采购订单
    if suggestions:
        order = scheduler.create_order(suggestions[0]['material_id'], suggestions[0]['suggested_quantity'])
        print(f"\n创建订单: {order['material_name']} x {order['quantity']}")
        
        # 审批并入库
        scheduler.approve_order(order['id'])
        scheduler.arrive_order(order['id'])
        print("订单已完成入库")
    
    # 创建配送
    print("\n=== 创建配送 ===")
    allocation = scheduler.create_allocation('M002', 5, 'K100+500', '浇筑混凝土')
    print(f"配送计划: {allocation['material_name']} x {allocation['quantity']} -> {allocation['location']}")
    
    # 完成配送
    scheduler.complete_allocation(allocation['id'])
    print("配送完成")
