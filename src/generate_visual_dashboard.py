"""
Voynich_Project: HTML/CSS Visualization Matrix Dashboard Compiler
Generates an interactive dashboard from TokenToSiglaBridge mapping results.
"""

import json
from token_to_sigla import TokenToSiglaBridge

def compile_dashboard():
    # Initialize the mapping engine and run a comprehensive test batch
    engine = TokenToSiglaBridge()
    test_tokens = [
        "p_cross", "p_curl", "p_loop", 
        "q_tittle", "q_barmacron", "q_slash",
        "macron_suspension", "tittle_contraction", "omega_form",
        "est_sigla", "cross_et", "ser_loop", "unknown_token"
    ]
    results = engine.process_pipeline(test_tokens)

    # HTML and CSS Template for the Matrix Dashboard
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FVSM Voynich Manuscript - Shorthand Matrix Dashboard</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #0f172a;
            color: #f8fafc;
            margin: 0;
            padding: 40px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        header {{
            border-bottom: 1px solid #334155;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        h1 {{
            font-size: 24px;
            color: #38bdf8;
            margin: 0 0 10px 0;
        }}
        p.subtitle {{
            color: #94a3b8;
            margin: 0;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 20px;
        }}
        .card {{
            background-color: #1e293b;
            border: 1px solid #334155;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}
        .token-title {{
            font-size: 18px;
            font-weight: 600;
            color: #f1f5f9;
            margin-bottom: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .badge {{
            font-size: 10px;
            padding: 4px 8px;
            border-radius: 4px;
            background-color: #0369a1;
            color: #e0f2fe;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .badge.unmapped {{
            background-color: #475569;
        }}
        .metric-row {{
            display: flex;
            justify-content: space-between;
            margin: 8px 0;
            font-size: 14px;
            color: #cbd5e1;
        }}
        .metric-value {{
            font-weight: 500;
            color: #38bdf8;
        }}
        .progress-bar-bg {{
            background: #334155;
            border-radius: 4px;
            height: 8px;
            width: 100%;
            margin-top: 12px;
            overflow: hidden;
        }}
        .progress-bar-fill {{
            height: 100%;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Fixed Vector Shorthand Model (FVSM)</h1>
            <p class="subtitle">Paleographic Token-to-Sigla Compliance Matrix Dashboard</p>
        </header>
        <div class="grid">
"""

    for item in results:
        score_pct = int(item["compliance_score"] * 100)
        badge_class = "unmapped" if item["sigla_type"] == "unmapped" else ""
        fill_color = "#ef4444" if item["compliance_score"] == 0.0 else "#10b981"
        
        html_content += f"""
            <div class="card">
                <div class="token-title">
                    <code>{item["token"]}</code>
                    <span class="badge {badge_class}">{item["sigla_type"]}</span>
                </div>
                <div class="metric-row">
                    <span>Matched Expansion:</span>
                    <span class="metric-value">{item["matched_sigla"]}</span>
                </div>
                <div class="metric-row">
                    <span>Compliance Score:</span>
                    <span class="metric-value">{item["compliance_score"]:.2f}</span>
                </div>
                <div class="metric-row">
                    <span>Monte Carlo Margin:</span>
                    <span class="metric-value">{item["monte_carlo_isolation_margin"]}</span>
                </div>
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill" style="width: {score_pct}%; background-color: {fill_color};"></div>
                </div>
            </div>
"""

    html_content += """
        </div>
    </div>
</body>
</html>
"""

    output_filename = "fvsm_matrix_dashboard.html"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"Dashboard compiled successfully! Output saved to: {output_filename}")

if __name__ == "__main__":
    compile_dashboard()
