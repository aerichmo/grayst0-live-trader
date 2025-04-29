import datetime, logging, os, requests
import filters.spread_filter as sp
import filters.dollar_vol_filter as dv
from risk.manager import shares, TRADIER_TOKEN, ACCOUNT_ID

LOG      = logging.getLogger("Strategy.Gap")
POLYGON  = os.getenv("POLYGON_API_KEY")
LOG.setLevel(logging.INFO)
if not LOG.handlers:
    h = logging.StreamHandler();
    h.setFormatter(logging.Formatter("[%(asctime)s] %(name)s %(message)s"));
    LOG.addHandler(h)
TRADIER  = os.getenv("TRADIER_TOKEN")
ACCOUNT  = os.getenv("ACCOUNT_ID")

# ---------- helpers -------------------------------------------------
def _opening_range(symbol: str):
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    r = requests.get(
        f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/minute/{today}/{today}",
        params={"adjusted": "true", "limit": "5", "apiKey": POLYGON},
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


# ---------- main decision path -------------------------------------
def trade(symbol: str):
    if not (POLYGON and TRADIER_TOKEN and ACCOUNT):
        LOG.error("Missing API creds"); return

    low, high = _opening_range(symbol)
    if low is None:                       # still waiting for data
        return

    gap_pct = (high - low) / low * 100
    if gap_pct < 4:                     # TEMP threshold
        LOG.info("%s gap %.2f%% < 0.1 — skip", symbol, gap_pct)
        return

    if not sp.passes(symbol): return
    if not dv.passes(symbol): return

    entry, stop = high, low
    qty = shares(entry, stop)
    if qty < 1:
        LOG.info("%s Sizing <1 share — skip", symbol); return

    live = os.getenv("TRADING_MODE", "paper").lower() == "live"\n
    entry_payload = {\n
        "class":"equity","symbol":symbol,"side":"buy","quantity":qty,\n
        "type":"market","duration":"day",\n
        "preview": "false" if live else "true"\n
    }\n
    r = requests.post(\n
        f"https://api.tradier.com/v1/accounts/{ACCOUNT_ID}/orders",\n
        headers={"Authorization":f"Bearer {TRADIER_TOKEN}",\n
                 "Accept":"application/json"},\n
        data=entry_payload,timeout=4)\n
    LOG.info("%s %s order %s", symbol, "LIVE" if live else "PREVIEW", r.text[:120])\n
\n
    # ---- protective stop --------------------------------------------\n
    if live:  # only place the stop in live mode\n
        stop_price = round(low-0.05, 2)   # long side; mirror later for shorts\n
        stop_payload = {\n
            "class":"equity","symbol":symbol,"side":"sell","quantity":qty,\n
            "type":"stop_market","stop":stop_price,"duration":"day"\n
        }\n
        r2 = requests.post(\n
            f"https://api.tradier.com/v1/accounts/{ACCOUNT_ID}/orders",\n
            headers={"Authorization":f"Bearer {TRADIER_TOKEN}",\n
                     "Accept":"application/json"},\n
            data=stop_payload,timeout=4)\n
        LOG.info("%s STOP @ %.2f response %s", symbol, stop_price, r2.text[:120])


    low, high = _opening_range(symbol)
    if low is None:        # still waiting for data
        return

    gap_pct = (high - low) / low * 100
    if gap_pct < 4:
        LOG.info("%s gap %.2f%% < 0.1 — skip", symbol, gap_pct)
        return

    if not sp.passes(symbol):
        return
    if not dv.passes(symbol):
        return

    LOG.info("%s PASSED Enhanced-Plus filters — would place order here", symbol)
