#!/bin/bash

set -e  # Exit on error

echo "Checking if python3-venv and docker.io are installed..."

if ! dpkg -s python3-venv >/dev/null 2>&1 || ! dpkg -s docker.io >/dev/null 2>&1; then
    echo "Installing python3-venv and docker.io..."
    sudo apt update
    sudo apt install -y python3-venv docker.io curl jq python3-pip -y
    echo "python3-venv and docker.io installed."
else
    echo "python3-venv and docker.io are already installed."
fi

# Enable and start Docker
sudo systemctl enable docker
sudo systemctl start docker

# Install Docker Compose
if ! command -v docker-compose >/dev/null 2>&1; then
    echo "Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo "Docker Compose installed."
else
    echo "Docker Compose is already installed."
fi

# Create virtual environment if missing or broken
VENV_DIR="venv"
ACTIVATE="$VENV_DIR/bin/activate"

if [ ! -f "$ACTIVATE" ]; then
    echo "Creating virtual environment in $VENV_DIR..."
    rm -rf "$VENV_DIR"
    python3 -m venv "$VENV_DIR"
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$ACTIVATE"

# Install Python dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing Python packages from requirements.txt..."
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "Python packages installed."
else
    echo "requirements.txt not found."
    exit 1
fi

# Check Docker installation
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed or not in PATH."
    exit 1
fi

# Fix Docker socket permissions
if [ -S /var/run/docker.sock ]; then
    echo "Fixing Docker socket permissions..."
    sudo chmod 777 /var/run/docker.sock
    echo "Docker socket permissions updated."
else
    echo "Docker socket not found."
    exit 1
fi

# Run Python application
#echo "Running app.py..."
python3 app.py

#nohup gunicorn --bind 127.0.0.1:5000 app:app > gunicorn.log 2>&1 &