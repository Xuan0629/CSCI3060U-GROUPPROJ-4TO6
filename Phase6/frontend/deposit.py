from check import Check

class Deposit:
    """
    Handles deposit transactions for a user's account with input validation.
    """
    def __init__(self, userType, user, amount=None, write_console=None):
        """
        Initializes the Deposit class with user type, user details, deposit amount, and console output method.
        
        :param userType: str - Specifies whether the user is an 'admin' or a 'user'.
        :param user: User object - Contains user account details.
        :param amount: float (optional) - The amount to be deposited.
        :param write_console: function (optional) - Function to handle console output.
        """
        self.userType = userType
        self.user = user
        self.amount = amount
        self.check = Check()
        
        # Provide a default no-op if not given
        if write_console is None:
            def _default_console(msg): pass
            self.write_console = _default_console
        else:
            self.write_console = write_console

    def process_deposit(self):
        # Validate input fields
        all_inputs_valid, missing_fields = self.check.missing_input_check(
            user=self.user, amount=self.amount
        )
        if not all_inputs_valid:
            self.write_console(f"Error: The deposit {', '.join(missing_fields)} is missing, so the process will be rejected. Please re-try.")
            return

        # Validate deposit amount
        if not self.check.invalid_character_check(self.amount):
            self.write_console("Error: Invalid deposit amount. Amount must be numeric.")
            return
        if not self.check.negative_amount_check(self.amount):
            self.write_console("Error: Invalid deposit amount. Amount must be positive.")
            return
        if not self.check.zero_amount_check(self.amount):
            self.write_console("Error: Deposit amount must be greater than zero.")
            return

        # Check if the account is active
        if not self.check.availability_check(self.user):
            self.write_console("Error: Account is inactive. Please use an available account.")
            return

        # Process the deposit by updating the balance
        self.user.balance += self.amount

        if self.user.balance > 10000:
            self.write_console("Error: Cannot deposit more funds than accounts balance limit of 10000")
            return
            
        self.write_console(f"Deposit successful. Funds unavailable for this session. New balance: ${self.user.balance:.2f}")

        # Generate and return transaction log entry
        transaction_output = self.return_transaction_output()
        return transaction_output  # Return this so main.py can log it

    def return_transaction_output(self):
        formatted_username = self.user.user_name.replace(" ", "_").ljust(20, "_")
        # Format amount to have 5 digits before decimal
        formatted_amount = f"{float(self.amount):08.2f}"
        transaction_output = (
            f"04_{formatted_username}"
            f"{self.user.account_number:>5}_"
            f"{formatted_amount}_00"
        )
        return transaction_output