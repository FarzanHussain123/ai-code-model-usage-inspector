from app.standards.mapper import map_risks_to_standards

from app.chains.risk_enrichment import build_risk_enrichment_chain

from app.detectors.prompt_risk_detector import assess_prompt_risks

from app.detectors.prompt_extractor import extract_prompts

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
        return {
            "models": [],
            "prompts": []
        }

    # 2. Static model detection
    static_results = []

    for file in code_files:
        static_results.extend(
            detect_models_from_code(
                file_path=file["file_path"],
                content=file["content"]
            )
        )

    # 3. Prompt extraction (ALWAYS runs)
    all_prompts = []

    for file in code_files:
        all_prompts.extend(
            extract_prompts(
                file_path=file["file_path"],
                content=file["content"]
            )
        )

    # 4. Try LangChain enrichment (OPTIONAL, MODELS ONLY)
    enriched_models = static_results

    static_payload = {
        "models": [m.dict() for m in static_results]
    }

    try:
        enrichment_chain = build_model_enrichment_chain()
        enriched = enrichment_chain.invoke({
            "detections": json.dumps(static_payload, indent=2)
        })

        # If enrichment succeeds, use enriched models
        enriched_models = enriched.models

    except Exception:
        # If enrichment fails, fall back silently
        pass

    # 5. Prompt risk detection
    prompt_risks = assess_prompt_risks(all_prompts)

    # 8. LangChain risk enrichment (OPTIONAL)
    enriched_risks = prompt_risks

    if prompt_risks:
        try:
            enrichment_chain = build_risk_enrichment_chain()
            risk_payload = [
                {
                    "file": r["file"],
                    "original_risk": r["risk"],
                    "severity": r["severity"]
                }
                for r in prompt_risks
            ]

            enriched = enrichment_chain.invoke({
                "risks": json.dumps(risk_payload, indent=2)
            })

            enriched_risks = enriched.risks
        except Exception as e:
            print("Risk enrichment failed:", e)


    # 6. Final unified return (IMPORTANT)
    standards_report = map_risks_to_standards(enriched_risks)

    return {
        "models": enriched_models,
        "prompts": all_prompts,
        "prompt_risks": prompt_risks,
        "enriched_risks": enriched_risks,
        "standards_mapping": standards_report
    }