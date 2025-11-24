"""HTTP Receiver for Local Bridge
Accepts POST /ingest with JSON payload: {'token':..., 'pair':..., 'candles':[...]} and inserts candles into core DB via core.data_manager.insert_candle
"""
import argparse, asyncio, json
from aiohttp import web
import datetime

async def ingest(request):
    try:
        data = await request.json()
    except Exception as e:
        return web.json_response({'error':'invalid_json'}, status=400)
    cfg = request.app['cfg']
    token = cfg.get('http',{}).get('auth_token')
    if token and data.get('token') != token:
        return web.json_response({'error':'unauthorized'}, status=401)
    pair = data.get('pair')
    candles = data.get('candles', [])
    if not pair or not candles:
        return web.json_response({'error':'missing_fields'}, status=400)
    # Insert candles into core DB
    try:
        from core.data_manager import insert_candle
        for c in candles:
            # normalize timestamp: accept int or iso string
            ts = c.get('ts')
            if isinstance(ts, str):
                # try parse ISO
                import dateutil.parser as dp
                ts = int(dp.parse(ts).timestamp())
                c['ts'] = ts
            insert_candle(pair, c)
    except Exception as e:
        return web.json_response({'error':'db_error','detail':str(e)}, status=500)
    return web.json_response({'status':'ok','received':len(candles)})

async def init_app(cfg_path):
    import json
    with open(cfg_path) as f:
        cfg = json.load(f)
    app = web.Application()
    app['cfg'] = cfg
    app.router.add_post('/ingest', ingest)
    return app

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg','-c', default='examples/local_bridge_config.json')
    args = parser.parse_args()
    app = asyncio.run(init_app(args.cfg))
    web.run_app(app, host='127.0.0.1', port=5000)
