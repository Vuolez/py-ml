import dataclasses
from enum import Enum
from typing import Optional
from datetime import datetime


class AccountType(Enum):
    CHECKING = "checking"
    SAVINGS = "savings"
    BUSINESS = "business"
    CREDIT = "credit"


class BankAccount:
    def __init__(self, *, account_number: str, account_holder: str, account_type: AccountType, balance: float = 0):
        if not account_number or not account_number.strip():
            raise ValueError("Account number required")
        if not account_holder or not account_holder.strip():
            raise ValueError("Account holder required")
        if account_type is None:
            raise ValueError("Account type required")
        if balance < 0:
            raise ValueError("Initial balance can't be negative")
        self.__account_number = account_number
        self.__account_holder = account_holder
        self.__balance = balance
        self.__account_type = account_type

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.__balance += amount

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self.__balance:
            raise ValueError("Insufficient balance")
        self.__balance -= amount

    def get_balance(self):
        return self.__balance

    def get_account_info(self) -> dict[str, str]:
        return {
            "account_number": self.__account_number,
            "account_holder": self.__account_holder,
            "account_type": self.__account_type
        }

    def __str__(self):
        return (f"account_number: {self.__account_number},"
                f" account_holder: {self.__account_holder},"
                f" balance: {self.__balance},"
                f" account_type: {self.__account_type.value}")

    def get_account_holder(self):
        return self.__account_holder

    def get_account_number(self):
        return self.__account_number


class SavingsAccount(BankAccount):
    def __init__(self, account_number: str, account_holder: str,
                 balance: int = 0, interest_rate: int = 0, min_balance: int = 0):
        super().__init__(account_number=account_number, account_holder=account_holder, account_type=AccountType.SAVINGS,
                         balance=balance)
        self.__interest_rate = interest_rate
        self.__min_balance = min_balance

    def withdraw(self, amount: int):
        if (self.get_balance() - amount) < self.__min_balance:
            raise ValueError(f"Can't exceed minimum balance: "
                             f"balance:{self.get_balance()}, "
                             f"min_balance:{self.__min_balance}, "
                             f"value:{amount}")
        return super().withdraw(amount)

    def add_interest(self):
        interest = self.get_balance() * (self.__interest_rate / 100)
        self.deposit(interest)

    def get_account_info(self):
        return {
            **super().get_account_info(),
            "interest_rate": self.__interest_rate,
            "min_balance": self.__min_balance
        }

    def __str__(self):
        base_info = super().__str__()
        return (f"{base_info},"
                f" interest_rate: {self.__interest_rate}%,"
                f" min_balance: {self.__min_balance}")


class TransactionType(Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    TRANSFER = "transfer"

@dataclasses.dataclass(frozen = True)
class Transaction:
    transaction_type: TransactionType
    account_number: str
    amount: float
    account_number_to: Optional[str] = None
    timestamp = datetime.now()

    def __str__(self):
        if self.transaction_type == "transfer":
            return (f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - "
                    f"{self.transaction_type}: {self.amount} "
                    f"from {self.account_number} to {self.account_number_to}")
        return (f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - "
                f"{self.transaction_type}: {self.amount} "
                f"account: {self.account_number}")

class Bank:
    def __init__(self, name: str, accounts: Optional[dict[str, BankAccount]] = None):
        self.__name = name
        self.__accounts = accounts if accounts is not None else {}
        self.__transactions: list[Transaction] = []  # История транзакций

    def add_account(self, account: BankAccount):
        if account.get_account_number() in self.__accounts:
            raise ValueError(f"Account with number:{account.get_account_number()} already exists")
        self.__accounts[account.get_account_number()] = account

    def remove_account(self, account_number: str):
        del self.__accounts[account_number]

    def find_account(self, account_number: str):
        if account_number not in self.__accounts:
            raise ValueError(f"Account with number:{account_number} does not exists")

    def get_total_balance(self):
        return sum(account.get_balance() for account in self.__accounts.values())

    def deposit(self, account_number: str, amount: float):
        if account_number not in self.__accounts:
             raise ValueError(f"Account with number:{account_number} does not exists")
        self.__accounts[account_number].deposit(amount)
        self.__transactions.append(Transaction(TransactionType.DEPOSIT, account_number, amount))

    def withdraw(self, account_number: str, amount: float):
        if account_number not in self.__accounts:
            raise ValueError(f"Account with number:{account_number} does not exists")
        self.__accounts[account_number].withdraw(amount)
        self.__transactions.append(Transaction(TransactionType.WITHDRAW, account_number, amount))

    def transfer(self, account_number_from: str, account_number_to: str, amount: float):
        if account_number_from not in self.__accounts:
            raise ValueError(f"Account name:{account_number_from} does not exists")
        if account_number_to not in self.__accounts:
            raise ValueError(f"Account name:{account_number_to} does not exists")
        if self.__accounts[account_number_from].get_balance() - amount < 0:
            raise ValueError(f"There are not enough funds in the account")

        self.__accounts[account_number_from].withdraw(amount)
        self.__accounts[account_number_to].deposit(amount)
        self.__transactions.append(Transaction(TransactionType.TRANSFER, account_number_from, amount, account_number_to))

    def get_accounts_by_holder(self, account_holder: str):
        return (account for account in self.__accounts.values() if account.get_account_holder() == account_holder)

    def get_transaction_history(self) -> list[Transaction]:
        return self.__transactions

    def get_account_transactions(self, account_number: str) -> list[Transaction]:
        return [t for t in self.__transactions 
                if t.account_number == account_number
                or t.account_number_to == account_number]

    def __str__(self):
        if not self.__accounts:
            return f"name:{self.__name}, accounts: []"
        accounts_str = '\n  '.join(str(v) for v in self.__accounts.values())
        return (f"name: {self.__name}, "
                f"\naccounts: [\n  {accounts_str}\n]")

if __name__ == "__main__":
    test_account_1 = SavingsAccount(
        account_number="1",
        account_holder="deniz",
        balance=10,
        interest_rate=10,
        min_balance=10
    )

    test_account_2 = SavingsAccount(
        account_number="2",
        account_holder="gelka",
        balance=20,
        interest_rate=10,
        min_balance=10
    )

    bank = Bank(name = "bank_1")
    bank.add_account(test_account_1)
    bank.add_account(test_account_2)
    bank.deposit("1", 10)
    bank.withdraw("1", 5)
    bank.transfer("1", "2", 3)

    print(bank.get_account_transactions("1"))