import os
import sys
from config import RAW_FILES_DIR, CONVERTED_FILES_DIR, TXT_EXT, CSV_EXT
from file_proc_converter import convert_single_file
from file_proc_metadata import metadata_extract_single_file, metadata_generate_report
from logger import init_logger, log_batch_start, log_batch_end, log_conversion_success, log_conversion_failure, log_skip, log_metadata_extracted


def get_files_by_extension(directory, ext):
    files = []
    if os.path.exists(directory):
        for f in os.listdir(directory):
            f_path = os.path.join(directory, f)
            if os.path.isfile(f_path) and f.lower().endswith(ext):
                files.append(f_path)
    return sorted(files)


def batch_process(direction):
    os.makedirs(RAW_FILES_DIR, exist_ok=True)
    os.makedirs(CONVERTED_FILES_DIR, exist_ok=True)
    
    init_logger()
    log_batch_start(direction, RAW_FILES_DIR, CONVERTED_FILES_DIR)
    
    direction_normalized = direction.replace("->", "→")
    
    if direction_normalized in ["TXT→CSV", "TXT2CSV", "txt2csv", "TXT_CSV"]:
        source_ext = TXT_EXT
        files = get_files_by_extension(RAW_FILES_DIR, source_ext)
    elif direction_normalized in ["CSV→TXT", "CSV2TXT", "csv2txt", "CSV_TXT"]:
        source_ext = CSV_EXT
        files = get_files_by_extension(RAW_FILES_DIR, source_ext)
    else:
        print(f"不支持的转换方向: {direction}")
        print("请使用: TXT→CSV 或 CSV→TXT")
        return
    
    if not files:
        print(f"在 {RAW_FILES_DIR} 中未找到 {source_ext} 文件")
        return
    
    print(f"找到 {len(files)} 个文件，开始批量处理...")
    
    success_count = 0
    fail_count = 0
    skip_count = 0
    metadata_list = []
    
    for file_path in files:
        file_size = os.path.getsize(file_path)
        metadata = metadata_extract_single_file(file_path)
        
        if metadata:
            log_metadata_extracted(file_path)
            
            if file_size == 0:
                skip_count += 1
                reason = "空文件"
                log_skip(file_path, reason)
                print(f"跳过: {os.path.basename(file_path)} ({reason})")
                metadata["status"] = "skipped"
                metadata["reason"] = reason
                metadata_list.append(metadata)
                continue
            
            result_path, result_msg = convert_single_file(file_path, direction)
            
            if result_path and result_msg == "Success":
                success_count += 1
                log_conversion_success(file_path, result_path)
                print(f"成功: {os.path.basename(file_path)} -> {os.path.basename(result_path)}")
                metadata["status"] = "converted"
                metadata_list.append(metadata)
            else:
                fail_count += 1
                reason = result_msg if result_msg else "未知错误"
                log_conversion_failure(file_path, reason)
                print(f"失败: {os.path.basename(file_path)} ({reason})")
                metadata["status"] = "failed"
                metadata["reason"] = reason
                metadata_list.append(metadata)
        else:
            fail_count += 1
            reason = "无法提取元数据"
            log_conversion_failure(file_path, reason)
            print(f"失败: {os.path.basename(file_path)} ({reason})")
    
    if metadata_list:
        report_path = metadata_generate_report(metadata_list)
        print(f"\n元数据清单已生成: {report_path}")
    
    log_batch_end(success_count, fail_count, skip_count)
    
    print(f"\n处理完成:")
    print(f"  成功: {success_count}")
    print(f"  失败: {fail_count}")
    print(f"  跳过: {skip_count}")
    print(f"\n转换日志已保存")


def main():
    print("=" * 50)
    print("批量文件格式转换与元数据提取工具")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        direction = sys.argv[1]
    else:
        print("\n请选择转换方向:")
        print("  1. TXT→CSV")
        print("  2. CSV→TXT")
        choice = input("\n请输入选项 (1 或 2): ").strip()
        
        if choice == "1":
            direction = "TXT→CSV"
        elif choice == "2":
            direction = "CSV→TXT"
        else:
            print("无效选项")
            return
    
    batch_process(direction)


if __name__ == "__main__":
    main()
