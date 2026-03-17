import os
from datetime import datetime
from config import METADATA_REPORTS_DIR, LOG_FILENAME

LOG_FILE_PATH = os.path.join(METADATA_REPORTS_DIR, LOG_FILENAME)


def init_logger():
    os.makedirs(METADATA_REPORTS_DIR, exist_ok=True)
    with open(LOG_FILE_PATH, "w", encoding="utf-8") as f:
        f.write("")


def log_operation(operation_type, file_path, result):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"{timestamp} - {operation_type} - {file_path} - {result}\n"
    with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
        f.write(log_line)


def log_conversion_success(source_path, target_path):
    log_operation("CONVERT", source_path, f"Success -> {target_path}")


def log_conversion_failure(file_path, reason):
    log_operation("CONVERT", file_path, f"Failed: {reason}")


def log_skip(file_path, reason):
    log_operation("SKIP", file_path, f"Skipped: {reason}")


def log_metadata_extracted(file_path):
    log_operation("EXTRACT_METADATA", file_path, "Success")


def log_batch_start(operation, source_dir, target_dir):
    log_operation("BATCH_START", f"{source_dir} -> {target_dir}", f"Operation: {operation}")


def log_batch_end(success_count, fail_count, skip_count):
    log_operation("BATCH_END", "Summary", f"Success: {success_count}, Failed: {fail_count}, Skipped: {skip_count}")
