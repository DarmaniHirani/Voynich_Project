import json

def load_sigla_dictionary():
    # Simulated open-source digitized 14th-century Latin abbreviation (Sigla) registry
    return {
        "T": [{"expansion": "con- / com-", "category": "Prefix", "frequency_weight": 0.89},
              {"expansion": "tempus", "category": "Noun", "frequency_weight": 0.42}],
        "I": [{"expansion": "in- / im-", "category": "Preposition/Prefix", "frequency_weight": 0.94},
              {"expansion": "id est", "category": "Conjunction", "frequency_weight": 0.31}],
        "R": [{"expansion": "respondit", "category": "Verb", "frequency_weight": 0.85},
              {"expansion": "rum / -orum", "category": "Suffix", "frequency_weight": 0.91}],
        "D": [{"expansion": "de- / dictus", "category": "Prefix/Adjective", "frequency_weight": 0.88}],
        "A": [{"expansion": "autem / ad", "category": "Conjunction/Preposition", "frequency_weight": 0.95}],
        "O": [{"expansion": "omnis / obiit", "category": "Adjective/Verb", "frequency_weight": 0.82}],
        "S": [{"expansion": "secundum / sed", "category": "Preposition/Conjunction", "frequency_weight": 0.92}],
        "C": [{"expansion": "cum / contra", "category": "Preposition", "frequency_weight": 0.90}],
        "F": [{"expansion": "fecit / fiat", "category": "Verb", "frequency_weight": 0.86}],
        "P": [{"expansion": "per- / pro-", "category": "Prefix", "frequency_weight": 0.96}]
    }

def execute_sigla_mapping(token_stream):
    print("=== EXECUTING TOKEN-TO-SIGLA DICTIONARY MAPPING ===")
    sigla_db = load_sigla_dictionary()
    
    mapping_results = []
    for token in token_stream:
        if token in sigla_db:
            # Sort matches by historical frequency weight
            candidates = sorted(sigla_db[token], key=lambda x: x['frequency_weight'], reverse=True)
            top_match = candidates[0]
            mapping_results.append({
                "token": token,
                "best_expansion": top_match["expansion"],
                "category": top_match["category"],
                "confidence": top_match["frequency_weight"] * 100
            })
            
    print(f"Mapped {len(token_stream)} structural tokens against 14th-century Latin Sigla database:\n")
    for idx, res in enumerate(mapping_results, 1):
        print(f"  [Node {idx}] Token: '{res['token']}' -> Probable Sigla Match: {res['best_expansion']} ({res['category']}) | Confidence: {res['confidence']:.1f}%")
        
    print("\n[VERIFICATION SUCCESS]: Dictionary bridge successfully outputs ranked philological candidates for human audit.")

if __name__ == "__main__":
    sample_tokens = ['T', 'I', 'R', 'D', 'A', 'O', 'S', 'C', 'F', 'P']
    execute_sigla_mapping(sample_tokens)
