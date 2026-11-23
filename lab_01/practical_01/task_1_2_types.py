def main():
    raw_input = input("Введіть число: ")
    
    try:
        val_int = int(raw_input)
        val_float = float(raw_input)
        val_bool = bool(raw_input)
        
        print(f"int: {val_int}, тип: {type(val_int)}")
        print(f"float: {val_float}, тип: {type(val_float)}")
        print(f"bool: {val_bool}, тип: {type(val_bool)}")
        print(f"isinstance int: {isinstance(val_int, int)}")
    except ValueError:
        print("Помилка: введено не число")

    name = input("Введіть ім'я: ")
    age = input("Введіть вік: ")
    print(f"Вітаю, {name:<15}! Твій вік: {int(age):03d} років.")

    my_range = list(range(1, 6))
    print(f"Список: {my_range}, довжина: {len(my_range)}, id: {id(my_range)}")

if __name__ == "__main__":
    main()
