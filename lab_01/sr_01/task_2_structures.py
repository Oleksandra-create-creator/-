class ReverseIterator:
    def __init__(self, data):
        self._data = data
        self._index = len(data) - 1

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < 0:
            raise StopIteration
        value = self._data[self._index]
        self._index -= 1
        return value

def square_generator(data):
    for item in data:
        if isinstance(item, (int, float)):
            yield item ** 2

def main():
    students_list = [
        ("Олена", 95),
        ("Іван", 78),
        ("Марія", 92)
    ]

    students_dict = {name: grade for name, grade in students_list}

    print("=== Робота зі структурами даних ===")
    print(f"Список кортежів: {students_list}")
    print(f"Словник: {students_dict}")

    print("\n=== Робота з ітератором (зворотний обхід) ===")
    rev_iter = ReverseIterator(students_list)
    for student in rev_iter:
        print(f"  {student[0]}: {student[1]}")

    print("\n=== Робота з генератором (квадрати чисел) ===")
    numbers = [1, 2, 3, 4, 5, "текст", 6]
    gen = square_generator(numbers)
    
    print("Оригінальний список:", numbers)
    print("Згенеровані квадрати:", list(gen))

    print("\n=== Демонстрація функції next() ===")
    gen2 = square_generator([10, 20])
    print(next(gen2))
    print(next(gen2))

if __name__ == "__main__":
    main()
