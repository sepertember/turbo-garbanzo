"""
通用文件操作工具函数
"""
import json
import os
from typing import Any, Dict, Optional


def ensure_directory_exists(dir_path: str) -> None:
    """
    确保目录存在，如果不存在则创建
    
    Args:
        dir_path: 目录路径
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)


def safe_read_json(file_path: str, default: Optional[Any] = None) -> Any:
    """
    安全读取JSON文件
    
    Args:
        file_path: JSON文件路径
        default: 读取失败时返回的默认值
        
    Returns:
        解析后的JSON数据，或默认值
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, IOError):
        return default


def safe_write_json(file_path: str, data: Any, indent: int = 2) -> bool:
    """
    安全写入JSON文件
    
    Args:
        file_path: 目标文件路径
        data: 要写入的数据
        indent: JSON缩进空格数
        
    Returns:
        写入是否成功
    """
    try:
        # 确保目标目录存在
        dir_path = os.path.dirname(file_path)
        if dir_path:
            ensure_directory_exists(dir_path)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        return True
    except (IOError, TypeError) as e:
        print(f"写入JSON文件失败: {file_path}, 错误: {e}")
        return False


def get_file_extension(file_path: str) -> str:
    """
    获取文件扩展名（小写，包含点号）
    
    Args:
        file_path: 文件路径
        
    Returns:
        小写的文件扩展名（如 '.txt'），如果没有扩展名则返回空字符串
    """
    _, ext = os.path.splitext(file_path)
    return ext.lower()


def validate_input_directory(input_dir: str) -> bool:
    """
    验证输入目录是否存在
    
    Args:
        input_dir: 输入目录路径
        
    Returns:
        目录是否存在
        
    Raises:
        SystemExit: 如果目录不存在，打印错误信息并退出
    """
    if not os.path.exists(input_dir):
        print(f"错误: 输入目录不存在: {input_dir}")
        exit(1)
    if not os.path.isdir(input_dir):
        print(f"错误: 输入路径不是目录: {input_dir}")
        exit(1)
    return True
