#!/bin/bash

# Load environment variables from .env file
set -a
source .env
set +a

# Variables from .env file (provide safe defaults)
LOGS_DIR="${LOGS_DIR:-logs}"
RUN_DIR="${RUN_DIR:-run}"
VENV_DIR="${VENV_DIR:-venv}"
LOG_FILE="${LOG_FILE:-router.log}"
PID_FILE="${LOG_FILE:-router.pid}"

# Create directories if missing
mkdir -p "$LOGS_DIR" "$RUN_DIR"

# Create virtual environment if missing
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Define function to install package
install_package() {
    PACKAGE="$1"
    if ! "$VENV_DIR/bin/pip3" show "$PACKAGE" &> /dev/null; then
        echo "Installing $PACKAGE..."
        "$VENV_DIR/bin/pip3" install "$PACKAGE"
    else
        echo "$PACKAGE is already installed."
    fi
}

# Install dependencies
install_package fastapi
install_package uvicorn
install_package httpx
install_package python-dotenv

# Check if already running
if [ -f "$RUN_DIR/$PID_FILE" ]; then
    PID=$(cat "$RUN_DIR/$PID_FILE")
    if ps -p "$PID" > /dev/null; then
        echo "Router already running (PID $PID). Exiting."
        exit 0
    else
        echo "Stale PID file found. Removing."
        rm "$RUN_DIR/$PID_FILE"
    fi
fi

# Start router in background
nohup "$VENV_DIR/bin/python3" router.py > "$LOGS_DIR/$LOG_FILE" 2>&1 &

# Save new PID
echo $! > "$RUN_DIR/$PID_FILE"
echo "Router started with PID $!"
