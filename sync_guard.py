import time

class SyncGuard:
    def __init__(self, max_delay_ms=1500):
        self.max_delay = max_delay_ms
        self.last_timestamp = {}  # key -> ts_ms

    def _now_ms(self):
        return int(time.time() * 1000)

    def check(self, symbol: str, tf: str, ts_ms: int) -> bool:
        key = f"{symbol}_{tf}"
        now = self._now_ms()
        # Reject if too old or too far in future
        if abs(now - ts_ms) > self.max_delay:
            return False
        # Prevent duplicate or out-of-order
        last = self.last_timestamp.get(key)
        if last is not None and ts_ms <= last:
            return False
        self.last_timestamp[key] = ts_ms
        return True
