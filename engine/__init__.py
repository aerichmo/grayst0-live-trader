import os, time, json, logging, requests, yaml

LOG = logging.getLogger("Engine")
LOG.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("[%(asctime)s] %(message)s"))
LOG.addHandler(handler)

RULE_PATH = os.path.join(os.path.dirname(__file__), "..", "graystone_rules.yaml")

def load_rules():
    with open(RULE_PATH, "r") as f:
        yaml.safe_load(f)  # we don’t use it yet—just prove it parses
    LOG.info("YAML v1.0 loaded")

def tradier_auth_ok():
    token = os.getenv("TRADIER_TOKEN")
    acct  = os.getenv("ACCOUNT_ID")
    if not (token and acct):
        LOG.error("Tradier creds missing")
        return False
    r = requests.get(
        f"https://api.tradier.com/v1/markets/clock",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        timeout=5,
    )
    good = r.status_code == 200
    LOG.info("Tradier authenticated %s", "OK" if good else f"FAIL ({r.status_code})")
    return good

def heartbeat_loop():
    load_rules()
    tradier_auth_ok()
    while True:
        LOG.info("Engine heartbeat OK")
        time.sleep(60)
