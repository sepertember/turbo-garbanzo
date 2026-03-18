"""
报告生成模块
生成结构化的检索报告
"""

import os
from datetime import datetime
from constants import OUTPUT_DIR, REPORT_FILE_NAME, ENCODING_UTF8


class ReportBuilder:
    """
    报告构建器类，用于生成关键词检索报告
    """

    def __init__(self, keywords, scan_statistics=None):
        """
        初始化报告构建器

        Args:
            keywords: 关键词列表
            scan_statistics: 扫描统计信息
        """
        self.keywords = keywords if keywords else []
        self.scan_statistics = scan_statistics if scan_statistics else {}
        self.report_lines = []

    def build_report(self, keyword_results, skipped_files=None):
        """
        构建完整的检索报告

        Args:
            keyword_results: 关键词统计结果
            skipped_files: 被跳过的文件列表

        Returns:
            str: 报告内容
        """
        self.report_lines = []

        self._add_header()
        self._add_separator()
        self._add_scan_info()
        self._add_separator()
        self._add_keywords_info()
        self._add_separator()
        self._add_results(keyword_results)

        if skipped_files:
            self._add_separator()
            self._add_skipped_files(skipped_files)

        self._add_separator()
        self._add_summary(keyword_results)
        self._add_footer()

        return "\n".join(self.report_lines)

    def save_report(self, content, output_dir=None):
        """
        保存报告到文件

        Args:
            content: 报告内容
            output_dir: 输出目录，默认为 OUTPUT_DIR

        Returns:
            str: 保存的文件路径

        Raises:
            PermissionError: 当没有写入权限时
            OSError: 当创建目录或写入文件失败时
        """
        output_dir = output_dir if output_dir else OUTPUT_DIR

        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except OSError as e:
                raise OSError(f"无法创建输出目录: {str(e)}")

        if not os.access(output_dir, os.W_OK):
            raise PermissionError(f"无权限写入目录: {output_dir}")

        file_path = os.path.join(output_dir, REPORT_FILE_NAME)

        try:
            with open(file_path, 'w', encoding=ENCODING_UTF8) as f:
                f.write(content)
        except (OSError, IOError) as e:
            raise OSError(f"无法写入报告文件: {str(e)}")

        return file_path

    def _add_header(self):
        """添加报告头部"""
        self.report_lines.append("=" * 80)
        self.report_lines.append(" " * 25 + "本地文件内容检索报告")
        self.report_lines.append("=" * 80)
        self.report_lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def _add_footer(self):
        """添加报告尾部"""
        self.report_lines.append("=" * 80)
        self.report_lines.append("报告生成完成")
        self.report_lines.append("=" * 80)

    def _add_separator(self):
        """添加分隔线"""
        self.report_lines.append("-" * 80)

    def _add_scan_info(self):
        """添加扫描信息"""
        self.report_lines.append("【扫描信息】")

        if self.scan_statistics:
            self.report_lines.append(f"扫描目录: {self.scan_statistics.get('root_dir', 'N/A')}")
            self.report_lines.append(f"有效文件数: {self.scan_statistics.get('valid_files_count', 0)}")
            self.report_lines.append(f"跳过文件数: {self.scan_statistics.get('skipped_files_count', 0)}")
            self.report_lines.append(f"总处理文件数: {self.scan_statistics.get('total_processed', 0)}")
        else:
            self.report_lines.append("扫描信息不可用")

    def _add_keywords_info(self):
        """添加关键词信息"""
        self.report_lines.append("【检索关键词】")

        if self.keywords:
            for i, keyword in enumerate(self.keywords, 1):
                self.report_lines.append(f"  {i}. {keyword}")
        else:
            self.report_lines.append("  无关键词")

    def _add_results(self, keyword_results):
        """添加统计结果"""
        self.report_lines.append("【检索结果】")

        if not keyword_results:
            self.report_lines.append("  无检索结果")
            return

        sorted_results = sorted(
            keyword_results.items(),
            key=lambda x: sum(x[1].get("counts", {}).values()) if "error" not in x[1].get("counts", {}) else 0,
            reverse=True
        )

        for rank, (file_path, data) in enumerate(sorted_results, 1):
            counts = data.get("counts", {})
            file_size = data.get("size", 0)

            if "error" in counts:
                self.report_lines.append(f"\n  [{rank}] 文件: {file_path}")
                self.report_lines.append(f"      错误: {counts['error']}")
                continue

            total_count = sum(counts.values())

            self.report_lines.append(f"\n  [{rank}] 文件路径: {file_path}")
            self.report_lines.append(f"      文件大小: {self._format_file_size(file_size)}")
            self.report_lines.append(f"      关键词出现总次数: {total_count}")

            if counts:
                self.report_lines.append("      各关键词统计:")
                for keyword, count in counts.items():
                    self.report_lines.append(f"        - '{keyword}': {count} 次")
            else:
                self.report_lines.append("      无关键词统计")

    def _add_skipped_files(self, skipped_files):
        """添加被跳过的文件信息"""
        self.report_lines.append("【跳过的文件】")

        if not skipped_files:
            self.report_lines.append("  无")
            return

        for i, item in enumerate(skipped_files, 1):
            file_path = item.get("path", "N/A")
            reason = item.get("reason", "未知原因")
            self.report_lines.append(f"  {i}. {file_path}")
            self.report_lines.append(f"     原因: {reason}")

    def _add_summary(self, keyword_results):
        """添加统计摘要"""
        self.report_lines.append("【统计摘要】")

        if not keyword_results:
            self.report_lines.append("  无数据")
            return

        keyword_totals = {keyword: 0 for keyword in self.keywords}
        valid_files = 0

        for file_path, data in keyword_results.items():
            counts = data.get("counts", {})
            if "error" not in counts:
                valid_files += 1
                for keyword, count in counts.items():
                    if keyword in keyword_totals:
                        keyword_totals[keyword] += count

        self.report_lines.append(f"成功扫描文件数: {valid_files}")
        self.report_lines.append("")
        self.report_lines.append("各关键词总出现次数:")

        sorted_totals = sorted(keyword_totals.items(), key=lambda x: x[1], reverse=True)

        for keyword, total in sorted_totals:
            self.report_lines.append(f"  - '{keyword}': {total} 次")

    @staticmethod
    def _format_file_size(size_bytes):
        """
        格式化文件大小

        Args:
            size_bytes: 字节数

        Returns:
            str: 格式化后的大小字符串
        """
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.2f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.2f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
