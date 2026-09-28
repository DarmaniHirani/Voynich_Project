import json
import os
from collections import Counter

def audit_full_manuscript(corpus_path="data/full_manuscript_transcription.txt", lexicon_path="data/fvsm_master_lexicon.json"):
    if not os.path.exists(corpus_path) or not os.path.exists(lexicon_path):
        print("[ERROR] Corpus or lexicon file missing.")
        return

    with open(lexicon_path, 'r', encoding='utf-8') as f:
        lexicon_data = json.load(f)
        stems = lexicon_data.get("mapped_stems", {})

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
    token_usage_counts = Counter()
    domain_breakdown = Counter()

    print("--- Running Full-Manuscript Diagnostic Audit ---")

    with open(corpus_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            if line.startswith("["):
                continue
            tokens = [t.strip("[].,").upper() for t in line.split() if not t.startswith("[")]
            if not tokens:
                continue
            
            total_lines += 1
            line_is_compliant = True

            for i in range(len(tokens)):
                t = tokens[i]
                token_usage_counts[t] += 1
                theme = token_themes.get(t, "MODIFIER")
                domain_breakdown[theme] += 1

                # Check grammar rule (no back-to-back syntax binders)
                if i < len(tokens) - 1:
                    t1, t2 = tokens[i], tokens[i+1]
                    th1 = token_themes.get(t1, "MODIFIER")
                    th2 = token_themes.get(t2, "MODIFIER")
                    if th1 == "SYNTAX" and th2 == "SYNTAX":
                        line_is_compliant = False

            if line_is_compliant:
                compliant_lines += 1

    compliance_score = (compliant_lines / total_lines) * 100 if total_lines > 0 else 0

    print(f"\n📊 Full-Manuscript Audit Results:")
    print(f"   - Total Lines Evaluated: {total_lines}")
    print(f"   - Fully Compliant Lines: {compliant_lines}")
    print(f"   - Overall Structural Compliance: {compliance_score:.1f}%")
    
    print(f"\n📈 Thematic Token Distribution Across Corpus:")
    for theme, count in domain_breakdown.items():
        print(f"   - {theme}: {count} occurrences")

    print(f"\n🔥 Top 5 Most Frequent Tokens Across Manuscript:")
    for tok, count in token_usage_counts.most_common(5):
        print(f"   - '{tok}': {count} times")

if __name__ == "__main__":
    audit_full_manuscript()
