import os
import csv
from datetime import datetime
from file_proc_encoder import detect_encoding
from config import METADATA_REPORTS_DIR, METADATA_CSV_FILENAME


def metadata_get_creation_time(file_path):
    try:
        creation_time = os.path.getctime(file_path)
        return datetime.fromtimestamp(creation_time).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return "N/A"


def metadata_get_modification_time(file_path):
    try:
        modification_time = os.path.getmtime(file_path)
        return datetime.fromtimestamp(modification_time).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return "N/A"


def metadata_get_file_size(file_path):
    try:
        return os.path.getsize(file_path)
    except Exception:
        return 0


def metadata_get_file_encoding(file_path):
    encoding = detect_encoding(file_path)
    return encoding if encoding else "Unknown"


def metadata_extract_single_file(file_path):
    if not os.path.exists(file_path):
        return None
    
    file_size = metadata_get_file_size(file_path)
    if file_size == 0:
        return {
            "filename": os.path.basename(file_path),
            "file_path": file_path,
            "creation_time": "N/A",
            "modification_time": "N/A",
            "file_size_bytes": 0,
            "encoding": "N/A",
            "status": "skipped",
            "reason": "Empty file"
        }
    
    return {
        "filename": os.path.basename(file_path),
        "file_path": file_path,
        "creation_time": metadata_get_creation_time(file_path),
        "modification_time": metadata_get_modification_time(file_path),
        "file_size_bytes": file_size,
        "encoding": metadata_get_file_encoding(file_path),
        "status": "processed",
        "reason": ""
    }


def metadata_generate_report(metadata_list):
    os.makedirs(METADATA_REPORTS_DIR, exist_ok=True)
    report_path = os.path.join(METADATA_REPORTS_DIR, METADATA_CSV_FILENAME)
    
    fieldnames = [
        "filename", "file_path", "creation_time", "modification_time",
        "file_size_bytes", "encoding", "status", "reason"
    ]
    
    with open(report_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in metadata_list:
            writer.writerow(data)
    
    return report_path
