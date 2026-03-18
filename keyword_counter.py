import os
from typing import Dict, List
from constants import PYTHON_COMMENT_PREFIX, MARKDOWN_COMMENT_PREFIX, MARKDOWN_COMMENT_SUFFIX


class KeywordCounter:
    def __init__(self, keywords: List[str]):
        self.keywords = keywords

    @staticmethod
    def _is_comment_line(line: str, file_ext: str) -> bool:
        stripped = line.strip()
        if file_ext == ".py":
            return stripped.startswith(PYTHON_COMMENT_PREFIX)
        elif file_ext == ".md":
            return stripped.startswith(MARKDOWN_COMMENT_PREFIX) and stripped.endswith(MARKDOWN_COMMENT_SUFFIX)
        return False

    @staticmethod
    def _remove_markdown_comment(line: str) -> str:
        result = line
        while MARKDOWN_COMMENT_PREFIX in result and MARKDOWN_COMMENT_SUFFIX in result:
            start = result.find(MARKDOWN_COMMENT_PREFIX)
            end = result.find(MARKDOWN_COMMENT_SUFFIX, start) + len(MARKDOWN_COMMENT_SUFFIX)
            result = result[:start] + result[end:]
        return result

    def count_keywords_in_file(self, file_path: str) -> Dict[str, int]:
        counts = {kw: 0 for kw in self.keywords}
        file_ext = os.path.splitext(file_path)[1].lower()

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if self._is_comment_line(line, file_ext):
                        continue

                    processed_line = line
                    if file_ext == ".md":
                        processed_line = self._remove_markdown_comment(line)

                    for keyword in self.keywords:
                        counts[keyword] += processed_line.count(keyword)
        except (OSError, IOError, PermissionError):
            pass

        return counts
