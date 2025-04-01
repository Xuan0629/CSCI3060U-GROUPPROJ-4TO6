import pytest
from write_new_master_bank_accounts import write_new_master_bank_accounts
import os

# Test data setup
def create_test_account(account_number, name, status, balance, transactions, plan):
    """Helper function to create test account dictionaries"""
    return {
        'account_number': account_number,
        'name': name,
        'status': status,
        'balance': balance,
        'total_transactions': transactions,
        'plan': plan
    }

# Decision Coverage Tests
def test_account_number_validation():
    """
    Test account number validation:
    - Non-string account number
    - Non-digit account number
    - Account number longer than 5 digits
    """
    invalid_accounts = [
        # Test non-string account number
        create_test_account(12345, "Test Name", "A", 1000.00, 0, "NP"),
        # Test non-digit account number
        create_test_account("abcde", "Test Name", "A", 1000.00, 0, "NP"),
        # Test account number longer than 5 digits
        create_test_account("123456", "Test Name", "A", 1000.00, 0, "NP")
    ]
    
    for account in invalid_accounts:
        with pytest.raises(ValueError):
            write_new_master_bank_accounts([account], "test_write_new_master_bank_accounts_output.txt")

def test_name_validation():
    """
    Test name validation:
    - Name longer than 20 characters
    """
    invalid_account = create_test_account(
        "00001", 
        "This is a very long name that exceeds 20 characters", 
        "A", 
        1000.00, 
        0, 
        "NP"
    )
    
    with pytest.raises(ValueError):
        write_new_master_bank_accounts([invalid_account], "test_write_new_master_bank_accounts_output.txt")

def test_status_validation():
    """Test status validation:
    - Invalid status (not 'A' or 'D')
    """
    invalid_account = create_test_account("00001", "Test Name", "X", 1000.00, 0, "NP")
    
    with pytest.raises(ValueError):
        write_new_master_bank_accounts([invalid_account], "test_write_new_master_bank_accounts_output.txt")

def test_balance_validation():
    """
    Test balance validation:
    - Non-numeric balance
    - Balance greater than 99999.99
    - Negative balance
    """
    invalid_accounts = [
        # Test non-numeric balance
        create_test_account("00001", "Test Name", "A", "1000.00", 0, "NP"),
        # Test balance > 99999.99
        create_test_account("00001", "Test Name", "A", 100000.00, 0, "NP"),
        # Test negative balance
        create_test_account("00001", "Test Name", "A", -1000.00, 0, "NP")
    ]
    
    for account in invalid_accounts:
        with pytest.raises(ValueError):
            write_new_master_bank_accounts([account], "test_write_new_master_bank_accounts_output.txt")

def test_transaction_count_validation():
    """
    Test transaction count validation:
    - Non-integer transaction count
    - Transaction count greater than 9999
    - Negative transaction count
    """
    invalid_accounts = [
        # Test non-integer transaction count
        create_test_account("00001", "Test Name", "A", 1000.00, "0", "NP"),
        # Test transaction count > 9999
        create_test_account("00001", "Test Name", "A", 1000.00, 10000, "NP"),
        # Test negative transaction count
        create_test_account("00001", "Test Name", "A", 1000.00, -1, "NP")
    ]
    
    for account in invalid_accounts:
        with pytest.raises(ValueError):
            write_new_master_bank_accounts([account], "test_write_new_master_bank_accounts_output.txt")

def test_plan_validation():
    """
    Test plan type validation:
    - Invalid plan type (not 'SP' or 'NP')
    """
    invalid_account = create_test_account("00001", "Test Name", "A", 1000.00, 0, "XX")
    
    with pytest.raises(ValueError):
        write_new_master_bank_accounts([invalid_account], "test_write_new_master_bank_accounts_output.txt")

# Loop Coverage Tests
def test_empty_account_list():
    """Test handling of empty account list"""
    write_new_master_bank_accounts([], "test_write_new_master_bank_accounts_output.txt")
    with open("test_write_new_master_bank_accounts_output.txt", "r") as f:
        content = f.read()
        assert "00000 END OF FILE          A 00000.00 0000 NP" in content

def test_single_account():
    """Test writing a single account"""
    account = create_test_account("00001", "Test Name", "A", 1000.00, 0, "NP")
    write_new_master_bank_accounts([account], "test_write_new_master_bank_accounts_output.txt")
    with open("test_write_new_master_bank_accounts_output.txt", "r") as f:
        content = f.read()
        assert "00001 Test Name            A 01000.00 0000 NP" in content

def test_multiple_accounts():
    """Test writing multiple accounts"""
    accounts = [
        create_test_account("00001", "First Account", "A", 1000.00, 0, "NP"),
        create_test_account("00002", "Second Account", "A", 2000.00, 0, "SP"),
        create_test_account("00003", "Third Account", "A", 3000.00, 0, "NP")
    ]
    write_new_master_bank_accounts(accounts, "test_write_new_master_bank_accounts_output.txt")
    with open("test_write_new_master_bank_accounts_output.txt", "r") as f:
        content = f.read()
        assert "00001 First Account        A 01000.00 0000 NP" in content
        assert "00002 Second Account       A 02000.00 0000 SP" in content
        assert "00003 Third Account        A 03000.00 0000 NP" in content

def test_boundary_values():
    """Test boundary values for all fields"""
    account = create_test_account(
        "99999",  # Maximum account number
        "Max Length Name Here",  # Maximum length name
        "A",
        99999.99,  # Maximum balance
        9999,  # Maximum transaction count
        "SP"
    )
    write_new_master_bank_accounts([account], "test_write_new_master_bank_accounts_output.txt")
    with open("test_write_new_master_bank_accounts_output.txt", "r") as f:
        content = f.read()
        assert "99999 Max Length Name Here A 99999.99 9999 SP" in content

# Cleanup test output after test since we do not need to check it
def teardown_module(module):
    """Clean up test files after all tests"""
    if os.path.exists("test_write_new_master_bank_accounts_output.txt"):
        os.remove("test_write_new_master_bank_accounts_output.txt")