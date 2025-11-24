"""Multi-asset scanner: periodically checks configured assets and runs strategy on latest candles."""
import argparse, time, json
from core.config_loader import Config
from core.logger import get_logger
from data_feed import DataFeed
from core.strategy_engine import StrategyEngine

def run(cfg_path):
    cfg = Config(cfg_path)
    logger = get_logger()
    conf = cfg.settings
    scanner_cfg = conf.get('scanner', {})
    assets = scanner_cfg.get('assets', ['EURUSD'])
    poll = scanner_cfg.get('poll_seconds', 60)
    df = DataFeed(pairs=assets)
    df.start()
    strategy = StrategyEngine(logger)
    try:
        while True:
            for a in assets:
                candles = df.get_candles(a, limit=200)
                if len(candles) < 30:
                    continue
                # just use close series for strategy as bootstrap
                closes = [c['close'] for c in candles]
                signal = strategy.ema_crossover(closes)
                logger.info(f"Scanner: {a} signal={signal} len={len(closes)}")
            time.sleep(poll)
    except KeyboardInterrupt:
        df.stop()

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg','-c', default='examples/local_bridge_config.json')
    args = parser.parse_args()
    run(args.cfg)
