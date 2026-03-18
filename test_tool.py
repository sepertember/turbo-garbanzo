"""
测试脚本 - 非交互式测试本地文件检索工具
"""

import sys
from constants import SCAN_ROOT_DIR, OUTPUT_DIR
from directory_scanner import DirectoryScanner
from keyword_counter import KeywordCounter
from report_builder import ReportBuilder


def test_search(keywords):
    """
    测试文件检索功能

    Args:
        keywords: 关键词列表
    """
    print("=" * 60)
    print(" " * 15 + "本地文件内容检索工具 - 测试模式")
    print("=" * 60)
    print(f"\n扫描目录: {SCAN_ROOT_DIR}")
    print(f"输出目录: {OUTPUT_DIR}")
    print(f"\n测试关键词: {', '.join(keywords)}")
    print("=" * 60)

    try:
        print("\n[1/4] 正在扫描目录...")
        scanner = DirectoryScanner(SCAN_ROOT_DIR)
        valid_files, skipped_files = scanner.scan()
        scan_stats = scanner.get_statistics()

        print(f"      找到 {len(valid_files)} 个有效文件")
        for f in valid_files:
            print(f"        - {f['path']} ({f['size']} bytes)")
        print(f"      跳过 {len(skipped_files)} 个文件")
        for f in skipped_files:
            print(f"        - {f['path']}: {f['reason']}")

        if not valid_files:
            print("\n警告: 未找到符合条件的文件")
            return False

        print("\n[2/4] 正在统计关键词...")
        counter = KeywordCounter(keywords)
        keyword_results = counter.count_in_files(valid_files)

        for file_path, data in keyword_results.items():
            counts = data.get("counts", {})
            if "error" in counts:
                print(f"      错误: {file_path} - {counts['error']}")
            else:
                total = sum(counts.values())
                print(f"      {file_path}: {total} 处匹配")
                for kw, cnt in counts.items():
                    print(f"        - '{kw}': {cnt}")

        print("\n[3/4] 正在生成报告...")
        builder = ReportBuilder(keywords, scan_stats)
        report_content = builder.build_report(keyword_results, skipped_files)

        report_path = builder.save_report(report_content)
        print(f"      报告已保存: {report_path}")

        print("\n[4/4] 测试完成!")
        print("=" * 60)

        print_summary(keyword_results, keywords)

        return True

    except Exception as e:
        print(f"\n错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def print_summary(keyword_results, keywords):
    """
    打印检索摘要
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


if __name__ == "__main__":
    test_keywords = ["test", "Python", "search", "关键字"]
    success = test_search(test_keywords)
    sys.exit(0 if success else 1)
