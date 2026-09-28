import json
import os
import csv

def analyze_and_export_report(report_path="outputs/corpus_audit_report.json", csv_output="outputs/corpus_summary_export.csv"):
    if not os.path.exists(report_path):
        print(f"[ERROR] Report not found at {report_path}")
        return

    with open(report_path, 'r', encoding='utf-8') as f:
        records = json.load(f)

    categories = {
        "Herbal / Botanical": 0,
        "Celestial / Astronomical": 0,
        "Vessels / Operational": 0,
        "Syntax & Structural Binders": 0,
        "Positional & Degree Markers": 0
    }

    print(f"--- Running Advanced Corpus Analysis on {len(records)} Records ---")
    
    categorized_records = []
    for record in records:
        definition = record["definition"].lower()
        cat = "Syntax & Structural Binders"
        
        if any(kw in definition for kw in ["herba", "leaves", "stem", "plant", "botanical", "foliage"]):
            cat = "Herbal / Botanical"
        elif any(kw in definition for kw in ["solar", "celestial", "orbit", "astronomical"]):
            cat = "Celestial / Astronomical"
        elif any(kw in definition for kw in ["vessel", "fluid", "distilled", "water", "bath", "solvent", "boil"]):
            cat = "Vessels / Operational"
        elif any(kw in definition for kw in ["degree", "circle", "position", "aligned", "scale"]):
            cat = "Positional & Degree Markers"
            
        categories[cat] += 1
        
        enriched_record = record.copy()
        enriched_record["category"] = cat
        categorized_records.append(enriched_record)

    print("\n[Refined Thematic Breakdown]")
    for category, count in categories.items():
        print(f"  - {category}: {count} matches")

    os.makedirs("outputs", exist_ok=True)
    with open(csv_output, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["line", "folio", "section", "token", "definition", "category"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in categorized_records:
            writer.writerow(row)
            
    print(f"\n[SUCCESS] Summary export saved to {csv_output}")

if __name__ == "__main__":
    analyze_and_export_report()
