#!/bin/bash

echo "Enter your choice (1 or 2 or 9): "
read user_input

if [[ "$user_input" != "1" && "$user_input" != "2" && "$user_input" != "9" ]]; then
    echo "Invalid input! Please enter 1, 2, or 9."
    exit 1
fi

# Run the Python script with nohup and redirect logs
nohup python3 run_wrapped_tokenizer.py "$user_input" > run.log 2>&1 &

echo "Process started with input $user_input. Logs are in run.log"