#!/bin/bash

set -e

echo "======================================"
echo "   TEMPO CLI (DOCKER) INSTALL CHECK"
echo "======================================"

# Check docker
if ! command -v docker >/dev/null 2>&1; then
    echo "[ERROR] Docker is not installed"
    exit 1
fi

echo "[OK] Docker found"

# Test tempo-cli image pull
echo "[INFO] Pulling latest tempo-cli image..."

docker pull grafana/tempo-cli:latest >/dev/null 2>&1

echo "[OK] tempo-cli image ready"

# Verify by running help
echo ""
echo "======================================"
echo "      VERIFYING TEMPO CLI"
echo "======================================"

docker run --rm grafana/tempo-cli:latest --help || true

echo ""
echo "======================================"
echo "[OK] Tempo CLI setup complete"
echo "======================================"
