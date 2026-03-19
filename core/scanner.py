"""
目录扫描模块：负责递归扫描输入目录，生成文件列表
"""
import os
from typing import List

from config.settings import INPUT_DIR


def scan_directory(directory: str = INPUT_DIR) -> List[str]:
    """
    递归扫描目录，获取所有文件的相对路径列表
    
    Args:
        directory: 要扫描的目录路径，默认为配置的输入目录
        
    Returns:
        文件相对路径列表（相对于输入目录）
    """
    file_list = []
    
    for root, dirs, files in os.walk(directory):
        for filename in files:
            # 获取绝对路径
            abs_path = os.path.join(root, filename)
            # 计算相对于输入目录的相对路径
            rel_path = os.path.relpath(abs_path, directory)
            file_list.append(rel_path)
    
    return file_list


def get_absolute_path(relative_path: str, base_dir: str = INPUT_DIR) -> str:
    """
    将相对路径转换为绝对路径
    
    Args:
        relative_path: 相对路径
        base_dir: 基础目录
        
    Returns:
        绝对路径
    """
    return os.path.join(base_dir, relative_path)


def get_relative_path(absolute_path: str, base_dir: str = INPUT_DIR) -> str:
    """
    将绝对路径转换为相对路径
    
    Args:
        absolute_path: 绝对路径
        base_dir: 基础目录
        
    Returns:
        相对路径
    """
    return os.path.relpath(absolute_path, base_dir)
