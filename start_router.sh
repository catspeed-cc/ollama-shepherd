#!/bin/bash

# Load environment variables from .env file
set -a
source .env
set +a

# Check if ROUTER_TIMEOUT is a valid number
if ! [[ "$ROUTER_TIMEOUT" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
    echo "Error: ROUTER_TIMEOUT must be a valid number"
    exit 1
fi

# Variables from .env file (provide safe defaults)
LOGS_DIR="${LOGS_DIR:-logs}"
RUN_DIR="${RUN_DIR:-run}"
VENV_DIR="${VENV_DIR:-venv}"
LOG_FILE="${LOG_FILE:-router.log}"
PID_FILE="${PID_FILE:-router.pid}"

# Create logs directory if missing
if [ ! -d "$LOGS_DIR" ]; then
    mkdir -p "$LOGS_DIR"
fi

# Create log file if missing
LOG_FILE_PATH="$LOGS_DIR/$LOG_FILE"
if [ ! -f "$LOG_FILE_PATH" ]; then
    touch "$LOG_FILE_PATH"
fi

# Create RUN directory if missing
mkdir -p "$RUN_DIR"

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

install_dependencies() {
    install_package fastapi
    install_package uvicorn
    install_package httpx
    install_package python-dotenv
}

# Install dependencies
install_dependencies

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
PID=$!

# Save new PID
echo $PID > "$RUN_DIR/$PID_FILE"

( wait $PID; rm -f "$RUN_DIR/$PID_FILE" ) &
