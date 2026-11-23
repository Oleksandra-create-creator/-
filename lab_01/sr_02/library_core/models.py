import logging
from .decorators import validate_book_data

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class LoggingMeta(type):
    def __call__(cls, *args, **kwargs):
        logging.info(f"Створення об'єкта класу: {cls.__name__}")
        instance = super().__call__(*args, **kwargs)
        return instance


class Author(metaclass=LoggingMeta):
    def __init__(self, name: str):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Ім'я автора не може бути порожнім")
        self.name = name


class Book(metaclass=LoggingMeta):
    @validate_book_data
    def __init__(self, title: str, year: int, author: Author):
        self.title = title
        self.year = year
        self.author = author
        self.is_borrowed = False


class Reader(metaclass=LoggingMeta):
    def __init__(self, name: str, reader_id: str):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Ім'я читача не може бути порожнім")
        if not isinstance(reader_id, str) or not reader_id.strip():
            raise ValueError("ID читача не може бути порожнім")
        self.name = name
        self.reader_id = reader_id
        self.borrowed_books = []
