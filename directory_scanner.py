"""
目录扫描模块
递归扫描目录，筛选符合条件的文件
"""

import os
from constants import SCAN_ROOT_DIR
from file_validator import FileValidator


class DirectoryScanner:
    """
    目录扫描器类，用于递归扫描指定目录下的文件
    """

    def __init__(self, root_dir=None):
        """
        初始化目录扫描器

        Args:
            root_dir: 扫描根目录，默认为 SCAN_ROOT_DIR
        """
        self.root_dir = root_dir if root_dir else SCAN_ROOT_DIR
        self.valid_files = []
        self.skipped_files = []

    def scan(self):
        """
        递归扫描目录，返回符合条件的文件列表

        Returns:
            tuple: (有效文件列表, 跳过的文件列表)

        Raises:
            FileNotFoundError: 当根目录不存在时
            PermissionError: 当没有权限访问根目录时
        """
        self.valid_files = []
        self.skipped_files = []

        if not os.path.exists(self.root_dir):
            raise FileNotFoundError(f"扫描目录不存在: {self.root_dir}")

        if not os.path.isdir(self.root_dir):
            raise NotADirectoryError(f"路径不是目录: {self.root_dir}")

        if not os.access(self.root_dir, os.R_OK | os.X_OK):
            raise PermissionError(f"无权限访问目录: {self.root_dir}")

        self._scan_recursive(self.root_dir)

        return self.valid_files, self.skipped_files

    def _scan_recursive(self, current_dir):
        """
        递归扫描目录内部方法

        Args:
            current_dir: 当前扫描的目录
        """
        try:
            entries = os.listdir(current_dir)
        except (OSError, PermissionError) as e:
            self.skipped_files.append({
                "path": current_dir,
                "reason": f"无法列出目录内容: {str(e)}"
            })
            return

        for entry in entries:
            full_path = os.path.join(current_dir, entry)

            if os.path.isdir(full_path):
                self._scan_recursive(full_path)
            elif os.path.isfile(full_path):
                self._process_file(full_path)

    def _process_file(self, file_path):
        """
        处理单个文件

        Args:
            file_path: 文件路径
        """
        is_valid, message = FileValidator.is_valid_file(file_path)

        if is_valid:
            file_info = FileValidator.get_file_info(file_path)
            if file_info:
                self.valid_files.append(file_info)
        else:
            self.skipped_files.append({
                "path": file_path,
                "reason": message
            })

    def get_statistics(self):
        """
        获取扫描统计信息

        Returns:
            dict: 包含扫描统计信息的字典
        """
        return {
            "root_dir": self.root_dir,
            "valid_files_count": len(self.valid_files),
            "skipped_files_count": len(self.skipped_files),
            "total_processed": len(self.valid_files) + len(self.skipped_files)
        }
