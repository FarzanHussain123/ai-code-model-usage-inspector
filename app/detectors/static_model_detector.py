import re
from typing import List
from app.schemas.report import DetectedModel


OPENAI_MODEL_PATTERN = re.compile(r'model\s*=\s*["\']([^"\']+)["\']')
OPENAI_USAGE_PATTERN = re.compile(r'openai\.ChatCompletion\.create')

HF_MODEL_PATTERN = re.compile(r'AutoModel|pipeline\(')
HF_MODEL_NAME_PATTERN = re.compile(
    r'["\']([a-zA-Z0-9\-_/]+)["\']'
)
LANGCHAIN_PATTERN = re.compile(r'langchain|ChatOpenAI')


def detect_models_from_code(file_path: str, content: str) -> List[DetectedModel]:
    detected = []

    # ---- OpenAI detection ----
    if OPENAI_USAGE_PATTERN.search(content):
        model_match = OPENAI_MODEL_PATTERN.search(content)
        model_name = model_match.group(1) if model_match else "unknown"

        detected.append(
            DetectedModel(
                model_name=model_name,
                provider="OpenAI",
                framework="openai",
                file=file_path,
                confidence=1.0
            )
        )

    # ---- Hugging Face detection ----
    if HF_MODEL_PATTERN.search(content):
        model_match = HF_MODEL_NAME_PATTERN.search(content)
        model_name = model_match.group(1) if model_match else "unknown"

        detected.append(
            DetectedModel(
                model_name=model_name,
                provider="Hugging Face",
                framework="transformers",
                file=file_path,
                confidence=0.9 if model_match else 0.7
            )
        )


    # ---- LangChain detection ----
    if LANGCHAIN_PATTERN.search(content):
        detected.append(
            DetectedModel(
                model_name="unknown",
                provider="Various",
                framework="langchain",
                file=file_path,
                confidence=0.7
            )
        )

    return detected
