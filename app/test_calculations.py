from app.calculations import add,subtract, multiply, divide,BankAccount
import pytest


def test_add():
    print("testing add function")
    assert add(1, 1) == 2


@pytest.mark.parametrize("x,y,expected", [
    (1, 2, 3),
    (3, 3, 6),
    (9, 0, 9)])
def test_add(x,y,expected):
    print("testing add function")
    assert add(x,y) == expected


def test_subtract():
    assert subtract(9, 4) == 5


def test_multiply():
    assert multiply(4, 3) == 12


def test_divde():
    assert divide(20, 5) == 4


def test_bank_account_class():
    bank_account = BankAccount(50)
    assert bank_account.balance == 50


def test_default_account_balance():
    bank_account = BankAccount()
    assert bank_account.balance == 0


def test_with_draw():
    bank_account = BankAccount(50)
    bank_account.withdraw(25)
    assert bank_account.balance ==25


def test_deposit():
    bank_account = BankAccount(50)
    bank_account.deposit(30)
    assert bank_account.balance == 80


def test_interest():
    bank_account = BankAccount(50)
    bank_account.collect_interest()
    assert round(bank_account.balance) == 55


#fixtures
@pytest.fixture
def zero_account():
    print("creating fixtures")
    return BankAccount()


@pytest.fixture()
def balance_check():
    print("the balance is present")
    return BankAccount(50)
def test_default_balance(zero_account):
    print("checking default amount")
    assert zero_account.balance == 0

def test_deposit(balance_check):
    balance_check.deposit(30)
    assert balance_check.balance == 80

 #example for fixture and parametrised
@pytest.mark.parametrize("deposit,withdraw,expected",[(100,20,80),(100,100,0),(90,40,50)])
def test_bank_class(zero_account,deposit,withdraw,expected):
    zero_account.deposit(deposit)
    zero_account.withdraw(withdraw)
    zero_account.balance == expected


def test_insufficient_funds(balance_check):
    with pytest.raises(Exception):
        balance_check.withdraw(200)