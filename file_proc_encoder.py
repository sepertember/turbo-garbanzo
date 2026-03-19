"""
字符编码检测和转换模块
自动检测文件编码（支持 UTF-8、GBK、GB2312），并提供编码转换功能
仅使用 Python 标准库实现
"""
import os
from config import SUPPORTED_ENCODINGS, DEFAULT_ENCODING


def detect_encoding(file_path: str) -> str:
    """
    检测文件的字符编码
    
    通过尝试用不同编码读取文件来检测编码格式，
    优先检测 UTF-8，然后是 GBK，最后是 GB2312
    
    Args:
        file_path: 要检测的文件路径
        
    Returns:
        检测到的编码格式，如果都失败则返回 DEFAULT_ENCODING
    """
    if not os.path.exists(file_path):
        return DEFAULT_ENCODING
    
    # 按优先级尝试各种编码
    for encoding in SUPPORTED_ENCODINGS:
        try:
            with open(file_path, "r", encoding=encoding) as f:
                f.read()
            return encoding
        except (UnicodeDecodeError, UnicodeError):
            continue
        except Exception:
            continue
    
    return DEFAULT_ENCODING


def read_file_with_encoding(file_path: str, encoding: str = None) -> tuple[str, str]:
    """
    使用指定编码或自动检测的编码读取文件内容
    
    Args:
        file_path: 文件路径
        encoding: 指定编码，为 None 时自动检测
        
    Returns:
        tuple: (文件内容, 使用的编码)
    """
    if encoding is None:
        encoding = detect_encoding(file_path)
    
    try:
        with open(file_path, "r", encoding=encoding) as f:
            content = f.read()
        return content, encoding
    except Exception as e:
        raise IOError(f"读取文件失败: {e}")


def write_file_with_encoding(file_path: str, content: str, encoding: str = DEFAULT_ENCODING):
    """
    使用指定编码写入文件内容
    
    Args:
        file_path: 文件路径
        content: 要写入的内容
        encoding: 编码格式，默认为 UTF-8
    """
    # 确保目录存在
    dir_path = os.path.dirname(file_path)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
    
    try:
        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)
    except Exception as e:
        raise IOError(f"写入文件失败: {e}")


def convert_encoding(source_path: str, target_path: str, 
                     source_encoding: str = None, 
                     target_encoding: str = DEFAULT_ENCODING) -> tuple[bool, str]:
    """
    转换文件编码
    
    Args:
        source_path: 源文件路径
        target_path: 目标文件路径
        source_encoding: 源文件编码，None 表示自动检测
        target_encoding: 目标文件编码
        
    Returns:
        tuple: (是否成功, 消息)
    """
    try:
        # 读取源文件
        content, detected_encoding = read_file_with_encoding(source_path, source_encoding)
        
        # 写入目标文件
        write_file_with_encoding(target_path, content, target_encoding)
        
        return True, f"编码转换成功: {detected_encoding} -> {target_encoding}"
    except Exception as e:
        return False, str(e)


def is_valid_text_file(file_path: str) -> tuple[bool, str]:
    """
    检查文件是否为有效的文本文件（可以被支持的编码读取）
    
    Args:
        file_path: 文件路径
        
    Returns:
        tuple: (是否有效, 检测到的编码或错误信息)
    """
    if not os.path.exists(file_path):
        return False, "文件不存在"
    
    if os.path.getsize(file_path) == 0:
        return False, "空文件"
    
    encoding = detect_encoding(file_path)
    
    try:
        with open(file_path, "r", encoding=encoding) as f:
            content = f.read()
            # 检查内容是否包含空字符（可能是二进制文件）
            if '\x00' in content:
                return False, "文件包含空字符，可能是二进制文件"
        return True, encoding
    except Exception as e:
        return False, str(e)
