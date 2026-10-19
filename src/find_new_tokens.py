import json
import os
import re
from collections import Counter

def find_unmatched_tokens(corpus_path="data/full_manuscript_transcription.txt", lexicon_path="data/fvsm_master_lexicon.json", output_path="outputs/unmatched_candidates.json"):
    if os.path.exists(lexicon_path):
        with open(lexicon_path, 'r', encoding='utf-8') as f:
            lexicon_data = json.load(f)
        mapped_stems = lexicon_data.get("mapped_stems", {})
    else:
        print(f"[ERROR] Lexicon not found at {lexicon_path}")
        return

    if not os.path.exists(corpus_path):
        print(f"[ERROR] Corpus file not found at {corpus_path}")
        return

    unmatched_counter = Counter()
    current_folio = "Unknown Folio"

    print(f"--- Scanning Corpus for Unmatched Candidate Tokens ---")

    with open(corpus_path, 'r', encoding='utf-8') as f:
        for line in f:
            line_str = line.strip()
            if not line_str:
                continue

            # Check for folio headers
            header_match = re.search(r'\[(.*?)\]', line_str)
            if header_match and len(line_str.split()) <= 6:
                header_text = header_match.group(1)
                if "f" in header_text.lower() or "folio" in header_text.lower():
                    current_folio = header_text
                continue

            # Tokenize and check against mapped stems
            tokens = line_str.split()
            for token in tokens:
                clean_token = token.strip("[].,").upper()
                # Filter out standard English words or already mapped stems
                if clean_token and clean_token not in mapped_stems and not clean_token.lower() in ["and", "entry", "one"]:
                    unmatched_counter[clean_token] += 1

    # Format findings into a structured list sorted by frequency
    candidates = [
        {"token": token, "frequency": count} 
        for token, count in unmatched_counter.most_common()
    ]

    os.makedirs("outputs", exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(candidates, f, indent=4)

    print(f"\n[SUCCESS] Found {len(candidates)} unique unmatched candidate tokens.")
    print(f"[SUCCESS] Candidate report saved to {output_path}")
    
    print("\n[Top Unmatched Candidates Discovered]")
    for item in candidates[:10]:
        print(f"  - Token '{item['token']}': appears {item['frequency']} time(s)")

if __name__ == "__main__":
    find_unmatched_tokens()
