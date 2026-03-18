"""
文件元数据提取功能模块
提取文件的创建时间、修改时间、文件大小、编码格式等元数据
所有元数据相关函数均以 metadata_ 为前缀
"""
import os
import csv
from datetime import datetime
from config import METADATA_CSV_PATH, METADATA_REPORTS_DIR
from file_proc_encoder import detect_encoding


def metadata_get_file_size(file_path: str) -> int:
    """
    获取文件大小（字节）
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件大小（字节），文件不存在返回 -1
    """
    if not os.path.exists(file_path):
        return -1
    return os.path.getsize(file_path)


def metadata_get_creation_time(file_path: str) -> str:
    """
    获取文件创建时间
    
    Args:
        file_path: 文件路径
        
    Returns:
        创建时间字符串（格式：YYYY-MM-DD HH:MM:SS），文件不存在返回空字符串
    """
    if not os.path.exists(file_path):
        return ""
    
    try:
        # Windows 使用 st_ctime 作为创建时间
        timestamp = os.path.getctime(file_path)
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return ""


def metadata_get_modification_time(file_path: str) -> str:
    """
    获取文件修改时间
    
    Args:
        file_path: 文件路径
        
    Returns:
        修改时间字符串（格式：YYYY-MM-DD HH:MM:SS），文件不存在返回空字符串
    """
    if not os.path.exists(file_path):
        return ""
    
    try:
        timestamp = os.path.getmtime(file_path)
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return ""


def metadata_get_encoding(file_path: str) -> str:
    """
    获取文件编码格式
    
    Args:
        file_path: 文件路径
        
    Returns:
        编码格式字符串
    """
    return detect_encoding(file_path)


def metadata_get_filename(file_path: str) -> str:
    """
    获取文件名（不含路径）
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件名
    """
    return os.path.basename(file_path)


def metadata_get_file_extension(file_path: str) -> str:
    """
    获取文件扩展名
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件扩展名（包含点，如 .txt）
    """
    return os.path.splitext(file_path)[1].lower()


def metadata_extract_all(file_path: str) -> dict:
    """
    提取文件的所有元数据
    
    Args:
        file_path: 文件路径
        
    Returns:
        包含所有元数据的字典
    """
    return {
        "filename": metadata_get_filename(file_path),
        "file_path": file_path,
        "extension": metadata_get_file_extension(file_path),
        "size_bytes": metadata_get_file_size(file_path),
        "creation_time": metadata_get_creation_time(file_path),
        "modification_time": metadata_get_modification_time(file_path),
        "encoding": metadata_get_encoding(file_path)
    }


def metadata_generate_csv_header() -> list:
    """
    生成元数据 CSV 文件的表头
    
    Returns:
        表头字段列表
    """
    return ["文件名", "文件路径", "扩展名", "大小(字节)", "创建时间", "修改时间", "编码格式"]


def metadata_dict_to_row(metadata_dict: dict) -> list:
    """
    将元数据字典转换为 CSV 行数据
    
    Args:
        metadata_dict: 元数据字典
        
    Returns:
        CSV 行数据列表
    """
    return [
        metadata_dict.get("filename", ""),
        metadata_dict.get("file_path", ""),
        metadata_dict.get("extension", ""),
        metadata_dict.get("size_bytes", 0),
        metadata_dict.get("creation_time", ""),
        metadata_dict.get("modification_time", ""),
        metadata_dict.get("encoding", "")
    ]


def metadata_save_to_csv(metadata_list: list, csv_path: str = None) -> tuple[bool, str]:
    """
    将元数据列表保存为 CSV 文件
    
    Args:
        metadata_list: 元数据字典列表
        csv_path: CSV 文件路径，默认为 config.METADATA_CSV_PATH
        
    Returns:
        tuple: (是否成功, 消息)
    """
    if csv_path is None:
        csv_path = METADATA_CSV_PATH
    
    # 确保目录存在
    report_dir = os.path.dirname(csv_path)
    if not os.path.exists(report_dir):
        os.makedirs(report_dir, exist_ok=True)
    
    try:
        with open(csv_path, "w", newline="", encoding="UTF-8") as f:
            writer = csv.writer(f)
            # 写入表头
            writer.writerow(metadata_generate_csv_header())
            # 写入数据行
            for metadata in metadata_list:
                writer.writerow(metadata_dict_to_row(metadata))
        
        return True, f"元数据清单已保存: {csv_path}"
    except Exception as e:
        return False, f"保存元数据清单失败: {e}"


def metadata_batch_extract(file_paths: list) -> list:
    """
    批量提取多个文件的元数据
    
    Args:
        file_paths: 文件路径列表
        
    Returns:
        元数据字典列表
    """
    metadata_list = []
    for file_path in file_paths:
        if os.path.exists(file_path):
            metadata = metadata_extract_all(file_path)
            metadata_list.append(metadata)
    return metadata_list
