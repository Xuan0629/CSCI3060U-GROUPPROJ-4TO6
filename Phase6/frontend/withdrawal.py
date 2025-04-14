# Test withdrawal 
from check import Check


class Withdrawal:
    """
    A class to handle the withdrawal process for users.
    
    Attributes:
        user (object): The user object containing account details.
        amount (float): The amount to be withdrawn.
        check (Check): An instance of the Check class for verification checks.
    """
    def __init__(self, user, amount):
        self.user = user  # User object
        self.amount = amount  # Amount to be withdrawn
        self.check = Check()

    def check_account_number(self):
        """
        Checks if the user's account exists in the system.
        
        Returns:
            bool: True if the account exists, False otherwise.
        """
        if not self.check.account_existence_check(self.user):
            print("Error: Invalid account number.")
            return False
        return True

    def check_balance(self):
        """
        Verifies if the user has sufficient balance for the withdrawal.
        
        Returns:
            bool: True if the balance is sufficient, False otherwise.
        """
        if not self.check.balance_check(self.user, self.amount):
            print("Error: Account balance less than requested withdrawal amount.")
            return False
        return True

    def process_withdrawal(self):
        """
        Processes the withdrawal request by performing necessary validation checks.
        
        Validates missing input fields, invalid characters, negative amounts, 
        zero amounts, and account balance before proceeding with withdrawal.
        """
        # Basic input validation
        all_inputs_valid, missing_fields = self.check.missing_input_check(
            user=self.user,
            amount=self.amount
        )
        if not all_inputs_valid:
            print(f"Error: The withdrawal {', '.join(missing_fields)} is missing, so the process will be rejected. Please re-try.")
            return
        if not self.check.invalid_character_check(self.amount):
            print("Error: Invalid withdrawal amount. Amount must be numeric.")
            return
        if not self.check.negative_amount_check(self.amount):
            print("Error: Invalid withdrawal amount. Amount must be positive.")
            return
        if not self.check.zero_amount_check(self.amount):
            print("Error: Withdrawal amount must be greater than zero.")
            return
        if not self.check.balance_check(self.user, self.amount):
            print("Error: Account balance less than requested withdrawal amount.")
            return

        # Process withdrawal
        self.user.balance -= self.amount
        print(f"Withdrawal successful. New balance: ${self.user.balance:.2f}")
        return self.return_transaction_output()
    
    def return_transaction_output(self):
        """
        Generates a formatted transaction output string.
        
        Returns:
            str: A formatted transaction string with user details and withdrawal amount.
        """
        formatted_username = self.user.user_name.replace(" ", "_").ljust(20, "_")
        # Format amount to have 5 digits before decimal
        formatted_amount = f"{float(self.amount):08.2f}"
        transaction_output = (
            f"01_{formatted_username}"
            f"{self.user.account_number:>5}_"
            f"{formatted_amount}_00"
        )
        return transaction_output