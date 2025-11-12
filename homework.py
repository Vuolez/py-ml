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
    def __init__(self, account_number: str, account_holder: str, balance: float = 0,
                 account_type: AccountType = AccountType.CHECKING):
        self.__account_number = account_number
        self.__account_holder = account_holder
        self.__balance = balance
        self.__account_type = account_type
        pass

    def deposit(self, value: float) -> OperationResult:
        self.__balance += value
        return OperationResult(result=True)

    def withdraw(self, value: int) -> OperationResult:
        self.__balance -= value
        return OperationResult(result=True)

    def get_balance(self):
        return self.__balance

    def get_account_info(self):
        return str(self)

    def __str__(self):
        return (f"account_number: {self.__account_number},"
                f" account_holder: {self.__account_holder},"
                f" balance: {self.__balance},"
                f" account_type: {self.__account_type.value}")


class SavingsAccount(BankAccount):
    def __init__(self, account_number: str, account_holder: str, balance: int = 0,
                 account_type: AccountType = AccountType.CHECKING, interest_rate: int = 0, min_balance: int = 0):
        super().__init__(account_number, account_holder, balance, account_type)
        self.__interest_rate = interest_rate
        self.__min_balance = min_balance

    def withdraw(self, value: int) -> OperationResult:
        if self.get_balance() - value >= self.__min_balance:
            return super().withdraw(value)
        else:
            return OperationResult(result=False,
                                   error_message=f"Ошибка при снятии счета: не хватает лимита: "
                                                 f"balance:{self.get_balance()}, "
                                                 f"min_balance:{self.__min_balance}, value:{value}")

    def add_interest(self) -> OperationResult:
        self.deposit(self.get_balance() * (self.__interest_rate / 100))
        return OperationResult(result=True)

    def get_account_info(self):
        return str(self)

    def __str__(self):
        base_info = super().__str__()
        return (f"{base_info},"
                f" interest_rate: {self.__interest_rate}%,"
                f" min_balance: {self.__min_balance}")


if __name__ == "__main__":
    bank_account = SavingsAccount(
        account_number="1",
        account_holder="deniz",
        balance=10,
        account_type=AccountType.SAVINGS,
        interest_rate=10,
        min_balance=10
    )

    bank_account.deposit(10)
    print(bank_account)

    print(bank_account.withdraw(5))
    print(bank_account)

    print(bank_account.add_interest())
    print(bank_account.get_account_info())
