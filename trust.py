def calculate_trust_score(is_anomaly: bool) -> int:
    score = 100
    if is_anomaly:
        score -= 40
    return max(score, 0)
