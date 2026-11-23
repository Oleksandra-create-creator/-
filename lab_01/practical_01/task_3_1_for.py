def factorial(n: int) -> int:
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def harmonic_sum(n: int) -> float:
    total = 0.0
    for i in range(1, n + 1):
        total += 1 / i
    return total

def multiplication_table(n: int) -> None:
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            print(f"{i * j:4}", end="")
        print()

def main():
    try:
        n = int(input("Введіть число n: "))
        print(f"{n}! = {factorial(n)}")
        print(f"Гармонічна сума H({n}) = {harmonic_sum(n):.6f}")
        print(f"\nТаблиця множення {n}x{n}:")
        multiplication_table(n)
    except ValueError:
        print("Помилка: введіть ціле число")

if __name__ == "__main__":
    main()
