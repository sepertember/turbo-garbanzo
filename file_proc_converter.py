"""
文件格式转换核心逻辑模块
实现 TXT 和 CSV 文件之间的相互转换
"""
import os
import csv
from config import (
    RAW_FILES_DIR,
    CONVERTED_FILES_DIR,
    CSV_DELIMITER,
    SUPPORTED_EXTENSIONS,
    DEFAULT_ENCODING
)
from file_proc_encoder import (
    read_file_with_encoding,
    write_file_with_encoding,
    is_valid_text_file
)
from file_proc_metadata import metadata_extract_all
from logger import get_logger


class FileConverter:
    """文件转换器类，处理 TXT 和 CSV 之间的转换"""
    
    def __init__(self):
        self.logger = get_logger()
        self.processed_files = []
        self.skipped_files = []
    
    def txt_to_csv(self, source_path: str, target_path: str = None) -> tuple[bool, str]:
        """
        将 TXT 文件转换为 CSV 文件
        
        将 TXT 文件的每一行转换为 CSV 的一行数据
        如果 TXT 行中包含分隔符，则按分隔符分割为多列
        
        Args:
            source_path: 源 TXT 文件路径
            target_path: 目标 CSV 文件路径，为 None 则自动生成
            
        Returns:
            tuple: (是否成功, 消息)
        """
        # 验证源文件
        is_valid, result = is_valid_text_file(source_path)
        if not is_valid:
            self.logger.log_skip(source_path, f"无效文件: {result}")
            self.skipped_files.append((source_path, result))
            return False, f"跳过无效文件: {result}"
        
        # 自动生成目标路径
        if target_path is None:
            filename = os.path.basename(source_path)
            name_without_ext = os.path.splitext(filename)[0]
            target_path = os.path.join(CONVERTED_FILES_DIR, f"{name_without_ext}.csv")
        
        # 确保目标目录存在
        target_dir = os.path.dirname(target_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)
        
        try:
            # 读取源文件内容
            content, encoding = read_file_with_encoding(source_path)
            
            # 解析内容为 CSV 格式
            lines = content.strip().split('\n')
            
            # 写入 CSV 文件
            with open(target_path, "w", newline="", encoding=DEFAULT_ENCODING) as f:
                writer = csv.writer(f, delimiter=CSV_DELIMITER)
                for line in lines:
                    # 如果行中包含分隔符，则分割为多列
                    if CSV_DELIMITER in line:
                        row = line.split(CSV_DELIMITER)
                    else:
                        row = [line]
                    writer.writerow(row)
            
            # 记录成功日志
            self.logger.log_conversion_success(source_path, target_path)
            self.processed_files.append(source_path)
            
            return True, f"转换成功: {source_path} -> {target_path}"
            
        except Exception as e:
            error_msg = str(e)
            self.logger.log_conversion_failed(source_path, error_msg)
            return False, f"转换失败: {error_msg}"
    
    def csv_to_txt(self, source_path: str, target_path: str = None) -> tuple[bool, str]:
        """
        将 CSV 文件转换为 TXT 文件
        
        将 CSV 的每一行转换为 TXT 的一行，列之间用分隔符连接
        
        Args:
            source_path: 源 CSV 文件路径
            target_path: 目标 TXT 文件路径，为 None 则自动生成
            
        Returns:
            tuple: (是否成功, 消息)
        """
        # 验证源文件
        is_valid, result = is_valid_text_file(source_path)
        if not is_valid:
            self.logger.log_skip(source_path, f"无效文件: {result}")
            self.skipped_files.append((source_path, result))
            return False, f"跳过无效文件: {result}"
        
        # 自动生成目标路径
        if target_path is None:
            filename = os.path.basename(source_path)
            name_without_ext = os.path.splitext(filename)[0]
            target_path = os.path.join(CONVERTED_FILES_DIR, f"{name_without_ext}.txt")
        
        # 确保目标目录存在
        target_dir = os.path.dirname(target_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)
        
        try:
            # 读取 CSV 文件
            lines = []
            with open(source_path, "r", newline="", encoding=DEFAULT_ENCODING) as f:
                reader = csv.reader(f, delimiter=CSV_DELIMITER)
                for row in reader:
                    # 将列用分隔符连接成一行
                    line = CSV_DELIMITER.join(row)
                    lines.append(line)
            
            # 写入 TXT 文件
            content = '\n'.join(lines)
            write_file_with_encoding(target_path, content, DEFAULT_ENCODING)
            
            # 记录成功日志
            self.logger.log_conversion_success(source_path, target_path)
            self.processed_files.append(source_path)
            
            return True, f"转换成功: {source_path} -> {target_path}"
            
        except Exception as e:
            error_msg = str(e)
            self.logger.log_conversion_failed(source_path, error_msg)
            return False, f"转换失败: {error_msg}"
    
    def convert_file(self, source_path: str, direction: str) -> tuple[bool, str]:
        """
        根据方向转换单个文件
        
        Args:
            source_path: 源文件路径
            direction: 转换方向，"txt_to_csv" 或 "csv_to_txt"
            
        Returns:
            tuple: (是否成功, 消息)
        """
        if direction == "txt_to_csv":
            return self.txt_to_csv(source_path)
        elif direction == "csv_to_txt":
            return self.csv_to_txt(source_path)
        else:
            return False, f"不支持的转换方向: {direction}"
    
    def batch_convert(self, direction: str) -> dict:
        """
        批量转换目录中的所有文件
        
        Args:
            direction: 转换方向，"txt_to_csv" 或 "csv_to_txt"
            
        Returns:
            转换结果统计字典
        """
        self.processed_files = []
        self.skipped_files = []
        
        # 确定源文件扩展名
        if direction == "txt_to_csv":
            source_ext = ".txt"
        elif direction == "csv_to_txt":
            source_ext = ".csv"
        else:
            return {
                "success": 0,
                "failed": 0,
                "skipped": 0,
                "message": f"不支持的转换方向: {direction}"
            }
        
        # 获取所有源文件
        source_files = []
        if os.path.exists(RAW_FILES_DIR):
            for filename in os.listdir(RAW_FILES_DIR):
                if filename.lower().endswith(source_ext):
                    source_files.append(os.path.join(RAW_FILES_DIR, filename))
        
        if not source_files:
            return {
                "success": 0,
                "failed": 0,
                "skipped": 0,
                "message": f"在 {RAW_FILES_DIR} 中未找到 {source_ext} 文件"
            }
        
        # 执行批量转换
        success_count = 0
        failed_count = 0
        skipped_count = 0
        
        for source_path in source_files:
            success, message = self.convert_file(source_path, direction)
            if success:
                success_count += 1
            else:
                # 检查是否是跳过的文件
                if any(skipped[0] == source_path for skipped in self.skipped_files):
                    skipped_count += 1
                else:
                    failed_count += 1
        
        return {
            "success": success_count,
            "failed": failed_count,
            "skipped": skipped_count,
            "total": len(source_files),
            "message": f"批量转换完成: 成功 {success_count}, 失败 {failed_count}, 跳过 {skipped_count}"
        }
    
    def get_processed_files(self) -> list:
        """获取已处理的文件列表"""
        return self.processed_files
    
    def get_skipped_files(self) -> list:
        """获取被跳过的文件列表"""
        return self.skipped_files


def convert_single_file(source_path: str, direction: str) -> tuple[bool, str]:
    """
    转换单个文件的便捷函数
    
    Args:
        source_path: 源文件路径
        direction: 转换方向
        
    Returns:
        tuple: (是否成功, 消息)
    """
    converter = FileConverter()
    return converter.convert_file(source_path, direction)


def convert_batch(direction: str) -> dict:
    """
    批量转换的便捷函数
    
    Args:
        direction: 转换方向
        
    Returns:
        转换结果统计字典
    """
    converter = FileConverter()
    return converter.batch_convert(direction)
