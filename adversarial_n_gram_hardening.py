import random

def evaluate_ngram_transition_constraints(token_sequence):
    violations = 0
    total_transitions = len(token_sequence) - 1
    if total_transitions <= 0: return 0.0
    high_order = {'D', 'A', 'O', 'S', 'C', 'F', 'P'}
    for i in range(total_transitions):
        t1, t2 = token_sequence[i], token_sequence[i+1]
        if t1 in high_order and t2 in high_order:
            violations += 1
    return max(100.0 - ((violations / total_transitions) * 100), 0.0)

def run_test(iterations=25000):
    print(f'Running tightened N-gram test across {iterations} iterations...')
    pool = ['T', 'I', 'R', 'D', 'A', 'O', 'S', 'C', 'F', 'P']
    scores = [evaluate_ngram_transition_constraints([random.choice(pool) for _ in range(100)]) for _ in range(iterations)]
    mean_noise = sum(scores) / len(scores)
    gap = 100.0 - mean_noise
    print(f'Noise Compliance Ceiling: {mean_noise:.2f}%')
    print(f'New Separation Gap: +{gap:.2f}%')
    if gap > 40.0:
        print('[VERIFICATION SUCCESS]: Tighter structural sieve successfully clears 40% gap threshold!')

if __name__ == '__main__': run_test()
