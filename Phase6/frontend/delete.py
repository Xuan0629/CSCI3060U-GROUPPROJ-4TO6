from check import Check

class Delete:
    """
    This class handles the deletion of user accounts. 
    Only administrators are allowed to delete accounts.
    """

    def __init__(self, userType, accounts, write_console=None, transaction_file="daily_transaction_file.txt"):
        """
        Initializes the Delete class.

        Parameters:
        - userType (str): Specifies whether the user is an 'admin' or 'user'.
        - accounts (dict): Dictionary containing existing accounts.
        - write_console (function): Function to write to the console (default: print).
        - transaction_file (str): File where transactions are logged (default: "daily_transaction_file.txt").
        """
        self.userType = userType
        self.accounts = accounts
        self.write_console = write_console
        self.transaction_file = transaction_file
        self.check = Check()

        if write_console is None:
            def _default_console(msg): pass
            self.write_console = _default_console
        else:
            self.write_console = write_console

    def process_deletion(self, account_holder_name, account_number):
        """
        Handles the account deletion process.

        Steps:
        1. Ensures that only an admin can delete accounts.
        2. Takes input for the account holder's name and account number.
        3. Checks if the provided account exists and belongs to the entered user.
        4. If valid, logs the deletion transaction and removes the account.
        """

        if self.userType != "admin":
            self.write_console("Error: Only admins can delete accounts.")
            return None

        if not account_holder_name:
            self.write_console("Error: Account holder name cannot be empty.")
            return None

        account_found = None
        if account_number in self.accounts and self.accounts[account_number].user_name.strip() == account_holder_name:
            account_found = self.accounts[account_number]

        if not account_found:
            self.write_console(f"Error: No account found for {account_holder_name} with account number {account_number}.")
            return None

        transaction_output = self.return_transaction_output(account_found)
        self.log_transaction(transaction_output)

        del self.accounts[account_number]

        self.write_console(f"Account with account number {account_number} has been deleted successfully.")
        return transaction_output

    def return_transaction_output(self, deleted_account):
        """
        Formats the transaction output for logging.

        Parameters:
        - deleted_account (dict): The account that is being deleted.

        Returns:
        - str: A formatted transaction string representing the deletion.
        """

        formatted_username = deleted_account.user_name.replace(" ", "_").ljust(20, "_")
        # Format amount to have 5 digits before decimal
        formatted_amount = "00000.00"

        transaction_output = (
            f"06_{formatted_username}"
            f"{deleted_account.account_number:>5}_"
            f"{formatted_amount}_00"
        )
        return transaction_output

    def log_transaction(self, transaction_output):
        """
        Logs the transaction details to the daily transaction file.

        Parameters:
        - transaction_output (str): The formatted transaction string to be recorded.
        """

        with open(self.transaction_file, "a") as file:
            file.write(transaction_output + "\n")