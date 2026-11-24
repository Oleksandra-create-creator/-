def display_product(product):
    pid, name, qty, price = product
    print(f"  [{pid:3d}] {name:<15} | к-сть: {qty:3d} | ціна: {price:7.2f} грн")


def total_value(products):
    total = 0.0
    for _, _, qty, price in products:
        total += qty * price
    return total


def tuples_to_dicts(products):
    keys = ("id", "name", "quantity", "price")
    return [dict(zip(keys, p)) for p in products]


products = [
    (1, "Яблука",  50, 25.50),
    (2, "Хліб",    30, 18.00),
    (3, "Молоко",  20, 32.75),
    (4, "Сир",     10, 120.00),
]

print("=" * 55)
print("ТОВАРИ (кортежі):")
for p in products:
    display_product(p)

total = total_value(products)
print(f"\nЗагальна вартість: {total:.2f} грн")

print("\n--- Спроба змінити кортеж ---")
try:
    products[0][1] = "Груші"
except TypeError as e:
    print(f"  Помилка: {e}")

print("\n--- Кортеж зі вкладеним списком ---")
student = ("Петренко", "ГР-01", [4, 5, 5, 4, 5])
print(f"  До: {student}")
student[2].append(5)
print(f"  Після: {student}")

print("\n--- Як словники ---")
for d in tuples_to_dicts(products):
    print(f"  {d}")
