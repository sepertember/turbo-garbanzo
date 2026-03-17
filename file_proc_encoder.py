from config import SUPPORTED_ENCODINGS


def detect_encoding(file_path):
    for encoding in SUPPORTED_ENCODINGS:
        try:
            with open(file_path, "rb") as f:
                content = f.read()
            content.decode(encoding)
            return encoding
        except (UnicodeDecodeError, LookupError):
            continue
    return None


def read_file_with_encoding(file_path):
    encoding = detect_encoding(file_path)
    if encoding is None:
        return None, None
    try:
        with open(file_path, "r", encoding=encoding) as f:
            content = f.read()
        return content, encoding
    except Exception:
        return None, None


def convert_encoding(content, target_encoding="utf-8"):
    if target_encoding.lower() not in SUPPORTED_ENCODINGS:
        raise ValueError(f"Unsupported encoding: {target_encoding}")
    return content.encode(target_encoding).decode(target_encoding)
