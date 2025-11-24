class Indicators:
    def sma(self, data, period):
        if len(data) < period: return None
        return sum(data[-period:]) / period
    def ema(self, data, period):
        if len(data) < period: return None
        k = 2/(period+1)
        ema = data[-period]
        for price in data[-period+1:]:
            ema = price*k + ema*(1-k)
        return ema
