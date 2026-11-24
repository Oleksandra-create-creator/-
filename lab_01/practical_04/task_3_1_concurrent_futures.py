from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import time
import hashlib


def io_bound_task(url: str) -> dict:
    time.sleep(0.2)
    return {"url": url, "status": 200, "size": len(url) * 42}


def cpu_bound_task(n: int) -> dict:
    hasher = hashlib.sha256()
    for i in range(n):
        hasher.update(str(i).encode())
    return {"n": n, "hash": hasher.hexdigest()[:16]}


def risky_task(value: int) -> float:
    if value == 0:
        raise ZeroDivisionError("Ділення на нуль!")
    if value < 0:
        raise ValueError(f"Від'ємне значення: {value}")
    return 1000.0 / value


def benchmark_io_bound():
    urls = [f"https://api.example.com/data/{i}" for i in range(20)]

    start_time = time.perf_counter()
    for url in urls:
        io_bound_task(url)
    seq_time = time.perf_counter() - start_time

    start_time = time.perf_counter()
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(io_bound_task, urls))
    par_time = time.perf_counter() - start_time

    print(f"Послідовно: {seq_time:.3f} сек")
    print(f"ThreadPoolExecutor: {par_time:.3f} сек")
    print(f"Прискорення: {seq_time / par_time:.2f}x")


def benchmark_cpu_bound():
    tasks = [300_000] * 8

    start_time = time.perf_counter()
    for n in tasks:
        cpu_bound_task(n)
    seq_time = time.perf_counter() - start_time

    start_time = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(cpu_bound_task, tasks))
    par_time = time.perf_counter() - start_time

    print(f"Послідовно: {seq_time:.3f} сек")
    print(f"ProcessPoolExecutor: {par_time:.3f} сек")
    print(f"Прискорення: {seq_time / par_time:.2f}x")


def handle_exceptions():
    values = [10, 5, 0, -3, 8, 2]

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(risky_task, v): v for v in values}
        for future in as_completed(futures):
            val = futures[future]
            try:
                result = future.result()
                print(f"Успіх: 1000 / {val} = {result:.2f}")
            except Exception as e:
                print(f"Помилка для значення {val}: {type(e).__name__} -> {e}")


def main():
    print("=" * 60)
    print("=== I/O-bound: ThreadPoolExecutor ===")
    print("=" * 60)
    benchmark_io_bound()

    print(f"\n{'=' * 60}")
    print("=== CPU-bound: ProcessPoolExecutor ===")
    print("=" * 60)
    benchmark_cpu_bound()

    print(f"\n{'=' * 60}")
    print("=== Обробка виключень у пулах ===")
    print("=" * 60)
    handle_exceptions()


if __name__ == "__main__":
    main()
