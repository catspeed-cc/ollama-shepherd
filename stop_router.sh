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
PID_FILE="${PID_FILE:-router.pid}"

# Check if already running
if [ -f "$RUN_DIR/$PID_FILE" ]; then
    PID=$(cat "$RUN_DIR/$PID_FILE")
    if ps -p "$PID" > /dev/null; then
        echo "Router found running (PID $PID). Killing."
        kill -9 "$PID"
        rm "$RUN_DIR/$PID_FILE"
        exit 0
    else
        echo "Stale PID file found. Removing."
        rm "$RUN_DIR/$PID_FILE"
    fi
fi


