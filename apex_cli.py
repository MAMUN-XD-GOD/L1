from core.bridge_local import LocalBridge
from core.strategy_engine import StrategyEngine
from core.logger import get_logger

class ApexCLI:
    def __init__(self):
        self.logger = get_logger()
        self.bridge = LocalBridge(self.logger)
        self.strategy = StrategyEngine(self.logger)
    def run(self):
        print('\n=== Quantum Apex CLI ===')
        print('1. Live Signal')
        print('2. Strategy Test (EMA crossover)')
        print('3. Exit')
        choice = input('\nSelect: ')
        if choice == '1':
            price = self.bridge.get_live_price('EURUSD')
            print('Live Price:', price)
        elif choice == '2':
            hist = self.bridge.get_history('EURUSD', 50)
            signal = self.strategy.ema_crossover(hist)
            print('Signal:', signal)
        else:
            print('Exiting…')
