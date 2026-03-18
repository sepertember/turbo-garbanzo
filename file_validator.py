import os
from constants import SCAN_EXTENSIONS, MIN_FILE_SIZE_BYTES, EXCLUDED_FILENAME


class FileValidator:
    @staticmethod
    def has_valid_extension(file_path: str) -> bool:
        return file_path.endswith(SCAN_EXTENSIONS)

    @staticmethod
    def is_large_enough(file_path: str) -> bool:
        try:
            return os.path.getsize(file_path) >= MIN_FILE_SIZE_BYTES
        except (OSError, IOError):
            return False

    @staticmethod
    def is_not_excluded(file_path: str) -> bool:
        filename = os.path.basename(file_path)
        return filename != EXCLUDED_FILENAME

    @staticmethod
    def is_readable(file_path: str) -> bool:
        return os.access(file_path, os.R_OK)

    @staticmethod
    def validate_file(file_path: str) -> bool:
        if not FileValidator.is_not_excluded(file_path):
            return False
        if not FileValidator.has_valid_extension(file_path):
            return False
        if not FileValidator.is_large_enough(file_path):
            return False
        if not FileValidator.is_readable(file_path):
            return False
        return True
