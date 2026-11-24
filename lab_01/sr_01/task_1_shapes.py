import math

def calculate_factorial(n):
    if n < 0:
        return None
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def calculate_shape_area(shape, *args):
    if shape == "circle":
        r = args[0]
        return math.pi * (r ** 2)
    elif shape == "rectangle":
        a, b = args[0], args[1]
        return a * b
    elif shape == "triangle":
        a, b, c = args[0], args[1], args[2]
        s = (a + b + c) / 2
        return math.sqrt(s * (s - a) * (s - b) * (s - c))
    return 0.0

def main():
    print("=== Меню обчислень ===")
    while True:
        print("\n1. Факторіал числа")
        print("2. Площа фігури")
        print("3. Вихід")
        choice = input("Оберіть дію (1-3): ").strip()

        if choice == "1":
            try:
                n = int(input("Введіть ціле число: "))
                fact = calculate_factorial(n)
                if fact is not None:
                    print(f"Факторіал {n}! = {fact}")
                else:
                    print("Факторіал від'ємного числа не визначений.")
            except ValueError:
                print("Помилка: введіть ціле число.")

        elif choice == "2":
            shape = input("Введіть фігуру (circle, rectangle, triangle): ").strip().lower()
            try:
                if shape == "circle":
                    r = float(input("Радіус: "))
                    area = calculate_shape_area(shape, r)
                    print(f"Площа кола: {area:.2f}")
                elif shape == "rectangle":
                    a = float(input("Сторона a: "))
                    b = float(input("Сторона b: "))
                    area = calculate_shape_area(shape, a, b)
                    print(f"Площа прямокутника: {area:.2f}")
                elif shape == "triangle":
                    a = float(input("Сторона a: "))
                    b = float(input("Сторона b: "))
                    c = float(input("Сторона c: "))
                    area = calculate_shape_area(shape, a, b, c)
                    print(f"Площа трикутника: {area:.2f}")
                else:
                    print("Невідома фігура.")
            except ValueError:
                print("Помилка: введіть коректні числа.")

        elif choice == "3":
            print("Вихід з програми.")
            break
        else:
            print("Невірний вибір, спробуйте ще раз.")

if __name__ == "__main__":
    main()
