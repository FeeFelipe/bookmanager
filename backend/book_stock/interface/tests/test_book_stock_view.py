import pytest
from rest_framework.test import APIClient

from book.domain.book_entities import Book
from book_stock.domain.book_stock_entities import BookStock
from branch.domain.branch_entities import Branch


def make_book(**overrides):
    data = {
        "id": 1,
        "title": "Clean Code",
        "isbn": "1234567890123",
        "publisher": "Prentice Hall",
        "edition": "1st",
        "language": "English",
        "book_type": "Technical",
        "synopsis": "A book about writing clean code.",
        "publication_date": "2008-08-01",
        "authors": [],
        "categories": [],
    }
    data.update(overrides)
    return Book(**data)


def make_branch(**overrides):
    data = {
        "id": 1,
        "name": "Central Library",
        "location": "123 Main St"
    }
    data.update(overrides)
    return Branch(**data)


@pytest.fixture
def client(mocker):
    client = APIClient()
    client.force_authenticate(user=mocker.Mock())
    return client


@pytest.fixture
def make_book_stock():
    def _make_book_stock(**overrides):
        data = {
            "id": 1,
            "book": make_book(),
            "branch": make_branch(),
            "shelf": "220D 400F",
            "floor": "1 floor",
            "room": "4 d",
            "status": "available"
        }
        data.update(overrides)
        return BookStock(**data)
    return _make_book_stock


def test_get_book_stock_found(client, mocker, make_book_stock):
    mock_query = mocker.patch("book_stock.interface.book_stock_view.BookStockQueries")
    mock_query().get_by_id.return_value = make_book_stock()

    response = client.get("/api/bookstock/1/")

    assert response.status_code == 200
    assert response.data["book"]["id"] == 1


def test_get_book_stock_not_found(client, mocker):
    mock_query = mocker.patch("book_stock.interface.book_stock_view.BookStockQueries")
    mock_query().get_by_id.return_value = None

    response = client.get("/api/bookstock/999/")

    assert response.status_code == 404
    assert response.data["detail"] == "BookStock not found"


def test_get_book_stock_exception(client, mocker):
    mock_query = mocker.patch("book_stock.interface.book_stock_view.BookStockQueries")
    mock_query().get_by_id.side_effect = Exception("unexpected")

    response = client.get("/api/bookstock/1/")

    assert response.status_code == 500
    assert response.data["detail"] == "Error retrieving book_stock"


def test_get_all_book_stocks(client, mocker, make_book_stock):
    mock_query = mocker.patch("book_stock.interface.book_stock_view.BookStockQueries")
    mock_query().get_all.return_value = [
        make_book_stock(),
        make_book_stock(id=2, book=make_book(id=2))
    ]

    response = client.get("/api/bookstock/")

    assert response.status_code == 200
    assert len(response.data) == 2


def test_get_all_book_stocks_exception(client, mocker):
    mock_query = mocker.patch("book_stock.interface.book_stock_view.BookStockQueries")
    mock_query().get_all.side_effect = Exception("db error")

    response = client.get("/api/bookstock/")

    assert response.status_code == 500
    assert response.data["detail"] == "Error retrieving book_stock list"


def test_post_book_stock_created(client, mocker, make_book_stock):
    mock_command = mocker.patch("book_stock.interface.book_stock_view.BookStockCommands")
    mock_command().create.return_value = make_book_stock()

    data = make_book_stock()
    response = client.post("/api/bookstock/", {
        "book": data.book.id,
        "branch": data.branch.id,
        "shelf": data.shelf,
        "floor": data.floor,
        "room": data.room,
        "status": data.status
    }, format="json")

    assert response.status_code == 201
    assert response.data["book"]["id"] == 1


def test_post_book_stock_invalid(client):
    response = client.post("/api/bookstock/", {}, format="json")

    assert response.status_code == 400
    assert "book" in response.data


def test_post_book_stock_exception(client, mocker, make_book_stock):
    mock_command = mocker.patch("book_stock.interface.book_stock_view.BookStockCommands")
    mock_command().create.side_effect = Exception("unexpected")

    data = make_book_stock()
    response = client.post("/api/bookstock/", {
        "book": data.book.id,
        "branch": data.branch.id,
        "shelf": data.shelf,
        "floor": data.floor,
        "room": data.room,
        "status": data.status
    }, format="json")

    assert response.status_code == 500
    assert response.data["detail"] == "Error creating book_stock"


def test_put_book_stock_success(client, mocker, make_book_stock):
    mock_command = mocker.patch("book_stock.interface.book_stock_view.BookStockCommands")
    mock_command().update.return_value = make_book_stock()

    data = make_book_stock()
    response = client.put("/api/bookstock/1/", {
        "book": data.book.id,
        "branch": data.branch.id,
        "shelf": data.shelf,
        "floor": data.floor,
        "room": data.room,
        "status": data.status
    }, format="json")

    assert response.status_code == 200
    assert response.data["book"]["id"] == 1


def test_put_book_stock_not_found(client, mocker, make_book_stock):
    mock_command = mocker.patch("book_stock.interface.book_stock_view.BookStockCommands")
    mock_command().update.side_effect = ValueError("BookStock not found")

    data = make_book_stock()
    response = client.put("/api/bookstock/999/", {
        "book": data.book.id,
        "branch": data.branch.id,
        "shelf": data.shelf,
        "floor": data.floor,
        "room": data.room,
        "status": data.status
    }, format="json")

    assert response.status_code == 404
    assert response.data["detail"] == "BookStock not found"


def test_put_book_stock_invalid(client):
    response = client.put("/api/bookstock/1/", {}, format="json")

    assert response.status_code == 400
    assert "book" in response.data


def test_put_book_stock_exception(client, mocker, make_book_stock):
    mock_command = mocker.patch("book_stock.interface.book_stock_view.BookStockCommands")
    mock_command().update.side_effect = Exception("unexpected")

    data = make_book_stock()
    response = client.put("/api/bookstock/1/", {
        "book": data.book.id,
        "branch": data.branch.id,
        "shelf": data.shelf,
        "floor": data.floor,
        "room": data.room,
        "status": data.status
    }, format="json")

    assert response.status_code == 500
    assert response.data["detail"] == "Error updating book_stock"


def test_delete_book_stock_success(client, mocker):
    mock_command = mocker.patch("book_stock.interface.book_stock_view.BookStockCommands")

    response = client.delete("/api/bookstock/1/")

    assert response.status_code == 204
    mock_command().delete.assert_called_once_with(1)


def test_delete_book_stock_not_found(client, mocker):
    mock_command = mocker.patch("book_stock.interface.book_stock_view.BookStockCommands")
    mock_command().delete.side_effect = ValueError("BookStock not found")

    response = client.delete("/api/bookstock/999/")

    assert response.status_code == 404
    assert response.data["detail"] == "BookStock not found"


def test_delete_book_stock_exception(client, mocker):
    mock_command = mocker.patch("book_stock.interface.book_stock_view.BookStockCommands")
    mock_command().delete.side_effect = Exception("unexpected")

    response = client.delete("/api/bookstock/1/")

    assert response.status_code == 500
    assert response.data["detail"] == "Error deleting book_stock"
