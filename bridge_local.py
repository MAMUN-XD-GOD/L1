import time, random

class LocalBridge:
    def __init__(self, logger):
        self.logger = logger
    def get_live_price(self, symbol):
        price = round(1.10000 + random.uniform(-0.001, 0.001), 5)
        self.logger.info(f"LocalBridge → Live Price {symbol}: {price}")
        return price
    def get_history(self, symbol, candles=50):
        return [round(1.10000 + random.uniform(-0.005, 0.005),5) for _ in range(candles)]
