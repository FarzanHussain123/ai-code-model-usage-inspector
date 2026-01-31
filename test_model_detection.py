from app.orchestrator import run_model_detection
from app.reports.excel_exporter import export_excel_report
from app.reports.pdf_exporter import export_pdf_report


def main():
    repo_path = "samples/test_repo_multi"

    print("[*] Running AI Code & Model Usage Inspector...")
    report = run_model_detection(repo_path)

    print("[*] Exporting Excel report...")
    export_excel_report(report, output_path="ai_governance_report.xlsx")

    print("[*] Exporting PDF report...")
    export_pdf_report(report, output_path="ai_governance_report.pdf")

    print("[✓] Reports generated successfully.")
    print("    - ai_governance_report.xlsx")
    print("    - ai_governance_report.pdf")

    # -------------------------------
    # CI POLICY ENFORCEMENT
    # Fail if ANY HIGH severity risk exists
    # -------------------------------
    high_risks = [
        r for r in report.get("enriched_risks", [])
        if r.severity == "HIGH"
    ]

    if high_risks:
        print("[!] HIGH severity AI risks detected. Failing CI.")
        for r in high_risks:
            print(f"    - {r.original_risk} ({r.file})")
        exit(1)

    print("[✓] No HIGH severity AI risks detected.")
    exit(0)


if __name__ == "__main__":
    main()
