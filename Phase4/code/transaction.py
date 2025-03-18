from print_error import log_constraint_error

class Transaction:
    """
    Represents a single transaction record in the format:
    CC_AAAAAAAAAAAAAAAAAAAA_NNNNN_PPPPPPP_MM (40 chars total).
    """

    def __init__(self, code, name, acctNum, amount, misc):
        self.code = code
        self.name = name
        self.acctNum = acctNum
        self.amount = amount
        self.misc = misc

    @staticmethod
    def read_merged_transaction(line: str):
        """
        Parses a 40-char transaction line into a Transaction object.
        """
        if len(line) != 40:
            log_constraint_error("Fatal error", "Invalid transaction line length (expected 40).")
            return None

        # Extract fields using correct indices
        code = line[0:2]
        name = line[3:23].rstrip("_")
        acctNum = line[24:29]
        amountStr = line[30:37]
        misc = line[38:40]

        # Validate account number format
        if not acctNum.isdigit() or len(acctNum) != 5:
            log_constraint_error("Fatal error", f"Invalid account number format: {acctNum}")
            return None

        # Convert amountStr
        try:
            amount = float(amountStr)
        except ValueError:
            log_constraint_error("Fatal error", f"Could not parse transaction amount '{amountStr}'.")
            amount = 0.0

        return Transaction(code, name, acctNum, amount, misc)