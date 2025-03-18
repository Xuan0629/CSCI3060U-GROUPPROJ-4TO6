from read import read_old_bank_accounts, read_transaction_file
from print_error import log_constraint_error

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
        self.accounts = read_old_bank_accounts(filePath)
        # Convert account numbers to dictionary keys
        self.accounts = {acc['account_number']: acc for acc in self.accounts}

    def readTransactions(self, mergedTxnFile: str):
        """
        Reads the merged Bank Account Transaction file.
        Returns a list of Transaction objects.
        """
        return read_transaction_file(mergedTxnFile)

    def applyTransactions(self, transactions):
        """
        Applies each transaction in 'transactions' to the relevant accounts.
        Only validates transaction fees can be covered, all other validations
        are handled by the front end.
        """
        for txn in transactions:
            code = txn.code
            
            if code == "05":  # create (no fee)
                self.accounts[txn.acctNum] = {
                    'account_number': txn.acctNum,
                    'name': txn.name,
                    'status': 'A',
                    'balance': txn.amount,
                    'total_transactions': 0,
                    'plan': "NP"
                }
                continue

            # Handle account deletion 
            elif code == "06":  # delete (no fee)
                del self.accounts[txn.acctNum]
                continue

            # Get account and set fee
            account = self.accounts[txn.acctNum]
            feePerTransaction = 0.05 if account['plan'] == "SP" else 0.10
            # feePerTransaction = 0.05

            # Process different transaction types
            if code == "01":  # withdrawal
                newBalance = account['balance'] - txn.amount - feePerTransaction
                if newBalance < 0:
                    log_constraint_error("Constraint Error", f"Fee caused overdraw for account {account['account_number']}")
                    continue
                account['balance'] = newBalance
                account['total_transactions'] += 1
            
            elif code == "02":  # transfer
                newBalance = account['balance'] - txn.amount - feePerTransaction
                if newBalance < 0:
                    log_constraint_error("Constraint Error", f"Fee caused overdraw for account {account['account_number']}")
                    continue

                receiving_account = self.accounts["000" + txn.misc]
                
                account['balance'] = newBalance
                account['total_transactions'] += 1

                receiving_account['balance'] += txn.amount
                receiving_account['total_transactions'] += 1

            elif code == "03":  # paybill
                newBalance = account['balance'] - txn.amount - feePerTransaction
                if newBalance < 0:
                    log_constraint_error("Constraint Error", f"Fee caused overdraw for account {account['account_number']}")
                    continue

                company_account = self.accounts[self.company_accounts[txn.misc]]
                
                account['balance'] = newBalance
                account['total_transactions'] += 1

                company_account['balance'] += txn.amount
                company_account['total_transactions'] += 1

            elif code == "04":  # deposit
                account['balance'] += (txn.amount - feePerTransaction)
                account['total_transactions'] += 1

            elif code == "07":  # disable
                newBalance = account['balance'] - feePerTransaction
                if newBalance < 0:
                    log_constraint_error("Constraint Error", f"Fee caused overdraw for account {account['account_number']}")
                    continue
                account['status'] = 'D'
                account['balance'] = newBalance
                account['total_transactions'] += 1

            elif code == "08":  # changeplan
                newBalance = account['balance'] - feePerTransaction
                if newBalance < 0:
                    log_constraint_error("Constraint Error", f"Fee caused overdraw for account {account['account_number']}")
                    continue
                account['plan'] = txn.misc
                account['balance'] = newBalance
                account['total_transactions'] += 1