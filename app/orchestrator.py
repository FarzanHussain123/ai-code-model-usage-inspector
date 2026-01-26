from app.chains.model_enrichment import build_model_enrichment_chain
import json

from app.detectors.static_model_detector import detect_models_from_code

from dotenv import load_dotenv
load_dotenv()

from app.loaders.code_loader import load_source_code
from app.chains.model_detection import build_model_detection_chain




def serialize_codebase(code_files):
    serialized = []

    for file in code_files:
        block = (
            f"FILE_PATH: {file['file_path']}\n"
            f"FILE_TYPE: source_code\n"
            f"{'-' * 40}\n"
            f"{file['content']}\n"
            f"{'-' * 40}"
        )
        serialized.append(block)

    return "\n\n".join(serialized)


def run_model_detection(repo_path: str):
    # 1. Load code
    code_files = load_source_code(repo_path)

    if not code_files:
        return {"models": []}

    # 2. Serialize for LLM
    serialized_code = serialize_codebase(code_files)

    # 3. Static detection (deterministic)
    static_results = []

    for file in code_files:
        static_results.extend(
            detect_models_from_code(
                file_path=file["file_path"],
                content=file["content"]
            )
        )

    # Convert to dict for LLM
    static_payload = {
        "models": [m.dict() for m in static_results]
    }

    # OPTIONAL: LangChain enrichment (best-effort)
    try:
        enrichment_chain = build_model_enrichment_chain()
        enriched = enrichment_chain.invoke({
            "detections": json.dumps(static_payload, indent=2)
        })
        return enriched
    except Exception:
        # Fallback to static results if LLM fails
        return {"models": static_results}