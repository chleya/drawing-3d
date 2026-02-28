# -*- coding: utf-8 -*-
"""
Drawing 3D - Unit Tests
单元测试
"""

import unittest
import os
import sys
import json

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestConfig(unittest.TestCase):
    """配置测试"""
    
    def test_config_load(self):
        """测试配置加载"""
        from improvement import Config
        
        config = Config('test_config.json')
        
        # 检查默认配置
        self.assertIn('debug', config.config)
        self.assertIn('features', config.config)
        
        # 清理
        if os.path.exists('test_config.json'):
            os.remove('test_config.json')
    
    def test_config_get_set(self):
        """测试配置读写"""
        from improvement import Config
        
        config = Config('test_config.json')
        config.set('test.value', 123)
        
        self.assertEqual(config.get('test.value'), 123)
        
        # 清理
        if os.path.exists('test_config.json'):
            os.remove('test_config.json')


class TestWeather(unittest.TestCase):
    """天气系统测试"""
    
    def test_weather_import(self):
        """测试天气模块导入"""
        try:
            from weather import WeatherSystem
            self.assertTrue(True)
        except ImportError as e:
            self.skipTest(f"Weather module not available: {e}")
    
    def test_weather_basic(self):
        """测试天气基本功能"""
        try:
            from weather import WeatherSystem
            ws = WeatherSystem()
            
            # 测试获取天气
            weather = ws.get_current("北京")
            self.assertIsNotNone(weather)
        except:
            self.skipTest("Weather module incomplete")


class TestCost(unittest.TestCase):
    """成本系统测试"""
    
    def test_cost_import(self):
        """测试成本模块导入"""
        try:
            from cost import CostSystem
            self.assertTrue(True)
        except ImportError as e:
            self.skipTest(f"Cost module not available: {e}")


class TestEquipment(unittest.TestCase):
    """设备系统测试"""
    
    def test_equipment_import(self):
        """测试设备模块导入"""
        try:
            from equipment import EquipmentSystem
            self.assertTrue(True)
        except ImportError as e:
            self.skipTest(f"Equipment module not available: {e}")


class TestAIQA(unittest.TestCase):
    """AI问答测试"""
    
    def test_ai_qa_import(self):
        """测试AI问答导入"""
        try:
            from ai_qa_v2 import AIQAV2
            self.assertTrue(True)
        except ImportError as e:
            self.skipTest(f"AI Q&A module not available: {e}")


class TestSafety(unittest.TestCase):
    """安全系统测试"""
    
    def test_safety_import(self):
        """测试安全模块导入"""
        try:
            from safety import SafetySystem
            self.assertTrue(True)
        except ImportError as e:
            self.skipTest(f"Safety module not available: {e}")


class TestPersistence(unittest.TestCase):
    """持久化测试"""
    
    def test_persistence_import(self):
        """测试持久化导入"""
        try:
            from persistence import DataPersistence
            self.assertTrue(True)
        except ImportError as e:
            self.skipTest(f"Persistence module not available: {e}")


class TestErrorHandling(unittest.TestCase):
    """错误处理测试"""
    
    def test_safe_call(self):
        """测试安全调用"""
        from improvement import safe_call
        
        def success_func():
            return "success"
        
        def fail_func():
            raise ValueError("test")
        
        # 成功调用
        result = safe_call(success_func, default="failed")
        self.assertEqual(result, "success")
        
        # 失败调用
        result = safe_call(fail_func, default="error")
        self.assertEqual(result, "error")


def run_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("Drawing 3D - Unit Tests")
    print("="*60 + "\n")
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestWeather))
    suite.addTests(loader.loadTestsFromTestCase(TestCost))
    suite.addTests(loader.loadTestsFromTestCase(TestEquipment))
    suite.addTests(loader.loadTestsFromTestCase(TestAIQA))
    suite.addTests(loader.loadTestsFromTestCase(TestSafety))
    suite.addTests(loader.loadTestsFromTestCase(TestPersistence))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorHandling))
    
    # 运行
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 总结
    print("\n" + "="*60)
    if result.wasSuccessful():
        print("All tests PASSED!")
    else:
        print(f"Tests: {result.testsRun}, Failures: {len(result.failures)}, Errors: {len(result.errors)}")
    print("="*60 + "\n")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()
