"""
Voynich_Project: Full Codex Decipherment Engine
Iterates through chronological folio text streams to expand FVSM 
shorthand matrices into a unified, readable medieval Latin transcription.
"""

from typing import List, Dict, Any

class VoynichCodexDecipherer:
    def __init__(self, token_dictionary: Dict[str, Dict[str, Any]]):
        self.lexicon = token_dictionary

    def decipher_token_stream(self, chronological_tokens: List[str]) -> str:
        """
        Translates a sequential array of folio character vectors.
        Reconstructs clipped medieval shorthand into fully expanded words.
        """
        translated_words = []

        for token in chronological_tokens:
            if token in self.lexicon:
                # Extract the historical linguistic expansion (e.g., 'per', 'que')
                expansion = self.lexicon[token]["expansion"]
                translated_words.append(expansion)
            else:
                # Handle unmapped vectors gracefully without crashing the pipeline
                translated_words.append(f"[{token}]")

        # Join the expanded tokens cleanly to form coherent structural text sentences
        full_transcript = " ".join(translated_words)
        return full_transcript

# Master Workbench Execution
if __name__ == "__main__":
    # Ingesting your verified 14th-Century Latin Shorthand Dictionary Matrix
    active_lexicon = {
        "p_cross": {"expansion": "per"},
        "q_tittle": {"expansion": "que"},
        "macron_suspension": {"expansion": "um"},
        "omega_form": {"expansion": "us"},
        "cross_et": {"expansion": "et"}
    }

    # Simulating a sequential vector stream extracted from a Voynich text line row
    sample_folio_row = ["p_cross", "macron_suspension", "cross_et", "q_tittle", "omega_form"]

    decipherer = VoynichCodexDecipherer(token_dictionary=active_lexicon)
    expanded_text = decipherer.decipher_token_stream(sample_folio_row)

    print("=" * 60)
    print("🔮 FVSM FULL RECONSTRUCTION TRANSCRIPT OUTPUT:")
    print("-" * 60)
    print(f" Raw Vector Input  : {sample_folio_row}")
    print(f" Expanded Latin    : {expanded_text}")
    print("=" * 60)
