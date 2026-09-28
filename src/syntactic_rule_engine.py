import json
import os
from collections import defaultdict, Counter

def analyze_syntax_rules(corpus_path="data/full_manuscript_transcription.txt", lexicon_path="data/fvsm_master_lexicon.json"):
    if not os.path.exists(corpus_path) or not os.path.exists(lexicon_path):
        print("[ERROR] Corpus or lexicon file missing.")
        return

    with open(lexicon_path, 'r', encoding='utf-8') as f:
        lexicon_data = json.load(f)
        stems = lexicon_data.get("mapped_stems", {})

    print("--- Running Syntactic Sequencing & Grammar Rule Analysis ---\n")

    # Map token themes for sequence checks (safely handling string vs dict definitions)
    token_themes = {}
    for token, details in stems.items():
        if isinstance(details, dict):
            defn = details.get("definition", "").lower()
        else:
            defn = str(details).lower()

        if any(k in defn for k in ["binder", "conjunction", "structural", "aligned"]):
            token_themes[token] = "SYNTAX"
        elif any(k in defn for k in ["herba", "plant", "botanical", "root", "leaves", "stem"]):
            token_themes[token] = "HERBAL"
        elif any(k in defn for k in ["vessel", "fluid", "distilled", "water", "bath", "solvent", "boil"]):
            token_themes[token] = "PHARMACEUTICAL"
        else:
            token_themes[token] = "OTHER"

    transition_counts = Counter()
    total_transitions = 0

    with open(corpus_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith("["):
                continue
            tokens = [t.strip("[].,").upper() for t in line.split() if not t.startswith("[")]
            for i in range(len(tokens) - 1):
                t1, t2 = tokens[i], tokens[i+1]
                theme1 = token_themes.get(t1, "UNKNOWN")
                theme2 = token_themes.get(t2, "UNKNOWN")
                transition_counts[(theme1, theme2)] += 1
                total_transitions += 1

    print("📊 Positional Transition Probabilities (Grammar Flow):")
    for (th1, th2), count in transition_counts.most_common():
        percentage = (count / total_transitions) * 100 if total_transitions > 0 else 0
        print(f"   {th1} -> {th2}: {count} occurrences ({percentage:.1f}%)")

    # Evaluate strict syntactic rule conformity
    syntax_prefixed_count = sum(count for (th1, th2), count in transition_counts.items() if th1 == "SYNTAX")
    syntax_adherence = (syntax_prefixed_count / total_transitions) * 100 if total_transitions > 0 else 0

    print(f"\n==================================================")
    print(f" Syntactic Order Adherence Score: {syntax_adherence:.1f}%")
    print(f"==================================================")

if __name__ == "__main__":
    analyze_syntax_rules()
