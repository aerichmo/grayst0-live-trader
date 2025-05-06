import logging
import os

import requests

LOG = logging.getLogger("Risk.Manager")

RISK_PER_TRADE = float(os.getenv("RISK_PER_TRADE", "100"))  # USD
TRADIER_TOKEN = os.getenv("TRADIER_TOKEN")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")


def _cash_available() -> float:
    r = requests.get(
        f"https://api.tradier.com/v1/accounts/{ACCOUNT_ID}/balances",
        headers={
            "Authorization": f"Bearer {TRADIER_TOKEN}",
            "Accept": "application/json",
        },
        timeout=4,
    )
    r.raise_for_status()
    return float(r.json()["balances"]["cash_available"])


def shares(entry: float, stop: float) -> int:
    risk_dollars = min(RISK_PER_TRADE, 0.02 * _cash_available())  # cap at 2 % acct
    per_share_risk = max(0.01, abs(entry - stop))  # >= 1 ¢ guard-rail
    qty = int(risk_dollars // per_share_risk)
    LOG.info(
        "Sizing %d sh @ %.2f risk %.2f (cash %.0f)",
        qty,
        entry,
        per_share_risk,
        risk_dollars,
    )
    return qty
