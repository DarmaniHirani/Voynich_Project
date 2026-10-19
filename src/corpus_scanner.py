import json
import os
import re

def run_lexicon_corpus_scanner(corpus_path="data/full_manuscript_transcription.txt", lexicon_path="data/fvsm_master_lexicon.json", output_path="outputs/corpus_audit_report.json"):
    if os.path.exists(lexicon_path):
        with open(lexicon_path, 'r', encoding='utf-8') as f:
            lexicon_data = json.load(f)
        mapped_stems = lexicon_data.get("mapped_stems", {})
    else:
        print(f"[ERROR] Lexicon not found at {lexicon_path}")
        return

    if not os.path.exists(corpus_path):
        print(f"[ERROR] Corpus file not found at {corpus_path}.")
        return

    os.makedirs("outputs", exist_ok=True)
    audit_records = []

    print(f"--- Scanning Full Corpus with Folio Tracking: {corpus_path} ---")

    current_folio = "Unknown Folio"
    current_section = "Unknown Section"

    with open(corpus_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line_str = line.strip()
            if not line_str:
                continue

            # Check if line is a folio/section header, e.g., [Folio f1r - Herbal] or [f1r]
            header_match = re.search(r'\[(.*?)\]', line_str)
            if header_match and len(line_str.split()) <= 6:
                header_text = header_match.group(1)
                if "f" in header_text.lower() or "folio" in header_text.lower():
                    current_folio = header_text
                if "herbal" in header_text.lower():
                    current_section = "Herbal Section"
                elif "astron" in header_text.lower() or "celestial" in header_text.lower():
                    current_section = "Astronomical Section"
                elif "pharm" in header_text.lower() or "operational" in header_text.lower():
                    current_section = "Pharmaceutical / Operational Section"
                else:
                    current_section = "General / Unspecified Section"
                continue

            # Tokenize line
            tokens = line_str.split()
            for token in tokens:
                clean_token = token.strip("[].,").upper()
                if clean_token in mapped_stems:
                    definition = mapped_stems[clean_token]
                    audit_records.append({
                        "line": line_num,
                        "folio": current_folio,
                        "section": current_section,
                        "token": clean_token,
                        "definition": definition
                    })

    # Save output report
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(audit_records, f, indent=4)
    
    print(f"[SUCCESS] Scan complete. Total matches found: {len(audit_records)}")
    print(f"[SUCCESS] Report saved to {output_path}")

if __name__ == "__main__":
    run_lexicon_corpus_scanner()
