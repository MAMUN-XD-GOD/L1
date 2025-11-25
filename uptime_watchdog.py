import time
class Watchdog:
    def __init__(self): self.last_ping=time.time()
    def update(self): self.last_ping=time.time()
    def check(self): return 'RESTART' if time.time()-self.last_ping>3 else 'OK'
