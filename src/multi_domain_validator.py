import json
import os
from collections import defaultdict

def validate_multidomain_consistency(report_path="outputs/corpus_audit_report.json"):
    if not os.path.exists(report_path):
        print(f"[ERROR] Audit report not found at {report_path}.")
        return

    with open(report_path, 'r', encoding='utf-8') as f:
        records = json.load(f)

    folio_groups = defaultdict(list)
    for record in records:
        folio_groups[record["folio"]].append(record)

    print("--- Running Multi-Domain Weighted Folio Validation ---\n")

    total_folios = len(folio_groups)
    valid_folios = 0

    for folio, recs in sorted(folio_groups.items()):
        section = recs[0].get("section", "Unknown Section").lower()
        
        # Accumulate thematic weights
        theme_counts = {"herbal": 0, "astronomical": 0, "pharmaceutical": 0, "syntax": 0}
        total_tokens = len(recs)

        for r in recs:
            defn = r["definition"].lower()
            if any(k in defn for k in ["herba", "plant", "botanical", "root", "leaves", "stem", "foliage"]):
                theme_counts["herbal"] += 1
            if any(k in defn for k in ["celestial", "solar", "astronomical", "circle", "degree", "orbit"]):
                theme_counts["astronomical"] += 1
            if any(k in defn for k in ["vessel", "fluid", "distilled", "water", "bath", "solvent", "boil", "tincture"]):
                theme_counts["pharmaceutical"] += 1
            if any(k in defn for k in ["binder", "conjunction", "structural", "aligned", "index", "scale", "measure"]):
                theme_counts["syntax"] += 1

        # Calculate percentage weights
        theme_weights = {k: (v / total_tokens) * 100 if total_tokens > 0 else 0 for k, v in theme_counts.items()}
        
        # Multi-domain validation logic: A folio is valid if its primary matching theme 
        # accounts for at least 25% of its tokens, or if it shows a valid hybrid blend.
        max_theme = max(theme_weights, key=theme_weights.get)
        max_score = theme_weights[max_theme]

        is_valid = False
        if "herbal" in section and (theme_weights["herbal"] >= 25 or max_theme in ["herbal", "pharmaceutical"]):
            is_valid = True
        elif "astron" in section and (theme_weights["astronomical"] >= 25 or max_theme in ["astronomical", "syntax"]):
            is_valid = True
        elif ("pharm" in section or "operational" in section) and (theme_weights["pharmaceutical"] >= 25 or max_theme in ["pharmaceutical", "herbal"]):
            is_valid = True

        if is_valid:
            valid_folios += 1
            status = "[MULTI-VALIDATED]"
        else:
            status = "[REVIEW NEEDED]"

        print(f"{status} {folio} ({section})")
        formatted_weights = {k: f"{v:.1f}%" for k, v in theme_weights.items() if v > 0}
        print(f"   -> Domain Distribution: {formatted_weights} | Primary: {max_theme.upper()}")

    alignment_percentage = (valid_folios / total_folios) * 100 if total_folios > 0 else 0
    print(f"\n==================================================")
    print(f" Scaled Multi-Domain Alignment: {alignment_percentage:.1f}% ({valid_folios}/{total_folios} Folios)")
    print(f"==================================================")

if __name__ == "__main__":
    validate_multidomain_consistency()
