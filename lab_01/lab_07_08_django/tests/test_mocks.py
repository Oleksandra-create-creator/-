import pytest
from unittest.mock import patch
from catalog import services
from catalog.models import Book


@patch("catalog.services.urllib.request.urlopen")
def test_notify_external_mock(mock_urlopen):
    mock_urlopen.return_value.__enter__.return_value.status = 200
    assert services.notify_external("Дюна") == 200
    mock_urlopen.assert_called_once_with("https://api.example.com/notify?title=Дюна", timeout=5)


@pytest.mark.django_db
@patch("catalog.views.notify_external")
@patch("catalog.views.generate_code", return_value="BK-0001")
def test_generate_code_mock(mock_code, mock_notify, client, category):
    client.post("/books/new/", {"title": "Тест", "year": 2021, "category": category.pk})
    mock_code.assert_called_once_with()
    assert Book.objects.filter(title="Тест").exists()
