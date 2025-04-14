"""
Check Class

This class provides various validation methods to ensure proper transaction processing in the banking system.
It includes methods for checking user account validity, balance sufficiency, transaction limits, and input correctness.
"""

class Check:
    """
    Provides validation checks for different banking transactions.
    """

    def user_check(self, user1, user2):
        """ Ensures that the two users involved in a transaction are not the same. """
        return user1.account_number != user2.account_number

    def availability_check(self, user):
        """ Checks if the user's account is active. """
        return user.availability == "A"

    def balance_check(self, user, amount):
        """ Verifies if the user's balance is sufficient for the transaction. """
        return user.balance >= amount

    def limit_check(self, amount, limit):
        """ Ensures that the transaction amount does not exceed the predefined limit. """
        return amount <= limit

    def negative_amount_check(self, amount):
        """ Checks if the transaction amount is positive. """
        return amount > 0

    def zero_amount_check(self, amount):
        """ Ensures the transaction amount is not zero. """
        return amount != 0

    def account_existence_check(self, user):
        """ Validates if the user account exists. """
        return user is not None

    def admin_override_check(self, user):
        """ Checks if the user has admin privileges. """
        return user.userType == "admin"

    def valid_company_check(self, company):
        """ Confirms that the provided company code is valid. """
        VALID_COMPANIES = ["EC", "CQ", "FI"]
        return company in VALID_COMPANIES

    def company_id_check(self, company):
        """ Retrieves the corresponding account ID for a given company code. """
        COMPANY_ACCOUNTS = {
            "EC": "10000",
            "CQ": "20000",
            "FI": "30000"
        }
        return COMPANY_ACCOUNTS.get(company)

    def invalid_character_check(self, value):
        """ Ensures that the value contains only numeric characters. """
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False

    def missing_input_check(self, **kwargs):
        """ Checks for missing input fields in a transaction. """
        missing_fields = [key for key, value in kwargs.items() if not value]
        if missing_fields:
            return False, missing_fields
        return True, ""

    def sender_account_match(self, user, sender_account):
        """ Verifies that the sender's account matches the logged-in user. """
        return user.account_number == sender_account
