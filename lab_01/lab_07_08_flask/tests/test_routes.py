from unittest.mock import patch


def test_book_list_200(client, book):
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json[0]["title"] == "Дюна"


def test_book_detail_404(client):
    assert client.get("/books/999").status_code == 404


def test_book_create_400(client):
    assert client.post("/books", json={"title": ""}).status_code == 400


@patch("app.generate_code", return_value="BK-0001")
def test_book_create_201(mock_code, client, category):
    response = client.post("/books", json={"title": "Нова", "year": 2020, "category_id": category.id})
    assert response.status_code == 201
    assert response.json["code"] == "BK-0001"
    mock_code.assert_called_once_with()
