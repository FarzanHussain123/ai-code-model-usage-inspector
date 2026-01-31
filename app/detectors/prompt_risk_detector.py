import re
from typing import List, Dict

# ---- High-risk patterns ----
API_KEY_PATTERN = re.compile(
    r'(sk-[a-zA-Z0-9]{20,})'
)

BYPASS_PATTERN = re.compile(
    r'ignore (all|any) (previous|earlier) instructions',
    re.IGNORECASE
)

# ---- Medium-risk patterns ----
INJECTION_PATTERN = re.compile(
    r'(system:|assistant:|user:)',
    re.IGNORECASE
)

# ---- Heuristic thresholds ----
LONG_PROMPT_THRESHOLD = 500


def assess_prompt_risks(prompts: List[Dict]) -> List[Dict]:
    risks = []

    for p in prompts:
        prompt_text = p["prompt"]
        file_path = p["file"]

        # ---- High risk: hardcoded API keys ----
        if API_KEY_PATTERN.search(prompt_text):
            risks.append({
                "file": file_path,
                "prompt": prompt_text,
                "risk": "Hardcoded API key detected",
                "severity": "HIGH"
            })

        # ---- High risk: bypass instructions ----
        if BYPASS_PATTERN.search(prompt_text):
            risks.append({
                "file": file_path,
                "prompt": prompt_text,
                "risk": "Instruction bypass attempt",
                "severity": "HIGH"
            })

        # ---- Medium risk: prompt injection patterns ----
        if INJECTION_PATTERN.search(prompt_text):
            risks.append({
                "file": file_path,
                "prompt": prompt_text,
                "risk": "Possible prompt injection pattern",
                "severity": "MEDIUM"
            })

        # ---- Low risk: excessively long prompts ----
        if len(prompt_text) > LONG_PROMPT_THRESHOLD:
            risks.append({
                "file": file_path,
                "prompt": prompt_text[:200] + "...",
                "risk": "Very long prompt (token risk)",
                "severity": "LOW"
            })

    return risks
