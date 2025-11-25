class DataIntegrity:
    def verify(self, feed):
        if feed is None: return False
        if 'price' not in feed: return False
        if feed['price']<=0: return False
        return True
