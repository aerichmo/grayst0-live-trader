import datetime
import logging
import os

import requests

LOG = logging.getLogger("Filter.DollarVol")


def passes(symbol):
    key = os.getenv("POLYGON_API_KEY")
    if not key:
        LOG.error("POLYGON_API_KEY missing")
        return False

    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    r = requests.get(
        f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/5/minute/{today}/{today}",
        params={"adjusted": "true", "limit": "1", "apiKey": key},
        timeout=4,
    )
    r.raise_for_status()
    agg = r.json()["results"][0]
    dollar_vol = agg["v"] * agg["vw"]
    ok = dollar_vol >= 1_000_000
    LOG.info("%s DollarVol %.0f %s", symbol, dollar_vol, "PASS" if ok else "FAIL")
    return ok
