import pytest
from django.db import IntegrityError
from django.db.models import ProtectedError
from catalog.models import Book, Loan, ReaderProfile
from datetime import date, timedelta

pytestmark = pytest.mark.django_db


def test_book_str(book):
    assert str(book) == "Дюна (1965)"


def test_default_available(book):
    assert book.available is True


def test_unique_category(category):
    from catalog.models import Category
    with pytest.raises(IntegrityError):
        Category.objects.create(name="Фантастика", slug="other")


def test_cascade_delete_books(category, book):
    category.delete()
    assert Book.objects.count() == 0


def test_protect_book_with_loan(book, reader):
    Loan.objects.create(book=book, reader=reader, due_date=date.today() + timedelta(days=7))
    with pytest.raises(ProtectedError):
        book.delete()


def test_onetoone_profile(reader):
    ReaderProfile.objects.create(reader=reader, phone="+380500000000", city="Львів")
    assert reader.profile.city == "Львів"


@pytest.mark.parametrize("year,expected", [(1965, "1965"), (2000, "2000"), (1840, "1840")])
def test_book_str_years(category, year, expected):
    book = Book.objects.create(title=f"Книга {year}", year=year, category=category)
    assert expected in str(book)
