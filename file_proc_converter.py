import os
import csv
from file_proc_encoder import read_file_with_encoding, detect_encoding
from config import CONVERTED_FILES_DIR, TXT_EXT, CSV_EXT


def txt_to_csv(file_path, output_dir=None):
    if output_dir is None:
        output_dir = CONVERTED_FILES_DIR
    
    os.makedirs(output_dir, exist_ok=True)
    
    content, encoding = read_file_with_encoding(file_path)
    if content is None:
        return None, "无法检测文件编码或读取文件"
    
    if len(content.strip()) == 0:
        return None, "文件内容为空"
    
    lines = content.splitlines()
    rows = []
    for line in lines:
        if line.strip():
            rows.append([line.strip()])
    
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_path = os.path.join(output_dir, base_name + CSV_EXT)
    
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    
    return output_path, "Success"


def csv_to_txt(file_path, output_dir=None):
    if output_dir is None:
        output_dir = CONVERTED_FILES_DIR
    
    os.makedirs(output_dir, exist_ok=True)
    
    encoding = detect_encoding(file_path)
    if encoding is None:
        return None, "无法检测文件编码"
    
    rows = []
    try:
        with open(file_path, "r", newline="", encoding=encoding) as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(",".join(row))
    except csv.Error as e:
        return None, f"CSV解析错误: {str(e)}"
    except Exception as e:
        return None, f"读取错误: {str(e)}"
    
    if not rows:
        return None, "文件内容为空"
    
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_path = os.path.join(output_dir, base_name + TXT_EXT)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rows))
    
    return output_path, "Success"


def convert_single_file(file_path, direction):
    if not os.path.exists(file_path):
        return None, "文件不存在"
    
    file_size = os.path.getsize(file_path)
    if file_size == 0:
        return None, "空文件"
    
    direction_normalized = direction.replace("->", "→")
    
    if direction_normalized in ["TXT→CSV", "TXT2CSV", "txt2csv", "TXT_CSV"]:
        if not file_path.lower().endswith(TXT_EXT):
            return None, f"非TXT文件，无法转换为CSV"
        return txt_to_csv(file_path)
    
    elif direction_normalized in ["CSV→TXT", "CSV2TXT", "csv2txt", "CSV_TXT"]:
        if not file_path.lower().endswith(CSV_EXT):
            return None, f"非CSV文件，无法转换为TXT"
        return csv_to_txt(file_path)
    
    else:
        return None, f"不支持的转换方向: {direction}"
