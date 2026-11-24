import pytest
from sqlalchemy.exc import IntegrityError
from models import db, Book, ReaderProfile


def test_book_repr(book):
    assert repr(book) == "<Book Дюна (1965)>"


def test_default_available(book):
    assert book.available is True


def test_unique_email(reader):
    from models import Reader
    db.session.add(Reader(name="Інша", email="olena@example.com"))
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()


def test_cascade_delete_category(category, book):
    db.session.delete(category)
    db.session.commit()
    assert Book.query.count() == 0


def test_onetoone_profile(reader):
    db.session.add(ReaderProfile(phone="+380500000000", city="Львів", reader_id=reader.id))
    db.session.commit()
    assert reader.profile.city == "Львів"


@pytest.mark.parametrize("year", [1965, 2000, 1840])
def test_book_years(category, year):
    obj = Book(title=f"Книга {year}", year=year, category=category)
    db.session.add(obj)
    db.session.commit()
    assert str(year) in repr(obj)
