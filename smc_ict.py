import pandas as pd

def detect_bos(ch):
    # ch: DataFrame with columns open,high,low,close indexed by time asc
    # returns list of dicts {type:'BOS'/'CHoCH', ts:..., direction:'BUY'/'SELL'}
    events = []
    highs = ch['high'].tolist(); lows = ch['low'].tolist()
    for i in range(2, len(ch)-1):
        # simple heuristic: higher high than previous two -> bullish BOS
        if highs[i] > highs[i-1] and highs[i-1] > highs[i-2]:
            events.append({'type':'BOS','ts':int(ch.index[i].timestamp()), 'direction':'BUY'})
        if lows[i] < lows[i-1] and lows[i-1] < lows[i-2]:
            events.append({'type':'BOS','ts':int(ch.index[i].timestamp()), 'direction':'SELL'})
    return events
