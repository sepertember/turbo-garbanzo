"""
程序入口
处理用户输入、调用扫描和统计模块
"""

import sys
from constants import SCAN_ROOT_DIR, OUTPUT_DIR
from directory_scanner import DirectoryScanner
from keyword_counter import KeywordCounter
from report_builder import ReportBuilder


def get_keywords_from_user():
    """
    从用户输入获取关键词列表

    Returns:
        list: 关键词列表
    """
    print("=" * 60)
    print(" " * 15 + "本地文件内容检索工具")
    print("=" * 60)
    print(f"\n扫描目录: {SCAN_ROOT_DIR}")
    print(f"输出目录: {OUTPUT_DIR}")
    print("\n请输入要检索的关键词（支持中英文，区分大小写）")
    print("多个关键词请用逗号分隔，输入 'quit' 退出程序")
    print("-" * 60)

    while True:
        user_input = input("\n请输入关键词: ").strip()

        if user_input.lower() == 'quit':
            print("程序已退出")
            sys.exit(0)

        if not user_input:
            print("错误: 关键词不能为空，请重新输入")
            continue

        keywords = [kw.strip() for kw in user_input.split(",") if kw.strip()]

        if not keywords:
            print("错误: 未检测到有效关键词，请重新输入")
            continue

        print(f"\n已输入 {len(keywords)} 个关键词:")
        for i, keyword in enumerate(keywords, 1):
            print(f"  {i}. {keyword}")

        confirm = input("\n确认开始检索? (y/n): ").strip().lower()
        if confirm == 'y':
            return keywords
        else:
            print("请重新输入关键词")


def run_search(keywords):
    """
    执行文件检索

    Args:
        keywords: 关键词列表

    Returns:
        bool: 检索是否成功
    """
    print("\n" + "=" * 60)
    print("开始执行文件检索...")
    print("=" * 60)

    try:
        print("\n[1/4] 正在扫描目录...")
        scanner = DirectoryScanner(SCAN_ROOT_DIR)
        valid_files, skipped_files = scanner.scan()
        scan_stats = scanner.get_statistics()

        print(f"      找到 {len(valid_files)} 个有效文件")
        print(f"      跳过 {len(skipped_files)} 个文件")

        if not valid_files:
            print("\n警告: 未找到符合条件的文件，检索结束")
            return False

        print("\n[2/4] 正在统计关键词...")
        counter = KeywordCounter(keywords)
        keyword_results = counter.count_in_files(valid_files)

        total_matches = 0
        for data in keyword_results.values():
            counts = data.get("counts", {})
            if "error" not in counts:
                total_matches += sum(counts.values())

        print(f"      共找到 {total_matches} 处匹配")

        print("\n[3/4] 正在生成报告...")
        builder = ReportBuilder(keywords, scan_stats)
        report_content = builder.build_report(keyword_results, skipped_files)

        report_path = builder.save_report(report_content)
        print(f"      报告已保存: {report_path}")

        print("\n[4/4] 检索完成!")
        print("-" * 60)

        print_summary(keyword_results, keywords)

        return True

    except FileNotFoundError as e:
        print(f"\n错误: {str(e)}")
        print(f"请确保目录存在: {SCAN_ROOT_DIR}")
        return False

    except PermissionError as e:
        print(f"\n错误: 权限不足 - {str(e)}")
        return False

    except Exception as e:
        print(f"\n错误: 检索过程中发生异常 - {str(e)}")
        return False


def print_summary(keyword_results, keywords):
    """
    打印检索摘要

    Args:
        keyword_results: 关键词统计结果
        keywords: 关键词列表
    """
    print("\n【检索摘要】")

    keyword_totals = {keyword: 0 for keyword in keywords}

    for file_path, data in keyword_results.items():
        counts = data.get("counts", {})
        if "error" not in counts:
            for keyword, count in counts.items():
                if keyword in keyword_totals:
                    keyword_totals[keyword] += count

    sorted_totals = sorted(keyword_totals.items(), key=lambda x: x[1], reverse=True)

    print("\n各关键词总出现次数（按频率排序）:")
    for rank, (keyword, total) in enumerate(sorted_totals, 1):
        print(f"  {rank}. '{keyword}': {total} 次")

    print("\n" + "=" * 60)


def main():
    """
    程序主入口
    """
    try:
        keywords = get_keywords_from_user()
        success = run_search(keywords)

        if success:
            print("\n详细报告请查看: ./search_results/search_report.txt")

    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
        sys.exit(0)

    except EOFError:
        print("\n\n输入结束")
        sys.exit(0)


if __name__ == "__main__":
    main()
