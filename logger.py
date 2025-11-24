import logging, os

def get_logger():
    logger = logging.getLogger("QuantumApex")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    os.makedirs('logs', exist_ok=True)
    fh = logging.FileHandler('logs/app.log')
    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    logger.addHandler(sh)
    return logger
