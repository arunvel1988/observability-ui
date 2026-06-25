#!/bin/bash

set -e

echo "======================================"
echo "   LOGCLI LATEST INSTALL SCRIPT"
echo "======================================"

if command -v logcli >/dev/null 2>&1; then
    echo "[OK] logcli already installed"
    logcli --version
    exit 0
fi

echo "[INFO] Installing latest logcli..."

wget -q https://github.com/grafana/loki/releases/latest/download/logcli-linux-amd64.zip -O logcli.zip

apt-get update -y >/dev/null 2>&1 || true
apt-get install -y unzip >/dev/null 2>&1 || true

unzip -o logcli.zip >/dev/null 2>&1

chmod +x logcli-linux-amd64
mv logcli-linux-amd64 /usr/local/bin/logcli

rm -f logcli.zip

echo "======================================"
echo "[OK] logcli installed (latest)"
echo "======================================"

logcli --version
