import pytest
from transaction_processor import TransactionProcessor

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

def test_empty_list():
    system = TransactionProcessor()
    system.accounts = create_test_accounts(
        '12345',
        "Bob",
        "A",
        0.25,
        0,
        "NP"
    )
    # Test Case 01
    # Should throw error as list of transactions is empty
    with pytest.raises(ValueError):
        system.applyTransactions([])

def test_withdrawal():
    #newBalance = account['balance'] - txn.amount - feePerTransaction
    system = TransactionProcessor()
    system.accounts = create_test_accounts(
        '12345',
        "Bob",
        "A",
        0.25,
        0,
        "NP"
    )

    # Test Case 02
    # newBalance will be 0.0
    txn1 = type('Txn', (),
                {'code': "01",
                 'acctNum': "12345",
                 'amount': 0.15})
    system.applyTransactions([txn1])
    assert system.accounts.get("balance") == pytest.approx(0.0)

    system.accounts = create_test_accounts(
        '12345',
        "Bob",
        "A",
        0.25,
        0,
        "NP"
    )

    # Test Case 03
    # newBalance will be 0.1
    txn2 = type('Txn', (),
                {'code': "01",
                 'acctNum': "12345",
                 'amount': 0.05})
    system.applyTransactions([txn2])
    assert system.accounts.get("balance") == pytest.approx(0.1)

    system.accounts = create_test_accounts(
        '12345',
        "Bob",
        "A",
        0.25,
        0,
        "NP"
    )

    # Test Case 04
    # Will throw error as balance will be -0.1
    txn3 = type('Txn', (),
                {'code': "01",
                 'acctNum': "12345",
                 'amount': 0.25})
    with pytest.raises(ValueError, match="overdraw"):
        system.applyTransactions([txn3])
    assert system.accounts["12345"]["balance"] == pytest.approx(0.25)

def test_transfer():
    #newBalance = account['balance'] - txn.amount - feePerTransaction
    system = TransactionProcessor()
    system.accounts = create_test_accounts(
        '12345',
         "Bob",
         "A",
         0.25,
         0,
         "NP"
    )

    # Test Case 05
    # newBalance will be 0.0
    txn1 = type('Txn', (),
                {'code': "02",
                 'acctNum': "12345",
                 'amount': 0.15,
                 'misc': '23456'})
    system.applyTransactions([txn1])

    assert system.accounts.get("balance") == pytest.approx(0.0)

    # Test Case 06
    # newBalance will be 0.1
    txn2 = type('Txn', (),
                {'code': "02",
                 'acctNum': "12345",
                 'amount': 0.05})
    system.applyTransactions([txn2])
    assert system.accounts.get("balance") == pytest.approx(0.1)

    # # Test Case 07
    # # Will throw error as balance will be -0.1
    txn3 = type('Txn', (),
                {'code': "02",
                 'acctNum': "12345",
                 'amount': 0.25})
    with pytest.raises(ValueError, match="overdraw"):
        system.applyTransactions([txn3])
    assert system.accounts.get("balance") == pytest.approx(0.25)


def test_pay_bill():
    #newBalance = account['balance'] - txn.amount - feePerTransaction
    system = TransactionProcessor()
    system.accounts = create_test_accounts(
        '12345',
        "Bob",
        "A",
        0.25,
        0,
        "NP"
    )

    # Test Case 08
    # newBalance will be 0.0
    txn1 = type('Txn', (),
                {'code': "03",
                 'acctNum': "12345",
                 'amount': 0.15})
    system.applyTransactions([txn1])
    assert system.accounts.get("balance") == pytest.approx(0.0)

    system.accounts = create_test_accounts(
        '12345',
        "Bob",
        "A",
        0.25,
        0,
        "NP"
    )

    # Test Case 09
    # newBalance will be 0.1
    txn2 = type('Txn', (),
                {'code': "03",
                 'acctNum': "12345",
                 'amount': 0.05})
    system.applyTransactions([txn2])
    assert system.accounts["12345"]["balance"] == pytest.approx(0.1)

    system.accounts = create_test_accounts(
        '12345',
        "Bob",
        "A",
        0.25,
        0,
        "NP"
    )

    # Test Case 10
    # Will throw error as newBalance will be -0.1
    txn3 = type('Txn', (),
                {'code': "03",
                 'acctNum': "12345",
                 'amount': 0.25})
    with pytest.raises(ValueError, match="overdraw"):
        system.applyTransactions([txn3])
    assert system.accounts.get("balance") == pytest.approx(0.25)

