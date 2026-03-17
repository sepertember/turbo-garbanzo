"""
批量文件格式转换与元数据提取工具 - 程序入口

功能：
- 批量处理指定目录下的文本类文件
- 完成 TXT ↔ CSV 格式转换
- 提取文件元数据（创建时间、大小、编码格式）
- 生成元数据清单和转换日志

使用方法：
    python main.py
    
然后按提示选择转换方向：
    1. TXT → CSV
    2. CSV → TXT
"""
import os
import sys
from config import (
    RAW_FILES_DIR,
    CONVERTED_FILES_DIR,
    METADATA_REPORTS_DIR,
    SUPPORTED_EXTENSIONS
)
from file_proc_converter import FileConverter
from file_proc_metadata import (
    metadata_batch_extract,
    metadata_save_to_csv
)
from file_proc_encoder import is_valid_text_file
from logger import get_logger


def print_banner():
    """打印程序欢迎信息"""
    print("=" * 60)
    print("  批量文件格式转换与元数据提取工具")
    print("=" * 60)
    print()


def print_directories():
    """打印目录信息"""
    print("目录配置：")
    print(f"  输入目录:  {RAW_FILES_DIR}")
    print(f"  输出目录:  {CONVERTED_FILES_DIR}")
    print(f"  报告目录:  {METADATA_REPORTS_DIR}")
    print()


def ensure_directories():
    """确保所有必要的目录都存在"""
    for directory in [RAW_FILES_DIR, CONVERTED_FILES_DIR, METADATA_REPORTS_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"创建目录: {directory}")


def get_conversion_direction() -> str:
    """
    获取用户选择的转换方向
    
    Returns:
        转换方向字符串: "txt_to_csv" 或 "csv_to_txt"
    """
    print("请选择转换方向：")
    print("  1. TXT → CSV (将文本文件转换为逗号分隔的CSV文件)")
    print("  2. CSV → TXT (将CSV文件转换为文本文件)")
    print()
    
    while True:
        choice = input("请输入选项 (1 或 2): ").strip()
        
        if choice == "1":
            return "txt_to_csv"
        elif choice == "2":
            return "csv_to_txt"
        else:
            print("无效选项，请重新输入！")


def scan_source_files(direction: str) -> list:
    """
    扫描源文件目录中的文件
    
    Args:
        direction: 转换方向
        
    Returns:
        源文件路径列表
    """
    if direction == "txt_to_csv":
        source_ext = ".txt"
    else:
        source_ext = ".csv"
    
    source_files = []
    
    if not os.path.exists(RAW_FILES_DIR):
        print(f"错误: 输入目录不存在: {RAW_FILES_DIR}")
        return source_files
    
    for filename in os.listdir(RAW_FILES_DIR):
        if filename.lower().endswith(source_ext):
            source_files.append(os.path.join(RAW_FILES_DIR, filename))
    
    return source_files


def validate_files(file_paths: list) -> tuple[list, list]:
    """
    验证文件列表，区分有效文件和无效文件
    
    Args:
        file_paths: 文件路径列表
        
    Returns:
        tuple: (有效文件列表, 无效文件信息列表)
    """
    valid_files = []
    invalid_files = []
    
    for file_path in file_paths:
        is_valid, result = is_valid_text_file(file_path)
        if is_valid:
            valid_files.append(file_path)
        else:
            invalid_files.append((file_path, result))
    
    return valid_files, invalid_files


def extract_and_save_metadata(file_paths: list) -> tuple[bool, str]:
    """
    提取并保存文件元数据
    
    Args:
        file_paths: 文件路径列表
        
    Returns:
        tuple: (是否成功, 消息)
    """
    if not file_paths:
        return False, "没有文件需要提取元数据"
    
    print("\n正在提取文件元数据...")
    
    # 批量提取元数据
    metadata_list = metadata_batch_extract(file_paths)
    
    # 保存到 CSV
    success, message = metadata_save_to_csv(metadata_list)
    
    if success:
        print(f"✓ 元数据清单已生成: {message}")
        # 记录元数据提取日志
        logger = get_logger()
        for file_path in file_paths:
            logger.log_metadata_extracted(file_path)
    else:
        print(f"✗ 元数据提取失败: {message}")
    
    return success, message


def execute_conversion(direction: str) -> dict:
    """
    执行转换流程
    
    Args:
        direction: 转换方向
        
    Returns:
        转换结果统计字典
    """
    # 扫描源文件
    source_files = scan_source_files(direction)
    
    if not source_files:
        ext = ".txt" if direction == "txt_to_csv" else ".csv"
        print(f"\n警告: 在 {RAW_FILES_DIR} 中未找到 {ext} 文件")
        return {"success": 0, "failed": 0, "skipped": 0, "total": 0, "message": "未找到源文件"}
    
    print(f"\n发现 {len(source_files)} 个待处理文件")
    
    # 验证文件
    valid_files, invalid_files = validate_files(source_files)
    
    if invalid_files:
        print(f"  - 有效文件: {len(valid_files)} 个")
        print(f"  - 无效文件: {len(invalid_files)} 个")
        for file_path, reason in invalid_files:
            print(f"    * 跳过: {os.path.basename(file_path)} - {reason}")
    
    if not valid_files:
        print("\n没有有效的文件可以转换")
        return {"success": 0, "failed": 0, "skipped": len(invalid_files), "total": len(source_files), "message": "没有有效文件"}
    
    # 提取元数据（包括有效和无效文件）
    extract_and_save_metadata(source_files)
    
    # 执行转换
    print(f"\n开始转换文件...")
    converter = FileConverter()
    result = converter.batch_convert(direction)
    
    return result


def print_result(result: dict):
    """
    打印转换结果
    
    Args:
        result: 转换结果统计字典
    """
    print("\n" + "=" * 60)
    print("  转换结果")
    print("=" * 60)
    print(f"  总文件数: {result.get('total', 0)}")
    print(f"  成功:     {result.get('success', 0)}")
    print(f"  失败:     {result.get('failed', 0)}")
    print(f"  跳过:     {result.get('skipped', 0)}")
    print("=" * 60)
    
    if result.get('message'):
        print(f"\n{result['message']}")
    
    print(f"\n输出文件位置: {CONVERTED_FILES_DIR}")
    print(f"日志文件位置: {os.path.join(METADATA_REPORTS_DIR, 'conversion.log')}")
    print(f"元数据清单:   {os.path.join(METADATA_REPORTS_DIR, 'metadata_report.csv')}")


def main():
    """主函数 - 程序入口"""
    print_banner()
    
    # 确保目录存在
    ensure_directories()
    
    # 打印目录信息
    print_directories()
    
    # 获取转换方向
    direction = get_conversion_direction()
    
    # 清空之前的日志
    logger = get_logger()
    logger.clear_log()
    
    # 执行转换
    result = execute_conversion(direction)
    
    # 打印结果
    print_result(result)
    
    print("\n程序执行完毕！")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n程序发生错误: {e}")
        sys.exit(1)
