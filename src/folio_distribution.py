import json
import os
from collections import defaultdict

def generate_folio_report(report_path="outputs/corpus_audit_report.json"):
    if not os.path.exists(report_path):
        print(f"[ERROR] Report not found at {report_path}")
        return

    with open(report_path, 'r', encoding='utf-8') as f:
        records = json.load(f)

    # Dictionary to store counts per folio
    folio_stats = defaultdict(lambda: {"total_matches": 0, "tokens": []})

    for record in records:
        folio = record.get("folio", "Unknown Folio")
        token = record["token"]
        folio_stats[folio]["total_matches"] += 1
        folio_stats[folio]["tokens"].append(token)

    print("--- Folio-by-Folio Distribution Breakdown ---")
    for folio, data in sorted(folio_stats.items()):
        print(f"\n📁 {folio}")
        print(f"   Total Mapped Tokens: {data['total_matches']}")
        print(f"   Tokens Found: {', '.join(set(data['tokens']))}")

if __name__ == "__main__":
    generate_folio_report()
