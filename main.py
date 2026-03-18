import os
from constants import SCAN_ROOT_DIR, REPORT_OUTPUT_DIR
from directory_scanner import DirectoryScanner
from keyword_counter import KeywordCounter
from report_builder import ReportBuilder


def main():
    print("=" * 60)
    print("本地文件内容检索与关键词统计工具")
    print("=" * 60)

    print(f"\n扫描根目录: {os.path.abspath(SCAN_ROOT_DIR)}")
    if not os.path.exists(SCAN_ROOT_DIR):
        print(f"警告: 扫描目录不存在: {SCAN_ROOT_DIR}")
        try:
            os.makedirs(SCAN_ROOT_DIR, exist_ok=True)
            print(f"已创建扫描目录: {SCAN_ROOT_DIR}")
        except (OSError, PermissionError):
            print(f"错误: 无法创建扫描目录")
            return

    user_input = input("\n请输入关键词列表 (用空格分隔，支持中英文): ").strip()
    if not user_input:
        print("错误: 未输入任何关键词")
        return

    keywords = user_input.split()
    print(f"\n将统计以下关键词: {', '.join(keywords)}")

    print("\n开始扫描目录...")
    scanner = DirectoryScanner(SCAN_ROOT_DIR)
    valid_files = scanner.scan_directory()
    print(f"找到 {len(valid_files)} 个符合条件的文件")

    if not valid_files:
        print("\n未找到任何符合条件的文件进行统计")
        return

    print("\n开始统计关键词...")
    counter = KeywordCounter(keywords)
    results = []
    for file_path in valid_files:
        counts = counter.count_keywords_in_file(file_path)
        results.append({"file_path": file_path, "counts": counts})

    print("\n生成检索报告...")
    report_builder = ReportBuilder(REPORT_OUTPUT_DIR)
    report_path = report_builder.build_report(results, keywords)

    if report_path:
        print(f"\n报告已生成: {os.path.abspath(report_path)}")
    else:
        print("\n错误: 无法生成报告")


if __name__ == "__main__":
    main()
