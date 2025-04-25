#!/usr/bin/env bash
set -euxo pipefail

# ───── System setup ───────────────────────────────────────────
apt-get update -y
apt-get install -y git python3-pip

# ───── Python environment ─────────────────────────────────────
pip3 install --upgrade google-cloud-secret-manager \
                           google-cloud-bigquery \
                           pyyaml requests websockets

# ───── Clone repo to /opt/gs ──────────────────────────────────
mkdir -p /opt/gs
cd /opt/gs
git clone https://github.com/aerichmo/grayst0-live-trader.git || true
cd grayst0-live-trader

# (optional) create virtualenv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt || true

# ───── Mark success in syslog for Cloud Logging  ──────────────
logger -t gs-trader "BOOTSTRAP COMPLETE"
