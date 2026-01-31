import re
from typing import List, Dict

PROMPT_PATTERNS = [
    re.compile(r'["\']content["\']\s*:\s*["\']([^"\']+)["\']'),
    re.compile(r'prompt\s*=\s*["\']([^"\']+)["\']'),
    re.compile(r'system_prompt\s*=\s*["\']([^"\']+)["\']'),
]


def extract_prompts(file_path: str, content: str) -> List[Dict]:
    prompts = []

    for pattern in PROMPT_PATTERNS:
        for match in pattern.findall(content):
            prompts.append({
                "file": file_path,
                "prompt": match,
                "length": len(match)
            })

    return prompts
