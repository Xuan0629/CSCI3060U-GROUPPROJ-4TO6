#!/bin/bash

# Check if day number is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <day_number>"
    echo "Example: $0 1"
    exit 1
fi

DAY=$1
NEXT_DAY=$((DAY + 1))

# Create necessary directories
mkdir -p output
mkdir -p current_accounts
mkdir -p master_accounts

# Find all session files for the given day
SESSION_FILES=$(ls -1 input/day${DAY}_session*.inp 2>/dev/null | sort)

if [ -z "$SESSION_FILES" ]; then
    echo "No session files found for day $DAY"
    exit 1
fi

# Process each session for the given day
for INPUT_FILE in $SESSION_FILES; do
    # Extract session number from filename
    SESSION=$(echo $INPUT_FILE | grep -o 'session[0-9]*' | grep -o '[0-9]*')
    OUTPUT_FILE="output/day${DAY}_session${SESSION}.etf"
    
    echo "Processing $INPUT_FILE..."
    
    # Run the frontend program with input file
    python3 frontend/main.py \
        "current_accounts/day${DAY}_current_accounts_file.txt" \
        "$INPUT_FILE" \
        "output/day${DAY}_session${SESSION}.out" \
        "$OUTPUT_FILE"
done

# Merge all ETF files for the day
echo "Merging transaction files for day $DAY..."
MERGED_FILE="output/day${DAY}_merged_txns.txt"

# Clear the merged file if it exists
> "$MERGED_FILE"

# Append all ETF files for the day
ETF_FILES=$(ls -1 output/day${DAY}_session*.etf 2>/dev/null | sort)
for ETF_FILE in $ETF_FILES; do
    if [ -f "$ETF_FILE" ]; then
        cat "$ETF_FILE" >> "$MERGED_FILE"
    fi
done

echo "Done! Merged transaction file created at $MERGED_FILE"

# Run backend processing
echo "Running backend processing for day $DAY..."

# Run the backend program
python3 backend/main.py \
    "master_accounts/day${DAY}_master_accounts.txt" \
    "$MERGED_FILE" \
    "master_accounts/day${NEXT_DAY}_master_accounts.txt" \
    "current_accounts/day${NEXT_DAY}_current_accounts_file.txt"

echo "Backend processing complete!"
echo "Next day's files have been generated:"
echo "- master_accounts/day${NEXT_DAY}_master_accounts.txt"
echo "- current_accounts/day${NEXT_DAY}_current_accounts_file.txt"