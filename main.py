import time
from threading import Thread

from engine import heartbeat_loop
from risk.loss_guard import tripped as loss_tripped
from strategy_engine.gap_reversal import trade


def scan_loop():
    from scanner.premarket import top_gappers

    watch = top_gappers()  # TEMP – replace with pre-market gappers
    while True:
        if loss_tripped():

            LOG.info("Daily loss limit hit — trading paused")

            time.sleep(300)
            continue
        for sym in watch:
            trade(sym)
        time.sleep(300)


if __name__ == "__main__":
    Thread(target=heartbeat_loop, daemon=True).start()
    scan_loop()
