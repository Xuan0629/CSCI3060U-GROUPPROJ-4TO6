from read import read_old_bank_accounts
from print_error import log_constraint_error
from transaction import Transaction

class TransactionProcessor:
    """
    Coordinates loading the Old Master Bank Accounts, reading the
    merged transaction file, applying all transactions, and then
    writing out the New Master and New Current files.
    """

    def __init__(self):
        # Dictionary of accountNumber -> account_info
        self.accounts = {}
        # Dictionary of company codes -> company account numbers
        self.company_accounts = {
            'EC': '10000',  # EC company account
            'CQ': '20000',  # CQ company account
            'FI': '30000'   # FI company account
        }

    def loadMasterAccounts(self, filePath: str):
        """
        Reads the old master bank accounts file using read.py implementation.
        Populates self.accounts with account dictionaries.
        """
        # DEBUG: Print section header for master account loading
        print("\n=== Loading Master Accounts ===")
        accounts_list = read_old_bank_accounts(filePath)
        # DEBUG: Print number of accounts read
        print(f"Read {len(accounts_list)} accounts from file")

        # Convert account numbers to dictionary keys, ensuring 5-digit format
        self.accounts = {}
        for acc in accounts_list:
            # Convert account number to 5-digit format
            acc_num = acc['account_number'].zfill(5)
            acc['account_number'] = acc_num  # Update the account number in the dictionary
            self.accounts[acc_num] = acc
            # DEBUG: Print each account as it's loaded
            print(f"Loaded account: {acc_num} (original: {acc['account_number']})")

        # DEBUG: Print final list of account numbers
        print(f"Final accounts dictionary keys: {list(self.accounts.keys())}")
        # DEBUG: Print section footer
        print("=== End Loading Master Accounts ===\n")

    def readTransactions(self, mergedTxnFile: str):
        """
        Reads the merged Bank Account Transaction file.
        Returns a list of Transaction objects.
        """
        # DEBUG: Print section header for transaction reading
        print("\n=== Reading Transactions ===")
        transactions = Transaction.read_transaction_file(mergedTxnFile)
        # DEBUG: Print number of transactions read
        print(f"Read {len(transactions)} transactions")
        # DEBUG: Print details of each transaction
        for txn in transactions:
            print(f"Transaction: code={txn.code}, account={txn.acctNum}, amount={txn.amount}, misc={txn.misc}")
        # DEBUG: Print section footer
        print("=== End Reading Transactions ===\n")
        return transactions

    def applyTransactions(self, transactions):
        """
        Applies each transaction in 'transactions' to the relevant accounts.
        Only validates transaction fees can be covered, all other validations
        are handled by the front end.
        """
        # DEBUG: Print section header for transaction processing
        print("\n=== Applying Transactions ===")
        for txn in transactions:
            code = txn.code
            acct_num = txn.acctNum

            # DEBUG: Print transaction being processed and available accounts
            print(f"\nProcessing transaction: code={code}, account={acct_num}")
            print(f"Available accounts: {list(self.accounts.keys())}")

            if code == "05":  # create (no fee)
                # DEBUG: Print account creation
                print(f"Creating new account: {acct_num}")
                self.accounts[acct_num] = {
                    'account_number': acct_num,
                    'name': txn.name.replace("_", " "),
                    'status': 'A',
                    'balance': txn.amount,
                    'total_transactions': 0,
                    'plan': "NP"
                }
                continue

            elif code == "06":  # delete (no fee)
                # DEBUG: Print account deletion attempt
                print(f"Attempting to delete account: {acct_num}")
                if acct_num in self.accounts:
                    del self.accounts[acct_num]
                    # DEBUG: Print successful deletion
                    print(f"Account {acct_num} deleted")
                else:
                    # DEBUG: Print failed deletion
                    print(f"Account {acct_num} not found for deletion")
                continue

            # Get account and set fee
            if acct_num not in self.accounts.values():
                # DEBUG: Print account not found error
                print(f"ERROR: Account {acct_num} not found in accounts dictionary")
                print(f"Available accounts: {list(self.accounts.keys())}")
                log_constraint_error("Constraint Error", f"Account {acct_num} not found")
                continue
                
            account = self.accounts
            feePerTransaction = 0.05 if account['plan'] == "SP" else 0.10
            # DEBUG: Print account details and fee
            print(f"Found account: {acct_num}, balance={account['balance']}, fee={feePerTransaction}")

            # Process different transaction types
            if code == "01":  # withdrawal
                newBalance = account['balance'] - txn.amount - feePerTransaction
                if newBalance < 0:
                    # DEBUG: Print overdraw error
                    print(f"ERROR: Overdraw attempt on account {acct_num}")
                    log_constraint_error("Constraint Error", f"Fee caused overdraw for account {account['account_number']}")
                    continue
                account['balance'] = newBalance
                account['total_transactions'] += 1
                # DEBUG: Print withdrawal result
                print(f"Withdrawal: new balance={newBalance}")

            elif code == "02":  # transfer
                newBalance = account['balance'] - txn.amount - feePerTransaction
                if newBalance < 0:
                    # DEBUG: Print overdraw error
                    print(f"ERROR: Overdraw attempt on account {acct_num}")
                    log_constraint_error("Constraint Error", f"Fee caused overdraw for account {account['account_number']}")
                    continue

                receiving_acct_num = txn.misc
                # DEBUG: Print transfer details
                print(f"Transfer to account: {receiving_acct_num}")
                if receiving_acct_num not in self.accounts:
                    # DEBUG: Print receiving account not found error
                    print(f"ERROR: Receiving account {receiving_acct_num} not found")
                    print(f"Available accounts: {list(self.accounts.keys())}")
                    log_constraint_error("Constraint Error", f"Receiving account {receiving_acct_num} not found")
                    continue

                receiving_account = self.accounts[receiving_acct_num]

                account['balance'] = newBalance
                account['total_transactions'] += 1
                receiving_account['balance'] += txn.amount
                receiving_account['total_transactions'] += 1
                # DEBUG: Print transfer result
                print(f"Transfer complete: from={acct_num}({newBalance}), to={receiving_acct_num}({receiving_account['balance']})")

            elif code == "03":  # paybill
                newBalance = account['balance'] - txn.amount - feePerTransaction
                if newBalance < 0:
                    # DEBUG: Print overdraw error
                    print(f"ERROR: Overdraw attempt on account {acct_num}")
                    log_constraint_error("Constraint Error", f"Fee caused overdraw for account {account['account_number']}")
                    continue

                company_account = self.accounts[self.company_accounts[txn.misc]]
                # DEBUG: Print bill payment details
                print(f"Paying bill to company: {txn.misc}")

                account['balance'] = newBalance
                account['total_transactions'] += 1
                company_account['balance'] += txn.amount
                company_account['total_transactions'] += 1
                # DEBUG: Print bill payment result
                print(f"Bill payment complete: account={acct_num}({newBalance}), company={txn.misc}({company_account['balance']})")

            elif code == "04":  # deposit
                account['balance'] += (txn.amount - feePerTransaction)
                account['total_transactions'] += 1
                # DEBUG: Print deposit result
                print(f"Deposit complete: account={acct_num}, new balance={account['balance']}")

            elif code == "07":  # disable
                newBalance = account['balance'] - feePerTransaction
                if newBalance < 0:
                    # DEBUG: Print overdraw error
                    print(f"ERROR: Overdraw attempt on account {acct_num}")
                    log_constraint_error("Constraint Error", f"Fee caused overdraw for account {account['account_number']}")
                    continue
                account['status'] = 'D'
                account['balance'] = newBalance
                account['total_transactions'] += 1
                # DEBUG: Print account disable result
                print(f"Account disabled: {acct_num}, new balance={newBalance}")

            elif code == "08":  # changeplan
                newBalance = account['balance'] - feePerTransaction
                if newBalance < 0:
                    # DEBUG: Print overdraw error
                    print(f"ERROR: Overdraw attempt on account {acct_num}")
                    log_constraint_error("Constraint Error", f"Fee caused overdraw for account {account['account_number']}")
                    continue
                account['plan'] = txn.misc
                account['balance'] = newBalance
                account['total_transactions'] += 1
                # DEBUG: Print plan change result
                print(f"Plan changed: account={acct_num}, new plan={txn.misc}, new balance={newBalance}")

        # DEBUG: Print section footer
        print("\n=== End Applying Transactions ===\n")