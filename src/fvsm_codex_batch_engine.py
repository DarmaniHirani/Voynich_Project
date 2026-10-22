"""
Voynich_Project: Full Codex Batch Decipherment Engine (Expanded Lexicon)
Processes multiple chronological folio text matrices, applies an expanded 
14th-century Latin shorthand lexicon, and generates a unified codex transcript.
"""

from typing import List, Dict, Any

class VoynichCodexBatchDecipherer:
    def __init__(self, token_dictionary: Dict[str, Dict[str, Any]]):
        self.lexicon = token_dictionary

    def decipher_token_stream(self, chronological_tokens: List[str]) -> str:
        """Translates a sequential array of folio character vectors into expanded Latin."""
        translated_words = []
        for token in chronological_tokens:
            if token in self.lexicon:
                expansion = self.lexicon[token]["expansion"]
                translated_words.append(expansion)
            else:
                translated_words.append(f"[{token}]")
        return " ".join(translated_words)

    def process_entire_codex(self, codex_folios: Dict[str, List[List[str]]]) -> Dict[str, List[str]]:
        """
        Iterates through all folios and text row streams in the manuscript,
        returning a structured mapping of full Latin transcriptions per folio.
        """
        codex_transcripts = {}
        
        print("📚 Initiating Full-Codex Batch Transcription Run (Expanded Lexicon)...")
        for folio_id, text_rows in codex_folios.items():
            print(f"   -> Processing {folio_id} ({len(text_rows)} rows detected)...")
            folio_output = []
            
            for row_idx, row_tokens in enumerate(text_rows):
                expanded_line = self.decipher_token_stream(row_tokens)
                folio_output.append(f"Row {row_idx + 1}: {expanded_line}")
                
            codex_transcripts[folio_id] = folio_output
            
        print("✅ Full-Codex Decipherment Pipeline Completed Successfully.")
        return codex_transcripts

# Master Workbench Execution
if __name__ == "__main__":
    # Expanded 14th-Century Latin Shorthand Dictionary Matrix
    active_lexicon = {
        "p_cross": {"expansion": "per"},
        "p_curl": {"expansion": "pro"},
        "q_tittle": {"expansion": "que"},
        "q_barmacron": {"expansion": "quam"},
        "macron_suspension": {"expansion": "um"},
        "omega_form": {"expansion": "us"},
        "cross_et": {"expansion": "et"},
        "est_sigla": {"expansion": "est"},
        "ser_loop": {"expansion": "ser"},
        # Newly added medieval shorthand tokens:
        "con_sigla": {"expansion": "cum"},
        "non_tilde": {"expansion": "non"},
        "aut_sigla": {"expansion": "aut"},
        "sed_sigla": {"expansion": "sed"}
    }
    
    # Simulating multi-folio extraction streams with new tokens
    mock_codex_data = {
        "folio_1r": [
            ["p_cross", "macron_suspension", "con_sigla", "non_tilde"],
            ["p_curl", "q_barmacron", "aut_sigla", "sed_sigla"]
        ]
    }
    
    decipherer = VoynichCodexBatchDecipherer(token_dictionary=active_lexicon)
    master_transcript = decipherer.process_entire_codex(mock_codex_data)
    
    print("\n" + "=" * 65)
    print("🔮 MASTER CODEX RECONSTRUCTION TRANSCRIPT REPORT:")
    print("=" * 65)
    for folio, lines in master_transcript.items():
        print(f"\n📖 Folio Target: {folio.upper()}")
        print("-" * 43)
        for line in lines:
            print(f"  {line}")
    print("=" * 65)
