import numpy as np
from typing import List, Dict, Any

class VectorizedVoynichEngine:
    def __init__(self, num_quires: int = 20):
        self.token_registry = [
            "unknown_token", "p_cross", "p_curl", "p_loop", "q_tittle", 
            "q_barmacron", "q_slash", "macron_suspension", "tittle_contraction", 
            "omega_form", "est_sigla", "cross_et", "ser_loop"
        ]
        self.num_quires = num_quires
        
        base_scores = np.array([
            0.00, 0.94, 0.89, 0.85, 0.95, 0.91, 0.88, 0.93, 0.90, 0.96, 0.97, 0.98, 0.87
        ], dtype=np.float64)
        
        self.compliance_matrix = np.tile(base_scores[:, np.newaxis], (1, num_quires))
        self.margins_matrix = np.ones((len(self.token_registry), num_quires), dtype=np.float64) * 0.25

    def set_quire_override(self, quire_id: int, token_name: str, compliance_score: float, margin_score: float = None):
        """
        Allows custom fine-tuning of specific tokens for a given quire 
        to reflect unique scribal hands or regional paleographic shifts.
        """
        if token_name in self.token_registry:
            token_idx = self.token_registry.index(token_name)
            if 0 <= quire_id < self.num_quires:
                self.compliance_matrix[token_idx, quire_id] = compliance_score
                if margin_score is not None:
                    self.margins_matrix[token_idx, quire_id] = margin_score

    def vectorize_token_stream(self, raw_tokens: List[str], quire_ids: List[int]) -> Dict[str, np.ndarray]:
        token_indices = np.array([
            self.token_registry.index(t) if t in self.token_registry else 0 
            for t in raw_tokens
        ], dtype=np.int32)
        
        quire_indices = np.array(quire_ids, dtype=np.int32)

        batch_compliance = self.compliance_matrix[token_indices, quire_indices]
        batch_margins = self.margins_matrix[token_indices, quire_indices]

        return {
            "token_ids": token_indices,
            "quire_ids": quire_indices,
            "compliance_scores": batch_compliance,
            "monte_carlo_margins": batch_margins
        }

if __name__ == "__main__":
    simulated_folio_stream = [
        "p_cross", "q_tittle", "macron_suspension", "unknown_vector", 
        "cross_et", "omega_form", "p_curl", "est_sigla"
    ]
    simulated_quire_stream = [1, 1, 8, 8, 1, 8, 1, 8]
    
    engine = VectorizedVoynichEngine(num_quires=20)
    engine.set_quire_override(quire_id=8, token_name="macron_suspension", compliance_score=0.99)
    
    vectorized_results = engine.vectorize_token_stream(simulated_folio_stream, simulated_quire_stream)
    
    print("=" * 65)
    print("🚀 QUIRE-AWARE VECTORIZED NUMPY MATRIX CALCULATIONS COMPLETE:")
    print("-" * 65)
    print(f" Token IDs Array    : {vectorized_results['token_ids']}")
    print(f" Quire IDs Array    : {vectorized_results['quire_ids']}")
    print(f" Compliance Vector  : {vectorized_results['compliance_scores']}")
    print(f" Isolation Margins  : {vectorized_results['monte_carlo_margins']}")
    print("=" * 65)
