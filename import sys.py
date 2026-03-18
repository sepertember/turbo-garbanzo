import sys
from typing import Dict
from constants import SCAN_TARGET_DIR, RESULTS_OUTPUT_DIR
from directory_scanner import DirectoryScanner
from keyword_counter import KeywordCounter
from report_builder import ReportBuilder


def get_user_keywords() -> list:
    print("\n" + "=" * 60)
    print("本地文件内容检索与关键词统计工具")
    print("=" * 60)
    print(f"扫描目录: {SCAN_TARGET_DIR}")
    print(f"报告输出目录: {RESULTS_OUTPUT_DIR}")
    print("-" * 60)
    
    while True:
        user_input = input("请输入关键词列表（用逗号分隔，支持中英文）: ").strip()
        
        if not user_input:
            print("错误: 关键词不能为空，请重新输入。")
            continue
        
        keywords = [kw.strip() for kw in user_input.split(',') if kw.strip()]
        
        if not keywords:
            print("错误: 未检测到有效关键词，请重新输入。")
            continue
        
        print(f"\n已识别 {len(keywords)} 个关键词:")
        for i, kw in enumerate(keywords, 1):
            print(f"  {i}. \"{kw}\"")
        
        confirm = input("\n确认关键词列表？(Y/n): ").strip().lower()
        if confirm in ('', 'y', 'yes'):
            return keywords
        
        print("请重新输入关键词...\n")


def build_file_size_dict(file_list: list) -> Dict[str, int]:
    return {file_path: file_size for file_path, file_size in file_list}


def main():
    try:
        keywords = get_user_keywords()
        
        print("\n正在扫描目录...")
        scanner = DirectoryScanner()
        valid_files = scanner.scan()
        
        if not valid_files:
            print("未找到符合条件的文件。")
            print("请确保:")
            print(f"  1. 目录 {SCAN_TARGET_DIR} 存在")
            print("  2. 目录中包含 .txt, .md 或 .py 文件")
            print("  3. 文件大小 >= 1KB")
            return
        
        print(f"扫描完成，找到 {len(valid_files)} 个符合条件的文件。")
        
        skipped = scanner.get_skipped_files()
        if skipped:
            print(f"跳过 {len(skipped)} 个不符合条件的文件/目录。")
        
        print("\n正在统计关键词...")
        counter = KeywordCounter(keywords)
        results = counter.count_in_files(valid_files)
        sorted_results = counter.get_sorted_results()
        
        print("统计完成，正在生成报告...")
        
        file_sizes = build_file_size_dict(valid_files)
        
        builder = ReportBuilder()
        report_content = builder.build_report(
            results,
            sorted_results,
            file_sizes,
            skipped
        )
        
        output_path = builder.save_report(report_content)
        
        if output_path:
            print(f"\n报告已生成: {output_path}")
            print("\n" + "-" * 60)
            print("报告预览:")
            print("-" * 60)
            preview_lines = report_content.split('\n')[:30]
            print('\n'.join(preview_lines))
            if len(report_content.split('\n')) > 30:
                print("\n... (更多内容请查看完整报告)")
        else:
            print("报告生成失败。")
    
    except KeyboardInterrupt:
        print("\n\n用户取消操作。")
        sys.exit(0)
    except Exception as e:
        print(f"\n程序运行出错: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()