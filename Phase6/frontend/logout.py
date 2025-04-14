from check import Check

class Logout:
    """
    Logout class to handle ending a Front End session.
    The logout transaction should only be processed if a user is logged in
    (either admin or standard). Once processed, the session is terminated and
    no further transactions should be accepted.
    
    The fixed-length logout transaction output format is:
      "00_________________________00000_00000.00__"
    where:
      - "00" is the transaction code for logout.
      - The following 21-character field is for the account holder's name (here blank/padded).
      - The next field is the 5-digit account number (here "00000").
      - The monetary field is "00000.00" (no funds involved).
      - The final 2 characters are unused (here "__").
    """
    
    def __init__(self, logged_in, session_type, current_user, write_console=None):
        """
        :param logged_in: Boolean indicating if a session is active.
        :param session_type: The session type ("admin" or "standard").
        :param current_user: The current User object (or None for admin sessions without a user).
        :param write_console: Callback function to write messages (defaults to print if not provided).
        """
        self.logged_in = logged_in
        self.session_type = session_type
        self.current_user = current_user
        self.check = Check()
        self.processed = False
        self.write_console = write_console if write_console is not None else print

    def process_logout(self):
        """
        Processes the logout transaction:
          - Verifies that a session is active.
          - Prevents multiple logout attempts in the same session.
          - Uses write_console() to output messages.
          
        Returns True if logout is successful, False otherwise.
        """
        if not self.logged_in:
            self.write_console("Error: You are not logged in.")
            return False

        if self.processed:
            self.write_console("Error: Logout has already been performed for this session.")
            return False

        
        self.processed = True
        return True

    def return_transaction_output(self):
        """
        Returns the fixed-length logout transaction string:
          "00_____________________00000_00000.00_00"
        """
        return "00_____________________00000_00000.00_00"
