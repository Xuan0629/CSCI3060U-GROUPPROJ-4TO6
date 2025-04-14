from check import Check

class Create:
    """
    A class to handle the creation of new user accounts.
    Only admins can create new accounts.
    """
    def __init__(self, userType, accounts, account_holder_name, initial_balance, transaction_file="daily_transaction_file.txt", write_console=None):
        """
        Initializes the Create class.
        
        :param userType: The type of user (should be 'admin' for account creation).
        :param accounts: A dictionary containing existing accounts.
        :param account_holder_name: Name of the new account holder.
        :param initial_balance: The initial balance for the account.
        :param transaction_file: The file where transaction logs are stored.
        :param write_console: Function to handle console output.
        """
        self.userType = userType
        self.accounts = accounts
        self.account_holder_name = account_holder_name
        self.initial_balance = initial_balance
        self.transaction_file = transaction_file
        self.check = Check()

        # Provide a default no-op if not given
        if write_console is None:
            def _default_console(msg): pass
            self.write_console = _default_console
        else:
            self.write_console = write_console

    def process_creation(self):
        """
        Handles the process of creating a new account.
        Ensures the user is an admin and validates input before account creation.
        """
        # Ensure only admins can create an account
        if self.userType != "admin":
            self.write_console("Error: Only admins can create new accounts.")
            return None

        # Validate account holder name
        if not self.account_holder_name:
            self.write_console("Error: Account holder name cannot be empty.")
            return None
        if len(self.account_holder_name) > 20:
            self.write_console("Error: Account holder name must be at most 20 characters.")
            return None

        # Validate balance
        if not self.check.negative_amount_check(self.initial_balance):
            self.write_console("Error: Balance cannot be negative.")
            return None
        if self.initial_balance > 99999.99:
            self.write_console("Error: Initial balance cannot exceed $99,999.99.")
            return None

        # Generate unique account number (ensures 5-digit format)
        account_number = str(len(self.accounts) + 1).zfill(5)

        # Create the new account entry
        new_account = {
            "account_number": account_number,
            "user_name": self.account_holder_name,
            "balance": self.initial_balance,
            "availability": "A",  # Mark the account as active
        }

        # Add the new account to the accounts dictionary
        self.accounts[account_number] = new_account

        # Log the transaction details
        transaction_output = self.return_transaction_output(new_account, self.initial_balance)
        self.log_transaction(transaction_output)

        self.write_console(f"Account created successfully for '{self.account_holder_name}' with initial balance of ${self.initial_balance}0.")
        return transaction_output  # Return transaction output for logging

    def return_transaction_output(self, new_account, initial_balance):
        """
        Formats the transaction output string for logging.
        
        :param new_account: The newly created account dictionary.
        :param initial_balance: The initial deposit balance.
        :return: Formatted transaction string.
        """
        formatted_username = new_account["user_name"].replace(" ", "_").ljust(20, "_")
        # Format amount to have 5 digits before decimal
        formatted_amount = f"{float(initial_balance):08.2f}"
        transaction_output = (
            f"05_{formatted_username}"
            f"{new_account['account_number']:>5}_"
            f"{formatted_amount}_00"
        )
        return transaction_output

    def log_transaction(self, transaction_output):
        """
        Logs the transaction into the daily transaction file.
        
        :param transaction_output: The formatted transaction string.
        """
        with open(self.transaction_file, "a") as file:
            file.write(transaction_output + "\n")