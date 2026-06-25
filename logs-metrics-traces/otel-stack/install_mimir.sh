#!/bin/bash

echo "======================================"
echo " MIMIRTOOL INSTALL"
echo "======================================"

if command -v mimirtool >/dev/null 2>&1; then
    echo "[OK] mimirtool already installed"
    mimirtool version
    exit 0
fi

echo "[INFO] mimirtool not found. Installing..."

wget -q https://github.com/grafana/mimir/releases/latest/download/mimirtool-linux-amd64 -O mimirtool

chmod +x mimirtool
sudo mv mimirtool /usr/local/bin/mimirtool

echo "[OK] Installation complete"
mimirtool version
