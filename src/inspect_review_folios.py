import json
import os
from collections import defaultdict

def inspect_review_folios(report_path="outputs/corpus_audit_report.json"):
    if not os.path.exists(report_path):
        print(f"[ERROR] Audit report not found at {report_path}.")
        return

    with open(report_path, 'r', encoding='utf-8') as f:
        records = json.load(f)

    folio_groups = defaultdict(list)
    for record in records:
        folio_groups[record["folio"]].append(record)

    print("--- Review Flag Inspector: Mixed-Domain Analysis ---\n")
    review_count = 0

    for folio, recs in sorted(folio_groups.items()):
        section = recs[0].get("section", "Unknown Section").lower()
        
        match_scores = {"herbal": 0, "astronomical": 0, "pharmaceutical": 0}
        for r in recs:
            defn = r["definition"].lower()
            if any(k in defn for k in ["herba", "plant", "botanical", "root", "leaves", "stem", "foliage"]):
                match_scores["herbal"] += 1
            if any(k in defn for k in ["celestial", "solar", "astronomical", "circle", "degree", "orbit"]):
                match_scores["astronomical"] += 1
            if any(k in defn for k in ["vessel", "fluid", "distilled", "water", "bath", "solvent", "boil", "tincture"]):
                match_scores["pharmaceutical"] += 1

        dominant_theme = max(match_scores, key=match_scores.get)
        is_aligned = False
        
        if "herbal" in section and dominant_theme == "herbal":
            is_aligned = True
        elif "astron" in section and dominant_theme == "astronomical":
            is_aligned = True
        elif ("pharm" in section or "operational" in section) and dominant_theme == "pharmaceutical":
            is_aligned = True

        if not is_aligned:
            review_count += 1
            print(f"🔍 [INSPECTION TARGET] {folio} ({section})")
            print(f"   Scores: {match_scores} -> Dominant: {dominant_theme.upper()}")
            print(f"   Tokens & Mappings Found:")
            for r in recs:
                print(f"     - Token '{r['token']}': {r['definition']}")
            print("-" * 50)

    print(f"\n[SUMMARY] Total folios requiring review inspection: {review_count}")

if __name__ == "__main__":
    inspect_review_folios()
