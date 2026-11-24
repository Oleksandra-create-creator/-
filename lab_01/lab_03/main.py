import os
from bank_system import BankAccount, ValidationError, InsufficientFundsError, BankError
from bank_system import read_config_safely, process_multiple_errors

def demonstrate_exceptions() -> None:
    print("=== 1. Демонстрація власних виключень та ланцюжків ===")
    account = BankAccount("UA123", "Марія", 1000.0)
    
    try:
        account.withdraw(1500.0)
    except InsufficientFundsError as e:
        print(f"Перехоплено: {e}")
        
    try:
        account.process_transaction("не_число")
    except ValidationError as e:
        print(f"Перехоплено ланцюжок: {e}")
        if e.__cause__:
            print(f"Першопричина (__cause__): {type(e.__cause__).__name__} -> {e.__cause__}")

def demonstrate_try_except_else_finally() -> None:
    print("\n=== 2. Демонстрація try/except/else/finally та with ===")
    test_file = "temp_config.txt"
    
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("valid data")
        
    try:
        result = read_config_safely(test_file)
    except Exception as e:
        print(f"Помилка: {e}")
    else:
        print(f"Успішний шлях, отримані дані: {result}")
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)
            print("Ресурси очищено.")

def demonstrate_introspection() -> None:
    print("\n=== 3. Демонстрація інтроспекції (help та __annotations__) ===")
    print("--- help(BankAccount.deposit) ---")
    help(BankAccount.deposit)
    
    print("\n--- __annotations__ ---")
    print(BankAccount.withdraw.__annotations__)

def main() -> None:
    demonstrate_exceptions()
    demonstrate_try_except_else_finally()
    process_multiple_errors("0")
    process_multiple_errors("abc")
    demonstrate_introspection()

if __name__ == "__main__":
    main()
