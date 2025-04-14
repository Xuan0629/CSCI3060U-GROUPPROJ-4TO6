from check import Check

class Disable:
    """
    Disable class to handle disabling a bank account.
    This transaction sets the account's status from active (A) to disabled (D)
    and is a privileged transaction (admin only).

    Transaction output format (fixed-length, 40 chars):
      CC_AAAAAAAAAAAAAAAAAAAA_NNNNN_PPPPPPPP_MM
    where:
      - CC = "07" for disable
      - AAAAAAAAAAAAAAAAAAAA = account holder's name (left-justified, padded)
      - NNNNN = 5-digit account number (right-justified)
      - PPPPPPPP = "00000.00" (since no funds are involved)
      - MM = new status ("D", padded to 2 characters, e.g. "D_")
    """

    def __init__(self, userType, provided_account_holder, provided_account_number, users, write_console=None):
        """
        :param userType: Session type; must be "admin" for this transaction.
        :param provided_account_holder: The account holder name provided by the user.
        :param provided_account_number: The account number provided by the user.
        :param users: Dictionary of User objects keyed by account number.
        :param write_console: Callback to write output messages. Defaults to print if not provided.
        """
        self.userType = userType
        self.provided_account_holder = provided_account_holder
        self.provided_account_number = provided_account_number
        self.users = users
        self.check = Check()
        self.user = None  # Will hold the actual User object if found
        self.write_console = write_console if write_console is not None else print

    def process_disable(self):
        """Performs validations and disables the account if all checks pass.
           Returns 1 if successful, 0 otherwise.
        """
        if self.userType != "admin":
            self.write_console("Error: Disable transaction requires admin privileges.")
            return 0

        # 1. Check if an account with the provided name exists.
        found_user = None
        for user in self.users.values():
            if user.user_name.strip().lower() == self.provided_account_holder.lower():
                found_user = user
                break

        if found_user is None:
            self.write_console("Error: Account holder name not found.")
            return 0

        # 2. Check if the provided account number matches that account.
        if found_user.account_number != self.provided_account_number:
            self.write_console("Error: Provided account number does not match the account holder name.")
            return 0

        # Set the found user.
        self.user = found_user

        # 3. Check if the account is already disabled.
        if not self.check.availability_check(self.user):
            self.write_console(f"Error: Account {self.user.account_number} is already disabled.")
            return 0

        # 4. Disable the account.
        self.user.availability = "D"
        self.write_console(f"Account {self.user.account_number} ({self.user.user_name}) has been disabled.")
        return 1

    def return_transaction_output(self):
        """
        Returns the fixed-length transaction output string for a disable transaction:
        07_{username padded}_NNNNN_00000.00_D_
        """
        if self.user is None:
            return ""
        formatted_username = self.user.user_name.replace(" ", "_").ljust(20, "_")
        # Format amount to have 5 digits before decimal
        formatted_amount = "00000.00"
        transaction_output = (
            f"07_{formatted_username}"
            f"{self.user.account_number:>5}_"
            f"{formatted_amount}_D_"
        )
        return transaction_output
