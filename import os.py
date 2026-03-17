import os
from datetime import datetime
from pathlib import Path
from config import METADATA_REPORTS_DIR, LOG_FILENAME


class ConversionLogger:
    def __init__(self):
        self.log_file = METADATA_REPORTS_DIR / LOG_FILENAME
        self._ensure_log_file()
    
    def _ensure_log_file(self):
        METADATA_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        if not self.log_file.exists():
            with open(self.log_file, "w", encoding="utf-8") as f:
                f.write("")
    
    def _get_timestamp(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def log(self, operation_type: str, file_path: str, result: str):
        timestamp = self._get_timestamp()
        log_entry = f"{timestamp} - {operation_type} - {file_path} - {result}\n"
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
    
    def log_success(self, operation_type: str, file_path: str, message: str = "成功"):
        self.log(operation_type, file_path, f"成功: {message}")
    
    def log_error(self, operation_type: str, file_path: str, error_message: str):
        self.log(operation_type, file_path, f"失败: {error_message}")
    
    def log_skip(self, file_path: str, reason: str):
        self.log("跳过文件", file_path, f"原因: {reason}")