import json
import os
from botanical_mapper import BotanicalNomenclatureMapper

def save_botanical_audit(audit_results, filename="outputs/botanical_audit_report.json"):
    """Ensures the outputs directory exists and saves the audit results to JSON."""
    os.makedirs("outputs", exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(audit_results, f, indent=4)
    print(f"[SUCCESS] Full-corpus audit report saved to {filename}")

def run_corpus_audit(input_file="data/manuscript_sample.txt"):
    mapper = BotanicalNomenclatureMapper("data/fvsm_master_lexicon.json")
    matched_records = []
    
    print(f"--- Running Full Corpus Audit on {input_file} ---")
    
    if not os.path.exists(input_file):
        print(f"[ERROR] Input file {input_file} not found.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            tokens = line.strip().split()
            for token in tokens:
                # Clean token of basic punctuation if necessary
                clean_token = token.strip("[].,")
                audit_result = mapper.map_token_to_species(clean_token)
                
                if "[MATCH]" in audit_result:
                    print(f"Line {line_num}: {audit_result}")
                    matched_records.append({
                        "line": line_num,
                        "token": clean_token,
                        "audit_detail": audit_result
                    })
                    
    save_botanical_audit(matched_records)

if __name__ == "__main__":
    run_corpus_audit()
