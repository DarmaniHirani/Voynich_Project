import json
from fvsm_codex_batch_engine import MasterVoynichCodexEngine

token_lexicon = {
    "cross_et": "et",
    "p_cross": "per",
    "q_titile": "que",
    "omega_form": "m",
    "est_sigla": "est",
    "ser_loop": "ser",
    "q_barmacron": "q",
    "p_curl": "pro",
    "con_sigla": "con",
    "non_tilde": "non"
}

with open("../outputs/expanded_corpus_audit_report.json", "r", encoding="utf-8") as f:
    corpus_data = json.load(f)

engine = MasterVoynichCodexEngine(token_dictionary=token_lexicon)

print("=== Scanning Corpus for Immobile / Zero-Variance Folios ===")

immobile_count = 0
# Handle the corpus structure safely
folios = corpus_data.get("folios", corpus_data)

for folio_name, folio_payload in folios.items():
    try:
        result = engine.process_codex({folio_name: folio_payload})
        for entry in result.get("folio_details", []):
            if entry.get("ambiguity_score", 1.0) == 0.0:
                immobile_count += 1
                print(f"🔒 Immobile Folio Found: {folio_name} -> Row Data: {entry}")
    except Exception as e:
        # Skip non-folio summary keys in the audit report smoothly
        continue

print(f"\nScan complete. Total immobile data points isolated: {immobile_count}")
