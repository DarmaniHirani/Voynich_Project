"""
Unit Test Suite for FVSM Master Codex Engine
Validates shorthand decipherment, confidence scoring, suffix rules, and n-grams.
"""

import unittest
from fvsm_codex_batch_engine import MasterVoynichCodexEngine

class TestFVSMEngine(unittest.TestCase):
    def setUp(self):
        self.lexicon = {
            "p_cross": {"expansion": "per", "ambiguous": False, "apply_suffix": True, "suffix_variants": ["ibus"]},
            "non_tilde": {"expansion": "non", "ambiguous": False, "apply_suffix": False}
        }
        self.engine = MasterVoynichCodexEngine(token_dictionary=self.lexicon)

    def test_decipher_token_stream(self):
        tokens = ["p_cross", "non_tilde"]
        result = self.engine.decipher_token_stream(tokens)
        self.assertEqual(result["translation"], "peribus non")
        self.assertEqual(result["confidence"], 100.0)

    def test_ngram_analysis(self):
        words = ["peribus", "non", "peribus"]
        ngrams = self.engine.analyze_ngram_frequencies(words)
        self.assertTrue(len(ngrams["top_bigrams"]) > 0)

if __name__ == "__main__":
    unittest.main()
