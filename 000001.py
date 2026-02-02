#!/bin/bash

PID1=12345   # <-- replace with actual PID
SLEEP=30     # check every 30 seconds

echo "Waiting for PID $PID1 to finish..."

while kill -0 $PID1 2>/dev/null; do
    sleep $SLEEP
done

echo "PID $PID1 finished. Starting second job..."

nohup python second.py > second.out 2>&1 &


save as wait_and_run.sh

chmod +x wait_and_run.sh

nohup ./wait_and_run.sh &