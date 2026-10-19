import json
import os
from collections import defaultdict

def validate_semantic_consistency(report_path="outputs/corpus_audit_report.json"):
    if not os.path.exists(report_path):
        print(f"[ERROR] Audit report not found at {report_path}. Run corpus_scanner.py first.")
        return

    with open(report_path, 'r', encoding='utf-8') as f:
        records = json.load(f)

    print("--- Running Semantic & Syntactic Folio Validation ---\n")

    folio_groups = defaultdict(list)
    for record in records:
        folio_groups[record["folio"]].append(record)

    total_folios = len(folio_groups)
    aligned_folios = 0

    for folio, recs in sorted(folio_groups.items()):
        section = recs[0].get("section", "Unknown Section").lower()
        
        # Determine dominant thematic keyword for this section
        match_scores = {"herbal": 0, "astronomical": 0, "pharmaceutical": 0}
        
        for r in recs:
            defn = r["definition"].lower()
            if any(k in defn for k in ["herba", "plant", "botanical", "root", "leaves", "stem", "foliage"]):
                match_scores["herbal"] += 1
            if any(k in defn for k in ["celestial", "solar", "astronomical", "circle", "degree", "orbit"]):
                match_scores["astronomical"] += 1
            if any(k in defn for k in ["vessel", "fluid", "distilled", "water", "bath", "solvent", "boil", "tincture"]):
                match_scores["pharmaceutical"] += 1

        # Check alignment with declared section
        dominant_theme = max(match_scores, key=match_scores.get)
        is_aligned = False
        
        if "herbal" in section and dominant_theme == "herbal":
            is_aligned = True
        elif "astron" in section and dominant_theme == "astronomical":
            is_aligned = True
        elif ("pharm" in section or "operational" in section) and dominant_theme == "pharmaceutical":
            is_aligned = True
        elif sum(match_scores.values()) == 0:
            dominant_theme = "unclassified"
        
        if is_aligned:
            aligned_folios += 1
            status = "[VALIDATED]"
        else:
            status = "[REVIEW NEEDED]"

        print(f"{status} {folio} ({section})")
        print(f"   -> Semantic Scores: {match_scores} | Dominant: {dominant_theme.upper()}")

    alignment_percentage = (aligned_folios / total_folios) * 100 if total_folios > 0 else 0
    print(f"\n=========================================")
    print(f" Corpus Semantic Alignment: {alignment_percentage:.1f}% ({aligned_folios}/{total_folios} Folios)")
    print(f"=========================================")

if __name__ == "__main__":
    validate_semantic_consistency()
