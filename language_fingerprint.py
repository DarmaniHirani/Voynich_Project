import math
from collections import Counter
import matplotlib.pyplot as plt

HISTORICAL_BASELINES = {
    "Medieval_Latin_Shorthand": {
        'T': 12.5, 'I': 9.2, 'R': 8.5, 'D': 6.1, 'A': 10.8,
        'O': 11.5, 'S': 6.8, 'C': 5.2, 'F': 3.4, 'P': 2.9
    },
    "Old_Italian_Control": {
        'T': 10.1, 'I': 11.3, 'R': 7.9, 'D': 5.8, 'A': 13.2,
        'O': 10.9, 'S': 5.1, 'C': 6.4, 'F': 2.1, 'P': 4.2
    }
}

def calculate_shannon_entropy(token_string):
    if not token_string:
        return 0.0
    counts = Counter(token_string)
    total_chars = len(token_string)
    entropy = 0.0
    for count in counts.values():
        probability = count / total_chars
        entropy -= probability * math.log2(probability)
    return round(entropy, 4)

def calculate_token_frequencies(token_string, target_vectors=None):
    if not token_string:
        return {}
    counts = Counter(token_string)
    total_chars = len(token_string)
    if target_vectors is None:
        target_vectors = ['T', 'I', 'R', 'D', 'A', 'O', 'S', 'C', 'F', 'P']
    frequencies = {}
    for vector in target_vectors:
        count = counts.get(vector, 0)
        percentage = (count / total_chars) * 100
        frequencies[vector] = round(percentage, 2)
    return frequencies

def calculate_compliance_score(extracted_frequencies, baseline_profile):
    total_variance = 0.0
    keys = extracted_frequencies.keys()
    for key in keys:
        ext_val = extracted_frequencies.get(key, 0.0)
        base_val = baseline_profile.get(key, 0.0)
        total_variance += abs(ext_val - base_val)
    compliance_percentage = max(0.0, 100.0 - (total_variance / len(keys)))
    return round(compliance_percentage, 2)

def generate_compliance_chart(extracted_frequencies, historical_baselines, output_filename="outputs/compliance_comparison_chart.png"):
    tokens = list(extracted_frequencies.keys())
    ledger_vals = list(extracted_frequencies.values())
    
    plt.figure(figsize=(10, 6))
    plt.plot(tokens, ledger_vals, marker='o', linewidth=2.5, label='FVSM Ledger Output', color='#00d2ff')
    
    colors = {'Medieval_Latin_Shorthand': '#ff9900', 'Old_Italian_Control': '#ff3399'}
    for lang_name, baseline in historical_baselines.items():
        base_vals = [baseline.get(token, 0.0) for token in tokens]
        plt.plot(tokens, base_vals, marker='s', linestyle='--', linewidth=1.5, label=lang_name, color=colors.get(lang_name, '#666666'))
        
    plt.title('FVSM Token Distribution vs. Historical Language Fingerprints', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('FVSM Matrix Mapping Vector', fontsize=12, labelpad=10)
    plt.ylabel('Character Frequency Percentage (%)', fontsize=12, labelpad=10)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='upper right', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_filename, dpi=300)
    plt.close()
    print(f"Compliance chart successfully generated and saved to {output_filename}")

if __name__ == "__main__":
    corpus_file_path = "outputs/fvsm_output.txt"
    print(f"Reading corpus data from {corpus_file_path}...")
    try:
        with open(corpus_file_path, "r", encoding="utf-8") as f:
            ledger_corpus = f.read()
            
        print("Executing FVSM Linguistic Tool Kit Verification...")
        entropy_score = calculate_shannon_entropy(ledger_corpus)
        frequency_map = calculate_token_frequencies(ledger_corpus)
        
        print(f"Calculated Shannon Entropy Baseline: {entropy_score}")
        print(f"Extracted FVSM Token Frequency Profile (%): {frequency_map}")
        
        print("\nRunning Baseline Compliance Checks:")
        for lang_name, baseline in HISTORICAL_BASELINES.items():
            score = calculate_compliance_score(frequency_map, baseline)
            print(f"  -> Compliance with {lang_name}: {score}%")
            
        # Automatically generate and save the visual comparison chart
        generate_compliance_chart(frequency_map, HISTORICAL_BASELINES)
            
    except FileNotFoundError:
        print(f"Error: Could not find file at {corpus_file_path}. Check the path and try again.")
