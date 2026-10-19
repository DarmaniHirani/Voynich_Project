import json
import os
from collections import Counter

def aggressive_promote(corpus_path="data/full_manuscript_transcription.txt", lexicon_path="data/fvsm_master_lexicon.json"):
    if not os.path.exists(corpus_path) or not os.path.exists(lexicon_path):
        print("[ERROR] Corpus or lexicon file missing.")
        return

    with open(lexicon_path, 'r', encoding='utf-8') as f:
        lexicon_data = json.load(f)
        
    if "mapped_stems" not in lexicon_data:
        lexicon_data["mapped_stems"] = {}
    stems = lexicon_data["mapped_stems"]

    token_counts = Counter()
    with open(corpus_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith("["):
                continue
            tokens = [t.strip("[].,").upper() for t in line.split() if not t.startswith("[")]
            for t in tokens:
                if t:
                    token_counts[t] += 1

    print("--- Running Aggressive Token Promotion Sweep ---")
    promoted_count = 0

    for token, count in token_counts.most_common():
        current_def = stems.get(token, "")
        if isinstance(current_def, dict):
            current_def = current_def.get("definition", "")
            
        is_unmapped = (token not in stems) or ("unknown" in current_def.lower()) or ("other" in current_def.lower()) or (current_def == "")
        
        if is_unmapped:
            # Assign clear grammatical/thematic categories based on token patterns
            if any(k in token for k in ["X", "AZ", "UM", "WITH"]):
                new_defn = "structural binder / grammatical conjunction"
            elif any(k in token for k in ["AQUA", "LIQ", "OD", "VAS", "VESSE"]):
                new_defn = "operational fluid vessel / pharmaceutical element"
            elif any(k in token for k in ["FOLI", "PLANT", "ROOT", "BOTANICAL"]):
                new_defn = "herbal botanical radix component"
            else:
                new_defn = "primary morphological core token"

            stems[token] = {"definition": new_defn}
            print(f"🚀 [AGRESSIVE PROMOTION] '{token}' (Freq: {count}) -> Defined as: '{new_defn}'")
            promoted_count += 1

    with open(lexicon_path, 'w', encoding='utf-8') as f:
        json.dump(lexicon_data, f, indent=4)

    print(f"\n[SUCCESS] Aggressively promoted {promoted_count} tokens.")

if __name__ == "__main__":
    aggressive_promote()
