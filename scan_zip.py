import sys
from app.orchestrator import run_model_detection
from app.reports.excel_exporter import export_excel_report
from app.reports.pdf_exporter import export_pdf_report
from app.utils.zip_handler import extract_zip_to_temp, cleanup_temp_dir


def main():
    if len(sys.argv) != 2:
        print("Usage: python scan_zip.py <source_code.zip>")
        exit(2)

    zip_path = sys.argv[1]
    temp_dir = None

    try:
        print(f"[*] Extracting ZIP: {zip_path}")
        temp_dir = extract_zip_to_temp(zip_path)

        print("[*] Running AI Governance Scan...")
        report = run_model_detection(temp_dir)

        print("[*] Exporting reports...")
        export_excel_report(report, "ai_governance_report.xlsx")
        export_pdf_report(report, "ai_governance_report.pdf")

        print("[✓] Reports generated successfully.")

        # CI POLICY: fail on HIGH severity
        high_risks = [
            r for r in report.get("enriched_risks", [])
            if r.severity == "HIGH"
        ]

        if high_risks:
            print("[!] HIGH severity AI risks detected:")
            for r in high_risks:
                print(f"    - {r.original_risk} ({r.file})")
            exit(1)

        print("[✓] No HIGH severity AI risks detected.")
        exit(0)

    finally:
        if temp_dir:
            cleanup_temp_dir(temp_dir)


if __name__ == "__main__":
    main()
