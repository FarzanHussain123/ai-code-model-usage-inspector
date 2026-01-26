from pathlib import Path
from typing import List, Dict

SUPPORTED_EXTENSIONS = {".py", ".js", ".ts"}

MAX_FILE_SIZE_KB = 200  # prevent token explosion


def load_source_code(root_path: str) -> List[Dict[str, str]]:
    root = Path(root_path)
    code_files = []

    for file in root.rglob("*"):
        if (
            file.suffix in SUPPORTED_EXTENSIONS
            and file.is_file()
            and file.stat().st_size <= MAX_FILE_SIZE_KB * 1024
        ):
            try:
                content = file.read_text(encoding="utf-8", errors="ignore")
                code_files.append({
                    "file_path": str(file),
                    "content": content
                })
            except Exception:
                continue

    return code_files
