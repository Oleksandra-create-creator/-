import threading
import time
from .manager import LibraryManager


def concurrent_search(manager: LibraryManager, titles: list, results: list, lock: threading.Lock) -> None:
    for title in titles:
        time.sleep(0.1)
        book = next((b for b in manager.books if b.title == title), None)
        with lock:
            if book:
                results.append(f"Знайдено: '{book.title}' ({book.year} р.)")
            else:
                results.append(f"Не знайдено: '{title}'")


def run_concurrent_searches(manager: LibraryManager) -> list:
    search_lists = [
        ["1984", "Неіснуюча книга"],
        ["Майстер і Маргарита", "Ще одна книга"],
        ["Кобзар", "Гаррі Поттер"]
    ]
    
    threads = []
    results = []
    lock = threading.Lock()

    for titles in search_lists:
        t = threading.Thread(target=concurrent_search, args=(manager, titles, results, lock))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return results
