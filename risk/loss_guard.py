import logging
LOG = logging.getLogger("Risk.Circuit")
def tripped() -> bool:
    """Return True when realised P/L for **today** is ≤ –5 % of buying power."""
    realized_pnl = 0.0                    # always defined
    bp     = _buying_power()              # current buying power
    limit  = -0.05 * bp                   # –5 % circuit

    # ---- fetch today’s realised trades ----
    r = requests.get(
        f"https://api.tradier.com/v1/accounts/{ACCOUNT_ID}/history",
        params={
            "type":  "trades",
            "start": _today_iso(),
            "end":   _today_iso()
        },
        headers={
            "Authorization": f"Bearer {TRADIER_TOKEN}",
            "Accept":        "application/json"
        },
        timeout=4,
    )
    r.raise_for_status()
    trades = r.json().get("history", {}).get("trade", [])
    if not trades:
        return False

    realized_pnl = sum(float(t.get("gainloss", 0)) for t in trades)
    if realized_pnl <= limit:
        LOG.warning("Circuit tripped: %+.0f vs limit %.0f", realized_pnl, limit)
        return True
    return False
