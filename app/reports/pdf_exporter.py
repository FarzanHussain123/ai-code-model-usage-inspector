from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


def export_pdf_report(report, output_path="ai_governance_report.pdf"):
    doc = SimpleDocTemplate(output_path)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph(
        "<b>AI Governance Report</b>", styles["Title"]
    ))
    elements.append(Spacer(1, 20))

    # Summary
    elements.append(Paragraph(
        f"Detected AI Models: {len(report['models'])}", styles["Normal"]
    ))
    elements.append(Paragraph(
        f"Detected Prompt Risks: {len(report['prompt_risks'])}", styles["Normal"]
    ))
    elements.append(Spacer(1, 20))

    # Models Table
    elements.append(Paragraph("<b>Detected AI Models</b>", styles["Heading2"]))

    model_table = [
        ["Model", "Provider", "Framework", "File"]
    ] + [
        [m.model_name, m.provider, m.framework, m.file]
        for m in report["models"]
    ]

    elements.append(Table(model_table, style=[
        ("GRID", (0,0), (-1,-1), 1, colors.black)
    ]))

    elements.append(Spacer(1, 20))

    # Risks
    elements.append(Paragraph("<b>Key Risks</b>", styles["Heading2"]))

    for r in report["enriched_risks"]:
        elements.append(Paragraph(
            f"<b>{r.original_risk}</b> (Severity: {r.severity}, Likelihood: {r.likelihood})",
            styles["Normal"]
        ))
        elements.append(Paragraph(
            f"Explanation: {r.explanation}", styles["Normal"]
        ))
        elements.append(Paragraph(
            f"Recommendation: {r.recommendation}", styles["Normal"]
        ))
        elements.append(Spacer(1, 12))

    doc.build(elements)
