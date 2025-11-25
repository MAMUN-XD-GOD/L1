import pandas as pd
from signal_brain import SignalBrain

if __name__=='__main__':
    df = pd.read_csv('examples/historical_1m.csv')
    df = df.set_index('ts')
    sb = SignalBrain()
    out = sb.analyze(df)
    import json
    print(json.dumps(out, indent=2))
