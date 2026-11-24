from .models import Book, Author, Reader


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class LibraryEvent:
    def __init__(self):
        self._listeners = []

    def subscribe(self, listener):
        self._listeners.append(listener)

    def notify(self, message: str):
        for listener in self._listeners:
            listener(message)


class LibraryManager(metaclass=SingletonMeta):
    def __init__(self):
        self.books = []
        self.readers = []
        self.events = LibraryEvent()

    def add_book(self, title: str, year: int, author_name: str) -> None:
        try:
            author = Author(author_name)
            book = Book(title, year, author)
            self.books.append(book)
            self.events.notify(f"Успішно додано книгу: '{title}'")
        except ValueError as e:
            print(f"Помилка додавання книги: {e}")

    def borrow_book(self, reader: Reader, book_title: str) -> None:
        book = next((b for b in self.books if b.title == book_title), None)
        
        if not book:
            print(f"Помилка: книгу '{book_title}' не знайдено у бібліотеці")
            return
            
        if book.is_borrowed:
            print(f"Помилка: книгу '{book_title}' вже взято іншим читачем")
            return
            
        book.is_borrowed = True
        reader.borrowed_books.append(book)
        self.events.notify(f"Читач '{reader.name}' взяв книгу '{book_title}'")

    def return_book(self, reader: Reader, book_title: str) -> None:
        book = next((b for b in reader.borrowed_books if b.title == book_title), None)
        if not book:
            print(f"Помилка: читач '{reader.name}' не брав книгу '{book_title}'")
            return
            
        book.is_borrowed = False
        reader.borrowed_books.remove(book)
        self.events.notify(f"Читач '{reader.name}' повернув книгу '{book_title}'")
