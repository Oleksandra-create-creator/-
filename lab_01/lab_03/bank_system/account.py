from typing import Optional
from .exceptions import ValidationError, InsufficientFundsError, AccountNotFoundError

class BankAccount:
    def __init__(self, account_id: str, owner: str, initial_balance: float = 0.0):
        if initial_balance < 0:
            raise ValidationError("initial_balance", "Початковий баланс не може бути від'ємним")
        
        self.account_id = account_id
        self.owner = owner
        self._balance = initial_balance

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValidationError("amount", "Сума депозиту має бути більшою за нуль")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValidationError("amount", "Сума зняття має бути більшою за нуль")
        if amount > self._balance:
            raise InsufficientFundsError(requested=amount, balance=self._balance)
        self._balance -= amount

    def process_transaction(self, transaction_data: str) -> None:
        try:
            amount = float(transaction_data)
            self.deposit(amount)
        except ValueError as e:
            raise ValidationError("transaction_data", "Некоректний формат даних транзакції") from e
        except Exception as e:
            raise BankError("Невідома помилка транзакції", error_code=500) from e
