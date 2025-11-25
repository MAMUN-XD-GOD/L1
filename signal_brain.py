import pandas as pd
from smc_ict import detect_bos
from fvg_ob import detect_fvg, detect_order_blocks
from ensemble import predict_proba
from confidence import technical_score_from_signals
from rules_engine import final_rule

class SignalBrain:
    def __init__(self, models=None):
        self.models = models

    def analyze(self, df_1m):
        df = df_1m.copy()
        df.index = pd.to_datetime(df.index, unit='s')
        bos = detect_bos(df)
        fvg = detect_fvg(df)
        obs = detect_order_blocks(df)
        signals = []
        for e in bos[:3]:
            signals.append({'direction':e['direction'],'strength':0.6})
        for g in fvg[:2]:
            signals.append({'direction':g['dir'],'strength':0.4})
        tech_score = technical_score_from_signals(signals)
        feat = [df['close'].iloc[-1], df['close'].iloc[-1]-df['open'].iloc[-1], df['high'].iloc[-1]-df['low'].iloc[-1]]
        ml_prob = predict_proba(feat)
        decision = final_rule('PAIR', ml_prob, tech_score)
        decision['meta'] = {'bos':bos,'fvg':fvg,'obs':obs,'tech_score':tech_score,'ml_prob':ml_prob}
        return decision
