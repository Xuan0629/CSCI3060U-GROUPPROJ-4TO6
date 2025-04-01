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
    def read_transaction_file(file_path):
        """
        Reads the merged Bank Account Transaction file.
        Returns a list of Transaction objects.
        Stops reading when it encounters "00" at the start of a line.
        """
        transactions = []
        with open(file_path, 'r') as file:
            for line_num, line in enumerate(file, 1):
                # Remove newline but preserve other characters
                clean_line = line.rstrip('\n')
                
                # Check for end of transaction marker
                if clean_line.startswith("00"):
                    break

                # Validate line length
                if len(clean_line) != 40:
                    log_constraint_error("Fatal error", f"Line {line_num}: Invalid transaction line length (expected 40).")
                    continue

                # Extract fields using correct indices
                code = clean_line[0:2]
                name = clean_line[3:23].rstrip("_")
                acctNum = clean_line[24:29]
                amountStr = clean_line[30:37]
                misc = clean_line[38:40]

                # Validate account number format
                if not acctNum.isdigit() or len(acctNum) != 5:
                    log_constraint_error("Fatal error", f"Line {line_num}: Invalid account number format: {acctNum}")
                    continue

                # Convert amountStr
                try:
                    amount = float(amountStr)
                except ValueError:
                    log_constraint_error("Fatal error", f"Line {line_num}: Could not parse transaction amount '{amountStr}'.")
                    continue

                transactions.append(Transaction(code, name, acctNum, amount, misc))

        return transactions