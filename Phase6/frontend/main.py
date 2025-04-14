"""
Main Banking System

Description:
This program simulates a banking system that allows users to perform transactions such as 
withdrawals, transfers, and bill payments. Users must log in before performing any transaction. 
The system supports both standard (user) and admin sessions, where admin sessions have special 
privileges (e.g., overriding account limits, accessing all user accounts).

Input Sources:
- No dedicated input file for accounts (hardcoded users)
- CLI-based user input for commands

Output File:
- daily_transaction_file.txt: Stores a record of all transactions performed during a session.

How to Run:
1. Execute main.py to start the application.
2. Enter "login" to authenticate:
   - Enter session type ("admin" or "standard").
   - Admin users get full access; standard users enter their account number.
3. After successful login, you can enter one of the following commands:
   - "withdrawal" to withdraw funds.
   - "transfer"  to move funds between accounts.
   - "paybill"   to pay a bill to a known company.
   - "create"    (admin only) to create a new account.
   - "delete"    (admin only) to remove an existing account.
   - "disable"   (admin only) to disable an account.
   - "changeplan" (admin only) to switch or toggle the account’s plan.
   - "logout"    to end the session and save all transactions.
4. Transaction details are automatically written to daily_transaction_file.txt upon each operation.
"""

import sys

from transfer import Transfer
from paybill import Paybill
from check import Check
from deposit import Deposit
from create import Create
from delete import Delete
from changeplan import ChangePlan
from disable import Disable
from login import Login
from withdrawal import Withdrawal
from logout import Logout

class User:
    def __init__(self, account_number, user_name, availability, balance, plan_type):
        self.account_number = account_number
        self.user_name = user_name.strip()
        self.availability = availability  # "A" for active, "D" for disabled
        self.balance = float(balance)
        self.user_type = "standard"  # Default all users to "standard"
        self.plan_type = plan_type


def parse_account_line(line):
    line = line.rstrip("\n")
    if len(line) < 38:
        return None  # ignore or handle lines that are too short

    if line.startswith("END_OF_FILE"):
        # we might treat this as a sentinel indicating no more real accounts
        return None

    # Slices based on the observed layout
    account_number = line[0:5]
    name_raw       = line[6:25]
    availability   = line[27]
    balance_str    = line[29:37]
    plan_type      = line[38:40]
    user_name      = name_raw.rstrip("_") 

    return (account_number, user_name, availability, balance_str, plan_type)

def load_users(accounts_filename):
    users_dict = {}
    with open(accounts_filename, "r") as f:
        for line in f:
            if not line.strip():
                continue
            fields = parse_account_line(line)
            if not fields:
                # might be the END_OF_FILE or invalid line
                continue
            acct_num, uname, avail, bal, plan = fields
            new_user = User(acct_num, uname, avail, bal, plan)
            users_dict[acct_num] = new_user
    return users_dict

