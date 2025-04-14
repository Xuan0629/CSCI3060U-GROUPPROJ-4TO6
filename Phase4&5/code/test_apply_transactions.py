import pytest
from transaction_processor import TransactionProcessor
import os

#Identical to function created by Xuan in test_write_new_master_bank_account.py
def create_test_accounts(account_number, name, status, balance, transactions, plan):
    """Helper function to create test accounts"""
    return {
        'account_number': account_number,
        'name': name,
        'status': status,
        'balance': balance,
        'total_transactions': transactions,
        'plan': plan
    }

# New mock transaction class for better testing
class MockTransaction:
    """Mock transaction class for testing"""
    def __init__(self, code, acctNum, amount=0.0, name="", misc=""):
        self.code = code
        self.acctNum = acctNum
        self.amount = amount
        self.name = name
        self.misc = misc

def setup_module(module):
    """Setup function to create a new output file at the start of testing"""
    with open("test_apply_transactions_output.txt", "w") as f:
        f.write("=== Test Results ===\n\n")

def append_test_result(test_name, content):
    """Helper function to append test results to the output file"""
    with open("test_apply_transactions_output.txt", "a") as f:
        f.write(f"\n=== {test_name} ===\n")
        f.write(content)
        f.write("\n" + "="*50 + "\n")

def test_empty_list():
    """Test empty transaction list handling"""
    system = TransactionProcessor()
    #Test Case 01
    account = create_test_accounts(
        "12345",
        "Bob",
        "A",
        0.0,
        0,
        "NP"
    )
    system.accounts["12345"] = account
    # Empty transaction list should be processed without error
    system.applyTransactions([])
    result = f"Test Case 01:\nInitial balance: 0.25\nFinal balance: {system.accounts['12345']['balance']}"
    append_test_result("Empty Transaction List", result)
    assert system.accounts["12345"]["balance"] == 0.0

def test_withdrawal():
    """Test withdrawal transactions"""
    system = TransactionProcessor()
    results = []
    
    # Test Case 02: newBalance will be 0.0
    account = create_test_accounts(
        "12345",
        "Bob",
        "A",
        0.25,
        0,
        "NP"
    )
    system.accounts["12345"] = account
    txn1 = MockTransaction("01", "12345", 0.15)
    system.applyTransactions([txn1])
    results.append(f"Test Case 02:\nInitial balance: 0.25\nWithdrawal amount: 0.15\nFee: 0.10\nFinal balance: {system.accounts['12345']['balance']}")
    assert system.accounts["12345"]["balance"] == pytest.approx(0.0)

    # Test Case 03: newBalance will be 0.1
    account = create_test_accounts(
        "12345",
        "Bob",
        "A",
        0.25,
        0,
        "NP"
    )
    system.accounts["12345"] = account
    txn2 = MockTransaction("01", "12345", 0.05)
    system.applyTransactions([txn2])
    results.append(f"Test Case 03:\nInitial balance: 0.25\nWithdrawal amount: 0.05\nFee: 0.10\nFinal balance: {system.accounts['12345']['balance']}")
    assert system.accounts["12345"]["balance"] == pytest.approx(0.1)

    # Test Case 04: Will throw error as balance will be -0.1
    account = create_test_accounts(
        "12345",
        "Bob",
        "A",
        0.25,
        0,
        "NP"
    )
    system.accounts["12345"] = account
    txn3 = MockTransaction("01", "12345", 0.25)
    system.applyTransactions([txn3])
    results.append(f"Test Case 04:\nInitial balance: 0.25\nWithdrawal amount: 0.25\nFee: 0.10\nFinal balance: {system.accounts['12345']['balance']}\nNote: Transaction rejected due to insufficient funds")
    assert system.accounts["12345"]["balance"] == pytest.approx(0.25)

    append_test_result("Withdrawal Tests", "\n\n".join(results))

