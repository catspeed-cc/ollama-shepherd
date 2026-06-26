#!/bin/bash

PIDFILE="/home/aider/router/router.pid"
LOGFILE="/home/aider/router/router.log"
VENV_ACTIVATE="/home/aider/aider-venv/bin/activate"

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


