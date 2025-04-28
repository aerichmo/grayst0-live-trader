import requests, os, logging
LOG = logging.getLogger("Filter.Spread")

def passes(symbol):
    token = os.getenv("TRADIER_TOKEN")
    r = requests.get(
        f"https://api.tradier.com/v1/markets/quotes",
        params={"symbols": symbol},
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        timeout=3,
    )
    q = r.json()["quotes"]["quote"]
    spread = abs(float(q["ask"]) - float(q["bid"]))
    price  = float(q["last"])
    ok = spread <= 0.02 or spread/price <= 0.0015
    LOG.info("%s Spread %.4f %s", symbol, spread, "PASS" if ok else "FAIL")
    return ok
