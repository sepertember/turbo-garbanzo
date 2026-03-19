"""
报告生成模块：负责生成最终的JSON报告
"""
import os
from datetime import datetime
from typing import Dict, List, Any

from config.settings import (
    INPUT_DIR,
    OUTPUT_DIR,
    REPORT_FILE_PATH,
    JSON_INDENT,
)
from utils.file_utils import safe_write_json


def format_timestamp(timestamp: float) -> str:
    """
    将时间戳格式化为可读字符串
    
    Args:
        timestamp: Unix时间戳
        
    Returns:
        格式化的时间字符串
    """
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def generate_file_info(
    relative_path: str,
    file_hash: str,
    backed_up: bool,
    input_dir: str = INPUT_DIR,
) -> Dict[str, Any]:
    """
    生成单个文件的信息字典
    
    Args:
        relative_path: 文件的相对路径
        file_hash: 文件的SHA-256哈希值
        backed_up: 是否已备份
        input_dir: 输入目录
        
    Returns:
        文件信息字典
    """
    abs_path = os.path.join(input_dir, relative_path)
    
    try:
        stat_info = os.stat(abs_path)
        file_size = stat_info.st_size
        modify_time = format_timestamp(stat_info.st_mtime)
    except (OSError, IOError):
        file_size = 0
        modify_time = ""
    
    return {
        "path": relative_path,
        "hash": file_hash,
        "size_bytes": file_size,
        "modified_time": modify_time,
        "backed_up": backed_up,
    }


def generate_report(
    file_data: List[Dict[str, Any]],
    report_path: str = REPORT_FILE_PATH,
    indent: int = JSON_INDENT,
) -> bool:
    """
    生成JSON格式的备份报告
    
    Args:
        file_data: 文件信息列表，每个元素包含路径、哈希值、大小、修改时间和备份状态
        report_path: 报告文件路径
        indent: JSON缩进空格数
        
    Returns:
        报告生成是否成功
    """
    report = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_files": len(file_data),
        "backed_up_count": sum(1 for f in file_data if f.get("backed_up", False)),
        "files": file_data,
    }
    
    return safe_write_json(report_path, report, indent)


def create_report_data(
    all_files: List[str],
    file_hashes: Dict[str, str],
    backed_up_files: List[str],
    input_dir: str = INPUT_DIR,
) -> List[Dict[str, Any]]:
    """
    创建报告数据列表
    
    Args:
        all_files: 所有文件的相对路径列表
        file_hashes: 文件路径到哈希值的映射
        backed_up_files: 已备份文件列表
        input_dir: 输入目录
        
    Returns:
        文件信息列表
    """
    backed_up_set = set(backed_up_files)
    report_data = []
    
    for relative_path in all_files:
        file_hash = file_hashes.get(relative_path, "")
        backed_up = relative_path in backed_up_set
        
        file_info = generate_file_info(
            relative_path,
            file_hash,
            backed_up,
            input_dir,
        )
        report_data.append(file_info)
    
    return report_data
