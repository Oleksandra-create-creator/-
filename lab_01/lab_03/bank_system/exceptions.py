class BankError(Exception):
    """Базовий клас для всіх помилок банківської системи."""

    def __init__(self, message: str, error_code: int):
        super().__init__(message)
        self.error_code = error_code

    def __str__(self) -> str:
        return f"[Код {self.error_code}] {super().__str__()}"


class ValidationError(BankError):
    """Виключення при некоректних вхідних даних."""

    def __init__(self, field_name: str, message: str):
        super().__init__(message, error_code=400)
        self.field_name = field_name

    def __str__(self) -> str:
        return f"Помилка валідації поля '{self.field_name}': {super().__str__()}"


class InsufficientFundsError(BankError):
    """Виключення при спробі зняти більше коштів, ніж є на рахунку."""

    def __init__(self, requested: float, balance: float):
        super().__init__("Недостатньо коштів на рахунку", error_code=402)
        self.requested = requested
        self.balance = balance

    def __str__(self) -> str:
        return f"{super().__str__()} (Запитано: {self.requested}, Доступно: {self.balance})"


class AccountNotFoundError(BankError):
    """Виключення при спробі знайти неіснуючий рахунок."""

    def __init__(self, account_id: str):
        super().__init__(f"Рахунок з ID '{account_id}' не знайдено", error_code=404)
        self.account_id = account_id
