import pytest
from rest_framework.test import APIClient

from book.application.commands.book_commands import BookCommands
from book.application.queries.book_queries import BookQueries
from book.domain.book_entities import Book


@pytest.fixture
def client(mocker):
    client = APIClient()
    client.force_authenticate(user=mocker.Mock())
    return client


@pytest.fixture
def make_book():
    def _make_book(**overrides):
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

    return _make_book


def test_get_book_found(client, mocker, make_book):
    mocker.patch.object(BookQueries, "get_by_id", return_value=make_book())

    response = client.get("/api/book/1/")

    assert response.status_code == 200
    assert response.data["title"] == "Clean Code"


def test_get_book_not_found(client, mocker):
    mocker.patch.object(BookQueries, "get_by_id", return_value=None)

    response = client.get("/api/book/999/")

    assert response.status_code == 404
    assert response.data["detail"] == "Book not found"


def test_get_book_error(client, mocker):
    mocker.patch.object(BookQueries, "get_by_id", side_effect=Exception("fail"))

    response = client.get("/api/book/1/")

    assert response.status_code == 500
    assert response.data["detail"] == "Error retrieving book"


def test_get_books_with_fuzzy_search(client, mocker, make_book):
    mock_queryset = mocker.Mock()
    mock_annotated = mocker.Mock()
    mock_filtered = [make_book(title="Clean Code")]

    mock_queryset.annotate.return_value = mock_annotated
    mock_annotated.filter.return_value.order_by.return_value = mock_filtered

    mocker.patch.object(BookQueries, "get_queryset", return_value=mock_queryset)

    response = client.get("/api/book/?search=clean")

    assert response.status_code == 200
    assert response.data[0]["title"] == "Clean Code"


def test_get_all_books(client, mocker, make_book):
    mocker.patch.object(BookQueries, "get_all", return_value=[make_book(), make_book(id=2, title="Refactoring")])

    response = client.get("/api/book/")

    assert response.status_code == 200
    assert len(response.data) == 2


def test_get_all_books_error(client, mocker):
    mocker.patch.object(BookQueries, "get_all", side_effect=Exception("fail"))

    response = client.get("/api/book/")

    assert response.status_code == 500
    assert response.data["detail"] == "Error retrieving book list"


def test_post_book_success(client, mocker, make_book):
    mocker.patch.object(BookCommands, "create", return_value=make_book())

    data = make_book().__dict__.copy()
    data.pop("id")

    response = client.post("/api/book/", data, format="json")

    assert response.status_code == 201
    assert response.data["title"] == "Clean Code"


def test_post_book_invalid(client):
    response = client.post("/api/book/", {}, format="json")
    assert response.status_code == 400
    assert "title" in response.data


def test_post_book_error(client, mocker, make_book):
    mocker.patch.object(BookCommands, "create", side_effect=Exception("fail"))

    data = make_book().__dict__.copy()
    data.pop("id")

    response = client.post("/api/book/", data, format="json")

    assert response.status_code == 500
    assert response.data["detail"] == "Error creating book"


def test_put_book_success(client, mocker, make_book):
    mocker.patch.object(BookCommands, "update", return_value=make_book(title="Updated"))

    data = make_book().__dict__.copy()
    data.pop("id")

    response = client.put("/api/book/1/", data, format="json")

    assert response.status_code == 200
    assert response.data["title"] == "Updated"


def test_put_book_not_found(client, mocker, make_book):
    mocker.patch.object(BookCommands, "update", side_effect=ValueError("Book not found"))

    data = make_book().__dict__.copy()
    data.pop("id")

    response = client.put("/api/book/999/", data, format="json")

    assert response.status_code == 404
    assert response.data["detail"] == "Book not found"


def test_put_book_invalid(client):
    response = client.put("/api/book/1/", {}, format="json")
    assert response.status_code == 400
    assert "title" in response.data


def test_put_book_exception(client, mocker, make_book):
    mock_command = mocker.patch("book.interface.book_view.BookCommands")
    mock_command().update.side_effect = Exception("update failed")

    data = make_book().__dict__.copy()
    data.pop("id")

    response = client.put("/api/book/1/", data, format="json")

    assert response.status_code == 500
    assert response.data["detail"] == "Error updating book"


def test_delete_book_success(client, mocker):
    mocker.patch.object(BookCommands, "delete")

    response = client.delete("/api/book/1/")

    assert response.status_code == 204


def test_delete_book_not_found(client, mocker):
    mocker.patch.object(BookCommands, "delete", side_effect=ValueError("Book not found"))

    response = client.delete("/api/book/123/")

    assert response.status_code == 404
    assert response.data["detail"] == "Book not found"


def test_delete_book_error(client, mocker):
    mocker.patch.object(BookCommands, "delete", side_effect=Exception("fail"))

    response = client.delete("/api/book/1/")

    assert response.status_code == 500
    assert response.data["detail"] == "Error deleting book"
