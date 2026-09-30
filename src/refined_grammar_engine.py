import json
import os
from collections import Counter

def evaluate_refined_rules(corpus_path="data/full_manuscript_transcription.txt", lexicon_path="data/fvsm_master_lexicon.json"):
    if not os.path.exists(corpus_path) or not os.path.exists(lexicon_path):
        print("[ERROR] Corpus or lexicon file missing.")
        return

    with open(lexicon_path, "r", encoding="utf-8") as f:
        lexicon_data = json.load(f)
        stems = lexicon_data.get("mapped_stems", {})

    print("\n--- Running Refined Prescriptive Grammar Rule Engine ---")

    token_themes = {}
    for token, details in stems.items():
        defn = details.get("definition", "").lower() if isinstance(details, dict) else str(details).lower()
        if any(k in defn for k in ["binder", "conjunction", "structural binder"]):
            token_themes[token] = "SYNTAX"
        elif any(k in defn for k in ["herba", "plant", "botanical", "root", "radix"]):
            token_themes[token] = "HERBAL"
        elif any(k in defn for k in ["vessel", "fluid", "pharmaceutical", "element", "operational"]):
            token_themes[token] = "PHARMACEUTICAL"
        else:
            token_themes[token] = "MODIFIER"

    total_lines = 0
    compliant_lines = 0
    rule_breakdown = Counter()

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("["):
                continue
            # Skip English annotation/gloss lines
            if any(term in line.lower() for term in ["mixed substance", "matter sign", "foliagenounmorph"]):
                continue
            tokens = [t.strip("[].,").upper() for t in line.split() if not t.startswith("[")]
            if not tokens:
                continue
            
            total_lines += 1
            is_compliant = True
            
            # RULE 1: Mandatory Core Term Check
            line_themes = [token_themes.get(t, "MODIFIER") for t in tokens]
            has_core_term = any(theme in ["HERBAL", "PHARMACEUTICAL"] for theme in line_themes)
            
            if not has_core_term:
                is_compliant = False
                rule_breakdown["Missing Core Anchor Term"] += 1
            
            # RULE 2: Strict Conjunction Clustering Check
            for i in range(len(tokens) - 1):
                t1, t2 = tokens[i], tokens[i+1]
                th1 = token_themes.get(t1, "MODIFIER")
                th2 = token_themes.get(t2, "MODIFIER")
                
                if th1 == "SYNTAX" and th2 == "SYNTAX":
                    is_compliant = False
                    rule_breakdown["Strict Conjunction Clustering Violation"] += 1

            if is_compliant:
                compliant_lines += 1
                rule_breakdown["Fully Compliant Lines"] += 1
            else:
                rule_breakdown["Non-Compliant Lines"] += 1

    compliance_score = (compliant_lines / total_lines) * 100 if total_lines > 0 else 0

    print(f"\n📊 Refined Grammar Evaluation Results:")
    for rule, count in rule_breakdown.items():
        print(f"   - {rule}: {count} lines")

    print(f"\n==================================================")
    print(f" Refined Grammar Compliance Score: {compliance_score:.1f}%")

if __name__ == "__main__":
    evaluate_refined_rules()
