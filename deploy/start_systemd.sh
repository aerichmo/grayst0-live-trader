#!/usr/bin/env bash
sudo cp /opt/gs/grayst0-live-trader/deploy/gs-trader.service /etc/systemd/system/
echo 'DRY_RUN=1' | sudo tee /etc/default/gs-trader
sudo systemctl daemon-reload
sudo systemctl enable gs-trader
sudo systemctl restart gs-trader
sudo systemctl status gs-trader --no-pager
