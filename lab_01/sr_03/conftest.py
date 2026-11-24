import pytest
from app import app, db, User, Book

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            db.session.add(User(username='testuser'))
            db.session.add(Book(title='Test Book', price=10.0))
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()
