class Heartbeat:
    def __init__(self): self.status='OK'
    def ping(self): return {'alive':True,'status':self.status}
