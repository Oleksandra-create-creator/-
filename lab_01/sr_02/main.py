from library_core import LibraryManager, Reader, run_concurrent_searches


def notification_listener(message: str):
    print(f"[СПОВІЩЕННЯ] {message}")


def main():
    manager = LibraryManager()
    manager.events.subscribe(notification_listener)

    print("--- Додавання книг ---")
    manager.add_book("1984", 1949, "Джордж Орвелл")
    manager.add_book("Майстер і Маргарита", 1967, "Михайло Булгаков")
    manager.add_book("", 2000, "Тестовий автор")
    manager.add_book("Кобзар", 1840, "Тарас Шевченко")

    print("\n--- Реєстрація читачів ---")
    reader1 = Reader("Олена", "R001")
    reader2 = Reader("Іван", "R002")

    print("\n--- Операції з книгами ---")
    manager.borrow_book(reader1, "1984")
    manager.borrow_book(reader1, "1984")
    manager.borrow_book(reader2, "Майстер і Маргарита")
    manager.borrow_book(reader2, "Неіснуюча книга")

    print("\n--- Мультипоточний пошук у базі ---")
    results = run_concurrent_searches(manager)
    for res in results:
        print(res)

    print(f"\n--- Підсумок ---")
    print(f"Книги Олени: {[b.title for b in reader1.borrowed_books]}")
    print(f"Книги Івана: {[b.title for b in reader2.borrowed_books]}")

    manager.return_book(reader1, "1984")
    print(f"Книги Олени після повернення: {[b.title for b in reader1.borrowed_books]}")


if __name__ == "__main__":
    main()
