#!/bin/bash

# FIBA 3x3 Events Daily Runner
# This script ensures the virtual environment is activated and runs the scraper

# Set the script directory
SCRIPT_DIR="/home/bakir/Desktop/fiba3x3BiH"
LOG_FILE="$SCRIPT_DIR/logs/daily_run.log"

# Create logs directory if it doesn't exist
mkdir -p "$SCRIPT_DIR/logs"

# Function to log with timestamp
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Change to the script directory
cd "$SCRIPT_DIR"

# Log start
log_message "Starting daily FIBA 3x3 events scraper"

# Activate virtual environment and run the script
if [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
    log_message "Virtual environment activated"
else
    log_message "ERROR: Virtual environment not found at $SCRIPT_DIR/venv/bin/activate"
    exit 1
fi

# Run the Python script and capture output
if python3 run.py >> "$LOG_FILE" 2>&1; then
    log_message "Script completed successfully"
else
    log_message "ERROR: Script failed with exit code $?"
    exit 1
fi

# Deactivate virtual environment
deactivate

# Record that we ran today
TODAY=$(date '+%Y-%m-%d')
echo "$TODAY" > "$SCRIPT_DIR/logs/last_run_date.txt"

log_message "Daily run completed"
