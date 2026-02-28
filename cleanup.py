# -*- coding: utf-8 -*-
"""
Drawing 3D - File Cleanup Script
清理旧文件
"""

import os
import shutil
from datetime import datetime

# 保留的核心文件
KEEP_FILES = {
    # 核心功能
    'main.py',
    'main_improved.py',
    'improvement.py',
    
    # 子系统
    'weather.py',
    'cost.py',
    'equipment.py',
    'report.py',
    'ai_qa_v2.py',
    'planning.py',
    'quality_detection.py',
    'safety.py',
    'drone.py',
    'ar_view.py',
    'material_scheduling.py',
    'web.py',
    'persistence.py',
    
    # 测试
    'test_all.py',
    
    # 配置
    'config.json',
    
    # 文档
    'README.md',
    'CRITICAL_REVIEW.md',
    'PRINCIPLES.md',
}

# 要归档的旧文件
ARCHIVE_FILES = [
    'ai_qa.py',           # 旧版，已被 ai_qa_v2.py 替换
    'simple.py',          # 简化版
    'advanced.py',        # 高级版
    'complete_data.py',   # 数据完整版
    'data_format.py',     # 数据格式
    'draw_ocr.py',       # OCR
    'draw_qa.py',        # 问答
    'features.py',       # 特性
    'flow.py',           # 流程
    'full_system.py',    # 完整系统
    'improved_ocr.py',  # 改进OCR
    'parser.py',         # 解析器
    'pdf_improved.py',  # PDF改进
    'pdf_ocr.py',       # PDF OCR
    'pdf_parser.py',    # PDF解析
    'practical.py',     # 实用版
    'production.py',    # 生产版
    'real_test.py',     # 真实测试
    'review.py',        # 审查
    'robust.py',        # 鲁棒版
    'site.py',          # 工地
    'spatial.py',       # 空间
    'ultimate.py',      # 终极版
    'visual.py',        # 可视化
    'working.py',       # 工作版
]


def cleanup():
    """清理旧文件"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    archive_dir = os.path.join(base_dir, 'archive')
    
    # 创建archive子目录
    timestamp = datetime.now().strftime('%Y%m%d')
    target_dir = os.path.join(archive_dir, f'cleanup_{timestamp}')
    os.makedirs(target_dir, exist_ok=True)
    
    print("\n" + "="*60)
    print("Drawing 3D - File Cleanup")
    print("="*60)
    
    archived = 0
    kept = []
    
    for f in os.listdir(base_dir):
        if not f.endswith('.py'):
            continue
        
        if f in ARCHIVE_FILES:
            # 归档
            src = os.path.join(base_dir, f)
            dst = os.path.join(target_dir, f)
            shutil.move(src, dst)
            print(f"  [ARCHIVE] {f}")
            archived += 1
        elif f in KEEP_FILES:
            # 保留
            kept.append(f)
        elif f.startswith('test_') and f != 'test_all.py':
            # 移动测试文件
            src = os.path.join(base_dir, f)
            dst = os.path.join(target_dir, f)
            shutil.move(src, dst)
            print(f"  [ARCHIVE] {f}")
            archived += 1
    
    print(f"\n  Archived: {archived} files")
    print(f"  Kept: {len(kept)} files")
    print(f"  Location: {target_dir}")
    print("="*60 + "\n")
    
    return archived, kept


if __name__ == "__main__":
    cleanup()
