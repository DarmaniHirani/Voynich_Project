import random
import os
from refined_grammar_engine import evaluate_refined_rules

def run_adversarial_test():
    print("\n[ADVERSARIAL TEST] Generating randomized control corpus...")
    os.makedirs("data", exist_ok=True)
    control_path = "data/adversarial_control_corpus.txt"
    
    # Generate random token lines mimicking manuscript structure
    vocab = ["TOKEN_A", "TOKEN_B", "SYNTAX", "HERBAL", "PHARMACEUTICAL", "MODIFIER"]
    with open(control_path, "w", encoding="utf-8") as f:
        for _ in range(100):
            line_len = random.randint(3, 10)
            line_tokens = [random.choice(vocab) for _ in range(line_len)]
            f.write(" ".join(line_tokens) + "\n")
            
    print("[ADVERSARIAL TEST] Running refined rules against control corpus...")
    evaluate_refined_rules(corpus_path=control_path)

if __name__ == "__main__":
    run_adversarial_test()
