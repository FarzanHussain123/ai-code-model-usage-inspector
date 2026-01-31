from app.standards.standards_mapping import STANDARDS_MAPPING


def map_risks_to_standards(enriched_risks):
    mapped = []

    for risk in enriched_risks:
        mapping = STANDARDS_MAPPING.get(
            risk.original_risk,
            {}
        )

        mapped.append({
            "file": risk.file,
            "risk": risk.original_risk,
            "severity": risk.severity,
            "likelihood": risk.likelihood,
            "nist": mapping.get("nist", []),
            "eu_ai_act": mapping.get("eu_ai_act", []),
            "cert": mapping.get("cert", [])
        })

    return mapped
