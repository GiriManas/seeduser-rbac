#!/bin/bash

PORT=6060  # change if needed

echo "Stopping server running on port $PORT ..."

# Find process ID using this TCP port
PID=$(lsof -ti tcp:$PORT)

if [ -z "$PID" ]; then
    echo "No server running on port $PORT."
    exit 0
fi

echo "Killing process: $PID"
kill -9 $PID

echo "Server on port $PORT stopped successfully."