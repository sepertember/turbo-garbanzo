from pathlib import Path
from typing import Dict, Any, List, Tuple

from utils.file_utils import copy_file_with_structure


def load_backup_rules(rules_path: Path) -> Dict[str, bool]:
    from utils.file_utils import safe_read_json
    
    rules = safe_read_json(rules_path)
    
    if rules is None:
        print(f"Warning: No rules file found at {rules_path}, no files will be backed up.")
        return {}
    
    return rules


def should_backup_file(file_path: Path, rules: Dict[str, bool]) -> bool:
    file_extension = file_path.suffix.lower()
    
    return rules.get(file_extension, False)


def backup_files(
    files_data: List[Dict[str, Any]],
    output_dir: Path,
    rules: Dict[str, bool]
) -> List[Dict[str, Any]]:
    results = []
    
    for file_info in files_data:
        file_path = file_info['file_path']
        relative_path = file_info['relative_path']
        
        should_backup = should_backup_file(file_path, rules)
        
        result = {
            'path': str(relative_path),
            'hash': file_info['hash'],
            'size': file_info['size'],
            'modified_time': file_info['modified_time'],
            'backed_up': False
        }
        
        if should_backup:
            success = copy_file_with_structure(file_path, output_dir, relative_path)
            result['backed_up'] = success
            
            if success:
                print(f"Backed up: {relative_path}")
            else:
                print(f"Failed to backup: {relative_path}")
        
        results.append(result)
    
    return results