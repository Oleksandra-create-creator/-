numbers = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]


def print_step(step, data):
    print(f"\n[{step}]")
    print(f"  Вміст : {data}")
    print(f"  Довжина: {len(data)}")


print("=" * 50)
print("ПОЧАТКОВИЙ СПИСОК")
print_step("Крок 0 — старт", numbers)

print_step("Крок 1 — [0]", numbers[0])
print_step("Крок 2 — [-1]", numbers[-1])
print_step("Крок 3 — [-2]", numbers[-2])

print_step("Крок 4 — [2:6]", numbers[2:6])
print_step("Крок 5 — [::-1]", numbers[::-1])
print_step("Крок 6 — [1:9:2]", numbers[1:9:2])

numbers.append(999)
print_step("Крок 7 — append(999)", numbers)

numbers.insert(0, 5)
print_step("Крок 8 — insert(0, 5)", numbers)

numbers.remove(50)
print_step("Крок 9 — remove(50)", numbers)

numbers[2:4] = [31, 32, 33]
print_step("Крок 10 — заміна [2:4]", numbers)

print("\n" + "=" * 50)
print("ФІНАЛ:", numbers)
