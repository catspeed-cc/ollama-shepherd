#!/bin/bash

# Load environment variables from .env file
set -a
source .env
set +a

LOGS_DIR="${LOGS_DIR:-logs}"
LOG_FILE="router.log"
RUN_DIR="run"
PID_FILE="router.pid"
VENV_ACTIVATE="/home/aider/aider-venv/bin/activate"

# Create directories if missing
mkdir -p "$LOGS_DIR" "$RUN_DIR"

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

# Activate venv and start LiteLLM in background
source "$VENV_ACTIVATE"
nohup python router.py > "$LOGS_DIR/$LOG_FILE" 2>&1 &

# Save new PID
echo $! > "$RUN_DIR/$PID_FILE"
echo "Router started with PID $!"
