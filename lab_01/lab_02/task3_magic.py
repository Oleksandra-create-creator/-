class Money:
    def __init__(self, amount, currency="UAH"):
        if not isinstance(amount, (int, float)):
            raise TypeError("Сума має бути числом")
        self.amount = round(float(amount), 2)
        self.currency = currency

    def __str__(self):
        return f"{self.amount:.2f} {self.currency}"

    def __repr__(self):
        return f"Money({self.amount}, {self.currency!r})"

    def __add__(self, other):
        if not isinstance(other, Money):
            raise TypeError("Можна додавати лише Money")
        if self.currency != other.currency:
            raise ValueError("Різні валюти")
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other):
        if not isinstance(other, Money):
            raise TypeError("Можна віднімати лише Money")
        if self.currency != other.currency:
            raise ValueError("Різні валюти")
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, factor):
        if not isinstance(factor, (int, float)):
            raise TypeError("Множник має бути числом")
        return Money(self.amount * factor, self.currency)

    def __eq__(self, other):
        if not isinstance(other, Money):
            return False
        return self.currency == other.currency and abs(self.amount - other.amount) < 1e-9

    def __lt__(self, other):
        if not isinstance(other, Money):
            raise TypeError("Порівнювати можна лише Money")
        if self.currency != other.currency:
            raise ValueError("Різні валюти")
        return self.amount < other.amount

    def __abs__(self):
        return Money(abs(self.amount), self.currency)

    def __bool__(self):
        return self.amount != 0


a = Money(100, "UAH")
b = Money(50.5, "UAH")
c = Money(100, "UAH")
d = Money(250, "UAH")

print("=" * 60)
print("ПРЕДСТАВЛЕННЯ:")
print(f"  str  : {a}")
print(f"  repr : {repr(a)}")

print("\n" + "-" * 60)
print("АРИФМЕТИКА:")
print(f"  {a} + {b} = {a + b}")
print(f"  {a} - {b} = {a - b}")
print(f"  {a} * 3    = {a * 3}")

print("\n" + "-" * 60)
print("ПОРІВНЯННЯ:")
print(f"  {a} == {c} : {a == c}")
print(f"  {a} == {b} : {a == b}")
print(f"  {b} < {a}  : {b < a}")
print(f"  {a} < {b}  : {a < b}")

print("\n" + "-" * 60)
print("КОНТЕЙНЕР / ВИКЛИК:")
neg = Money(-75, "UAH")
print(f"  abs({neg}) = {abs(neg)}")
print(f"  bool({a})  = {bool(a)}")
print(f"  bool(Money(0)) = {bool(Money(0))}")

print("\n" + "-" * 60)
print("ПЕРЕВІРКА ПОМИЛОК:")
try:
    a + Money(10, "USD")
except ValueError as e:
    print(f"  Різні валюти: {e}")

try:
    a * "три"
except TypeError as e:
    print(f"  Некоректний множник: {e}")
