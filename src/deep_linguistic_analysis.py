import json
import os
from collections import defaultdict

def run_deep_analysis(
    lexicon_path="data/fvsm_master_lexicon.json",
    corpus_path="outputs/full_manuscript_translation.txt"
):
    if not os.path.exists(lexicon_path) or not os.path.exists(corpus_path):
        print("[ERROR] Required lexicon or translation file missing.")
        return

    with open(lexicon_path, 'r', encoding='utf-8') as f:
        lexicon_data = json.load(f)
        stems = lexicon_data.get("mapped_stems", {})

    # Track domain-to-domain transitions (Markov chain approach)
    transition_matrix = defaultdict(lambda: defaultdict(int))
    prefix_counts = defaultdict(int)
    total_tokens = 0

    with open(corpus_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith("[") or not line.strip():
                continue
            
            tokens = line.split()
            domain_sequence = []

            for raw_t in tokens:
                if raw_t.startswith("(") and raw_t.endswith(")"):
                    continue
                
                total_tokens += 1
                token = "".join(c for c in raw_t if c.isalnum()).upper()
                
                # Extract potential morphological prefix (first 2-3 chars if token is long)
                if len(token) >= 3:
                    prefix = token[:2]
                    prefix_counts[prefix] += 1

                entry = stems.get(token, {})
                if isinstance(entry, dict):
                    domain = entry.get("domain", "UNMAPPED")
                else:
                    domain = str(entry) if entry else "UNMAPPED"
                
                domain_sequence.append(domain)

            # Build transition pairs
            for i in range(len(domain_sequence) - 1):
                current_domain = domain_sequence[i]
                next_domain = domain_sequence[i+1]
                transition_matrix[current_domain][next_domain] += 1

    print("\n==============================================")
    print("      DEEP LINGUISTIC & STRUCTURAL ANALYSIS   ")
    print("==============================================")
    print(f"Total Tokens Analyzed: {total_tokens}")
    
    print("\n--- Top Structural Prefixes Detected ---")
    for pfx, count in sorted(prefix_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  - Prefix '{pfx}': occurs {count} times")

    print("\n--- Key Domain Transitions (Sequential Flow) ---")
    printed_count = 0
    for src, targets in transition_matrix.items():
        for tgt, freq in sorted(targets.items(), key=lambda x: x[1], reverse=True):
            if freq > 1 and printed_count < 10:
                print(f"  [ {src} ]  --->  [ {tgt} ]  ({freq} occurrences)")
                printed_count += 1

    print("\n[SUCCESS] Deep linguistic transition audit completed.")

if __name__ == "__main__":
    run_deep_analysis()
