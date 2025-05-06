import datetime
import logging
import os

import requests

LOG = logging.getLogger("Scanner.Premarket")
LOG.setLevel(logging.INFO)

if not LOG.handlers:

    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("[%(asctime)s] %(name)s %(message)s"))

    LOG.addHandler(h)


def top_gappers(limit=50, min_gap=4.0):
    key = os.getenv("POLYGON_API_KEY")
    if not key:
        raise RuntimeError("POLYGON_API_KEY missing")
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    r = requests.get(
        f"https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/gainers",
        params={"apiKey": key},
        timeout=6,
    )
    r.raise_for_status()
    snaps = sorted(
        r.json()["tickers"], key=lambda s: abs(s["todaysChangePerc"]), reverse=True
    )
    watch = [s["ticker"] for s in snaps if abs(s["todaysChangePerc"]) >= min_gap][
        :limit
    ]
    LOG.info("Pre-market watch list: %s", ",".join(watch))
    return watch
