import functools
import time


def cache(max_size: int = 128):
    def decorator(func):
        _cache = {}
        _call_order = []

        @functools.wraps(func)
        def wrapper(*args):
            if args in _cache:
                print(f"[CACHE HIT] {func.__name__}{args}")
                return _cache[args]
            
            print(f"[CACHE MISS] {func.__name__}{args}")
            result = func(*args)
            _cache[args] = result
            _call_order.append(args)
            
            if len(_cache) > max_size:
                oldest = _call_order.pop(0)
                del _cache[oldest]
            return result

        wrapper.cache_info = lambda: {"size": len(_cache), "max_size": max_size}
        wrapper.cache_clear = lambda: (_cache.clear(), _call_order.clear())
        return wrapper
    return decorator


def rate_limit(max_calls: int, period: float = 60.0):
    def decorator(func):
        call_times = []

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            call_times[:] = [t for t in call_times if now - t < period]
            
            if len(call_times) >= max_calls:
                raise RuntimeError(f"Перевищено ліміт викликів: {max_calls} за {period}с")
            
            call_times.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def log(level: str = "INFO"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"[{level}] Виклик {func.__name__}{args}")
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                elapsed = time.time() - start_time
                print(f"[{level}] {func.__name__} → {result} (час: {elapsed:.4f}с)")
                return result
            except Exception as e:
                elapsed = time.time() - start_time
                print(f"[ERROR] {func.__name__} викинув {type(e).__name__}: {e} (час: {elapsed:.4f}")
                raise
        return wrapper
    return decorator


@cache(max_size=64)
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@rate_limit(max_calls=5, period=10.0)
def send_notification(message: str) -> str:
    return f"Надіслано: {message}"


@log(level="DEBUG")
def divide(a: float, b: float) -> float:
    return a / b


def main():
    print("--- Тест cache ---")
    result = fibonacci(30)
    print(f"Результат: {result}")
    print(f"Статистика кешу: {fibonacci.cache_info()}")

    print("\n--- Тест rate_limit ---")
    for i in range(6):
        try:
            print(send_notification(f"Повідомлення {i+1}"))
        except RuntimeError as e:
            print(f"Перехоплено: {e}")

    print("\n--- Тест log ---")
    divide(10, 3)
    try:
        divide(10, 0)
    except ZeroDivisionError:
        pass


if __name__ == "__main__":
    main()
