def calculator():
    print("=== Калькулятор ===")
    print("Формат: число оператор число (наприклад: 5 + 3)")
    print("Команди: 'quit' (вихід), 'history' (історія)")

    history = []

    while True:
        user_input = input("\n> ").strip()

        if user_input.lower() == 'quit':
            print("Вихід з калькулятора.")
            break

        if user_input.lower() == 'history':
            if not history:
                print("Історія порожня.")
            else:
                for idx, record in enumerate(history, 1):
                    print(f"{idx}. {record}")
            continue

        parts = user_input.split()
        if len(parts) != 3:
            print("Помилка: введіть у форматі 'число оператор число'")
            continue

        try:
            num1 = float(parts[0])
            operator = parts[1]
            num2 = float(parts[2])
        except ValueError:
            print("Помилка: перше та третє значення мають бути числами")
            continue

        if operator == '+':
            res = num1 + num2
        elif operator == '-':
            res = num1 - num2
        elif operator == '*':
            res = num1 * num2
        elif operator == '/':
            if num2 == 0:
                print("Помилка: ділення на нуль")
                continue
            res = num1 / num2
        elif operator == '//':
            if num2 == 0:
                print("Помилка: ділення на нуль")
                continue
            res = num1 // num2
        elif operator == '%':
            if num2 == 0:
                print("Помилка: ділення на нуль")
                continue
            res = num1 % num2
        elif operator == '**':
            res = num1 ** num2
        else:
            print("Помилка: невідомий оператор")
            continue

        history.append(f"{num1} {operator} {num2} = {res}")
        print(f"Результат: {res}")

if __name__ == "__main__":
    calculator()
