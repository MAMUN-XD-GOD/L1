import pandas as pd

def ema(series, span):
    return series.ewm(span=span, adjust=False).mean()

def sma(series, period):
    return series.rolling(period).mean()

def atr(df, period=14):
    high_low = df['high'] - df['low']
    high_close = (df['high'] - df['close'].shift()).abs()
    low_close = (df['low'] - df['close'].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(period).mean()
