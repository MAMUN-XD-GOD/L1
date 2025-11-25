from typing import Dict, Any
from core.event_bus import EventBus

class CandleRouter:
    def __init__(self, event_bus: EventBus):
        self.bus = event_bus
        self.subscriptions = {}  # symbol_timeframe -> [callbacks]

    def register(self, symbol: str, timeframe: str, callback):
        key = f"{symbol}_{timeframe}"
        if key not in self.subscriptions:
            self.subscriptions[key] = []
        self.subscriptions[key].append(callback)

    async def dispatch(self, candle: Dict[str, Any]):
        """Dispatch incoming candle to registered callbacks and publish global event."""
        key = f"{candle.get('symbol')}_{candle.get('tf')}"
        if key in self.subscriptions:
            for cb in list(self.subscriptions[key]):
                try:
                    r = cb(candle)
                    if hasattr(r, '__await__'):
                        await r
                except Exception as e:
                    print(f"[CandleRouter] callback error: {e}")
        # publish global event too (non-blocking)
        await self.bus.publish("CANDLE_ALL", candle)
