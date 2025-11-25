import time
class LatencyChecker:
    def __init__(self): self.bridge_latency=0
    def check_bridge(self): t=time.time(); self.bridge_latency=(time.time()-t)*1000; return self.bridge_latency
