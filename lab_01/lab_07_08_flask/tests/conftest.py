import pytest
from app import create_app
from models import db, Category, Book, Reader, Tag


@pytest.fixture
def app():
    application = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
    })
    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture
def category(app):
    obj = Category(name="Фантастика", slug="fantasy", description="Твори")
    db.session.add(obj)
    db.session.commit()
    return obj


@pytest.fixture
def tag(app):
    obj = Tag(name="Епіка", slug="epic")
    db.session.add(obj)
    db.session.commit()
    return obj


@pytest.fixture
def book(app, category):
    obj = Book(title="Дюна", year=1965, category=category)
    db.session.add(obj)
    db.session.commit()
    return obj


@pytest.fixture
def reader(app):
    obj = Reader(name="Олена", email="olena@example.com")
    db.session.add(obj)
    db.session.commit()
    return obj
