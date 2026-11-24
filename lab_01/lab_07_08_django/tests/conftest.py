import pytest
from catalog.models import Category, Book, Reader, Tag


@pytest.fixture
def category(db):
    return Category.objects.create(name="Фантастика", slug="fantasy", description="Твори")


@pytest.fixture
def tag(db):
    return Tag.objects.create(name="Епіка", slug="epic")


@pytest.fixture
def book(category):
    return Book.objects.create(title="Дюна", year=1965, category=category)


@pytest.fixture
def reader(db):
    return Reader.objects.create(name="Олена", email="olena@example.com")