def test_transfer():
    """Test transfer transactions"""
    system = TransactionProcessor()
    results = []
    account1 = create_test_accounts(
        "12345",
        "Bob",
        "A",
        0.25,
        0,
        "NP"
    )
    account2 = create_test_accounts(
        "23456",
        "Alice",
        "A",
        0.0,
        0,
        "NP"
    )
    system.accounts["12345"] = account1
    system.accounts["23456"] = account2

    # # Test Case 05: Successful transfer
    txn = MockTransaction("02", "12345", 0.15, misc="23456")
    system.applyTransactions([txn])
    results.append(f"Test Case 05:\nSender initial balance: 0.25\nReceiver initial balance: 0.0\nTransfer amount: 0.15\nFee: 0.10\nSender final balance: {system.accounts['12345']['balance']}\nReceiver final balance: {system.accounts['23456']['balance']}")
    assert system.accounts["12345"]["balance"] == pytest.approx(0.0)
    assert system.accounts["23456"]["balance"] == pytest.approx(0.15)

    # Test Case 06: Unsuccessful transfer
    txn = MockTransaction("02", "12345", 0.15, misc="23456")
    system.applyTransactions([txn])
    results.append(f"Test Case 06:\nInitial balance: 0.0\nWithdrawal amount: 0.15\nFee: 0.10\nFinal balance: {system.accounts['12345']['balance']}\nNote: Transaction rejected due to insufficient funds")
    assert system.accounts["12345"]["balance"] == pytest.approx(0.0)
    assert system.accounts["23456"]["balance"] == pytest.approx(0.15)

    append_test_result("Transfer Tests", "\n\n".join(results))

def test_pay_bill():
    """Test bill payment transactions"""
    system = TransactionProcessor()
    results = []
    account = create_test_accounts(
        "12345",
        "Bob",
        "A",
        0.25,
        0,
        "NP"
    )
    system.accounts["12345"] = account
    
    # Add company account
    company_account = create_test_accounts(
        "10000",
        "EC",
        "A",
        0.0,
        0,
        "NP"
    )
    system.accounts["10000"] = company_account

    # Test Case 07: Successful bill payment
    txn = MockTransaction("03", "12345", 0.15, misc="EC")
    system.applyTransactions([txn])
    results.append(f"Test Case 07:\nPayer initial balance: 0.25\nCompany initial balance: 0.0\nPayment amount: 0.15\nFee: 0.10\nPayer final balance: {system.accounts['12345']['balance']}\nCompany final balance: {system.accounts['10000']['balance']}")
    assert system.accounts["12345"]["balance"] == pytest.approx(0.0)
    assert system.accounts["10000"]["balance"] == pytest.approx(0.15)

    # Test Case 08: Unsuccessful bill payment
    txn = MockTransaction("03", "12345", 0.15, misc="EC")
    system.applyTransactions([txn])
    results.append(
        f"Test Case 08:\nPayer initial balance: 0.25\nCompany initial balance: 0.0\nPayment amount: 0.15\nFee: 0.10\nPayer final balance: {system.accounts['12345']['balance']}\nCompany final balance: {system.accounts['10000']['balance']} Note: Transaction rejected due to insufficient funds")
    assert system.accounts["12345"]["balance"] == pytest.approx(0.0)
    assert system.accounts["10000"]["balance"] == pytest.approx(0.15)
    append_test_result("Bill Payment Tests", "\n\n".join(results))



def test_deposit():
    """Test deposit transactions"""
    system = TransactionProcessor()
    results = []
    account = create_test_accounts(
        "12345",
        "Bob",
        "A",
        0.05,
        0,
        "NP"
    )
    system.accounts["12345"] = account

    # Test Case 09: Successful deposit
    txn = MockTransaction("04", "12345", 0.15)
    system.applyTransactions([txn])
    results.append(f"Test Case 09:\nInitial balance: 0.05\nDeposit amount: 0.15\nFee: 0.10\nFinal balance: {system.accounts['12345']['balance']}")
    assert system.accounts["12345"]["balance"] == pytest.approx(0.10)

    append_test_result("Deposit Tests", "\n\n".join(results))

def test_create():
    """Test account creation transactions"""
    system = TransactionProcessor()
    results = []
    # Test Case 10: Create new account
    txn = MockTransaction("05", "54321", 0.0, name="Alice")
    system.applyTransactions([txn])
    results.append(f"Test Case 10:\nAccount number: 54321\nName: Alice\nInitial balance: {system.accounts['54321']['balance']}\nStatus: {system.accounts['54321']['status']}\nPlan: {system.accounts['54321']['plan']}")
    assert "54321" in system.accounts
    assert system.accounts["54321"]["balance"] == 0.0
    assert system.accounts["54321"]["name"] == "Alice"

    append_test_result("Account Creation Tests", "\n\n".join(results))

