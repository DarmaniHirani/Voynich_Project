"""
Voynich_Project: Master FVSM Codex Engine (Ingestion, Scoring & HTML Export)
Performs multi-folio batch transcription, 14th-century Latin shorthand lexicon mapping,
confidence/ambiguity scoring, thematic semantic profiling, and HTML dashboard export.
"""

from typing import List, Dict, Any
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
        """Translates tokens, tracks ambiguity, and calculates row confidence scores."""
        translated_words = []
        resolved_count = 0
        total_tokens = len(chronological_tokens)
        
        for token in chronological_tokens:
            if token in self.lexicon:
                entry = self.lexicon[token]
                expansion = entry["expansion"]
                translated_words.append(expansion)
                # Check if ambiguity flag exists
                if entry.get("ambiguous", False):
                    resolved_count += 0.5  # Partial weight for ambiguous variants
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

    def analyze_folio_themes(self, translated_words: List[str]) -> Dict[str, int]:
        """Tallies thematic category matches for semantic profiling."""
        tag_counts = {"operational": 0, "logical_conditional": 0, "substance_association": 0}
        for word in translated_words:
            for category, keywords in self.semantic_categories.items():
                if word in keywords:
                    tag_counts[category] += 1
        return tag_counts

    def process_codex(self, codex_folios: Dict[str, List[List[str]]]) -> Dict[str, Any]:
        """Processes all codex folios, compiling transcripts, confidence, and themes."""
        codex_report = {}
        
        print("📚 Initiating Master FVSM Codex Pipeline (Ingestion, Scoring & Export)...")
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
                total_confidence += result["confidence"]
                
            avg_confidence = round(total_confidence / len(text_rows), 1) if text_rows else 0.0
            themes = self.analyze_folio_themes(all_folio_words)
            
            codex_report[folio_id] = {
                "rows": folio_output,
                "avg_confidence": avg_confidence,
                "themes": themes
            }
            
        print("✅ Master FVSM Pipeline Execution Completed Successfully.")
        return codex_report

    def export_html_dashboard(self, master_report: Dict[str, Any], filename: str = "fvsm_codex_master_dashboard.html"):
        """Compiles processed analytics into a fully styled, interactive HTML dashboard."""
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>FVSM Master Codex Visualization Dashboard</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 40px; }}
        .container {{ max-width: 1000px; margin: 0 auto; }}
        h1 {{ color: #38bdf8; border-bottom: 2px solid #334155; padding-bottom: 15px; }}
        .folio-card {{ background: #1e293b; border-radius: 12px; padding: 25px; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); border: 1px solid #334155; }}
        .folio-header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 10px; margin-bottom: 15px; }}
        .folio-title {{ font-size: 1.25rem; font-weight: bold; color: #e2e8f0; }}
        .badge {{ background: #0284c7; color: white; padding: 4px 10px; border-radius: 20px; font-size: 0.85rem; }}
        .row-item {{ margin: 8px 0; font-family: monospace; background: #0f172a; padding: 10px 14px; border-radius: 6px; display: flex; justify-content: space-between; }}
        .themes {{ margin-top: 15px; font-size: 0.9rem; color: #94a3b8; display: flex; gap: 20px; }}
        .theme-tag {{ background: #334155; padding: 4px 8px; border-radius: 4px; color: #e2e8f0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔮 FVSM Master Codex Reconstruction Matrix</h1>
        <p>Automated 14th-Century Latin Paleographic Shorthand Decipherment Report</p>
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
        print(f"✨ Interactive HTML Dashboard Successfully Exported to: {filename}")

# Master Workbench Execution
if __name__ == "__main__":
    # Expanded Lexicon with Ambiguity Tracking Flags
    active_lexicon = {
        "p_cross": {"expansion": "per", "ambiguous": False},
        "p_curl": {"expansion": "pro", "ambiguous": False},
        "q_tittle": {"expansion": "que", "ambiguous": True},
        "q_barmacron": {"expansion": "quam", "ambiguous": False},
        "macron_suspension": {"expansion": "um", "ambiguous": True},
        "omega_form": {"expansion": "us", "ambiguous": False},
        "cross_et": {"expansion": "et", "ambiguous": False},
        "est_sigla": {"expansion": "est", "ambiguous": False},
        "ser_loop": {"expansion": "ser", "ambiguous": True},
        "con_sigla": {"expansion": "cum", "ambiguous": False},
        "non_tilde": {"expansion": "non", "ambiguous": False},
        "aut_sigla": {"expansion": "aut", "ambiguous": False},
        "sed_sigla": {"expansion": "sed", "ambiguous": False}
    }
    
    # Structured Codex Corpus Dataset Stream
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
