def predict_proba(feat_list):
    # placeholder: return neutral probability if no model present
    try:
        from model_utils import load_model
        m = load_model()
        X = [feat_list]
        p = m.predict_proba(X)[0][1]
        return float(p)
    except Exception:
        return 0.5
