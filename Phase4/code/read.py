from print_error import log_constraint_error
from transaction import Transaction

def read_old_bank_accounts(file_path):
    """
    Reads and validates the bank account file format
    Returns list of accounts and prints fatal errors for invalid format
    Format: NNNNN_AAAAAAAAAAAAAAAAAAAA_S_PPPPPPPP_TTTT (42 chars total)
    """
    accounts = []
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, 1):
            # Remove newline but preserve other characters
            clean_line = line.rstrip('\n')
            
            # Validate line length
            if len(clean_line) != 42:
                log_constraint_error("Fatal error", f"Line {line_num}: Invalid length ({len(clean_line)} chars)")
                continue

            try:
                # Extract fields with positional validation
                account_number = clean_line[0:5]
                name = clean_line[6:26]
                status = clean_line[27]
                balance_str = clean_line[29:37]
                transactions_str = clean_line[38:42]

                # Validate account number format (5 digits)
                if not account_number.isdigit():
                    log_constraint_error("Fatal error", f"Line {line_num}: Invalid account number format")
                    continue

                # Validate status
                if status not in ('A', 'D'):
                    log_constraint_error("Fatal error", f"Line {line_num}: Invalid status '{status}'")
                    continue

                # Validate balance format (XXXXX.XX)
                if (len(balance_str) != 8 or 
                    balance_str[5] != '.' or 
                    not balance_str[:5].isdigit() or 
                    not balance_str[6:].isdigit()):
                    log_constraint_error("Fatal error", f"Line {line_num}: Invalid balance format")
                    continue

                # Validate transaction count format
                if not transactions_str.isdigit():
                    log_constraint_error("Fatal error", f"Line {line_num}: Invalid transaction count format")
                    continue

                # Convert numerical values
                balance = float(balance_str)
                transactions = int(transactions_str)

                # Validate business constraints
                if balance < 0:
                    log_constraint_error("Fatal error", f"Line {line_num}: Negative balance")
                    continue
                if transactions < 0:
                    log_constraint_error("Fatal error", f"Line {line_num}: Negative transaction count")
                    continue

                # Process name: remove trailing underscores but keep internal underscores
                processed_name = name.rstrip('_')

                accounts.append({
                    'account_number': account_number,  # Keep as 5-digit string
                    'name': processed_name,  # Keep underscores in name
                    'status': status,
                    'balance': balance,
                    'total_transactions': transactions,
                    'plan': "NP"  # Default to NP (Non student)
                })

            except Exception as e:
                log_constraint_error("Fatal error", f"Line {line_num}: Unexpected error: {str(e)}")
                continue

    return accounts

def read_transaction_file(file_path):
    """
    Reads the merged Bank Account Transaction file.
    Returns a list of Transaction objects.
    Stops reading when it encounters "00" at the start of a line.
    """
    transactions = []
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, 1):
            # Remove newline but preserve other characters
            clean_line = line.rstrip('\n')
            
            # Check for end of transaction marker
            if clean_line.startswith("00"):
                break

            # Use Transaction class to parse the line
            txn = Transaction.read_merged_transaction(clean_line)
            if txn is not None:
                transactions.append(txn)
            else:
                log_constraint_error("Fatal error", f"Line {line_num}: Invalid transaction format")

    return transactions
