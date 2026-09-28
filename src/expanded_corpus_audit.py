import json
import os

def run_expanded_audit(
    corpus_path="data/full_manuscript_transcription.txt",
    lexicon_path="data/fvsm_master_lexicon.json",
    output_report="outputs/expanded_corpus_audit_report.json"
):
    if not os.path.exists(lexicon_path):
        print("[ERROR] Missing lexicon file.")
        return

    with open(lexicon_path, 'r', encoding='utf-8') as f:
        lexicon_data = json.load(f)
        stems = lexicon_data.get("mapped_stems", {})

    # If raw corpus doesn't exist, fall back safely
    if not os.path.exists(corpus_path):
        corpus_path = "outputs/full_manuscript_translation.txt"

    total_lines = 0
    total_tokens = 0
    syntax_collisions = 0
    domain_counts = {}

    with open(corpus_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith("[") or not line.strip():
                continue
            
            total_lines += 1
            tokens = line.split()
            previous_is_syntax = False

            for raw_t in tokens:
                # Skip already formatted tags if reading translation file
                if raw_t.startswith("(") and raw_t.endswith(")"):
                    continue

                total_tokens += 1
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

    compliance_rate = 100.0 if total_tokens == 0 else ((total_tokens - syntax_collisions) / total_tokens) * 100.0

    report = {
        "total_lines_analyzed": total_lines,
        "total_tokens_evaluated": total_tokens,
        "syntax_collisions_found": syntax_collisions,
        "structural_compliance_rate": f"{compliance_rate:.2f}%",
        "domain_distribution": domain_counts
    }

    os.makedirs(os.path.dirname(output_report), exist_ok=True)
    with open(output_report, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=4)

    print(f"\n[SUCCESS] Cleaned Corpus Audit Complete!")
    print(f"Total Lines: {total_lines}")
    print(f"Total Tokens Evaluated: {total_tokens}")
    print(f"Syntax Collisions: {syntax_collisions}")
    print(f"Structural Compliance Score: {compliance_rate:.2f}%")
    print("\nDomain Distribution:")
    for domain, count in domain_counts.items():
        print(f"  - {domain}: {count}")

if __name__ == "__main__":
    run_expanded_audit()
