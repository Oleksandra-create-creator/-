import os
from typing import Any

def read_config_safely(filepath: str) -> dict[str, Any]:
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = file.read()
    except FileNotFoundError as e:
        print(f"Файл не знайдено: {filepath}")
        raise
    except PermissionError as e:
        print(f"Немає доступу до файлу: {filepath}")
        raise
    else:
        print(f"Файл '{filepath}' успішно прочитано.")
        return {"status": "success", "data": data}
    finally:
        print(f"Завершення операції читання файлу '{filepath}'.")


def process_multiple_errors(value: str) -> None:
    try:
        num = int(value)
        result = 100 / num
        print(f"Результат: {result}")
    except (ValueError, ZeroDivisionError) as e:
        print(f"Перехоплено помилку вводу або ділення: {type(e).__name__} -> {e}")
