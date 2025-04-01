import sys
from write_new_master_bank_accounts import write_new_master_bank_accounts


#accounts.append({
#                    'account_number': account_number.lstrip('0') or '0',
#                    'name': name.strip(),
#                    'status': status,
#                    'balance': balance,
#                    'total_transactions': transactions,
#                    'plan': plan_type
#
def main():
    test_account = []
    decision_coverage = []
    #00004 Alice Brown          A 03999.90 0001 SP
    #if the account number is not a string
    decision_coverage.append({
        'account_number': 90000,
        'name': "abcefghijklmnopqrstu",
        'status': "A",
        'balance': float(99999.99),
        'total_transactions': int(9999),
        'plan': "SP"
    })
    #if the account number is not digits
    decision_coverage.append({
        'account_number': "abcde",
        'name': "abcefghijklmnopqrstu",
        'status': "A",
        'balance': float(99999.99),
        'total_transactions': int(9999),
        'plan': "SP"
    })
    #if the account number is longer than 5 characters
    decision_coverage.append({
        'account_number': "123456",
        'name': "abcefghijklmnopqrstu",
        'status': "A",
        'balance': float(99999.99),
        'total_transactions': int(9999),
        'plan': "SP"
    })
    #if the account name is longer than 20 characters
    decision_coverage.append({
        'account_number': "00000",
        'name': "abcefghijklmnopqrstuv",
        'status': "A",
        'balance': float(99999.99),
        'total_transactions': int(9999),
        'plan': "SP"
    })
    #if the account status is not (“A”, or “D)
    decision_coverage.append({
        'account_number': "00000",
        'name': "abcefghijklmnopqrstu",
        'status': "F",
        'balance': float(99999.99),
        'total_transactions': int(9999),
        'plan': "SP"
    })
    #if the account balance is not a int or float
    decision_coverage.append({
        'account_number': "00000",
        'name': "abcefghijklmnopqrstu",
        'status': "A",
        'balance': str(99999.99),
        'total_transactions': int(9999),
        'plan': "SP"
    })
    #if the account balance is > than 99999.99
    decision_coverage.append({
        'account_number': "00000",
        'name': "abcefghijklmnopqrstu",
        'status': "A",
        'balance': float(123456.99),
        'total_transactions': int(9999),
        'plan': "SP"
    })
    #if the account balance is < 0
    decision_coverage.append({
        'account_number': "00000",
        'name': "abcefghijklmnopqrstu",
        'status': "A",
        'balance': float(-1),
        'total_transactions': int(9999),
        'plan': "SP"
    })
    #if the account’s transaction count is not an integer
    decision_coverage.append({
        'account_number': "00000",
        'name': "abcefghijklmnopqrstu",
        'status': "A",
        'balance': float(99999.99),
        'total_transactions': str(9999),
        'plan': "SP"
    })
    #if the account’s transaction count is > 9999
    decision_coverage.append({
        'account_number': "00000",
        'name': "abcefghijklmnopqrstu",
        'status': "A",
        'balance': float(99999.99),
        'total_transactions': int(12345),
        'plan': "SP"
    })
    #if the account’s transaction count is < 0
    decision_coverage.append({
        'account_number': "00000",
        'name': "abcefghijklmnopqrstu",
        'status': "A",
        'balance': float(99999.99),
        'total_transactions': int(-1),
        'plan': "SP"
    })
    #if the account’s plan is not (“SP” or “NP”)
    decision_coverage.append({
        'account_number': "00000",
        'name': "abcefghijklmnopqrstu",
        'status': "A",
        'balance': float(99999.99),
        'total_transactions': int(9999),
        'plan': "GP"
    })
    #passes no decisions
    decision_coverage.append({
                    'account_number': "00000",
                    'name': "abcefghijklmnopqrstu",
                    'status': "A",
                    'balance': float(99999.99),
                    'total_transactions': int(9999),
                    'plan': "SP"
                })
    test_account.append({
                    'account_number': "00000",
                    'name': "abcefghijklmnopqrstu",
                    'status': "A",
                    'balance': float(99999.99),
                    'total_transactions': int(9999),
                    'plan': "SP"
                })

    #Test for Decision coverage
    for i in decision_coverage:
        try:
            print("\n", i)
            temp = []
            temp.append(i)
            write_new_master_bank_accounts(temp, "test_write_decision.txt")
        except ValueError as error:
            print("An exception occurred:", error)
            pass

    loop_coverage_zero = []
    loop_coverage_one = []
    loop_coverage_one.append({
        'account_number': "00000",
        'name': "one loop",
        'status': "A",
        'balance': float(99999.99),
        'total_transactions': int(9999),
        'plan': "SP"
    })
    loop_coverage_two = []
    loop_coverage_two.append({
        'account_number': "00000",
        'name': "first of two",
        'status': "A",
        'balance': float(99999.99),
        'total_transactions': int(9999),
        'plan': "SP"
    })
    loop_coverage_two.append({
        'account_number': "00001",
        'name': "second of two",
        'status': "A",
        'balance': float(99999.99),
        'total_transactions': int(9999),
        'plan': "SP"
    })
    loop_coverage_many = []
    loop_coverage_many.append({
        'account_number': "00000",
        'name': "one of many",
        'status': "A",
        'balance': float(99999.99),
        'total_transactions': int(9999),
        'plan': "SP"
    })
    loop_coverage_many.append({
        'account_number': "00000",
        'name': "two of many",
        'status': "A",
        'balance': float(99999.99),
        'total_transactions': int(9999),
        'plan': "SP"
    })
    loop_coverage_many.append({
        'account_number': "00000",
        'name': "three of many",
        'status': "A",
        'balance': float(99999.99),
        'total_transactions': int(9999),
        'plan': "SP"
    })
    loop_coverage_many.append({
        'account_number': "00000",
        'name': "four of many",
        'status': "A",
        'balance': float(99999.99),
        'total_transactions': int(9999),
        'plan': "SP"
    })
    #test for loop coverage
    #write_new_master_bank_accounts(decision_coverage, "test_write_decision.txt")
    loop_coverage = []
    loop_coverage.append(loop_coverage_zero)
    loop_coverage.append(loop_coverage_one)
    loop_coverage.append(loop_coverage_two)
    loop_coverage.append(loop_coverage_many)
    #Make each loop coverage output to different txt file.
    for i in loop_coverage:
        try:
            print("\n", i)
            write_new_master_bank_accounts(i, "test_write_loop.txt")
        except ValueError as error:
            print("An exception occurred:", error)
            pass






main()