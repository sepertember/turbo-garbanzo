import os
from typing import List
from file_validator import FileValidator


class DirectoryScanner:
    def __init__(self, root_dir: str):
        self.root_dir = root_dir

    def scan_directory(self) -> List[str]:
        valid_files = []
        try:
            for dirpath, _, filenames in os.walk(self.root_dir):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    if FileValidator.validate_file(file_path):
                        valid_files.append(file_path)
        except (OSError, IOError, PermissionError):
            pass
        return valid_files
