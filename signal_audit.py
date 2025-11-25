class SignalAudit:
    def audit(self, signal):
        for c in ['pair','direction','strength','timestamp','confidence']:
            if c not in signal: return False
        return True
