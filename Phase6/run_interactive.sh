#!/bin/bash

# Check if day number is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <day_number>"
    echo "Example: $0 1"
    exit 1
fi

DAY=$1

# Check if the day is valid
if [ $DAY -lt 1 ] || [ $DAY -gt 7 ]; then
    echo "Error: Day must be between 1 and 7"
    exit 1
fi

# Check if the accounts file exists
if [ ! -f "current_accounts/day${DAY}_current_accounts_file.txt" ]; then
    echo "Error: Accounts file for day $DAY not found"
    echo "Please run the daily script first: ./run_daily.sh $((DAY-1))"
    exit 1
fi

# Run the interactive session
echo "Starting interactive session for Day $DAY..."
cd frontend
python3 interactive_session.py $DAY
cd ..

echo "Interactive session completed."
echo "The session output has been merged with the daily transaction file." 