import time
import numpy as np
from vectorized_engine import VectorizedVoynichEngine

def run_benchmark():
    # Generate a massive synthetic token stream simulating a full manuscript scan (100,000 tokens)
    vocabulary = [
        "p_cross", "p_curl", "p_loop", "q_tittle", 
        "q_barmacron", "q_slash", "macron_suspension", "tittle_contraction", 
        "omega_form", "est_sigla", "cross_et", "ser_loop", "unknown_noise"
    ]
    large_token_stream = list(np.random.choice(vocabulary, size=100000))

    engine = VectorizedVoynichEngine()

    # Benchmark Legacy Iterative Dictionary Approach
    start_legacy = time.time()
    legacy_results = []
    for t in large_token_stream:
        idx = engine.token_registry.index(t) if t in engine.token_registry else 0
        legacy_results.append(engine.compliance_scores[idx])
    legacy_duration = time.time() - start_legacy

    # Benchmark New Vectorized NumPy Approach
    start_vector = time.time()
    vector_results = engine.vectorize_token_stream(large_token_stream)
    vector_duration = time.time() - start_vector

    print("=" * 60)
    print("⚡ VOYNICH ENGINE PERFORMANCE BENCHMARK (100,000 Tokens)")
    print("-" * 60)
    print(f" Legacy Iterative Loop Duration : {legacy_duration:.4f} seconds")
    print(f" Vectorized NumPy Duration      : {vector_duration:.4f} seconds")
    if vector_duration > 0:
        speedup = legacy_duration / vector_duration
        print(f" Performance Speedup Factor     : {speedup:.1f}x FASTER")
    print("=" * 60)

if __name__ == "__main__":
    run_benchmark()
