import asyncio
from collections import defaultdict
from typing import Callable, Dict, List, Any

class EventBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self.queue = asyncio.Queue()

    def subscribe(self, event_name: str, callback: Callable):
        self.subscribers[event_name].append(callback)

    async def publish(self, event_name: str, data: Any):
        await self.queue.put((event_name, data))

    async def start(self):
        while True:
            event_name, data = await self.queue.get()
            coros = []
            for callback in list(self.subscribers.get(event_name, [])):
                try:
                    # if callback is coroutine function, schedule it
                    c = callback(data)
                    if asyncio.iscoroutine(c):
                        coros.append(c)
                except Exception as e:
                    print(f"[EventBus Error] callback error: {e}")
            if coros:
                await asyncio.gather(*coros, return_exceptions=True)
