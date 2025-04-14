#!/usr/bin/env python3
"""
Interactive Banking Session

This script allows users to interact with the banking system through the command line.
It saves the session output to the appropriate files for the current day.
"""

import os
import sys
import datetime
from main import banking_system

def get_next_session_number(day):
    """Determine the next session number for the given day."""
    # Check existing session files
    session_num = 1
    while os.path.exists(f"../output/day{day}_session{session_num}.etf"):
        session_num += 1
    return session_num

def create_temp_input_file():
    """Create a temporary file for storing user input."""
    return "temp_interactive_input.inp"

def main():
    # Get the current day (default to 1 if not specified)
    if len(sys.argv) > 1:
        try:
            day = int(sys.argv[1])
        except ValueError:
            print("Error: Day must be a number between 1 and 7")
            sys.exit(1)
    else:
        day = 1
    
    if day < 1 or day > 7:
        print("Error: Day must be between 1 and 7")
        sys.exit(1)
    
    # Get the next session number
    session_num = get_next_session_number(day)
    print(f"Starting interactive session for Day {day}, Session {session_num}")
    
    # Create file paths
    accounts_file = f"../current_accounts/day{day}_current_accounts_file.txt"
    temp_input_file = create_temp_input_file()
    console_out_file = f"../output/day{day}_session{session_num}.out"
    etf_file = f"../output/day{day}_session{session_num}.etf"
    
    # Check if accounts file exists
    if not os.path.exists(accounts_file):
        print(f"Error: Accounts file {accounts_file} not found")
        sys.exit(1)
    
    # Create temporary input file
    with open(temp_input_file, "w") as f:
        f.write("login\n")
    
    # Start interactive session
    print("\nInteractive Banking Session")
    print("==========================")
    print("Type 'help' for available commands")
    print("Type 'exit' to end the session, and auto logout")
    print("!!!For your convenience, the login command has been entered and you can start the session directly!!!")
    
    # Collect user input
    with open(temp_input_file, "a") as f:
        while True:
            command = input("\nEnter command: ").strip()
            
            if command.lower() == "exit":
                f.write("logout\n")
                break
            elif command.lower() == "help":
                print("\nAvailable commands:")
                print("  login - Start a new session")
                print("  admin - Login as administrator (after 'login' command)")
                print("  withdrawal - Withdraw money from an account")
                print("  transfer - Transfer money between accounts")
                print("  paybill - Pay a bill to a company")
                print("  create - Create a new account (admin only)")
                print("  delete - Delete an account (admin only)")
                print("  disable - Disable an account (admin only)")
                print("  changeplan - Change an account's plan (admin only)")
                print("  logout - End the current session")
                print("  exit - End the interactive session")
                continue
            
            f.write(command + "\n")
    
    # Run the banking system with the collected input
    print("\nProcessing session...")
    banking_system(accounts_file, temp_input_file, console_out_file, etf_file)
    
    # Clean up temporary file
    os.remove(temp_input_file)
    
    print(f"\nSession completed. Output saved to:")
    print(f"- Console output: {console_out_file}")
    print(f"- Transaction file: {etf_file}")
    print("\nTo apply these transactions, please run:")
    print(f"./run_daily.sh {day}")

if __name__ == "__main__":
    main() 