import dataclasses
from enum import Enum


class AccountType(Enum):
    CHECKING = "checking"
    SAVINGS = "savings"
    BUSINESS = "business"
    CREDIT = "credit"


@dataclasses.dataclass
class OperationResult:
    result: bool
    error_message: str = ""


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

    def deposit(self, amount: float) -> OperationResult:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.__balance += amount
        return OperationResult(result=True)

    def withdraw(self, amount: int) -> OperationResult:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self.__balance:
            raise ValueError("Insufficient balance")
        self.__balance -= amount
        return OperationResult(result=True)

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


class SavingsAccount(BankAccount):
    def __init__(self, account_number: str, account_holder: str,
                 balance: int = 0, interest_rate: int = 0, min_balance: int = 0):
        super().__init__(account_number=account_number, account_holder=account_holder, account_type=AccountType.SAVINGS,
                         balance=balance)
        self.__interest_rate = interest_rate
        self.__min_balance = min_balance

    def withdraw(self, amount: int) -> OperationResult:
        if (self.get_balance() - amount) < self.__min_balance:
            return OperationResult(result=False,
                                   error_message=f"Can't exceed minimum balance: "
                                                 f"balance:{self.get_balance()}, "
                                                 f"min_balance:{self.__min_balance}, "
                                                 f"value:{amount}")
        return super().withdraw(amount)

    def add_interest(self) -> OperationResult:
        interest = self.get_balance() * (self.__interest_rate / 100)
        self.deposit(interest)
        return OperationResult(result=True)

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


if __name__ == "__main__":
    account = SavingsAccount(
        account_number="1",
        account_holder="deniz",
        balance=10,
        interest_rate=10,
        min_balance=10
    )

    account.deposit(10)
    print(account)

    print(account.withdraw(5))
    print(account)

    print(account.add_interest())
    print(account.get_account_info())
