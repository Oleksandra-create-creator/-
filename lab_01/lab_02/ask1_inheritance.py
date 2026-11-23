class LibraryItem:
    def __init__(self, title, year):
        self.title = title
        self.year = year
        self._is_borrowed = False

    def borrow(self):
        if self._is_borrowed:
            print(f"  '{self.title}' вже видано.")
        else:
            self._is_borrowed = True
            print(f"  '{self.title}' видано користувачу.")

    def return_item(self):
        self._is_borrowed = False
        print(f"  '{self.title}' повернуто.")

    def describe(self):
        status = "видано" if self._is_borrowed else "в наявності"
        return f"{self.title} ({self.year}) — {status}"

    def __str__(self):
        return self.describe()

    def __repr__(self):
        return f"{self.__class__.__name__}(title={self.title!r}, year={self.year})"


class Book(LibraryItem):
    def __init__(self, title, year, author, pages):
        super().__init__(title, year)
        self.author = author
        self.pages = pages

    def describe(self):
        base = super().describe()
        return f"[Книга] {base} | автор: {self.author}, {self.pages} с."


class Magazine(LibraryItem):
    def __init__(self, title, year, issue_number):
        super().__init__(title, year)
        self.issue_number = issue_number

    def describe(self):
        base = super().describe()
        return f"[Журнал] {base} | випуск №{self.issue_number}"


class DVD(LibraryItem):
    def __init__(self, title, year, duration_min):
        super().__init__(title, year)
        self.duration_min = duration_min

    def describe(self):
        base = super().describe()
        return f"[DVD] {base} | тривалість: {self.duration_min} хв"


items = [
    Book("1984", 1949, "Дж. Орвелл", 328),
    Magazine("National Geographic", 2024, 11),
    DVD("Inception", 2010, 148),
    Book("Майстер і Маргарита", 1967, "М. Булгаков", 480),
]

print("=" * 60)
print("ПОЛІМОРФНИЙ ОБХІД (метод describe):")
for item in items:
    print(f"  {item}")

print("\n" + "-" * 60)
print("ВИДАЧА ПОВЕРНЕННЯ:")
items[0].borrow()
items[1].borrow()
items[0].borrow()
items[0].return_item()

print("\n" + "-" * 60)
print("ПЕРЕВІРКА ТИПІВ:")
print(f"  isinstance(items[0], Book)      : {isinstance(items[0], Book)}")
print(f"  isinstance(items[0], LibraryItem): {isinstance(items[0], LibraryItem)}")
print(f"  isinstance(items[1], Book)      : {isinstance(items[1], Book)}")
print(f"  issubclass(Book, LibraryItem)   : {issubclass(Book, LibraryItem)}")
print(f"  issubclass(DVD, Book)           : {issubclass(DVD, Book)}")
