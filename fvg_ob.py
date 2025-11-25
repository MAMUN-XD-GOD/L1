import pandas as pd

def detect_fvg(df):
    # Fair Value Gap detection heuristic
    gaps = []
    for i in range(2, len(df)):
        c1 = df.iloc[i-2]; c2 = df.iloc[i-1]; c3 = df.iloc[i]
        # bullish gap pattern
        if c1['close'] < c1['open'] and c2['close'] < c2['open'] and c3['close'] > c3['open']:
            if c3['open'] > c1['close']:
                gaps.append({'start':int(df.index[i-2].timestamp()), 'end':int(df.index[i].timestamp()), 'dir':'BUY'})
        # bearish gap
        if c1['close'] > c1['open'] and c2['close'] > c2['open'] and c3['close'] < c3['open']:
            if c3['open'] < c1['close']:
                gaps.append({'start':int(df.index[i-2].timestamp()), 'end':int(df.index[i].timestamp()), 'dir':'SELL'})
    return gaps

def detect_order_blocks(df, lookback=20):
    obs = []
    for i in range(lookback, len(df)):
        window = df.iloc[i-lookback:i].copy()
        window['body'] = (window['close'] - window['open']).abs()
        big_idx = window['body'].idxmax()
        if big_idx is not None:
            idx = df.index.get_loc(big_idx)
            top = df.iloc[idx]['high']; bottom = df.iloc[idx]['low']
            obs.append({'ts':int(big_idx.timestamp()), 'high':float(top), 'low':float(bottom)})
    return obs
