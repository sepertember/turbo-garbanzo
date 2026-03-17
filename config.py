"""
配置文件 - 存放所有路径常量、编码类型等配置信息
"""
import os

# 基础目录路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 输入文件目录 - 原始文件存放位置
RAW_FILES_DIR = os.path.join(BASE_DIR, "raw_files")

# 输出文件目录 - 转换后的文件存放位置
CONVERTED_FILES_DIR = os.path.join(BASE_DIR, "converted_files")

# 元数据报告目录 - 元数据清单和日志存放位置
METADATA_REPORTS_DIR = os.path.join(BASE_DIR, "metadata_reports")

# 支持的字符编码列表
SUPPORTED_ENCODINGS = ["UTF-8", "GBK", "GB2312"]

# 默认编码
DEFAULT_ENCODING = "UTF-8"

# 日志文件路径
LOG_FILE_PATH = os.path.join(METADATA_REPORTS_DIR, "conversion.log")

# 元数据清单文件路径
METADATA_CSV_PATH = os.path.join(METADATA_REPORTS_DIR, "metadata_report.csv")

# 支持的文件扩展名
SUPPORTED_EXTENSIONS = [".txt", ".csv"]

# CSV 分隔符
CSV_DELIMITER = ","

# 日志格式相关常量
LOG_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_LINE_FORMAT = "{timestamp} - {operation} - {filepath} - {result}"

# 操作类型常量
OPERATION_CONVERT = "CONVERT"
OPERATION_SKIP = "SKIP"
OPERATION_METADATA = "METADATA"

# 结果状态常量
RESULT_SUCCESS = "SUCCESS"
RESULT_FAILED = "FAILED"
RESULT_SKIPPED = "SKIPPED"
