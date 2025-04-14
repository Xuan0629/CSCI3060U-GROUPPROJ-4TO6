from print_error import log_constraint_error

def write_new_master_bank_accounts(accounts, file_path):
    """
    Writes Master Bank Accounts File with strict format validation.
    Format: NNNNN AAAAAAAAAAAAAAAAAAAA S PPPPPPPP TTTT YY
    Where YY is either SP (student plan) or NP (non-student plan)
    Raises ValueError for invalid data to enable testing.
    """
    with open(file_path, 'w') as file:
        for acc in accounts:
            try:
                # Validate account number
                if not isinstance(acc['account_number'], str) or not acc['account_number'].isdigit():
                    log_constraint_error("Constraint Error", f"Invalid account number: {acc['account_number']}")
                    raise ValueError(f"Invalid account number: {acc['account_number']}")
                if len(acc['account_number']) > 5:
                    log_constraint_error("Constraint Error", f"Account number too long: {acc['account_number']}")
                    raise ValueError(f"Account number too long: {acc['account_number']}")

                # Validate name length
                if len(acc['name']) > 20:
                    log_constraint_error("Constraint Error", f"Name exceeds 20 characters: {acc['name']}")
                    raise ValueError(f"Name exceeds 20 characters: {acc['name']}")

                # Validate status
                if acc['status'] not in ('A', 'D'):
                    log_constraint_error("Constraint Error", f"Invalid status: {acc['status']}")
                    raise ValueError(f"Invalid status: {acc['status']}")

                # Validate balance
                if not isinstance(acc['balance'], (int, float)):
                    log_constraint_error("Constraint Error", f"Invalid balance type: {type(acc['balance'])}")
                    raise ValueError(f"Invalid balance type: {type(acc['balance'])}")
                if acc['balance'] > 99999.99 or acc['balance'] < 0:
                    log_constraint_error("Constraint Error", f"Balance out of range: {acc['balance']}")
                    raise ValueError(f"Balance out of range: {acc['balance']}")

                # Validate transaction count
                if not isinstance(acc['total_transactions'], int):
                    log_constraint_error("Constraint Error", f"Invalid transaction count type: {type(acc['total_transactions'])}")
                    raise ValueError(f"Invalid transaction count type: {type(acc['total_transactions'])}")
                if acc['total_transactions'] > 9999 or acc['total_transactions'] < 0:
                    log_constraint_error("Constraint Error", f"Transaction count out of range: {acc['total_transactions']}")
                    raise ValueError(f"Transaction count out of range: {acc['total_transactions']}")

                # Validate plan type
                if acc['plan'] not in ('SP', 'NP'):
                    log_constraint_error("Constraint Error", f"Invalid plan type: {acc['plan']}")
                    raise ValueError(f"Invalid plan type: {acc['plan']}")

                # Format fields
                acc_num = acc['account_number'].zfill(5)
                # name = acc['name'].ljust(20, '_')
                name = acc['name'].ljust(20, ' ')
                balance = f"{acc['balance']:08.2f}"
                transactions = str(acc['total_transactions']).zfill(4)

                file.write(f"{acc_num} {name} {acc['status']} {balance} {transactions} {acc['plan']}\n")

            except ValueError as e:
                # Let the ValueError propagate up after logging
                raise e
            
        # Add END OF FILE marker
        file.write("00000 END OF FILE          A 00000.00 0000 NP\n") 
