#!/bin/bash

PIDFILE="/home/aider/router/router.pid"
LOGFILE="/home/aider/router/router.log"
VENV_ACTIVATE="/home/aider/aider-venv/bin/activate"

# Check if already running
if [ -f "$PIDFILE" ]; then
    PID=$(cat "$PIDFILE")
    if ps -p "$PID" > /dev/null; then
        echo "Router already running (PID $PID). Exiting."
        exit 0
    else
        echo "Stale PID file found. Removing."
        rm "$PIDFILE"
    fi
fi

# Activate venv and start LiteLLM in background
source "$VENV_ACTIVATE"
nohup python router.py > "$LOGFILE" 2>&1 &

# Save new PID
echo $! > "$PIDFILE"
echo "Router started with PID $!"
