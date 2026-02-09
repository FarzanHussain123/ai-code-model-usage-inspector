import zipfile
import os
import tempfile
import shutil

ALLOWED_EXTENSIONS = (
    ".py",
    ".ipynb",
    ".js",
    ".ts",
    ".java",
    ".go",
    ".rs",
    ".cpp",
    ".c",
    ".md",
    ".txt"
)

def extract_zip_to_temp(zip_path: str) -> str:
    temp_dir = tempfile.mkdtemp(prefix="ai_scan_")

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        for member in zip_ref.infolist():
            filename = member.filename

            # Skip directories
            if member.is_dir():
                continue

            # Skip long paths & non-code files
            if not filename.lower().endswith(ALLOWED_EXTENSIONS):
                continue

            # Defensive: avoid path traversal
            safe_path = os.path.normpath(filename)
            if ".." in safe_path:
                continue

            target_path = os.path.join(temp_dir, safe_path)
            os.makedirs(os.path.dirname(target_path), exist_ok=True)

            with zip_ref.open(member) as source, open(target_path, "wb") as target:
                target.write(source.read())

    return temp_dir

def cleanup_temp_dir(path: str):
    try:
        shutil.rmtree(path)
    except Exception:
        pass
