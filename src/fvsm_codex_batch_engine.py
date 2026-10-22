"""
Voynich_Project: Master FVSM Codex Engine with Suffix Expansion & N-Gram Analyzer
Performs paleographic abbreviation expansion, confidence scoring, thematic profiling,
bigram/trigram frequency analysis, and HTML dashboard export.
"""

from typing import List, Dict, Any
from collections import Counter
import html

class MasterVoynichCodexEngine:
    def __init__(self, token_dictionary: Dict[str, Dict[str, Any]]):
        self.lexicon = token_dictionary
        self.semantic_categories = {
            "operational": ["per", "pro", "ser"],
            "logical_conditional": ["aut", "sed", "que", "quam"],
            "substance_association": ["cum", "et", "est", "um", "us", "non"]
        }

    def decipher_token_stream(self, chronological_tokens: List[str]) -> Dict[str, Any]:
        """Translates tokens, handles suffix extensions, and calculates confidence."""
        translated_words = []
        resolved_count = 0
        total_tokens = len(chronological_tokens)
        
        for token in chronological_tokens:
            if token in self.lexicon:
                entry = self.lexicon[token]
                expansion = entry["expansion"]
                
                # Check for medieval suffix expansion rules (e.g., nasal bars/macrons)
                if "suffix_variants" in entry and entry.get("apply_suffix"):
                    expansion += entry["suffix_variants"][0]  # Apply primary probable suffix
                    
                translated_words.append(expansion)
                
                if entry.get("ambiguous", False):
                    resolved_count += 0.5
                else:
                    resolved_count += 1.0
            else:
                translated_words.append(f"[{token}]")
                
        confidence_score = (resolved_count / total_tokens) * 100 if total_tokens > 0 else 0.0
        return {
            "translation": " ".join(translated_words),
            "words": translated_words,
            "confidence": round(confidence_score, 1)
        }

    def analyze_ngram_frequencies(self, all_words: List[str]) -> Dict[str, List[tuple]]:
        """Calculates bi-gram and tri-gram frequencies across the translated corpus."""
        bigrams = [f"{all_words[i]} {all_words[i+1]}" for i in range(len(all_words) - 1)]
        trigrams = [f"{all_words[i]} {all_words[i+1]} {all_words[i+2]}" for i in range(len(all_words) - 2)]
        
        return {
            "top_bigrams": Counter(bigrams).most_common(3),
            "top_trigrams": Counter(trigrams).most_common(3)
        }

    def analyze_folio_themes(self, translated_words: List[str]) -> Dict[str, int]:
        """Tallies thematic category matches for semantic profiling."""
        tag_counts = {"operational": 0, "logical_conditional": 0, "substance_association": 0}
        for word in translated_words:
            for category, keywords in self.semantic_categories.items():
                if word in keywords or any(word.startswith(kw) for kw in keywords):
                    tag_counts[category] += 1
        return tag_counts

    def process_codex(self, codex_folios: Dict[str, List[List[str]]]) -> Dict[str, Any]:
        """Processes all codex folios, compiling transcripts, confidence, and n-grams."""
        codex_report = {}
        global_word_stream = []
        
        print("📚 Initiating Advanced FVSM Codex Pipeline (Suffixes & N-Grams)...")
        for folio_id, text_rows in codex_folios.items():
            print(f"   -> Processing {folio_id} ({len(text_rows)} rows detected)...")
            folio_output = []
            all_folio_words = []
            total_confidence = 0.0
            
            for row_idx, row_tokens in enumerate(text_rows):
                result = self.decipher_token_stream(row_tokens)
                folio_output.append({
                    "row": row_idx + 1,
                    "text": result["translation"],
                    "confidence": result["confidence"]
                })
                all_folio_words.extend(result["words"])
                global_word_stream.extend(result["words"])
                total_confidence += result["confidence"]
                
            avg_confidence = round(total_confidence / len(text_rows), 1) if text_rows else 0.0
            themes = self.analyze_folio_themes(all_folio_words)
            
            codex_report[folio_id] = {
                "rows": folio_output,
                "avg_confidence": avg_confidence,
                "themes": themes
            }
            
        # Global Corpus N-Gram Analysis
        corpus_ngrams = self.analyze_ngram_frequencies(global_word_stream)
        codex_report["corpus_analytics"] = corpus_ngrams
            
        print("✅ Advanced FVSM Pipeline Execution Completed Successfully.")
        return codex_report

    def export_html_dashboard(self, master_report: Dict[str, Any], filename: str = "fvsm_codex_master_dashboard.html"):
        """Compiles analytics, n-grams, and transcripts into an interactive HTML dashboard."""
        corpus_data = master_report.pop("corpus_analytics", {"top_bigrams": [], "top_trigrams": []})
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>FVSM Advanced Codex Visualization Dashboard</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 40px; }}
        .container {{ max-width: 1000px; margin: 0 auto; }}
        h1 {{ color: #38bdf8; border-bottom: 2px solid #334155; padding-bottom: 15px; }}
        .analytics-box {{ background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 20px; margin-bottom: 25px; }}
        .folio-card {{ background: #1e293b; border-radius: 12px; padding: 25px; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); border: 1px solid #334155; }}
        .folio-header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 10px; margin-bottom: 15px; }}
        .folio-title {{ font-size: 1.25rem; font-weight: bold; color: #e2e8f0; }}
        .badge {{ background: #0284c7; color: white; padding: 4px 10px; border-radius: 20px; font-size: 0.85rem; }}
        .row-item {{ margin: 8px 0; font-family: monospace; background: #0f172a; padding: 10px 14px; border-radius: 6px; display: flex; justify-content: space-between; }}
        .themes {{ margin-top: 15px; font-size: 0.9rem; color: #94a3b8; display: flex; gap: 20px; }}
        .theme-tag {{ background: #334155; padding: 4px 8px; border-radius: 4px; color: #e2e8f0; }}
        .ngram-list {{ display: flex; gap: 15px; flex-wrap: wrap; margin-top: 10px; }}
        .ngram-pill {{ background: #0284c7; padding: 6px 12px; border-radius: 6px; font-family: monospace; font-size: 0.9rem; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔮 FVSM Advanced Codex Reconstruction & Analytics</h1>
        <p>14th-Century Latin Shorthand with Automated Suffix Expansion & N-Gram Profiling</p>
        
        <div class="analytics-box">
            <h3 style="margin-top: 0; color: #38bdf8;">📊 Corpus Syntax Frequency (Top Bi-grams)</h3>
            <div class="ngram-list">
"""
        for bg, count in corpus_data["top_bigrams"]:
            html_content += f'<div class="ngram-pill">{html.escape(bg)} ({count})</div>'
            
        html_content += """            </div>
        </div>
"""
        
        for folio_id, data in master_report.items():
            html_content += f"""
        <div class="folio-card">
            <div class="folio-header">
                <div class="folio-title">📖 Folio Target: {folio_id.upper()}</div>
                <div class="badge">Confidence: {data['avg_confidence']}%</div>
            </div>
            <div class="rows-container">
"""
            for r in data["rows"]:
                html_content += f"""                <div class="row-item"><span>Row {r['row']}: {html.escape(r['text'])}</span><span style="color: #38bdf8;">{r['confidence']}% Conf.</span></div>\n"""
            
            t = data["themes"]
            html_content += f"""            </div>
            <div class="themes">
                <span class="theme-tag">Operational: {t['operational']}</span>
                <span class="theme-tag">Logical: {t['logical_conditional']}</span>
                <span class="theme-tag">Substance: {t['substance_association']}</span>
            </div>
        </div>
"""

        html_content += """
    </div>
</body>
</html>
"""
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"✨ Advanced Interactive HTML Dashboard Exported to: {filename}")

# Master Workbench Execution
if __name__ == "__main__":
    active_lexicon = {
        "p_cross": {"expansion": "per", "ambiguous": False, "apply_suffix": True, "suffix_variants": ["ibus"]},
        "p_curl": {"expansion": "pro", "ambiguous": False, "apply_suffix": False},
        "q_tittle": {"expansion": "que", "ambiguous": True, "apply_suffix": False},
        "q_barmacron": {"expansion": "quam", "ambiguous": False, "apply_suffix": False},
        "macron_suspension": {"expansion": "um", "ambiguous": True, "apply_suffix": False},
        "omega_form": {"expansion": "us", "ambiguous": False, "apply_suffix": False},
        "cross_et": {"expansion": "et", "ambiguous": False, "apply_suffix": False},
        "est_sigla": {"expansion": "est", "ambiguous": False, "apply_suffix": False},
        "ser_loop": {"expansion": "ser", "ambiguous": True, "apply_suffix": True, "suffix_variants": ["orum"]},
        "con_sigla": {"expansion": "cum", "ambiguous": False, "apply_suffix": False},
        "non_tilde": {"expansion": "non", "ambiguous": False, "apply_suffix": False},
        "aut_sigla": {"expansion": "aut", "ambiguous": False, "apply_suffix": False},
        "sed_sigla": {"expansion": "sed", "ambiguous": False, "apply_suffix": False}
    }
    
    codex_corpus_data = {
        "folio_1r": [
            ["p_cross", "macron_suspension", "con_sigla", "non_tilde"],
            ["p_curl", "q_barmacron", "aut_sigla", "sed_sigla"]
        ],
        "folio_1v": [
            ["cross_et", "p_cross", "q_tittle", "omega_form"],
            ["est_sigla", "ser_loop", "q_barmacron"]
        ]
    }
    
    engine = MasterVoynichCodexEngine(token_dictionary=active_lexicon)
    master_report = engine.process_codex(codex_corpus_data)
    engine.export_html_dashboard(master_report)
