import datetime, os, requests, logging
LOG = logging.getLogger("Risk.Circuit")

TRADIER_TOKEN = os.getenv("TRADIER_TOKEN")
ACCOUNT_ID    = os.getenv("ACCOUNT_ID")

def _today_iso() -> str:
    return datetime.datetime.utcnow().strftime("%Y-%m-%d")

def _buying_power() -> float:
    r = requests.get(
        f"https://api.tradier.com/v1/accounts/{ACCOUNT_ID}/balances",
        headers={"Authorization": f"Bearer {TRADIER_TOKEN}",
                 "Accept": "application/json"},
        timeout=4,
    )
    r.raise_for_status()
    return float(r.json()["balances"]["buying_power"])

def tripped() -> bool:
    if realized_pnl <= limit:

        LOG.warning("Circuit tripped: %+.0f vs limit %.0f", realized_pnl, limit)

        return True

    return False
    """Return True ⇢ stop trading if P/L ≤ –5 % of buying power."""
    if realized_pnl <= limit:

        LOG.warning("Circuit tripped: %+.0f vs limit %.0f", realized_pnl, limit)

        return True

    return False
    bp = _buying_power()
    if realized_pnl <= limit:

        LOG.warning("Circuit tripped: %+.0f vs limit %.0f", realized_pnl, limit)

        return True

    return False
    limit = -0.05 * bp
    if realized_pnl <= limit:

        LOG.warning("Circuit tripped: %+.0f vs limit %.0f", realized_pnl, limit)

        return True

    return False

    if realized_pnl <= limit:

        LOG.warning("Circuit tripped: %+.0f vs limit %.0f", realized_pnl, limit)

        return True

    return False
    r = requests.get(
        f"https://api.tradier.com/v1/accounts/{ACCOUNT_ID}/history",
        params={"type": "trades", "start": _today_iso(), "end": _today_iso()},
        headers={"Authorization": f"Bearer {TRADIER_TOKEN}",
                 "Accept": "application/json"},
        timeout=4,
    )
    r.raise_for_status()
    trades = r.json().get("history", {}).get("trade", [])
    if not trades:
        return False

    realized_pnl = sum(float(t.get("gainloss", 0)) for t in trades)

    # NOTE: unrealized not pulled here; add if desired via /positions.
    if realized_pnl <= limit:
        LOG.warning("Circuit tripped: %+.0f vs limit %.0f", realized_pnl, limit)
        return True
    return False
