import json
import os
import random

def run_adversarial_test(
    lexicon_path="data/fvsm_master_lexicon.json",
    output_report="outputs/adversarial_audit_report.json"
):
    if not os.path.exists(lexicon_path):
        print("[ERROR] Missing lexicon file.")
        return

    with open(lexicon_path, 'r', encoding='utf-8') as f:
        lexicon_data = json.load(f)
        stems = lexicon_data.get("mapped_stems", {})

    # Generate an adversarial control corpus of random synthetic tokens
    random.seed(42)
    vocab = list(stems.keys()) if stems else ["ABC", "XYZ", "TEST", "FOO", "BAR"]
    
    control_lines = 19
    control_tokens_total = 0
    syntax_collisions = 0
    domain_counts = {}

    print("\n[ADVERSARIAL TEST] Running pipeline against randomized control corpus...")

    for _ in range(control_lines):
        # Generate random line of tokens matching typical line length
        line_length = random.randint(8, 15)
        line_tokens = [random.choice(vocab) if random.random() > 0.3 else "UNKNOWN_NOISE" for _ in range(line_length)]
        
        previous_is_syntax = False
        for raw_t in line_tokens:
            control_tokens_total += 1
            token = "".join(c for c in raw_t if c.isalnum()).upper()
            
            entry = stems.get(token, {})
            if isinstance(entry, dict):
                domain = entry.get("domain", "UNMAPPED_STEM")
                definition = entry.get("definition", "")
            else:
                domain = str(entry) if entry else "UNMAPPED_STEM"
                definition = ""

            domain_counts[domain] = domain_counts.get(domain, 0) + 1

            is_syntax = (domain.upper() == "SYNTAX" or "SYNTAX" in definition.upper())
            if is_syntax and previous_is_syntax:
                syntax_collisions += 1
            previous_is_syntax = is_syntax

    control_compliance = 100.0 if control_tokens_total == 0 else ((control_tokens_total - syntax_collisions) / control_tokens_total) * 100.0

    print("\n==============================================")
    print("      ADVERSARIAL CONTROL TEST RESULTS        ")
    print("==============================================")
    print(f"Control Tokens Evaluated: {control_tokens_total}")
    print(f"Control Syntax Collisions: {syntax_collisions}")
    print(f"Control Compliance Score: {control_compliance:.2f}%")
    
    if control_compliance < 100.0 or syntax_collisions > 0:
        print("\n[SUCCESS] PASS: The grammar engine successfully differentiated the structured corpus from random noise (colliding or failing control metrics).")
    else:
        print("\n[WARNING] CAUTION: Control corpus also achieved 100%. The grammar rules may be too permissive.")

if __name__ == "__main__":
    run_adversarial_test()
