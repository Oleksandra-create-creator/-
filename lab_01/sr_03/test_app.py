import pytest
from app import User, Book, Order, db

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Test Book' in response.data

def test_login_and_session(client):
    response = client.post('/login', data={'username': 'testuser'}, follow_redirects=True)
    assert b'Вітаємо, testuser' in response.data

def test_api_get_books(client):
    response = client.get('/api/books')
    assert response.status_code == 200
    assert b'Test Book' in response.data

def test_api_create_book(client):
    response = client.post('/api/books', json={'title': 'New Book', 'price': 20.0})
    assert response.status_code == 201
    assert b'New Book' in response.data

def test_order_book(client):
    with client.session_transaction() as sess:
        sess['username'] = 'testuser'
    response = client.get('/order/1', follow_redirects=True)
    assert response.status_code == 200
    
    with client.application.app_context():
        user = User.query.filter_by(username='testuser').first()
        assert len(user.orders) == 1
