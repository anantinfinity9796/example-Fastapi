""" This file will have our tests defined and we would use the pytest library for testing the code"""
# Our code is probably a little advanced for testing because we are coming from a background of no testing
# So we want to start out with the simplest of functions.
# So we will create a new file called as calculations.py beacuse it would be a collection of functions
# In this file we will define our first test. A test is really just a function or a method within a class.


import pytest
from app.calculations import add, BankAccount, InsufficientFunds


@pytest.fixture    # initalize the decorator
def zero_bank_account(): # initialize the funtion
    return BankAccount()  # Return the repetitve line 

@ pytest.fixture
def bank_account():
    return BankAccount(50)   # return the bank account with an initial balance

@pytest.mark.parametrize("num1, num2, result",
    [(3,2,5),
    (10,5,15),
    (7,3,10)
])    # used to test for multiple input-output combinations for one test as a single string


def test_add(num1, num2, result):
    print("Testing the add function")
    assert add(num1, num2) == result


def test_bank_set_initial_amount(bank_account):
    """ Testing the BankAccount class """
    # Creating the BankAccount object from the contructor is handeled by the fixture bank_account.
    
    assert bank_account.balance == 50  # Checking if the constructor functionality works or not.



def test_default_bank_amount(zero_bank_account):

    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    bank_account.withdraw(10)
    assert bank_account.balance == 40

def test_deposit(bank_account):
    bank_account.deposit(20)

    assert bank_account.balance == 70

def test_collect_interest(bank_account):

    bank_account.collect_interest()

    assert bank_account.balance == 50*1.1




@pytest.mark.parametrize("deposited, withdrew, expected",
    [(200,100,100),
    (50,10,40),
    (1200,500,700)
]) 
def test_bank_transactions(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)

    assert zero_bank_account.balance == expected


def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)

