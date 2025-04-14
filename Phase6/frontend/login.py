# Test Login

from check import Check


class Login:
    """
    A class to handle the login process for users.
    
    Attributes:
        userType (str): The type of user ('admin' or 'standard').
        user (object): The user object containing account details.
        logged_in (bool): A flag indicating whether the user is already logged in.
        check (Check): An instance of the Check class for user verification.
    """
    def __init__(self, userType, user, logged_in):
        self.userType = userType  # 'admin' or 'standard'
        self.user = user  # User object with account details
        self.logged_in = logged_in
        self.check = Check()

    def check_user_type(self):
        """
        Checks if the user type is valid ('admin' or 'standard').
        
        Returns:
            bool: True if the user type is valid, False otherwise.
        """
        if self.userType not in ["admin", "standard"]:
            print("Error: Invalid session type.")
            return False
        return True
    
    def check_username(self):
        """
        Verifies if the username exists in the system.
        
        Returns:
            bool: True if the username exists, False otherwise.
        """
        if not self.check.account_existence_check(self.user):
            print("Error: Invalid account holder name")
            return False
        return True
    
    def check_double_login(self):
        """
        Ensures the user is not already logged in.
        
        Returns:
            bool: True if the user is not logged in, False otherwise.
        """
        if self.logged_in:
            print("Error: You are already logged in.")
            return False
        return True

    def process_login(self):
        """
        Processes the login by verifying login conditions.
        Ensures the user is not already logged in, has a valid user type,
        and if the user is standard, their username exists.
        """
        if not self.check_double_login():
            return
        if not self.check_user_type():
            return
        if self.userType == "standard" and not self.check_username():
            return
        
    #     return self.return_transaction_output()
    
    # def return_transaction_output(self):
    #     formatted_username = self.user.user_name.replace(" ", "_").ljust(21, "_")
    #     transaction_output = (
    #         f"01_{formatted_username}_"
    #         f"{self.user.account_number:>5}_"
    #         f"{self.userType}"
    #     )
    #     return transaction_output

if __name__ == "__main__":
    print("Welcome to the banking system")
    userType = input("Enter session type: ")
    user_name = input("Enter account holder name: ")
    account_number = input("Enter account number: ")
    
    user = type("User", (object,), {"user_name": user_name, "account_number": account_number, "userType": userType})
    login_instance = Login(userType, user)
    login_instance.process_login()
