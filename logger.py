"""
日志记录工具模块
提供转换日志的记录功能，日志格式：时间戳 - 操作类型 - 文件路径 - 结果
"""
import os
from datetime import datetime
from config import (
    LOG_FILE_PATH,
    LOG_TIMESTAMP_FORMAT,
    LOG_LINE_FORMAT,
    METADATA_REPORTS_DIR
)


class Logger:
    """日志记录器类，用于记录转换操作的日志"""
    
    def __init__(self, log_path: str = None):
        """
        初始化日志记录器
        
        Args:
            log_path: 日志文件路径，默认为 config.LOG_FILE_PATH
        """
        self.log_path = log_path or LOG_FILE_PATH
        self._ensure_log_directory()
    
    def _ensure_log_directory(self):
        """确保日志目录存在"""
        log_dir = os.path.dirname(self.log_path)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
    
    def _get_timestamp(self) -> str:
        """获取当前时间戳字符串"""
        return datetime.now().strftime(LOG_TIMESTAMP_FORMAT)
    
    def log(self, operation: str, filepath: str, result: str, message: str = ""):
        """
        记录一条日志
        
        Args:
            operation: 操作类型（如 CONVERT, SKIP, METADATA）
            filepath: 操作的文件路径
            result: 操作结果（如 SUCCESS, FAILED, SKIPPED）
            message: 附加消息（可选）
        """
        timestamp = self._get_timestamp()
        log_line = LOG_LINE_FORMAT.format(
            timestamp=timestamp,
            operation=operation,
            filepath=filepath,
            result=result
        )
        
        if message:
            log_line += f" - {message}"
        
        self._write_log(log_line)
    
    def _write_log(self, log_line: str):
        """
        将日志写入文件
        
        Args:
            log_line: 要写入的日志行
        """
        try:
            with open(self.log_path, "a", encoding="UTF-8") as f:
                f.write(log_line + "\n")
        except Exception as e:
            print(f"写入日志失败: {e}")
    
    def log_conversion_success(self, source_path: str, target_path: str):
        """
        记录转换成功的日志
        
        Args:
            source_path: 源文件路径
            target_path: 目标文件路径
        """
        from config import OPERATION_CONVERT, RESULT_SUCCESS
        message = f"转换成功: {source_path} -> {target_path}"
        self.log(OPERATION_CONVERT, source_path, RESULT_SUCCESS, message)
    
    def log_conversion_failed(self, filepath: str, error_msg: str):
        """
        记录转换失败的日志
        
        Args:
            filepath: 文件路径
            error_msg: 错误信息
        """
        from config import OPERATION_CONVERT, RESULT_FAILED
        self.log(OPERATION_CONVERT, filepath, RESULT_FAILED, error_msg)
    
    def log_skip(self, filepath: str, reason: str):
        """
        记录跳过文件的日志
        
        Args:
            filepath: 被跳过的文件路径
            reason: 跳过原因
        """
        from config import OPERATION_SKIP, RESULT_SKIPPED
        self.log(OPERATION_SKIP, filepath, RESULT_SKIPPED, reason)
    
    def log_metadata_extracted(self, filepath: str):
        """
        记录元数据提取的日志
        
        Args:
            filepath: 提取元数据的文件路径
        """
        from config import OPERATION_METADATA, RESULT_SUCCESS
        self.log(OPERATION_METADATA, filepath, RESULT_SUCCESS, "元数据提取完成")
    
    def clear_log(self):
        """清空日志文件"""
        if os.path.exists(self.log_path):
            try:
                with open(self.log_path, "w", encoding="UTF-8") as f:
                    f.write("")
            except Exception as e:
                print(f"清空日志失败: {e}")


# 全局日志记录器实例
_default_logger = None


def get_logger(log_path: str = None) -> Logger:
    """
    获取全局日志记录器实例（单例模式）
    
    Args:
        log_path: 日志文件路径
        
    Returns:
        Logger 实例
    """
    global _default_logger
    if _default_logger is None:
        _default_logger = Logger(log_path)
    return _default_logger
