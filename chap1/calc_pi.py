def calculate_pi(n_terms: int) -> float:
    numerater = 4.0
    denominator = 1.0
    operation = 1.0
    pi = 0.0
    for _ in range(n_terms):
        pi += operation * (numerater / denominator)
        operation *= -1.0
        denominator += 2.0
    return pi
