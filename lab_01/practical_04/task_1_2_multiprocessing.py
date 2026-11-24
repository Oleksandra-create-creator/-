import multiprocessing
import time
import os


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def sum_primes_in_range(start: int, end: int) -> tuple:
    pid = os.getpid()
    total_sum = 0
    count = 0
    for n in range(start, end):
        if is_prime(n):
            total_sum += n
            count += 1
    return total_sum, count, pid


def main():
    total_range = 1_000_000
    num_workers = 4
    chunk_size = total_range // num_workers
    ranges = []
    for i in range(num_workers):
        start = i * chunk_size if i > 0 else 2
        end = (i + 1) * chunk_size
        ranges.append((start, end))

    start_time = time.perf_counter()
    seq_results = [sum_primes_in_range(r[0], r[1]) for r in ranges]
    seq_time = time.perf_counter() - start_time

    start_time = time.perf_counter()
    with multiprocessing.Pool(processes=num_workers) as pool:
        par_results = pool.starmap(sum_primes_in_range, ranges)
    par_time = time.perf_counter() - start_time

    seq_total = sum(r[0] for r in seq_results)
    par_total = sum(r[0] for r in par_results)

    print(f"Послідовно: {seq_time:.3f} сек")
    print(f"Паралельно ({num_workers} процеси): {par_time:.3f} сек")
    print(f"Прискорення: {seq_time / par_time:.2f}x")
    print(f"Сума простих (посл.): {seq_total}, (пар.): {par_total}")
    print("PID процесів:", [r[2] for r in par_results])


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
