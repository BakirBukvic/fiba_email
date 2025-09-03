#!/bin/bash

# FIBA 3x3 Events Anacron Runner
# This script is called by anacron to run missed daily jobs

SCRIPT_DIR="/home/bakir/Desktop/fiba3x3BiH"
LOG_FILE="$SCRIPT_DIR/logs/anacron_run.log"

# Function to log with timestamp
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Check if the script already ran today
TODAY=$(date '+%Y-%m-%d')
LAST_RUN_FILE="$SCRIPT_DIR/logs/last_run_date.txt"

# Read last run date
if [ -f "$LAST_RUN_FILE" ]; then
    LAST_RUN_DATE=$(cat "$LAST_RUN_FILE")
else
    LAST_RUN_DATE=""
fi

# If it already ran today, skip
if [ "$LAST_RUN_DATE" = "$TODAY" ]; then
    log_message "Script already ran today ($TODAY), skipping anacron run"
    exit 0
fi

# Run the script
log_message "Running missed daily job via anacron"
"$SCRIPT_DIR/run_daily.sh"

# Update last run date
echo "$TODAY" > "$LAST_RUN_FILE"
log_message "Updated last run date to $TODAY"