def test_deposit():
    #account['balance'] += (txn.amount - feePerTransaction)
    system = TransactionProcessor()
    system.accounts = create_test_accounts(
        '12345',
        "Bob",
        "A",
        0.05,
        0,
        "NP"
    )
    # Test Case 11
    # newBalance will be 0.0
    txn3 = type('Txn', (),
                {'code': "04",
                 'acctNum': "12345",
                 'amount': 0.05})
    system.applyTransactions([txn3])
    assert system.accounts.get("balance") == pytest.approx(0.0)

def test_create():
    #creates account, no fee
    system = TransactionProcessor()
    system.accounts = create_test_accounts(
        '12345',
        "Bob",
        "A",
        0.25,
        0,
        "NP"
    )
    # Test Case 12
    # newBalance will be 0.0
    txn1 = type('Txn', (),
                {'code': "05",
                 'acctNum': "54321",
                 'amount': 0.0,
                 'name': "Alice"})

    system.applyTransactions([txn1])
    assert system.accounts["54321"]["balance"] == pytest.approx(0.0)

def test_delete():
    #deletes account, no fee
    system = TransactionProcessor()
    system.accounts = create_test_accounts(
        '12345',
        "Bob",
        "A",
        0.25,
        0,
        "NP"
    )
    # Test Case 13
    # newBalance will be 0.0
    txn1 = type('Txn', (),
                {'code': "06",
                 'acctNum': "12345",
                 'amount': 0.00})
    system.applyTransactions([txn1])
    assert system.accounts.get("balance") == pytest.approx(0.0)

def test_disable():
    #newBalance = account['balance'] - feePerTransaction

    system = TransactionProcessor()
    system.accounts = create_test_accounts(
        '12345',
        "Bob",
        "A",
        0.1,
        0,
        "NP"
    )

    # Test Case 14
    # newBalance will be 0.0
    txn1 = type('Txn', (),
                {'code': "07",
                 'acctNum': "12345"})
    system.applyTransactions([txn1])
    assert system.accounts.get("balance") == pytest.approx(0.0)

    # Test Case 15
    # newBalance will be 0.1
    system.accounts = create_test_accounts(
        '23456',
        "Bob",
        "A",
        0.2,
        0,
        "NP"
    )
    txn2 = type('Txn', (),
                {'code': "07",
                 'acctNum': "23456"})
    system.applyTransactions([txn2])
    assert system.accounts.get("balance") == pytest.approx(0.1)

    # Test Case 16
    # Will throw error as balance will be -0.1
    system.accounts = create_test_accounts(
        '23457',
        "Bob",
        "A",
        0.0,
        0,
        "NP"
    )
    txn3 = type('Txn', (),
                {'code': "07",
                 'acctNum': "23457"})
    with pytest.raises(ValueError, match="overdraw"):
        system.applyTransactions([txn3])
    assert system.accounts.get("balance") == pytest.approx(0.25)

def test_changeplan():
    #newBalance = account['balance'] - feePerTransaction
    system = TransactionProcessor()
    system.accounts = create_test_accounts(
        '12345',
        "Bob",
        "A",
        0.1,
        0,
        "NP"
    )
    # Test Case 17
    # newBalance will be -0.1
    txn1 = type('Txn', (),
                {'code': "08",
                 'acctNum': "12345",
                 'misc': "SP"})
    system.applyTransactions([txn1])
    assert system.accounts.get("balance") == pytest.approx(0.0)

    # Test Case 18
    # newBalance will be 0.1
    system.accounts = create_test_accounts(
        '12346',
        "Bob",
        "A",
        0.2,
        0,
        "NP"
    )
    txn2 = type('Txn', (),
                {'code': "08",
                 'acctNum': "12346",
                'misc': "SP"})
    system.applyTransactions([txn2])
    assert system.accounts.get("balance") == pytest.approx(0.1)


    #Test Case 19
    #Will throw error as balance will be -0.1
    system.accounts = create_test_accounts(
        '12347',
        "Bob",
        "A",
        0.0,
        0,
        "NP"
    )

    txn3 = type('Txn', (),
                {'code': "08",
                 'acctNum': "12347",
                 'misc': "SP"})
    with pytest.raises(ValueError, match="overdraw"):
        system.applyTransactions([txn3])
    assert system.accounts.get("balance") == pytest.approx(0.25)

