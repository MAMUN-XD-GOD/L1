class BridgeSyncMonitor:
    def sync_ok(self, bt, kt): return abs(bt-kt)<=0.3
