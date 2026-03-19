"""
哈希计算模块：负责计算文件的SHA-256哈希值
"""
import hashlib
import os
from typing import Optional

from config.settings import HASH_BUFFER_SIZE


def calculate_sha256(file_path: str) -> Optional[str]:
    """
    计算文件的SHA-256哈希值
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件的SHA-256哈希值（十六进制字符串），如果计算失败则返回None
    """
    sha256_hash = hashlib.sha256()
    
    try:
        with open(file_path, 'rb') as f:
            # 分块读取文件以处理大文件
            while True:
                data = f.read(HASH_BUFFER_SIZE)
                if not data:
                    break
                sha256_hash.update(data)
        return sha256_hash.hexdigest()
    except (IOError, OSError) as e:
        print(f"计算哈希值失败: {file_path}, 错误: {e}")
        return None


def calculate_sha256_from_bytes(data: bytes) -> str:
    """
    从字节数据计算SHA-256哈希值
    
    Args:
        data: 字节数据
        
    Returns:
        SHA-256哈希值（十六进制字符串）
    """
    return hashlib.sha256(data).hexdigest()
