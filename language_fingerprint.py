import math
from collections import Counter

def calculate_shannon_entropy(token_string):
    """
    Calculates the Shannon Entropy of the processed text 
    to measure structural predictability and randomness.
    """
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
    """
    Extracts positional frequency distributions for specific 
    target vector primitives (e.g., T, I, R, D, A, O, S, C, F, P).
    """
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

if __name__ == "__main__":
    sample_ledger_output = "TIRDDAOSCFPTIRDDAOSCFPTIR"
    
    print("Executing FVSM Linguistic Tool Kit Boilerplate Verification...")
    entropy_score = calculate_shannon_entropy(sample_ledger_output)
    frequency_map = calculate_token_frequencies(sample_ledger_output)
    
    print(f"Calculated Shannon Entropy Baseline: {entropy_score}")
    print(f"Extracted FVSM Token Frequency Profile (%): {frequency_map}")
