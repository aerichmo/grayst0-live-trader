# ────────────────────────────────────────────────────────────────────
#  Strategy – Gap-Reversal (clean “Phase-4 live/paper” version)
# ────────────────────────────────────────────────────────────────────


def trade(symbol: str) -> None:
    # ---------- prelim checks --------------------------------------
    if not (POLYGON and TRADIER_TOKEN and ACCOUNT):
        LOG.error("Missing API creds")
        return

    low, high = _opening_range(symbol)
    if low is None:  # still waiting for bars
        return

    gap_pct = (high - low) / low * 100
    if gap_pct < 4:  # real production threshold
        LOG.info("%s gap %.2f%% < 4 — skip", symbol, gap_pct)
        return

    if not sp.passes(symbol):
        return
    if not dv.passes(symbol):
        return

    # ---------- position sizing ------------------------------------
    entry, stop = high, low
    qty = shares(entry, stop)
    if qty < 1:
        LOG.info("%s Sizing <1 share — skip", symbol)
        return

    # ---------- live / paper toggle --------------------------------
    live = os.getenv("TRADING_MODE", "paper").lower() == "live"

    entry_payload = {
        "class": "equity",
        "symbol": symbol,
        "side": "buy",
        "quantity": qty,
        "type": "market",
        "duration": "day",
        "preview": "false" if live else "true",
    }

    r = requests.post(
        f"https://api.tradier.com/v1/accounts/{ACCOUNT_ID}/orders",
        headers={
            "Authorization": f"Bearer {TRADIER_TOKEN}",
            "Accept": "application/json",
        },
        data=entry_payload,
        timeout=4,
    )
    LOG.info("%s %s order %s", symbol, "LIVE" if live else "PREVIEW", r.text[:120])

    # ---------- protective stop (only when live) -------------------
    if live:
        stop_price = round(low - 0.05, 2)  # $0.05 below ORL
        stop_payload = {
            "class": "equity",
            "symbol": symbol,
            "side": "sell",
            "quantity": qty,
            "type": "stop_market",
            "stop": stop_price,
            "duration": "day",
        }
        r2 = requests.post(
            f"https://api.tradier.com/v1/accounts/{ACCOUNT_ID}/orders",
            headers={
                "Authorization": f"Bearer {TRADIER_TOKEN}",
                "Accept": "application/json",
            },
            data=stop_payload,
            timeout=4,
        )
        LOG.info("%s STOP @ %.2f placed → %s", symbol, stop_price, r2.text[:120])
