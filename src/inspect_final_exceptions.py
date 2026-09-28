import json
import os

def inspect_exceptions(corpus_path="data/full_manuscript_transcription.txt", lexicon_path="data/fvsm_master_lexicon.json"):
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
        else:
            token_themes[token] = "MODIFIER"

    print("--- Final Exception Inspector: Non-Compliant Lines ---\n")
    exception_count = 0

    with open(corpus_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            if line.startswith("["):
                continue
            tokens = [t.strip("[].,").upper() for t in line.split() if not t.startswith("[")]
            if not tokens:
                continue
            
            is_compliant = True
            violating_pairs = []
            for i in range(len(tokens) - 1):
                t1, t2 = tokens[i], tokens[i+1]
                th1 = token_themes.get(t1, "MODIFIER")
                th2 = token_themes.get(t2, "MODIFIER")
                if th1 == "SYNTAX" and th2 == "SYNTAX":
                    is_compliant = False
                    violating_pairs.append((t1, t2))

            if not is_compliant:
                exception_count += 1
                print(f"🔍 [EXCEPTION TARGET] Line {line_num}: {' '.join(tokens)}")
                print(f"   Violating Conjunction Pairs: {violating_pairs}")
                print("-" * 60)

    print(f"\n[SUMMARY] Total exception lines inspected: {exception_count}")

if __name__ == "__main__":
    inspect_exceptions()
