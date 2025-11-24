"""DataFeed: reads candles from core DB (core.data_manager DB), keeps per-pair deque buffers and provides resample utilities."""
import sqlite3, time
from collections import defaultdict, deque
import pandas as pd

DB='quantumapex_core.db'

class DataFeed:
    def __init__(self, pairs=None, maxlen=5000):
        self.pairs = pairs or []
        self.buffers = defaultdict(lambda: deque(maxlen=maxlen))
        self._last_id = 0
        self.running = False

    def poll_once(self):
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute('SELECT id,pair,ts,open,high,low,close,volume FROM candles WHERE id>? ORDER BY id ASC', (self._last_id,))
        rows = cur.fetchall()
        for r in rows:
            _id,pair,ts,o,h,l,c,vol = r
            self._last_id = _id
            self.buffers[pair].append({'ts':int(ts),'open':float(o),'high':float(h),'low':float(l),'close':float(c),'volume':float(vol)})
        conn.close()

    def start(self, interval=0.5):
        import threading
        self.running = True
        def loop():
            while self.running:
                try:
                    self.poll_once()
                except Exception:
                    pass
                time.sleep(interval)
        t = threading.Thread(target=loop, daemon=True)
        t.start()

    def stop(self):
        self.running = False

    def get_candles(self, pair, limit=200):
        arr = list(self.buffers.get(pair, []))
        return arr[-limit:]

    def resample(self, pair, rule='1T'):
        arr = self.get_candles(pair, limit=1000)
        if not arr:
            return []
        df = pd.DataFrame(arr)
        df['ts'] = pd.to_datetime(df['ts'], unit='s')
        df.set_index('ts', inplace=True)
        agg = df.resample(rule).agg({'open':'first','high':'max','low':'min','close':'last','volume':'sum'}).dropna()
        out = []
        for idx,row in agg.iterrows():
            out.append({'ts':int(idx.timestamp()),'open':float(row['open']),'high':float(row['high']),'low':float(row['low']),'close':float(row['close']),'volume':float(row['volume'])})
        return out
