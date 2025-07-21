#!/bin/bash

set -e  # Exit on error

echo "🔍 Checking if python3-venv is installed..."

if ! dpkg -s python3-venv >/dev/null 2>&1; then
    echo "python3-venv not found. Installing..."
    sudo apt update
    sudo apt install -y python3-venv
    echo "python3-venv installed."
else
    echo "python3-venv is already installed."
fi

# Create virtual environment if missing or broken
VENV_DIR="venv"
ACTIVATE="$VENV_DIR/bin/activate"

if [ ! -f "$ACTIVATE" ]; then
    echo "(Re)creating virtual environment in $VENV_DIR..."
    rm -rf "$VENV_DIR"
    python3 -m venv "$VENV_DIR"
    echo "Virtual environment created."
else
    echo "Virtual environment already exists and is valid."
fi

# Activate virtual environment
echo "🐍 Activating virtual environment..."
source "$ACTIVATE"

# Install requirements
if [ -f "requirements.txt" ]; then
    echo "📦 Installing Python packages from requirements.txt..."
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ Python packages installed."
else
    echo "❌ requirements.txt not found!"
    exit 1
fi

# Check Docker installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Give permissions to Docker socket (insecure but OK for demo/dev)
if [ -S /var/run/docker.sock ]; then
    echo "🛠️  Fixing Docker socket permissions (chmod 777)..."
    sudo chmod 777 /var/run/docker.sock
    echo "✅ Docker socket permissions updated."
else
    echo "❌ Docker socket not found!"
    exit 1
fi


# Run Python app
echo "🚀 Running windows-ui.py..."
python3 observability-ui.py
