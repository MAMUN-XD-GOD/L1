"""Forwarder helper: can be used to forward a JSON payload directly to bridge websocket (for testing)."""
import asyncio, websockets, json

async def forward(ws_url, payload):
    async with websockets.connect(ws_url) as ws:
        await ws.send(json.dumps(payload))
        r = await ws.recv()
        print('bridge resp', r)

if __name__=='__main__':
    import sys, json
    ws = sys.argv[1]
    data = json.loads(sys.argv[2])
    asyncio.run(forward(ws, data))
