import requests, os, logging
LOG = logging.getLogger("Filter.Spread")

def passes(symbol):

    token = os.getenv("TRADIER_TOKEN")

    if not token:

        LOG.error("TRADIER_TOKEN missing"); return False

    try:

        r = requests.get("https://api.tradier.com/v1/markets/quotes",

            params={"symbols": symbol},

            headers={"Authorization": f"Bearer {token}", "Accept":"application/json"},

            timeout=3)

        if r.status_code != 200:

            LOG.warning("%s Tradier HTTP %s", symbol, r.status_code); return False

        if "quotes" not in r.json():

            LOG.warning("%s Tradier response lacks quotes key", symbol); return False

        q = r.json()["quotes"]["quote"]

        if isinstance(q, list): q = q[0]

        spread = abs(float(q["ask"]) - float(q["bid"]))

        price  = float(q["last"])

        ok = spread <= 0.02 or spread/price <= 0.0015

        LOG.info("%s Spread %.4f %s", symbol, spread, "PASS" if ok else "FAIL")

        return ok

    except Exception as e:

        LOG.warning("%s spread-filter exception %s", symbol, e); return False

    token = os.getenv("TRADIER_TOKEN")

    if not token:

        LOG.error("TRADIER_TOKEN missing"); return False

    try:

        r = requests.get(

            "https://api.tradier.com/v1/markets/quotes",

            params={"symbols": symbol},

            headers={"Authorization": f"Bearer {token}", "Accept":"application/json"},

            timeout=3)

        if r.status_code != 200:

            LOG.warning("%s Tradier HTTP %s", symbol, r.status_code); return False

        if "quotes" not in r.json():

            LOG.warning("%s Tradier response lacks quotes key", symbol); return False

        q = r.json()["quotes"]["quote"]

        if isinstance(q, list): q = q[0]

        spread = abs(float(q["ask"]) - float(q["bid"]))

        price  = float(q["last"])

        ok = spread <= 0.02 or spread/price <= 0.0015

        LOG.info("%s Spread %.4f %s", symbol, spread, "PASS" if ok else "FAIL")

        return ok

    except Exception as e:

        LOG.warning("%s spread-filter exception %s", symbol, e); return False

    token = os.getenv("TRADIER_TOKEN")

    if not token:

        LOG.error("TRADIER_TOKEN missing"); return False

    try:

        r = requests.get(

            "https://api.tradier.com/v1/markets/quotes",

            params={"symbols": symbol},

            headers={"Authorization": f"Bearer {token}", "Accept":"application/json"},

            timeout=3)

        if r.status_code != 200:

            LOG.warning("%s Tradier HTTP %s", symbol, r.status_code); return False

        if "quotes" not in r.json():

            LOG.warning("%s Tradier response lacks quotes key", symbol); return False

        q = r.json()["quotes"]["quote"]

        if isinstance(q, list): q = q[0]

        spread = abs(float(q["ask"]) - float(q["bid"]))

        price  = float(q["last"])

        ok = spread <= 0.02 or spread/price <= 0.0015

        LOG.info("%s Spread %.4f %s", symbol, spread, "PASS" if ok else "FAIL")

        return ok

    except Exception as e:

        LOG.warning("%s spread-filter exception %s", symbol, e); return False

    token = os.getenv("TRADIER_TOKEN")

    if not token:

        LOG.error("TRADIER_TOKEN missing"); return False

    try:

        r = requests.get(

            "https://api.tradier.com/v1/markets/quotes",

            params={"symbols": symbol},

            headers={"Authorization": f"Bearer {token}", "Accept":"application/json"},

            timeout=3)

        if r.status_code != 200:

            LOG.warning("%s Tradier HTTP %s", symbol, r.status_code); return False

        if "quotes" not in r.json():

            LOG.warning("%s Tradier response lacks quotes key", symbol); return False

        q = r.json()["quotes"]["quote"]

        if isinstance(q, list): q = q[0]

        spread = abs(float(q["ask"]) - float(q["bid"]))

        price  = float(q["last"])

        ok = spread <= 0.02 or spread/price <= 0.0015

        LOG.info("%s Spread %.4f %s", symbol, spread, "PASS" if ok else "FAIL")

        return ok

    except Exception as e:

        LOG.warning("%s spread-filter exception %s", symbol, e); return False

    token = os.getenv("TRADIER_TOKEN")

    if not token:

        LOG.error("TRADIER_TOKEN missing"); return False



    try:

        r = requests.get(

            "https://api.tradier.com/v1/markets/quotes",

            params={"symbols": symbol},

            headers={"Authorization": f"Bearer {token}", "Accept":"application/json"},

            timeout=3)

        if r.status_code != 200:

            LOG.warning("%s Tradier HTTP %s", symbol, r.status_code); return False

        if "quotes" not in r.json():

            LOG.warning("%s Tradier response lacks quotes key", symbol); return False

        q = r.json()["quotes"]["quote"]

        if isinstance(q, list):

            q = q[0]

        spread = abs(float(q["ask"]) - float(q["bid"]))

        price  = float(q["last"])

        ok = spread <= 0.02 or spread/price <= 0.0015

        LOG.info("%s Spread %.4f %s", symbol, spread, "PASS" if ok else "FAIL")

        return ok

    except Exception as e:

        LOG.warning("%s spread-filter exception %s", symbol, e); return False

    r = requests.get(
        "https://api.tradier.com/v1/markets/quotes",
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
