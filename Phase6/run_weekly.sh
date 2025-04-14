#!/bin/bash

# Create necessary directories if they don't exist
mkdir -p output
mkdir -p current_accounts
mkdir -p master_accounts

# Check if initial files exist
if [ ! -f "current_accounts/day1_current_accounts_file.txt" ] || [ ! -f "master_accounts/day1_master_accounts.txt" ]; then
    echo "Error: Initial account files not found."
    echo "Please ensure the following files exist:"
    echo "- current_accounts/day1_current_accounts_file.txt"
    echo "- master_accounts/day1_master_accounts.txt"
    exit 1
fi

echo "Starting weekly bank simulation..."
echo "================================="

# Run the daily script for each day
for DAY in {1..7}; do
    echo "Processing Day $DAY..."
    echo "------------------------"
    
    # Run the daily script for the current day
    ./run_daily.sh $DAY
    
    # Check if the script executed successfully
    if [ $? -ne 0 ]; then
        echo "Error: Daily script failed for Day $DAY"
        exit 1
    fi
    
    # Verify that the next day's files were created
    NEXT_DAY=$((DAY + 1))
    if [ $NEXT_DAY -le 7 ]; then
        if [ ! -f "current_accounts/day${NEXT_DAY}_current_accounts_file.txt" ] || [ ! -f "master_accounts/day${NEXT_DAY}_master_accounts.txt" ]; then
            echo "Error: Next day's files were not created for Day $DAY"
            exit 1
        fi
    fi
    
    echo "Day $DAY processing complete."
    echo "------------------------"
done

echo "Weekly simulation complete!"
echo "================================="
echo "All seven days have been processed successfully."
echo "Final account files are available in:"
echo "- current_accounts/day7_current_accounts_file.txt"
echo "- master_accounts/day7_master_accounts.txt" 