def banking_system(accounts_file, commands_file, console_out_file, etf_file_path):
    
    # load users
    USERS = load_users(accounts_file)

    # open the .out (output) and .etf (transactions) files
    out_file = open(console_out_file, "w")
    etf_file = open(etf_file_path, "w")

    def write_console(msg):
        """
        Replaces all print statements in your code so that
        messages go to the .out file.
        """
        out_file.write(msg + "\n")

    def log_transaction(txn_str):
        """
        Write transaction lines to the .etf file.
        """
        etf_file.write(txn_str + "\n")
    
    # read commands from the commands_file
    with open(commands_file, "r") as cf:
        commands = [line.strip() for line in cf if line.strip()]
        
    logged_in = False
    current_user = None
    session_type = None
    check = Check()
    
    def errorEnd():
        write_console("Session terminated.")
        log_transaction("00_____________________00000_00000.00_00")
        logged_in = False
        current_user = None
        session_type = None
    
    
    i = 0
    while i < len(commands):
        command = commands[i].lower()
        i += 1
        
        if command == "login":
            if logged_in:
                write_console("You have already Login")
                break
            write_console("Welcome to the banking system.")
            if i >= len(commands):
                write_console("Error: Missing session type.")
                break
            session_type = commands[i].lower()
            write_console(f"Enter session type: {session_type}")
            i += 1

            if session_type == "admin":
                login_instance = Login(session_type, None, logged_in)
                login_instance.process_login()
                logged_in = True
                current_user = None
                # write_console("Login_Success")
            else:
                # standard user
                if i >= len(commands):
                    write_console("Error: Missing account holder name.")
                    break
                entered_name = commands[i]
                i += 1

                # find a user with that name
                found_user = None
                for u in USERS.values():
                    if u.user_name.lower() == entered_name.lower():
                        found_user = u
                        write_console(f"Enter account holder name: {entered_name}")
                        break
                if found_user:
                    login_instance = Login(session_type, found_user, logged_in)
                    login_instance.process_login()
                    logged_in = True
                    current_user = found_user
                    # write_console("Login_Success")
                else:
                    write_console("Error: Invalid account holder name.")

        elif command == "withdraw":
            # Default log string used for any error case.
            default_log = "00_____________________00000_00000.00_00"
            
            if not logged_in:
                write_console("Error: You must be logged in to withdraw.")
                log_transaction(default_log)
                continue

            # Branch based on session type
            if session_type == "admin":
                # For admin, read account holder name and then account number.
                if i >= len(commands):
                    write_console("Error: Missing account holder name for withdrawal.")
                    log_transaction(default_log)
                    break
                entered_name = commands[i]
                write_console(f"Enter account holder name: {entered_name}")
                i += 1

                found_user = None
                for u in USERS.values():
                    if u.user_name.lower() == entered_name.lower():
                        found_user = u
                        break
                if not found_user:
                    write_console("Error: Invalid account holder name")
                    log_transaction(default_log)
                    continue

                if i >= len(commands):
                    write_console("Error: Missing account number for withdrawal.")
                    log_transaction(default_log)
                    break
                provided_account = commands[i]
                i += 1
                write_console(f"Enter account name: {found_user.account_number}")
                if provided_account != found_user.account_number:
                    write_console("Error: Invalid account number")
                    log_transaction(default_log)
                    continue

                user_for_withdraw = found_user

            else:  # standard session
                # current_user is already set via login; just verify the account number.
                if current_user is None:
                    write_console("Error: No user logged in.")
                    log_transaction(default_log)
                    continue

                if i >= len(commands):
                    write_console("Error: Missing account number for withdrawal.")
                    log_transaction(default_log)
                    break
                provided_account = commands[i]
                i += 1
                write_console(f"Enter account name: {current_user.account_number}")
                if provided_account != current_user.account_number:
                    write_console("Error: Wrong account number")
                    log_transaction(default_log)
                    continue

                user_for_withdraw = current_user

            # Read the withdrawal amount
            if i >= len(commands):
                write_console("Error: Missing withdrawal amount.")
                log_transaction(default_log)
                break
            amount_str = commands[i]
            write_console(f"Enter Withdrawal amount: {amount_str}")
            i += 1
            try:
                amount = float(amount_str)
            except ValueError:
                write_console("Error: Invalid withdrawal amount.")
                log_transaction(default_log)
                continue

            # Check if withdrawal amount exceeds current balance.
            if amount > user_for_withdraw.balance:
                write_console("Error: Account balance less than 0")
                log_transaction(default_log)
                continue
            else:
                write_console("Withdrawal success")
                # Process the withdrawal and log the transaction output.
                withdrawal_instance = Withdrawal(user_for_withdraw, amount)
                withdrawal_instance.process_withdrawal()
                withdrawal_output = withdrawal_instance.return_transaction_output()
                log_transaction(withdrawal_output)
        
        elif command == "transfer":
            
            if not logged_in:
                write_console("Error: You must be logged in first.")
                continue
            
            # Sanity Check
            if session_type == "admin":
                if 7 > len(commands):
                    write_console("Error: Missing required fields for transfer. Please provide both source and destination account numbers and the amount.")
                    errorEnd()
                    break  
            elif 8 > len(commands):
                write_console("Error: Missing required fields for transfer. Please provide both source and destination account numbers and the amount.")
                errorEnd()
                break
            sender_account = commands[i]
            receiver_account = commands[i+1]
            i += 2

            if check.invalid_character_check(commands[i]):
                amount = float(commands[i])
            else:
                write_console("Error: Invalid transfer amount. Amount must be numeric.")
                errorEnd()
                break
            i += 1
            
            if session_type == "admin" or (current_user and check.sender_account_match(current_user, sender_account)):
                if receiver_account in USERS:
                    transfer = Transfer(session_type, USERS[sender_account], USERS[receiver_account], amount, write_console=write_console)
                    # Write transaction output to log file
                    # transaction_output = transfer.return_transaction_output()
                    # log_transaction(transaction_output)
                    # Then log the .etf lines:
                    if 0!=transfer.process_transfer():
                        txn_out = transfer.return_transaction_output()
                        for line in txn_out.splitlines():
                            log_transaction(line)
           
                else:
                    write_console("Error: Target account does not exist.")
            else:
                write_console("Error: Unauthorized transfer. You can only transfer from accounts you own.")
        
        elif command == "paybill":

            if not logged_in:
                write_console("Error: You must be logged in first.")
                continue
            # Sanity Check
            if session_type == "admin":
                if 7 > len(commands):
                    write_console("Error: The paybill argument is missing, so the process will be rejected. Please re-try.")
                    errorEnd()
                    break  
            elif 8 > len(commands):
                write_console("Error: The paybill argument is missing, so the process will be rejected. Please re-try.")
                errorEnd()
                break
            # sender acct, company code, amount
            sender_account = commands[i]
            company = commands[i+1]
            i += 2

            if check.invalid_character_check(commands[i]):
                amount = float(commands[i])
            else:
                write_console("Error: Invalid payment amount. Amount must be numeric.")
                errorEnd()
                break
            i += 1
            
            if session_type == "admin" or (current_user and check.sender_account_match(current_user, sender_account)):
                paybill = Paybill(session_type, USERS[sender_account], company, amount, write_console=write_console)
                if 0!= paybill.process_paybill():
                    c_id = paybill.check.company_id_check(company)
                    if c_id:
                            out_str = paybill.return_transaction_output(c_id)
                            for line in out_str.splitlines():
                                log_transaction(line)
                
            else:
                write_console("Error: You must be logged in as a standard user to pay bills.")
        

        elif command == "deposit":
            if not logged_in or session_type != "admin":
                write_console("Error: You must be logged in as an admin to deposit into other accounts.")
                continue
            
            if commands[i] == "logout":
                write_console("Error: Missing account holder name.")
                continue

            if i >= len(commands):
                write_console("Error: Missing account number.")
                break
            account_holder_name = commands[i].strip()
            i += 1

            if i >= len(commands):
                write_console("Error: Missing account holder name.")
                continue
            account_number = commands[i].strip()
            i += 1

            if account_number in USERS and USERS[account_number].user_name.strip() == account_holder_name:
                if i >= len(commands):
                    write_console("Error: Missing deposit amount.")
                    break

                if check.invalid_character_check(commands[i]):
                    deposit_amount = float(commands[i])
                else:
                    write_console("Error: Invalid deposit amount. Amount must be numeric.")
                    errorEnd()
                    break
                i += 1

                if deposit_amount > 0:
                    deposit = Deposit(session_type, USERS[account_number], deposit_amount, write_console)
                    transaction_output = deposit.process_deposit()

                    if transaction_output:  # Ensuring only successful deposits are logged
                        log_transaction(transaction_output)
                else:
                    write_console("Error: Deposit amount must be greater than zero.")
            else:
                write_console(f"Error: Invalid account number {account_number} for account holder '{account_holder_name}'.")
        
        elif command == "create":
            if not logged_in or session_type != "admin":
                write_console("Error: You must be logged in as an admin to create an account.")
                continue

            # Check for missing account holder name
            if i >= len(commands):
                write_console("Error: Missing account holder name.")
                errorEnd()
                break

            account_holder_name = commands[i].strip()
            if account_holder_name.isdigit() or account_holder_name.lower() == "logout": #added this check.
                write_console("Error: Account holder name cannot be blank.")
                errorEnd()
                break

            i += 1

            # Check for missing initial balance
            if i >= len(commands):
                write_console("Error: Missing initial balance.")
                errorEnd()
                break

            balance_str = commands[i]

            if balance_str.lower() == "logout": # added this check
                write_console("Error: Initial balance cannot be blank.")
                errorEnd()
                break

            # Check for invalid initial balance format
            if check.invalid_character_check(balance_str):
                initial_balance = float(balance_str)
            else:
                write_console("Error: Invalid initial balance. Amount must be numeric.")
                errorEnd()
                break

            i += 1

            # Check for negative initial balance
            if initial_balance >= 0:
                create_account = Create(session_type, USERS, account_holder_name, initial_balance, write_console=write_console)
                transaction_output = create_account.process_creation()

                if transaction_output:
                    log_transaction(transaction_output)
            else:
                write_console("Error: Initial balance cannot be negative.")
                errorEnd()
                continue
    
        elif command == "delete":
            if not logged_in or session_type != "admin":
                write_console("Error: You must be logged in as an admin to delete accounts.")
                continue

            # Get the account holder name from the input file.
            if i >= len(commands):
                write_console("Error: Missing account holder name for delete.")
                errorEnd()
                break
            account_holder_name = commands[i]

            if account_holder_name.lower().isdigit():
                write_console("Error: Account holder name cannot be blank.")
                errorEnd()
                break

            write_console(f"Enter account holder name: {account_holder_name}")
            i += 1

            # Get the account number from the input file.
            if i >= len(commands):
                write_console("Error: Missing account number for delete.")
                errorEnd()
                break

            account_number = commands[i]
            if account_number.lower() == "logout":
                write_console("Error: Account number cannot be blank.")
                errorEnd()
                break

            write_console(f"Enter account number: {account_number}")
            i += 1

            # Create and process the Delete transaction.
            delete_account = Delete(session_type, USERS, write_console=write_console)
            transaction_output=delete_account.process_deletion(account_holder_name, account_number)
            if transaction_output:  # Ensure only successful creations are logged
                    log_transaction(transaction_output)

        elif command == "changeplan":
            if not logged_in:
                write_console("Error: You must be logged in to perform transactions.")
                continue

            if session_type != "admin":
                write_console("Error: This is a privileged transaction that requires admin mode.")
                continue

            # Get the account holder name from the input file.
            if i >= len(commands):
                write_console("Error: Missing account holder name for changeplan.")
                errorEnd()
                break
            account_holder_name = commands[i]
            write_console(f"Enter account holder name: {account_holder_name}")
            i += 1

            # Search for a user with the given name.
            found_user = None
            for user in USERS.values():
                if user.user_name.strip().lower() == account_holder_name.lower():
                    found_user = user
                    break

            if found_user is None:
                write_console("Error: Account holder name not found.")
                continue

            # Get the account number from the input file.
            if i >= len(commands):
                write_console("Error: Missing account number for changeplan.")
                errorEnd()
                break
            account_number = commands[i]
            write_console(f"Enter account number: {account_number}")
            i += 1

            # Optionally, check if there's another token for new plan.
            new_plan = None
            if i < len(commands):
                # If the next token is "SP" or "NP", assume it's the desired new plan.
                if commands[i] in ["SP", "NP"]:
                    new_plan = commands[i]
                    write_console(f"Enter new plan: {new_plan}")
                    i += 1

            
            # Perform the changeplan transaction.
            change_plan = ChangePlan(session_type, found_user, account_number, new_plan, write_console=write_console)
            result = change_plan.process_changeplan()
            if result != 1:
                continue  # Do not log a transaction output if changeplan failed.
            transaction_output = change_plan.return_transaction_output()
            log_transaction(transaction_output)
 
        elif command == "disable":
            if not logged_in:
                write_console("Error: You must be logged in to perform transactions.")
                continue

            if session_type != "admin":
                write_console("Error: This is a privileged transaction that requires admin mode.")
                continue

            # Get the account holder name from the input file.
            if i >= len(commands):
                write_console("Error: Missing account holder name for disable.")
                errorEnd()
                break
            account_holder_name = commands[i]
            write_console(f"Enter account holder name: {account_holder_name}")
            i += 1

            # Preliminary check: verify the account holder name exists.
            found_user = None
            for user in USERS.values():
                if user.user_name.strip().lower() == account_holder_name.lower():
                    found_user = user
                    break

            if found_user is None:
                write_console("Error: Account holder name not found.")
                continue

            # Get the account number from the input file.
            if i >= len(commands):
                write_console("Error: Missing account number for disable.")
                errorEnd()
                break
            account_number = commands[i]
            write_console(f"Enter account number: {account_number}")
            i += 1

            # Create and process the Disable transaction.
            disable_txn = Disable(session_type, account_holder_name, account_number, USERS, write_console=write_console)
            result = disable_txn.process_disable()
            if result != 1:
                continue  # If disable failed, do not log a transaction output.

            # Log the transaction output.
            transaction_output = disable_txn.return_transaction_output()
            if transaction_output:
                log_transaction(transaction_output)
 
        elif command == "logout":
            # Create a Logout transaction instance using current session info, passing write_console.
            logout_txn = Logout(logged_in, session_type, current_user, write_console=write_console)
            
            # Process logout; if successful, log the transaction and clear session state.
            if logout_txn.process_logout():
                out_line = logout_txn.return_transaction_output()
                log_transaction(out_line)
                write_console("Session terminated.")
                logged_in = False
                current_user = None
                session_type = None

        else:
            pass
            
    # Cleanup
    out_file.close()
    etf_file.close()      

if __name__ == "__main__":
    # banking_system()
    """
    Now we expect four arguments, e.g.:
    python3 main.py current_accounts_file.txt \
                   inputs/02_transfer_inputs/transfer_01.inp \
                   outputs/02_transfer_outputs/02_test01.out \
                   transaction_outputs/02_transfer_transaction_outputs/02_test01.etf

    Where:
      1) current_accounts_file.txt => your user data
      2) inputs/02_transfer_inputs/transfer_01.inp => commands script
      3) outputs/02_transfer_outputs/02_test01.out => console/log output
      4) transaction_outputs/02_transfer_transaction_outputs/02_test01.etf => transaction logs
    """
    if len(sys.argv) < 5:
        print("Usage: python3 main.py <accounts_file> <commands_file> <console_out_file> <transaction_out_file>")
        sys.exit(1)

    accounts_file       = sys.argv[1]  # e.g. "current_accounts_file.txt"
    commands_file       = sys.argv[2]  # e.g. "transfer_01.inp"
    console_out_file    = sys.argv[3]  # e.g. "02_test01.out"
    etf_file            = sys.argv[4]  # e.g. "02_test01.etf"

    banking_system(accounts_file, commands_file, console_out_file, etf_file)