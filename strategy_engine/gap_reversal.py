import datetime, logging, os, requests
import filters.spread_filter as sp
import filters.dollar_vol_filter as dv

LOG = logging.getLogger("Strategy.Gap")
POLYGON = os.getenv("POLYGON_API_KEY")
TRADIER = os.getenv("TRADIER_TOKEN")
ACCOUNT = os.getenv("ACCOUNT_ID")

def _opening_range(symbol):
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    r = requests.get(
        f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/minute/{today}/{today}",
        params={"adjusted":"true","limit":"5","apiKey": POLYGON},
        timeout=4,
    )
    if r.status_code != 200:
        LOG.error("%s Polygon HTTP %s", symbol, r.status_code)
        return None, None
    data = r.json()
    if "results" not in data or not data["results"]:
        LOG.info("%s No minute bars yet – skip", symbol)
        return None, None
    bars = data["results"][:5]
    low  = min(b["l"] for b in bars)
    high = max(b["h"] for b in bars)
    return low, high

def trade(symbol):
    if not (POLYGON and TRADIER and ACCOUNT):
        LOG.error("Missing API creds"); return

    low, high = _opening_range(symbol)
    if low is None:   # no data yet
        return

    gap_pct = (high - low) / low * 100
    if gap_pct < 4:
        LOG.info("%s gap %.2f%% < 4 — skip", symbol, gap_pct)
        return

    if not sp.passes(symbol): return
    if not dv.passes(symbol): return

    LOG.info("%s PASSED Enhanced-Plus filters — would place order here", symbol)
