import math

def triangle_type(a: float, b: float, c: float) -> str:
    if not (a + b > c and a + c > b and b + c > a):
        return "не є трикутником"
    
    is_equilateral = (a == b == c)
    is_isosceles = (a == b or b == c or a == c)
    
    sides = sorted([a, b, c])
    is_right = abs(sides[0]**2 + sides[1]**2 - sides[2]**2) < 1e-9

    if is_equilateral:
        return "рівносторонній"
    elif is_right and is_isosceles:
        return "рівнобедрений прямокутний"
    elif is_right:
        return "прямокутний"
    elif is_isosceles:
        return "рівнобедрений"
    else:
        return "різносторонній"

def triangle_area(a: float, b: float, c: float) -> float:
    s = (a + b + c) / 2
    return math.sqrt(s * (s - a) * (s - b) * (s - c))

def main():
    try:
        a = float(input("Сторона a: "))
        b = float(input("Сторона b: "))
        c = float(input("Сторона c: "))
        
        t_type = triangle_type(a, b, c)
        print(f"Тип трикутника: {t_type}")
        
        if t_type != "не є трикутником":
            area = triangle_area(a, b, c)
            print(f"Площа: {area:.2f}")
    except ValueError:
        print("Помилка: введіть числа")

if __name__ == "__main__":
    main()
