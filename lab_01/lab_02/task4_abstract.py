from abc import ABC, abstractmethod


class Logger(ABC):
    @abstractmethod
    def log(self, message):
        pass

    @abstractmethod
    def format_header(self, title):
        pass

    @property
    @abstractmethod
    def level_name(self):
        pass

    def log_with_header(self, title, message):
        header = self.format_header(title)
        self.log(f"{header} {message}")


class ConsoleLogger(Logger):
    def __init__(self, prefix="LOG"):
        self.prefix = prefix

    def log(self, message):
        print(f"  [CONSOLE] {message}")

    def format_header(self, title):
        return f"=== {self.prefix}: {title} ==="

    @property
    def level_name(self):
        return "INFO"


class FileLogger(Logger):
    def __init__(self, filename):
        self.filename = filename
        self._buffer = []

    def log(self, message):
        self._buffer.append(message)

    def format_header(self, title):
        return f"[FILE:{self.filename}] {title} ->"

    @property
    def level_name(self):
        return "DEBUG"

    def flush(self):
        print(f"  (Записано {len(self._buffer)} рядків у {self.filename})")
        self._buffer.clear()


class OrderItem:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def total(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.name} x{self.quantity} @ {self.price}"


class Order:
    def __init__(self, order_id, logger):
        self.order_id = order_id
        self._logger = logger
        self.items = []

    def add_item(self, item):
        self.items.append(item)
        self._logger.log_with_header(
            f"Order #{self.order_id}",
            f"додано: {item}"
        )

    def total(self):
        return sum(i.total() for i in self.items)

    def print_receipt(self):
        self._logger.log_with_header(
            f"Чек #{self.order_id}",
            f"сума: {self.total():.2f} грн"
        )


print("=" * 60)
print("СПРОБА СТВОРИТИ АБСТРАКТНИЙ КЛАС:")
try:
    bad = Logger()
except TypeError as e:
    print(f"  TypeError: {e}")

print("\n" + "-" * 60)
print("КОНСОЛЬНИЙ ЛОГЕР:")
console = ConsoleLogger("SHOP")
print(f"  level_name = {console.level_name}")

print("\n" + "-" * 60)
print("КОМПОЗИЦІЯ — Order має Logger:")
order1 = Order(1001, console)
order1.add_item(OrderItem("Хліб", 18.0, 2))
order1.add_item(OrderItem("Молоко", 32.5, 1))
order1.print_receipt()

print("\n" + "-" * 60)
print("ФАЙЛОВИЙ ЛОГЕР (той самий Order, інший компонент):")
file_logger = FileLogger("orders.log")
print(f"  level_name = {file_logger.level_name}")
order2 = Order(1002, file_logger)
order2.add_item(OrderItem("Сир", 120.0, 1))
order2.add_item(OrderItem("Кава", 85.0, 3))
order2.print_receipt()
file_logger.flush()

print("\n" + "-" * 60)
print("ПОЛІМОРФНИЙ ОБХІД:")
loggers = [console, file_logger]
for lg in loggers:
    print(f"  {lg.__class__.__name__}: level = {lg.level_name}")
