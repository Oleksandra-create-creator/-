import pytest
from unittest.mock import patch

pytestmark = pytest.mark.django_db


def test_book_list_200(client, book):
    response = client.get("/")
    assert response.status_code == 200
    assert "catalog/book_list.html" in [t.name for t in response.templates]
    assert "Дюна" in response.content.decode()


def test_book_detail_404(client):
    assert client.get("/books/999/").status_code == 404


@patch("catalog.views.notify_external")
def test_book_create_redirect(mock_notify, client, category):
    response = client.post("/books/new/", {"title": "Нова", "year": 2020, "category": category.pk})
    assert response.status_code == 302
    mock_notify.assert_called_once_with("Нова")
