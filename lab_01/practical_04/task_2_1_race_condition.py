import threading
import time
import random


class BankAccount:
    def __init__(self, balance: float = 0.0):
        self.balance = balance
        self.transaction_count = 0

    def deposit(self, amount: float) -> None:
        current = self.balance
        time.sleep(random.uniform(0.0001, 0.001))
        self.balance = current + amount
        self.transaction_count += 1

    def withdraw(self, amount: float) -> bool:
        current = self.balance
        time.sleep(random.uniform(0.0001, 0.001))
        if current >= amount:
            self.balance = current - amount
            self.transaction_count += 1
            return True
        return False


class SafeBankAccount:
    def __init__(self, balance: float = 0.0):
        self.balance = balance
        self.transaction_count = 0
        self._lock = threading.Lock()

    def deposit(self, amount: float) -> None:
        with self._lock:
            current = self.balance
            time.sleep(random.uniform(0.0001, 0.001))
            self.balance = current + amount
            self.transaction_count += 1

    def withdraw(self, amount: float) -> bool:
        with self._lock:
            current = self.balance
            time.sleep(random.uniform(0.0001, 0.001))
            if current >= amount:
                self.balance = current - amount
                self.transaction_count += 1
                return True
            return False


def run_transactions(account, num_deposits: int, num_withdrawals: int, deposit_amount: float, withdraw_amount: float):
    threads = []
    for _ in range(num_deposits):
        t = threading.Thread(target=account.deposit, args=(deposit_amount,))
        threads.append(t)
        t.start()
        
    for _ in range(num_withdrawals):
        t = threading.Thread(target=account.withdraw, args=(withdraw_amount,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


def main():
    initial_balance = 1000.0
    num_deposits = 100
    deposit_amount = 50.0
    num_withdrawals = 100
    withdraw_amount = 50.0

    expected_balance = (
        initial_balance
        + num_deposits * deposit_amount
        - num_withdrawals * withdraw_amount
    )

    print("=== Тест без синхронізації ===")
    unsafe_account = BankAccount(initial_balance)
    run_transactions(unsafe_account, num_deposits, num_withdrawals, deposit_amount, withdraw_amount)
    print(f"Очікуваний баланс: {expected_balance:.2f}")
    print(f"Фактичний баланс: {unsafe_account.balance:.2f}")
    print(f"Збігаються: {abs(expected_balance - unsafe_account.balance) < 0.01}")
    print(f"Транзакцій: {unsafe_account.transaction_count}")

    print("\n=== Тест із синхронізацією (Lock) ===")
    safe_account = SafeBankAccount(initial_balance)
    run_transactions(safe_account, num_deposits, num_withdrawals, deposit_amount, withdraw_amount)
    print(f"Очікуваний баланс: {expected_balance:.2f}")
    print(f"Фактичний баланс: {safe_account.balance:.2f}")
    print(f"Збігаються: {abs(expected_balance - safe_account.balance) < 0.01}")
    print(f"Транзакцій: {safe_account.transaction_count}")


if __name__ == "__main__":
    main()
