import timeit

SIZES = [1_000, 10_000, 100_000]
REPEATS = 5


def build_data(n):
    lst = list(range(n))
    st = set(lst)
    dct = {i: i for i in range(n)}
    return lst, st, dct


def measure(func, repeats=REPEATS):
    times = timeit.repeat(func, number=1, repeat=repeats)
    return min(times), sum(times) / len(times)


print(f"{'n':>8} | {'list in':>10} | {'set in':>10} | {'dict in':>10} | {'list uniq':>12} | {'set uniq':>10}")
print("-" * 80)

for n in SIZES:
    lst, st, dct = build_data(n)
    target = n - 1
    data_with_dups = list(range(n // 2)) * 2

    t_list_in, _ = measure(lambda: target in lst)
    t_set_in, _ = measure(lambda: target in st)
    t_dict_in, _ = measure(lambda: target in dct)

    def via_list():
        seen = []
        for x in data_with_dups:
            if x not in seen:
                seen.append(x)
        return seen

    def via_set():
        return set(data_with_dups)

    t_list_uniq, _ = measure(via_list)
    t_set_uniq, _ = measure(via_set)

    print(f"{n:>8} | {t_list_in:>9.5f}s | {t_set_in:>9.5f}s | {t_dict_in:>9.5f}s | {t_list_uniq:>11.5f}s | {t_set_uniq:>9.5f}s")
