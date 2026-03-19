"""
常量定义模块
存放路径、文件格式、命名规范等常量
"""

import os

SCAN_ROOT_DIR = "./scan_target/"
OUTPUT_DIR = "./search_results/"

SCAN_EXTENSIONS = {".txt", ".md", ".py"}

MIN_FILE_SIZE_BYTES = 1024

EXCLUDE_FILE_NAME = "exclude_list.txt"

REPORT_FILE_NAME = "search_report.txt"

PYTHON_COMMENT_MARKER = "#"
MARKDOWN_COMMENT_MARKER = "<!--"
MARKDOWN_COMMENT_END_MARKER = "-->"

ENCODING_UTF8 = "utf-8"
