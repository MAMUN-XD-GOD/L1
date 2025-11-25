def final_rule(pair, ml_prob, tech_score, min_conf=0.55):
    from confidence import combine_confidence
    conf = combine_confidence(ml_prob, tech_score)
    if conf >= min_conf:
        return {'pair':pair, 'decision':'CALL', 'confidence':conf}
    if conf <= (1-min_conf):
        return {'pair':pair, 'decision':'PUT', 'confidence':1-conf}
    return {'pair':pair, 'decision':'HOLD', 'confidence':conf}
