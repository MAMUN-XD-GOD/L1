import sqlite3, os

DB='quantumapex_core.db'

def init_db():
    os.makedirs('data', exist_ok=True)
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS candles (id INTEGER PRIMARY KEY, pair TEXT, ts INTEGER, open REAL, high REAL, low REAL, close REAL, volume REAL)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS signals (id INTEGER PRIMARY KEY, pair TEXT, direction TEXT, confidence REAL, reasons TEXT, entry_ts INTEGER, result TEXT, resolved_ts INTEGER)''')
    conn.commit(); conn.close()

def insert_candle(pair, c):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('INSERT INTO candles(pair,ts,open,high,low,close,volume) VALUES(?,?,?,?,?,?,?)', (pair, int(c['ts']), float(c['open']), float(c['high']), float(c['low']), float(c['close']), float(c.get('volume',0))))
    conn.commit(); conn.close()
