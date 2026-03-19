"""
配置文件：存放路径常量和默认配置
"""
import os

# 基础路径配置
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 输入输出目录路径（相对路径）
INPUT_DIR = os.path.join(BASE_DIR, "data", "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "output")

# 规则文件名
RULES_FILENAME = "backup_rules.json"
RULES_FILE_PATH = os.path.join(INPUT_DIR, RULES_FILENAME)

# 报告文件名
REPORT_FILENAME = "backup_report.json"
REPORT_FILE_PATH = os.path.join(OUTPUT_DIR, REPORT_FILENAME)

# 默认规则：没有明确规则的扩展名默认不备份
DEFAULT_BACKUP_RULE = False

# JSON格式化缩进
JSON_INDENT = 2

# 哈希计算缓冲区大小（字节）
HASH_BUFFER_SIZE = 8192
