group_a = ["S01", "S02", "S03", "S04", "S02", "S05"]
group_b = ["S03", "S04", "S05", "S06", "S07", "S03"]
group_c = ["S03", "S05"]

set_a = set(group_a)
set_b = set(group_b)
set_c = set(group_c)

print(f"A: {sorted(set_a)}")
print(f"B: {sorted(set_b)}")
print(f"C: {sorted(set_c)}")

print("\n--- Операції ---")
print(f"A ∩ B : {sorted(set_a & set_b)}")
print(f"A ∪ B : {sorted(set_a | set_b)}")
print(f"A △ B : {sorted(set_a ^ set_b)}")

print("\n--- Підмножини ---")
print(f"C ⊆ A : {set_c <= set_a}")
print(f"B ⊆ A : {set_b <= set_a}")

print("\n--- frozenset як ключ ---")
permissions = {
    frozenset({"read"}): "guest",
    frozenset({"read", "write"}): "editor",
    frozenset({"read", "write", "admin"}): "owner",
}
print(f"Роль: {permissions[frozenset({'read', 'write'})]}")
