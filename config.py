import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RAW_FILES_DIR = os.path.join(BASE_DIR, "raw_files")
CONVERTED_FILES_DIR = os.path.join(BASE_DIR, "converted_files")
METADATA_REPORTS_DIR = os.path.join(BASE_DIR, "metadata_reports")

SUPPORTED_ENCODINGS = ["utf-8", "gbk", "gb2312"]

METADATA_CSV_FILENAME = "metadata_list.csv"
LOG_FILENAME = "conversion.log"

TXT_EXT = ".txt"
CSV_EXT = ".csv"
