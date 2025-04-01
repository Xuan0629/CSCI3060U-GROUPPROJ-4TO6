import sys
from transaction_processor import TransactionProcessor
from write import write_new_current_accounts
from write_new_master_bank_accounts import write_new_master_bank_accounts

def main():
    """
    Main function that orchestrates the back end processing of the bank accounts.
    Takes in 4 command line arguments:
    - oldMasterFile: path to the old master bank accounts file
    - mergedTxnFile: path to the merged bank account transactions file
    - newMasterFile: path to the new master bank accounts file
    - newCurrentFile: path to the new current bank accounts file
    
    Test way:
    delete all contents in the two .txt files starting with "new", then run:
    cd <path_to_this_folder>
    python3 main.py test_old_master.txt test_merged_txns.txt new_master_account.txt new_current_account.txt
    """
    if len(sys.argv) < 5:
        print("Usage: python3 main.py <oldMasterFile> <mergedTxnFile> <newMasterFile> <newCurrentFile>")
        sys.exit(1)

    oldMasterFile  = sys.argv[1]
    mergedTxnFile  = sys.argv[2]
    newMasterFile  = sys.argv[3]
    newCurrentFile = sys.argv[4]

    processor = TransactionProcessor()
    processor.loadMasterAccounts(oldMasterFile)

    txns = processor.readTransactions(mergedTxnFile)
    processor.applyTransactions(txns)

    # Get sorted accounts list for writing
    sorted_accounts = sorted(processor.accounts.values(), key=lambda x: int(x['account_number']))
    
    # Master accounts already in correct format
    write_new_master_bank_accounts(sorted_accounts, newMasterFile)

    # Create current accounts format
    current_accounts = [
        {
            'account_number': acc['account_number'],
            'name': acc['name'],
            'status': acc['status'],
            'balance': acc['balance'],
            'plan': acc['plan']
        }
        for acc in sorted_accounts
    ]
    write_new_current_accounts(current_accounts, newCurrentFile)

    print("Back End processing complete.")

if __name__ == "__main__":
    main()
