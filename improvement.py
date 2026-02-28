# -*- coding: utf-8 -*-
"""
Drawing 3D - Complete Improvement Plan
全面改进方案
"""

import os
import json
from datetime import datetime

# ==================== 1. 清理重复文件 ====================

DUPLICATES = [
    # 旧版本/重复
    'simple.py',
    'basic.py',
    'test_*.py',
    'old_*.py',
    'backup_*.py',
]

# 保留的核心文件
KEEP_CORE = [
    'main.py',
    'live_demo.py',
    'weather.py',
    'cost.py',
    'equipment.py',
    'report.py',
    'ai_qa_v2.py',
    'planning.py',
    'quality_detection.py',
    'safety.py',
    'compliance.py',
    'drone.py',
    'ar_view.py',
    'material_scheduling.py',
    'web.py',
    'persistence.py',
]

def cleanup_files():
    """清理重复文件"""
    print("\n=== 清理重复文件 ===")
    
    # 移动到archive
    archive_dir = 'archive'
    os.makedirs(archive_dir, exist_ok=True)
    
    # 扫描
    removed = 0
    for f in os.listdir('.'):
        if f.endswith('.py') and f not in KEEP_CORE:
            if f.startswith('test_') or f.startswith('old_') or f.startswith('backup_'):
                print(f"  Remove: {f}")
                removed += 1
    
    print(f"  Total: {removed} files")
    return removed


# ==================== 2. 配置管理系统 ====================

class Config:
    """配置管理"""
    
    DEFAULT = {
        'debug': False,
        'log_level': 'INFO',
        'data_dir': './data',
        'max_history': 1000,
        
        # API配置
        'llm': {
            'model': 'minimax/MiniMax-M2.1',
            'temperature': 0.7,
        },
        
        # 功能开关
        'features': {
            'weather': True,
            'cost': True,
            'equipment': True,
            'report': True,
            'ai_qa': True,
        },
        
        # 限制
        'limits': {
            'max_upload_size': 10 * 1024 * 1024,
            'max_query_length': 500,
            'rate_limit': 100,
        }
    }
    
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = self._load()
    
    def _load(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return {**self.DEFAULT, **json.load(f)}
        return self.DEFAULT.copy()
    
    def save(self):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def get(self, key, default=None):
        keys = key.split('.')
        value = self.config
        for k in keys:
            value = value.get(k, default)
        return value
    
    def set(self, key, value):
        keys = key.split('.')
        d = self.config
        for k in keys[:-1]:
            d = d.setdefault(k, {})
        d[keys[-1]] = value


# ==================== 3. 日志系统 ====================

import logging
from logging.handlers import RotatingFileHandler

def setup_logging(log_dir='logs', level=logging.INFO):
    """设置日志"""
    os.makedirs(log_dir, exist_ok=True)
    
    # 格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 控制台
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    
    # 文件
    file_handler = RotatingFileHandler(
        f'{log_dir}/drawing3d.log',
        maxBytes=10*1024*1024,
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    # 根日志
    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(console)
    root.addHandler(file_handler)
    
    return root


# ==================== 4. 错误处理 ====================

class Drawing3DError(Exception):
    """基础异常"""
    pass

class ConfigError(Drawing3DError):
    """配置错误"""
    pass

class DataError(Drawing3DError):
    """数据错误"""
    pass

class APIError(Drawing3DError):
    """API错误"""
    pass

def safe_call(func, *args, default=None, **kwargs):
    """安全调用"""
    try:
        return func(*args, **kwargs)
    except Drawing3DError as e:
        logging.error(f"Drawing3D Error: {e}")
        return default
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")
        return default


# ==================== 5. 单元测试 ====================

def run_tests():
    """运行测试"""
    import unittest
    
    # 发现测试
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试
    test_dir = 'tests'
    if os.path.exists(test_dir):
        suite.addTests(loader.discover(test_dir))
    
    # 运行
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


# ==================== 6. 主程序改进 ====================

def main():
    """主程序"""
    # 配置
    config = Config()
    config.set('debug', True)
    config.save()
    
    # 日志
    logger = setup_logging()
    logger.info("Drawing 3D Starting...")
    
    # 测试
    print("\n=== Running Tests ===")
    success = run_tests()
    
    print(f"\n=== Result: {'PASS' if success else 'FAIL'} ===")


if __name__ == "__main__":
    main()
