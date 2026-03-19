"""
备份模块：负责根据规则复制文件到输出目录
"""
import os
import shutil
from typing import Dict, List

from config.settings import (
    INPUT_DIR,
    OUTPUT_DIR,
    RULES_FILE_PATH,
    DEFAULT_BACKUP_RULE,
)
from utils.file_utils import (
    safe_read_json,
    ensure_directory_exists,
    get_file_extension,
)


def load_backup_rules() -> Dict[str, bool]:
    """
    加载备份规则文件
    
    Returns:
        备份规则字典，键为扩展名，值为是否备份
    """
    rules = safe_read_json(RULES_FILE_PATH, default={})
    
    # 确保规则是字典类型
    if not isinstance(rules, dict):
        print(f"警告: 规则文件格式不正确，使用空规则")
        return {}
    
    return rules


def should_backup(file_path: str, rules: Dict[str, bool]) -> bool:
    """
    根据规则判断文件是否需要备份
    
    Args:
        file_path: 文件路径
        rules: 备份规则字典
        
    Returns:
        是否需要备份
    """
    ext = get_file_extension(file_path)
    
    # 如果规则中有该扩展名的明确设置，使用规则值
    if ext in rules:
        return bool(rules[ext])
    
    # 默认不备份
    return DEFAULT_BACKUP_RULE


def backup_file(
    relative_path: str,
    rules: Dict[str, bool],
    input_dir: str = INPUT_DIR,
    output_dir: str = OUTPUT_DIR,
) -> bool:
    """
    备份单个文件到输出目录
    
    Args:
        relative_path: 文件的相对路径
        rules: 备份规则字典
        input_dir: 输入目录
        output_dir: 输出目录
        
    Returns:
        备份是否成功
    """
    # 检查是否需要备份
    if not should_backup(relative_path, rules):
        return False
    
    source_path = os.path.join(input_dir, relative_path)
    dest_path = os.path.join(output_dir, relative_path)
    
    # 确保目标目录存在
    dest_dir = os.path.dirname(dest_path)
    ensure_directory_exists(dest_dir)
    
    try:
        shutil.copy2(source_path, dest_path)
        return True
    except (IOError, OSError) as e:
        print(f"备份文件失败: {relative_path}, 错误: {e}")
        return False


def backup_files(
    file_list: List[str],
    rules: Dict[str, bool],
    input_dir: str = INPUT_DIR,
    output_dir: str = OUTPUT_DIR,
) -> List[str]:
    """
    批量备份文件
    
    Args:
        file_list: 文件相对路径列表
        rules: 备份规则字典
        input_dir: 输入目录
        output_dir: 输出目录
        
    Returns:
        成功备份的文件列表
    """
    backed_up_files = []
    
    for relative_path in file_list:
        if backup_file(relative_path, rules, input_dir, output_dir):
            backed_up_files.append(relative_path)
    
    return backed_up_files
