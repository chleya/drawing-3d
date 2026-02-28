# -*- coding: utf-8 -*-
"""
Drawing 3D - Logging System
日志系统
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime


class Logger:
    """日志管理器"""
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, log_dir='logs', level=logging.INFO):
        if hasattr(self, '_initialized'):
            return
        
        self.log_dir = log_dir
        self.level = level
        self._initialized = True
        
        # 创建日志目录
        os.makedirs(log_dir, exist_ok=True)
        
        # 配置日志格式
        self.formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 创建日志器
        self.logger = logging.getLogger('Drawing3D')
        self.logger.setLevel(level)
        
        # 清除现有处理器
        self.logger.handlers.clear()
        
        # 控制台处理器
        console = logging.StreamHandler()
        console.setFormatter(self.formatter)
        self.logger.addHandler(console)
        
        # 文件处理器 (按日期)
        log_file = os.path.join(log_dir, f'drawing3d_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=30
        )
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)
    
    def debug(self, msg):
        self.logger.debug(msg)
    
    def info(self, msg):
        self.logger.info(msg)
    
    def warning(self, msg):
        self.logger.warning(msg)
    
    def error(self, msg):
        self.logger.error(msg)
    
    def critical(self, msg):
        self.logger.critical(msg)
    
    def exception(self, msg):
        self.logger.exception(msg)


# 全局日志实例
logger = Logger()


def log_request(endpoint, params=None):
    """记录请求"""
    logger.info(f"REQUEST: {endpoint} | params: {params}")


def log_response(endpoint, status, data=None):
    """记录响应"""
    logger.info(f"RESPONSE: {endpoint} | status: {status}")


def log_error(endpoint, error):
    """记录错误"""
    logger.error(f"ERROR: {endpoint} | error: {error}")


def log_performance(endpoint, duration):
    """记录性能"""
    logger.info(f"PERFORMANCE: {endpoint} | duration: {duration:.3f}s")
