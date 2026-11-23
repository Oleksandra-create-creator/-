class BankAccount:
    def __init__(self, owner, balance, currency="UAH"):
        self.owner = owner
        self._currency = currency
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"Баланс має бути числом, отримано {type(value).__name__}")
        if value < 0:
            raise ValueError(f"Баланс не може бути від'ємним: {value}")
        self.__balance = round(float(value), 2)

    @property
    def balance_in_usd(self):
        rates = {"UAH": 0.027, "EUR": 1.08, "USD": 1.0}
        rate = rates.get(self._currency, 1.0)
        return round(self.__balance * rate, 2)

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError(f"Сума депозиту має бути > 0: {amount}")
        self.balance = self.__balance + amount

    def withdraw(self, amount):
        if amount > self.__balance:
            raise ValueError("Недостатньо коштів")
        self.balance = self.__balance - amount

    def __str__(self):
        return f"Рахунок {self.owner}: {self.__balance:.2f} {self._currency}"


print("=" * 60)
print("КОРЕКТНЕ СТВОРЕННЯ:")
acc = BankAccount("Марія", 1000.0, "UAH")
print(f"  {acc}")
print(f"  Баланс у USD: {acc.balance_in_usd}")

print("\n" + "-" * 60)
print("КОРЕКТНІ ОПЕРАЦІЇ:")
acc.deposit(500)
print(f"  Після депозиту 500: {acc}")
acc.withdraw(200)
print(f"  Після зняття 200: {acc}")
print(f"  Баланс у USD: {acc.balance_in_usd}")

print("\n" + "-" * 60)
print("НЕКОРЕКТНІ ЗНАЧЕННЯ (перехоплення):")

try:
    acc.balance = -100
except ValueError as e:
    print(f"  ValueError: {e}")

try:
    acc.balance = "тисяча"
except TypeError as e:
    print(f"  TypeError: {e}")

try:
    acc.withdraw(100000)
except ValueError as e:
    print(f"  ValueError: {e}")

print("\n" + "-" * 60)
print("ПРИМИТИВНИЙ ДОСТУП ДО __balance:")
try:
    print(acc.__balance)
except AttributeError as e:
    print(f"  AttributeError: {e}")

print("\n" + "-" * 60)
print("ДОСТУП ЧЕРЕЗ NAME MANGLING:")
print(f"  acc._BankAccount__balance = {acc._BankAccount__balance}")

print("\n" + "-" * 60)
print("ЗАХИЩЕНИЙ АТРИБУТ _currency (конвенція):")
print(f"  acc._currency = {acc._currency}")
print("  (доступ є, але це сигнал: 'не чіпати ззовні')")
