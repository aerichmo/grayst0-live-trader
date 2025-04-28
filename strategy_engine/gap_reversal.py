import datetime, logging, os, requests, yaml, filters.spread_filter as sp, filters.dollar_vol_filter as dv

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
    bars = r.json()["results"]
    low  = min(b["l"] for b in bars)
    high = max(b["h"] for b in bars)
    volume = sum(b["v"] for b in bars)
    avg10  = _ten_day_avg_vol(symbol)
    return low, high, volume, avg10

def _ten_day_avg_vol(symbol):
    today = datetime.datetime.utcnow().date()
    ten  = today - datetime.timedelta(days=15)
    r = requests.get(
        f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{ten}/{today}",
        params={"adjusted":"true","apiKey": POLYGON},
        timeout=4,
    )
    return sum(b["v"] for b in r.json()["results"][-10:]) / 10

def _float_check(symbol):
    r = requests.get(f"https://api.polygon.io/v3/reference/tickers/{symbol}", params={"apiKey": POLYGON}).json()
    return r["results"]["share_class_shares_outstanding"] >= 15_000_000

def _no_dilution(symbol):
    r = requests.get(f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={symbol}&type=&count=20&owner=exclude&output=atom")
    return not any(tag in r.text for tag in ("S-3", "424B", "ATM"))

def trade(symbol):
    low, high, vol, avg10 = _opening_range(symbol)
    gappct = (high - low) / low * 100
    if gappct < 4:
        LOG.info("%s reject gap %.2f%%", symbol, gappct)
        return

    if vol < 2 * avg10:
        LOG.info("%s reject vol %.0f vs avg %.0f", symbol, vol, avg10)
        return

    if not _float_check(symbol):
        LOG.info("%s reject float < 15M", symbol); return
    if not _no_dilution(symbol):
        LOG.info("%s reject dilution news", symbol); return
    if not sp.passes(symbol): return
    if not dv.passes(symbol): return

    stop  = low * 0.998   # low -0.2 %
    target1 = low + 2*(low - stop)
    target2 = low + 4*(low - stop)

    LOG.info("%s TAKING TRADE  stop %.2f  t1 %.2f  t2 %.2f", symbol, stop, target1, target2)
    _submit_order(symbol, stop)

def _submit_order(symbol, stop):
    # 1-share live order
    data = {"class":"equity","symbol":symbol,"side":"buy","quantity":"1","type":"market","duration":"day"}
    r = requests.post(
        f"https://api.tradier.com/v1/accounts/{ACCOUNT}/orders",
        headers={"Authorization": f"Bearer {TRADIER}", "Accept":"application/json"},
        data=data, timeout=5,
    )
    LOG.info("%s OrderResponse %s", symbol, r.text)
