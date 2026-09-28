import json
import os
from collections import defaultdict, Counter
import difflib

def run_advanced_suite():
    report_path = "outputs/corpus_audit_report.json"
    corpus_path = "data/full_manuscript_transcription.txt"
    lexicon_path = "data/fvsm_master_lexicon.json"

    if not os.path.exists(report_path) or not os.path.exists(corpus_path):
        print("[ERROR] Required audit report or corpus file missing.")
        return

    with open(report_path, 'r', encoding='utf-8') as f:
        records = json.load(f)

    with open(lexicon_path, 'r', encoding='utf-8') as f:
        lexicon_data = json.load(f)
        mapped_stems = list(lexicon_data.get("mapped_stems", {}).keys())

    os.makedirs("outputs", exist_ok=True)

    # --- Feature 1: Co-Occurrence Analysis ---
    print("--- Running Co-Occurrence Analysis ---")
    pair_counter = Counter()
    with open(corpus_path, 'r', encoding='utf-8') as f:
        for line in f:
            tokens = [t.strip("[].,").upper() for t in line.split() if not t.startswith("[")]
            tokens = [t for t in tokens if t in mapped_stems]
            for i in range(len(tokens) - 1):
                pair = (tokens[i], tokens[i+1])
                pair_counter[pair] += 1

    co_occurrence_output = "outputs/token_co_occurrence.json"
    co_occur_data = [{"token_a": p[0], "token_b": p[1], "frequency": count} for p, count in pair_counter.most_common(10)]
    with open(co_occurrence_output, 'w', encoding='utf-8') as f:
        json.dump(co_occur_data, f, indent=4)
    print(f"[SUCCESS] Co-occurrence report saved to {co_occurrence_output}")

    # --- Feature 2: Fuzzy-Matching Variant Clusterer ---
    print("\n--- Running Fuzzy-Matching Variant Clusterer ---")
    clusters = defaultdict(list)
    processed = set()
    for token in mapped_stems:
        if token in processed:
            continue
        similar = [s for s in mapped_stems if difflib.SequenceMatcher(None, token, s).ratio() >= 0.6]
        cluster_name = f"Cluster_{token}"
        for s in similar:
            clusters[cluster_name].append(s)
            processed.add(s)

    cluster_output = "outputs/lexicon_clusters.json"
    with open(cluster_output, 'w', encoding='utf-8') as f:
        json.dump(clusters, f, indent=4)
    print(f"[SUCCESS] Generated {len(clusters)} variant clusters, saved to {cluster_output}")

    # --- Feature 3: Executive Summary Report Generation ---
    print("\n--- Generating Executive Summary Report ---")
    summary_path = "outputs/executive_research_summary.txt"
    
    total_records = len(records)
    unique_tokens = len(set(r["token"] for r in records))
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("=========================================\n")
        f.write("  VOYNICH MANUSCRIPT RESEARCH PIPELINE\n")
        f.write("  Executive Summary Report\n")
        f.write("=========================================\n\n")
        f.write(f"Total Corpus Audit Records: {total_records}\n")
        f.write(f"Unique Mapped Tokens Identified: {unique_tokens}\n\n")
        f.write("Top Co-Occurring Token Pairs:\n")
        for item in co_occur_data[:5]:
            f.write(f"  - {item['token_a']} -> {item['token_b']} (Count: {item['frequency']})\n")
        f.write("\nPipeline Status: Fully Operational & Integrated.\n")

    print(f"[SUCCESS] Executive summary saved to {summary_path}")

if __name__ == "__main__":
    run_advanced_suite()
