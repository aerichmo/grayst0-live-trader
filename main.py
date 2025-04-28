from threading import Thread
from engine import heartbeat_loop
from strategy_engine.gap_reversal import trade
import time

def scan_loop():
    from scanner.premarket import top_gappers
    watch = top_gappers()  # TEMP – replace with pre-market gappers
    while True:
        for sym in watch: trade(sym)
        time.sleep(300)

if __name__ == "__main__":
    Thread(target=heartbeat_loop, daemon=True).start()
    scan_loop()