def test_delete():
    """Test account deletion transactions"""
    system = TransactionProcessor()
    results = []
    account = create_test_accounts(
        "12345",
        "Bob",
        "A",
        0.25,
        0,
        "NP"
    )
    system.accounts["12345"] = account

    # Test Case 11: Delete existing account
    txn = MockTransaction("06", "12345")
    results.append(f"Test Case 11:\nInitial account status: Account exists\nAccount number: 12345\nBalance: 0.25")
    system.applyTransactions([txn])
    results.append(f"Final account status: {'Account deleted' if '12345' not in system.accounts else 'Account still exists'}")
    assert "12345" not in system.accounts

    append_test_result("Account Deletion Tests", "\n\n".join(results))

def test_disable():
    """Test account disable transactions"""
    system = TransactionProcessor()
    results = []
    account = create_test_accounts(
        "12345",
        "Bob",
        "A",
        0.25,
        0,
        "NP"
    )
    system.accounts["12345"] = account

    # Test Case 12: Disable account with sufficient balance for fee
    txn = MockTransaction("07", "12345")
    system.applyTransactions([txn])
    results.append(f"Test Case 12:\nInitial status: Active\nInitial balance: 0.25\nFee: 0.10\nFinal status: {system.accounts['12345']['status']}\nFinal balance: {system.accounts['12345']['balance']}")
    assert system.accounts["12345"]["status"] == "D"
    assert system.accounts["12345"]["balance"] == pytest.approx(0.15)

    # Test Case 13: Disable account with insufficient balance for fee
    account = create_test_accounts(
        "12345",
        "Bob",
        "A",
        0.0,
        0,
        "NP"
    )
    system.accounts["12345"] = account

    txn = MockTransaction("07", "12345")
    system.applyTransactions([txn])
    results.append(
        f"Test Case 13:\nInitial status: Active\nInitial balance: 0.0\nFee: 0.10\nFinal status: {system.accounts['12345']['status']}\nFinal balance: {system.accounts['12345']['balance']} Note: Transaction rejected due to insufficient funds")
    assert system.accounts["12345"]["status"] == "A"
    assert system.accounts["12345"]["balance"] == pytest.approx(0.0)

    append_test_result("Account Disable Tests", "\n\n".join(results))

def test_changeplan():
    """Test plan change transactions"""
    system = TransactionProcessor()
    results = []
    account = create_test_accounts(
        "12345",
        "Bob",
        "A",
        0.25,
        0,
        "NP"
    )
    system.accounts["12345"] = account

    # Test Case 14: Change plan with sufficient balance for fee
    txn = MockTransaction("08", "12345", misc="SP")
    system.applyTransactions([txn])
    results.append(f"Test Case 14:\nInitial plan: NP\nInitial balance: 0.25\nFee: 0.10\nNew plan: {system.accounts['12345']['plan']}\nFinal balance: {system.accounts['12345']['balance']}")
    assert system.accounts["12345"]["plan"] == "SP"
    assert system.accounts["12345"]["balance"] == pytest.approx(0.15)

    # Test Case 15: Change plan with insufficient balance for fee
    account = create_test_accounts(
        "12345",
        "Bob",
        "A",
        0.0,
        0,
        "NP"
    )
    system.accounts["12345"] = account

    txn = MockTransaction("08", "12345", misc="SP")
    system.applyTransactions([txn])
    results.append(
        f"Test Case 15:\nInitial plan: NP\nInitial balance: 0.0\nFee: 0.10\nNew plan: {system.accounts['12345']['plan']}\nFinal balance: {system.accounts['12345']['balance']} Note: Transaction rejected due to insufficient funds")
    assert system.accounts["12345"]["plan"] == "NP"
    assert system.accounts["12345"]["balance"] == pytest.approx(0.0)

    append_test_result("Plan Change Tests", "\n\n".join(results))


def teardown_module(module):
    """Clean up temporary files after all tests"""
    if os.path.exists("temp_output.txt"):
        os.remove("temp_output.txt")

