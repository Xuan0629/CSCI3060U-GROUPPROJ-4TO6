from check import Check

class ChangePlan:
    """
    ChangePlan class to handle changing the transaction payment plan for a bank account.
    This transaction toggles the account's plan from Student Plan (SP) to Non-Student Plan (NP)
    (or vice versa) or sets it explicitly. It is a privileged transaction and must be executed
    in admin mode.
    
    Transaction output format (fixed-length, 40 chars):
      CC_AAAAAAAAAAAAAAAAAAAA_NNNNN_PPPPPPPP_MM
    where:
      - CC = "08" for changeplan
      - AAAAAAAAAAAAAAAAAAAA = account holder's name (left-justified, padded)
      - NNNNN = 5-digit account number
      - PPPPPPPP = "00000.00" (since no funds are moved)
      - MM = new plan ("SP" or "NP")
    """

    def __init__(self, userType, user, provided_account_number, new_plan=None, write_console=None):
        """
        :param userType: "admin" or "standard" (must be admin for this transaction)
        :param user: The User object whose plan we are changing
        :param provided_account_number: The account number provided as input
        :param new_plan: Optional. The desired new plan "SP" or "NP". If None, toggles the current plan.
        :param write_console: Optional callback for writing to the console output.
        """
        self.userType = userType
        self.user = user
        self.provided_account_number = provided_account_number
        self.new_plan = new_plan
        self.check = Check()
        # Use the provided write_console function; if none provided, default to print.
        self.write_console = write_console if write_console is not None else print


    # def process_changeplan(self):
    #     """Performs checks and changes the user's plan if valid."""
    #     if self.userType != "admin":
    #         print("Error: Change plan transaction requires admin privileges.")
    #         return

    #     if not self.check.account_existence_check(self.user):
    #         print("Error: Account does not exist.")
    #         return

    #     if not self.check.availability_check(self.user):
    #         print(f"Error: Account {self.user.account_number} is disabled. Cannot change plan.")
    #         return

    #     # Check if provided account number matches the user's actual account number.
    #     if self.user.account_number != self.provided_account_number:
    #         print("Error: The account number does not match the account holder name.")
    #         return

    #     # Get the current plan; if not set, assume 'SP'
    #     current_plan = getattr(self.user, 'plan', 'SP')
        
    #     # Determine the new plan (toggle if none provided)
    #     if self.new_plan is None:
    #         new_plan = "NP" if current_plan == "SP" else "SP"
    #     else:
    #         if self.new_plan not in ["SP", "NP"]:
    #             print("Error: Invalid plan provided. Must be 'SP' or 'NP'.")
    #             return
    #         new_plan = self.new_plan

    #     # Update the user's plan.
    #     self.user.plan = new_plan
    #     print(f"Plan change successful. New plan for account {self.user.account_number} is {new_plan}.")

    def process_changeplan(self):
        """Performs checks and changes the user's plan if valid.
        Returns 1 if successful, 0 otherwise.
        """
        if self.userType != "admin":
            self.write_console("Error: Change plan transaction requires admin privileges.")
            return 0

        if not self.check.account_existence_check(self.user):
            self.write_console("Error: Account does not exist.")
            return 0

        if not self.check.availability_check(self.user):
            self.write_console(f"Error: Account {self.user.account_number} is disabled. Cannot change plan.")
            return 0

        # Check if provided account number matches the user's actual account number.
        if self.user.account_number != self.provided_account_number:
            self.write_console("Error: The account number does not match the account holder name.")
            return 0

        current_plan = getattr(self.user, 'plan', 'SP')
        
        if self.new_plan is None:
            new_plan = "NP" if current_plan == "SP" else "SP"
        else:
            if self.new_plan not in ["SP", "NP"]:
                self.write_console("Error: Invalid plan provided. Must be 'SP' or 'NP'.")
                return 0
            new_plan = self.new_plan

        self.user.plan = new_plan
        self.write_console(f"Plan change successful. New plan for account {self.user.account_number} is {new_plan}.")
        return 1


    def return_transaction_output(self):
        """Returns the formatted transaction output for logging."""
        formatted_username = self.user.user_name.replace(" ", "_").ljust(20, "_")
        plan = getattr(self.user, 'plan', 'SP')
        # Format amount to have 5 digits before decimal
        formatted_amount = "00000.00"
        transaction_output = (
            f"08_{formatted_username}"
            f"{self.user.account_number:>5}_"
            f"{formatted_amount}_"
            f"{plan}"
        )
        return transaction_output


