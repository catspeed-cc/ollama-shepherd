#!/bin/bash

# Load environment variables from .env file
set -a
source .env
set +a

# Variables from .env file (provide safe defaults)
LOGS_DIR="${LOGS_DIR:-logs}"
RUN_DIR="${RUN_DIR:-run}"
VENV_DIR="${VENV_DIR:-venv}"

PIDFILE="$RUN_DIR/router.pid"
LOGFILE="$LOG_DIR/router.log"

# Check if already running
if [ -f "$PIDFILE" ]; then
    PID=$(cat "$PIDFILE")
    if ps -p "$PID" > /dev/null; then
        echo "Router found running (PID $PID). Killing."
        kill -9 $(cat "$PIDFILE")
        exit 0
    else
        echo "Stale PID file found. Removing."
        rm "$PIDFILE"
    fi
fi


