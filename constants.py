import os

SCAN_EXTENSIONS = (".txt", ".md", ".py")
MIN_FILE_SIZE_BYTES = 1024
EXCLUDED_FILENAME = "exclude_list.txt"
SCAN_ROOT_DIR = os.path.join(".", "scan_target")
REPORT_OUTPUT_DIR = os.path.join(".", "search_results")
PYTHON_COMMENT_PREFIX = "#"
MARKDOWN_COMMENT_PREFIX = "<!--"
MARKDOWN_COMMENT_SUFFIX = "-->"
