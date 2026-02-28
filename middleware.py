# -*- coding: utf-8 -*-
"""
Drawing 3D - Error Handling & Middleware
错误处理与中间件
"""

from flask import Flask, request, jsonify
from functools import wraps
import time
from logging_system import logger


class APIError(Exception):
    """API异常基类"""
    def __init__(self, message, code=400):
        self.message = message
        self.code = code
        super().__init__(message)


class ValidationError(APIError):
    """验证错误"""
    def __init__(self, message):
        super().__init__(message, 400)


class NotFoundError(APIError):
    """未找到错误"""
    def __init__(self, message="Resource not found"):
        super().__init__(message, 404)


class UnauthorizedError(APIError):
    """未授权错误"""
    def __init__(self, message="Unauthorized"):
        super().__init__(message, 401)


class ServerError(APIError):
    """服务器错误"""
    def __init__(self, message="Internal server error"):
        super().__init__(message, 500)


# ==================== 中间件 ====================

def handle_errors(app):
    """错误处理中间件"""
    
    @app.errorhandler(APIError)
    def handle_api_error(error):
        logger.error(f"API Error: {error.message}")
        return jsonify({
            'error': error.message,
            'code': error.code
        }), error.code
    
    @app.errorhandler(404)
    def handle_not_found(error):
        logger.warning(f"404 Not Found: {request.url}")
        return jsonify({
            'error': 'Endpoint not found',
            'code': 404
        }), 404
    
    @app.errorhandler(500)
    def handle_server_error(error):
        logger.exception(f"500 Server Error: {error}")
        return jsonify({
            'error': 'Internal server error',
            'code': 500
        }), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        logger.exception(f"Unhandled Exception: {error}")
        return jsonify({
            'error': str(error),
            'code': 500
        }), 500


def validate_params(required_params):
    """参数验证装饰器"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            for param in required_params:
                if param not in request.json:
                    raise ValidationError(f"Missing required parameter: {param}")
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def rate_limit(max_requests=100, window=60):
    """简单限流装饰器"""
    requests_cache = {}
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr
            now = time.time()
            
            # 清理旧记录
            requests_cache[client_ip] = [
                t for t in requests_cache.get(client_ip, [])
                if now - t < window
            ]
            
            # 检查限流
            if len(requests_cache.get(client_ip, [])) >= max_requests:
                raise APIError("Rate limit exceeded", 429)
            
            # 记录请求
            requests_cache.setdefault(client_ip, []).append(now)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def performance_monitor(f):
    """性能监控装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        duration = time.time() - start_time
        
        # 记录慢请求
        if duration > 1.0:
            logger.warning(f"Slow request: {request.path} took {duration:.3f}s")
        
        return result
    return decorated_function


def cors(f):
    """CORS中间件"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = f(*args, **kwargs)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    return decorated_function


# ==================== 请求日志 ====================

def request_logger(app):
    """请求日志中间件"""
    
    @app.before_request
    def log_request():
        request.start_time = time.time()
        logger.info(f"Request: {request.method} {request.path}")
    
    @app.after_request
    def log_response(response):
        duration = time.time() - getattr(request, 'start_time', time.time())
        
        # 记录响应
        if response.status_code >= 400:
            logger.warning(f"Response: {request.path} {response.status_code} ({duration:.3f}s)")
        else:
            logger.info(f"Response: {request.path} {response.status_code} ({duration:.3f}s)")
        
        return response
