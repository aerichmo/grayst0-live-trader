import datetime, logging, os, requests

LOG = logging.getLogger("Risk.Circuit")

TRADIER_TOKEN = os.getenv("TRADIER_TOKEN")
ACCOUNT_ID    = os.getenv("ACCOUNT_ID")

# ───────────────────────────────── helpers ────────────────────────────
_today_iso = lambda: datetime.datetime.utcnow().strftime("%Y-%m-%d")

def _buying_power() -> float:
    r = requests.get(
        f"https://api.tradier.com/v1/accounts/{ACCOUNT_ID}/balances",
        headers={
            "Authorization": f"Bearer {TRADIER_TOKEN}",
            "Accept":        "application/json",
        },
        timeout=4,
    )
    r.raise_for_status()
    return float(r.json()["balances"]["buying_power"])

# ───────────────────────── 5 % daily-loss circuit ─────────────────────
def tripped() -> bool:
    """
    Return **True** when realised P/L for *today* is ≤ –5 % of current
    buying-power.  When True the engine pauses trading for 5 min then re-checks.
    """
    bp     = _buying_power()
    limit  = -0.05 * bp

    r = requests.get(
        f"https://api.tradier.com/v1/accounts/{ACCOUNT_ID}/history",
        params={"type":"trades", "start":_today_iso(), "end":_today_iso()},
        headers={
            "Authorization": f"Bearer {TRADIER_TOKEN}",
            "Accept":        "application/json",
        },
        timeout=4,
    )
    r.raise_for_status()
    trades = r.json().get("history", {}).get("trade", [])
    if not trades:
        return False

    realized = sum(float(t.get("gainloss", 0)) for t in trades)

    if realized <= limit:
        LOG.warning("Circuit tripped: %+.0f vs limit %.0f", realized, limit)
        return True
    return False
