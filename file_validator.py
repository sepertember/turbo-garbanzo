"""
文件验证模块
验证文件大小、格式、权限等合法性
"""

import os
from constants import (
    SCAN_EXTENSIONS,
    MIN_FILE_SIZE_BYTES,
    EXCLUDE_FILE_NAME,
    ENCODING_UTF8
)


class FileValidator:
    """
    文件验证器类，用于验证文件是否符合扫描条件
    """

    @staticmethod
    def is_valid_extension(file_path):
        """
        检查文件扩展名是否在允许的列表中

        Args:
            file_path: 文件路径

        Returns:
            bool: 扩展名是否有效
        """
        _, ext = os.path.splitext(file_path)
        return ext.lower() in SCAN_EXTENSIONS

    @staticmethod
    def is_valid_size(file_path):
        """
        检查文件大小是否大于等于最小要求

        Args:
            file_path: 文件路径

        Returns:
            bool: 文件大小是否有效
        """
        try:
            file_size = os.path.getsize(file_path)
            return file_size >= MIN_FILE_SIZE_BYTES
        except (OSError, IOError):
            return False

    @staticmethod
    def is_excluded_file(file_path):
        """
        检查文件是否为排除列表文件

        Args:
            file_path: 文件路径

        Returns:
            bool: 是否为排除文件
        """
        file_name = os.path.basename(file_path)
        return file_name == EXCLUDE_FILE_NAME

    @staticmethod
    def has_read_permission(file_path):
        """
        检查是否有读取文件的权限

        Args:
            file_path: 文件路径

        Returns:
            bool: 是否有读取权限
        """
        return os.access(file_path, os.R_OK)

    @staticmethod
    def is_valid_file(file_path):
        """
        综合验证文件是否适合扫描

        Args:
            file_path: 文件路径

        Returns:
            tuple: (是否有效, 错误信息)
        """
        if not os.path.exists(file_path):
            return False, f"文件不存在: {file_path}"

        if not os.path.isfile(file_path):
            return False, f"路径不是文件: {file_path}"

        if FileValidator.is_excluded_file(file_path):
            return False, f"排除文件，跳过: {file_path}"

        if not FileValidator.is_valid_extension(file_path):
            return False, f"不支持的文件格式: {file_path}"

        if not FileValidator.is_valid_size(file_path):
            return False, f"文件小于 {MIN_FILE_SIZE_BYTES} 字节，跳过: {file_path}"

        if not FileValidator.has_read_permission(file_path):
            return False, f"无读取权限: {file_path}"

        return True, ""

    @staticmethod
    def get_file_info(file_path):
        """
        获取文件信息

        Args:
            file_path: 文件路径

        Returns:
            dict: 包含文件信息的字典，如果获取失败返回 None
        """
        try:
            stat_info = os.stat(file_path)
            return {
                "path": file_path,
                "size": stat_info.st_size,
                "modified_time": stat_info.st_mtime
            }
        except (OSError, IOError) as e:
            return None
