from .indicators import Indicators

class StrategyEngine:
    def __init__(self, logger):
        self.ind = Indicators()
        self.logger = logger
    def ema_crossover(self, prices):
        ema9 = self.ind.ema(prices, 9)
        ema21 = self.ind.ema(prices, 21)
        if ema9 is None or ema21 is None:
            return "WAIT"
        if ema9 > ema21:
            return "BUY"
        if ema9 < ema21:
            return "SELL"
        return "WAIT"
