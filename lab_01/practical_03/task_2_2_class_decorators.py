import functools
import time


def auto_repr(cls):
    init_params = cls.__init__.__code__.co_varnames[1:cls.__init__.__code__.co_argcount]
    
    def __repr__(self):
        values = [f"{param}={getattr(self, param, '???')!r}" for param in init_params]
        return f"{cls.__name__}({', '.join(values)})"
    
    cls.__repr__ = __repr__
    return cls


def frozen(cls):
    original_init = cls.__init__

    @functools.wraps(original_init)
    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        object.__setattr__(self, '_frozen', True)

    cls.__init__ = new_init

    def __setattr__(self, key, value):
        if getattr(self, '_frozen', False):
            raise AttributeError(f"Не можна змінити атрибут '{key}' у замороженому об'єкті")
        object.__setattr__(self, key, value)

    cls.__setattr__ = __setattr__
    return cls


def log_methods(cls):
    for attr_name, attr_value in cls.__dict__.items():
        if not attr_name.startswith('_') and callable(attr_value):
            @functools.wraps(attr_value)
            def wrapper(self, *args, **kwargs, _name=attr_name, _func=attr_value):
                print(f"[LOG] Виклик методу: {_name}{args}")
                result = _func(self, *args, **kwargs)
                print(f"[LOG] Метод {_name} повернув: {result}")
                return result
            setattr(cls, attr_name, wrapper)
    return cls


@auto_repr
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self. y = y

    def distance_to(self, other: "Point") -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


@frozen
class ImmutableConfig:
    def __init__(self, host: str, port: int, debug: bool = False):
        self.host = host
        self.port = port
        self.debug = debug


@log_methods
class MathService:
    def add(self, a: float, b: float) -> float:
        return a + b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Ділення на нуль")
        return a / b


def main():
    print("--- Тест @auto_repr ---")
    p = Point(3.0, 4.0)
    print(repr(p))

    print("\n--- Тест @frozen ---")
    cfg = ImmutableConfig("localhost", 8080, debug=True)
    print(f"Config: {cfg.host}:{cfg.port}")
    try:
        cfg.host = "remote"
    except AttributeError as e:
        print(f"Очікувана помилка: {e}")

    print("\n--- Тест @log_methods ---")
    svc = MathService()
    svc.add(10, 20)
    svc.multiply(3, 7)
    try:
        svc.divide(10, 0)
    except ValueError as e:
        print(f"Перехоплено: {e}")


if __name__ == "__main__":
    main()
