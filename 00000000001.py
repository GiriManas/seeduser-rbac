#!/bin/bash

# Ask user once before detaching
echo "Enter your choice (1 or 2): "
read user_input

# Validate input
if [[ "$user_input" != "1" && "$user_input" != "2" ]]; then
    echo "❌ Invalid input. Please enter 1 or 2."
    exit 1
fi

# Create a timestamped log file
timestamp=$(date +"%Y%m%d_%H%M%S")
logfile="run_${timestamp}.log"

# Run the Python script in background with nohup
nohup bash -c "echo $user_input | python3 main.py" > "$logfile" 2>&1 &

echo "✅ Script started in background."
echo "📄 Logs: $logfile"
echo "🔍 To check status: tail -f $logfile"