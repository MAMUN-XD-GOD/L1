def combine_confidence(ml_prob, technical_score, weights=(0.6,0.4)):
    tech = (technical_score + 1)/2  # normalize to 0..1
    return weights[0]*ml_prob + weights[1]*tech

def technical_score_from_signals(signals):
    score = 0.0
    for s in signals:
        if s.get('direction')=='BUY': score += s.get('strength',0.5)
        else: score -= s.get('strength',0.5)
    return max(-1,min(1, score))
