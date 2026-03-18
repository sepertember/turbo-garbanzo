"""
关键词统计模块
统计文件中关键词出现次数，过滤注释行
"""

import os
from constants import (
    PYTHON_COMMENT_MARKER,
    MARKDOWN_COMMENT_MARKER,
    MARKDOWN_COMMENT_END_MARKER,
    ENCODING_UTF8
)


class KeywordCounter:
    """
    关键词计数器类，用于统计关键词在文件中的出现次数
    """

    def __init__(self, keywords):
        """
        初始化关键词计数器

        Args:
            keywords: 关键词列表（支持中英文，区分大小写）
        """
        self.keywords = keywords if keywords else []
        self.results = {}

    def count_in_file(self, file_path):
        """
        统计单个文件中各关键词的出现次数

        Args:
            file_path: 文件路径

        Returns:
            dict: 包含各关键词出现次数的字典
        """
        keyword_counts = {keyword: 0 for keyword in self.keywords}

        try:
            with open(file_path, 'r', encoding=ENCODING_UTF8, errors='ignore') as f:
                lines = f.readlines()
        except (OSError, IOError, UnicodeDecodeError) as e:
            return {"error": f"无法读取文件: {str(e)}"}

        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        for line in lines:
            content = self._filter_comment_line(line, ext)
            if content is not None:
                for keyword in self.keywords:
                    count = self._count_keyword_in_line(content, keyword)
                    keyword_counts[keyword] += count

        return keyword_counts

    def count_in_files(self, file_list):
        """
        统计多个文件中各关键词的出现次数

        Args:
            file_list: 文件信息列表，每个元素为包含 'path' 键的字典

        Returns:
            dict: 包含各文件关键词统计结果的字典
        """
        self.results = {}

        for file_info in file_list:
            file_path = file_info.get("path", "")
            file_size = file_info.get("size", 0)

            if not file_path:
                continue

            counts = self.count_in_file(file_path)

            self.results[file_path] = {
                "size": file_size,
                "counts": counts
            }

        return self.results

    def _filter_comment_line(self, line, file_extension):
        """
        过滤注释行，返回有效内容

        Args:
            line: 原始行内容
            file_extension: 文件扩展名

        Returns:
            str or None: 过滤后的内容，如果是注释行则返回 None
        """
        stripped = line.strip()

        if not stripped:
            return None

        if file_extension == '.py':
            if stripped.startswith(PYTHON_COMMENT_MARKER):
                return None
            if PYTHON_COMMENT_MARKER in stripped:
                stripped = stripped[:stripped.index(PYTHON_COMMENT_MARKER)].strip()
                if not stripped:
                    return None

        elif file_extension == '.md':
            if stripped.startswith(MARKDOWN_COMMENT_MARKER):
                end_pos = stripped.find(MARKDOWN_COMMENT_END_MARKER)
                if end_pos != -1:
                    after_comment = stripped[end_pos + len(MARKDOWN_COMMENT_END_MARKER):].strip()
                    if after_comment:
                        return after_comment
                return None

        return stripped

    def _count_keyword_in_line(self, line, keyword):
        """
        统计关键词在一行中的出现次数

        Args:
            line: 行内容
            keyword: 关键词

        Returns:
            int: 出现次数
        """
        count = 0
        start = 0

        while True:
            pos = line.find(keyword, start)
            if pos == -1:
                break
            count += 1
            start = pos + len(keyword)

        return count

    def get_sorted_results(self, sort_by_keyword=None):
        """
        获取按关键词频率排序的结果

        Args:
            sort_by_keyword: 按哪个关键词排序，None 则按总频率排序

        Returns:
            list: 排序后的结果列表
        """
        sorted_results = []

        for file_path, data in self.results.items():
            counts = data.get("counts", {})

            if "error" in counts:
                continue

            if sort_by_keyword and sort_by_keyword in counts:
                sort_value = counts[sort_by_keyword]
            else:
                sort_value = sum(counts.values())

            sorted_results.append({
                "file_path": file_path,
                "size": data.get("size", 0),
                "counts": counts,
                "sort_value": sort_value
            })

        sorted_results.sort(key=lambda x: x["sort_value"], reverse=True)

        return sorted_results
