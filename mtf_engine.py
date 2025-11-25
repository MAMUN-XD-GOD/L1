import pandas as pd

def resample_to_tf(df, rule='5T'):
    df2 = df.copy()
    df2.index = pd.to_datetime(df2.index, unit='s')
    agg = df2.resample(rule).agg({'open':'first','high':'max','low':'min','close':'last','volume':'sum'}).dropna()
    agg.index = (agg.index.astype('int64') // 10**9).astype(int)
    return agg

def combine_tf(dict_of_dfs):
    latest = {}
    for k,v in dict_of_dfs.items():
        if len(v):
            latest[k] = v.iloc[-1].to_dict()
    return latest
