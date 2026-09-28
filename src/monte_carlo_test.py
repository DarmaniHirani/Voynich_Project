import json
import os
import random

def run_monte_carlo(corpus_path="data/full_manuscript_transcription.txt", lexicon_path="data/fvsm_master_lexicon.json", iterations=1000):
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

    # Read original lines
    corpus_lines = []
    with open(corpus_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith("["):
                continue
            tokens = [t.strip("[].,").upper() for t in line.split() if not t.startswith("[")]
            if tokens:
                corpus_lines.append(tokens)

    print(f"--- Running Monte Carlo Significance Test ({iterations} iterations) ---")
    random_perfect_scores = 0

    for _ in range(iterations):
        all_compliant = True
        for tokens in corpus_lines:
            shuffled = tokens.copy()
            random.shuffle(shuffled)
            for i in range(len(shuffled) - 1):
                t1, t2 = shuffled[i], shuffled[i+1]
                if token_themes.get(t1, "MODIFIER") == "SYNTAX" and token_themes.get(t2, "MODIFIER") == "SYNTAX":
                    all_compliant = False
                    break
            if not all_compliant:
                break
        if all_compliant:
            random_perfect_scores += 1

    p_value = random_perfect_scores / iterations
    print(f"\n📊 Monte Carlo Test Results:")
    print(f"   - Total Simulations: {iterations}")
    print(f"   - Randomly Achieved 100% Compliance: {random_perfect_scores} times")
    print(f"   - Calculated Statistical p-value: {p_value:.5f}")
    if p_value == 0:
        print("   - Significance: p < 0.001 (Extremely High Structural Significance)")

if __name__ == "__main__":
    run_monte_carlo()
