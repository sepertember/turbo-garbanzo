import os
from datetime import datetime
from typing import Dict, List


class ReportBuilder:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self._ensure_output_dir()

    def _ensure_output_dir(self):
        try:
            os.makedirs(self.output_dir, exist_ok=True)
        except (OSError, PermissionError):
            pass

    @staticmethod
    def _get_file_size(file_path: str) -> int:
        try:
            return os.path.getsize(file_path)
        except (OSError, IOError):
            return 0

    def build_report(self, results: List[Dict], keywords: List[str]) -> str:
        all_keyword_totals = {kw: 0 for kw in keywords}
        for result in results:
            for kw, count in result["counts"].items():
                all_keyword_totals[kw] += count

        sorted_keywords = sorted(keywords, key=lambda k: all_keyword_totals[k], reverse=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"search_report_{timestamp}.txt"
        report_path = os.path.join(self.output_dir, report_filename)

        try:
            with open(report_path, "w", encoding="utf-8") as f:
                f.write("=" * 70 + "\n")
                f.write("本地文件内容检索与关键词统计报告\n")
                f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 70 + "\n\n")

                f.write("关键词总频率统计 (按频率排序):\n")
                f.write("-" * 40 + "\n")
                for kw in sorted_keywords:
                    f.write(f"  {kw}: {all_keyword_totals[kw]} 次\n")
                f.write("\n")

                f.write("各文件详情:\n")
                f.write("=" * 70 + "\n")

                sorted_results = sorted(
                    results,
                    key=lambda r: sum(r["counts"].values()),
                    reverse=True
                )

                for result in sorted_results:
                    file_path = result["file_path"]
                    file_size = self._get_file_size(file_path)
                    f.write(f"\n文件路径: {file_path}\n")
                    f.write(f"文件大小: {file_size} 字节\n")
                    f.write("关键词统计:\n")
                    for kw in sorted_keywords:
                        count = result["counts"].get(kw, 0)
                        if count > 0:
                            f.write(f"  {kw}: {count} 次\n")
                    f.write("-" * 50 + "\n")

                f.write(f"\n扫描完成! 共扫描 {len(results)} 个有效文件.\n")
        except (OSError, IOError, PermissionError):
            return ""

        return report_path
