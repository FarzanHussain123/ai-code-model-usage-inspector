import pandas as pd


def export_excel_report(report, output_path="ai_governance_report.xlsx"):
    writer = pd.ExcelWriter(output_path, engine="openpyxl")

    # Models
    pd.DataFrame([
        {
            "Model": m.model_name,
            "Provider": m.provider,
            "Framework": m.framework,
            "File": m.file,
            "Confidence": m.confidence
        }
        for m in report["models"]
    ]).to_excel(writer, sheet_name="Models", index=False)

    # Prompts
    pd.DataFrame(report["prompts"]).to_excel(
        writer, sheet_name="Prompts", index=False
    )

    # Prompt Risks
    pd.DataFrame(report["prompt_risks"]).to_excel(
        writer, sheet_name="Prompt_Risks", index=False
    )

    # Enriched Risks
    pd.DataFrame([
        r.model_dump()
        for r in report["enriched_risks"]
    ]).to_excel(writer, sheet_name="Enriched_Risks", index=False)

    # Standards Mapping
    pd.DataFrame(report["standards_mapping"]).to_excel(
        writer, sheet_name="Standards_Mapping", index=False
    )

    writer.close()
