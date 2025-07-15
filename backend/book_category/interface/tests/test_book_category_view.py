import pytest
from rest_framework import status
from rest_framework.test import APIClient

from book_category.domain.book_category_entities import BookCategory


@pytest.fixture
def client(mocker):
    client = APIClient()
    client.force_authenticate(user=mocker.Mock())
    return client


@pytest.fixture
def make_book_category():
    def _make_book_category(**overrides):
        data = {
            "id": 1,
            "name": "Fiction"
        }
        data.update(overrides)
        return BookCategory(**data)

    return _make_book_category


def test_get_category_found(client, mocker, make_book_category):
    mock_query = mocker.patch("book_category.interface.book_category_view.BookCategoryQueries")
    mock_query().get_by_id.return_value = make_book_category()

    response = client.get("/api/bookcategory/1/")

    assert response.status_code == 200
    assert response.data["name"] == "Fiction"
    mock_query().get_by_id.assert_called_once_with(1)


def test_get_category_not_found(client, mocker):
    mock_query = mocker.patch("book_category.interface.book_category_view.BookCategoryQueries")
    mock_query().get_by_id.return_value = None

    response = client.get("/api/bookcategory/999/")

    assert response.status_code == 404
    assert response.data["detail"] == "BookCategory not found"


def test_get_category_exception(client, mocker):
    mock_query = mocker.patch("book_category.interface.book_category_view.BookCategoryQueries")
    mock_query().get_by_id.side_effect = Exception("Unexpected error")

    response = client.get("/api/bookcategory/1/")

    assert response.status_code == 500
    assert response.data["detail"] == "Error retrieving book"


def test_get_all_categories(client, mocker, make_book_category):
    mock_query = mocker.patch("book_category.interface.book_category_view.BookCategoryQueries")
    mock_query().get_all.return_value = [
        make_book_category(),
        make_book_category(id=2, name="History")
    ]

    response = client.get("/api/bookcategory/")

    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]["name"] == "Fiction"
    assert response.data[1]["name"] == "History"
    mock_query().get_all.assert_called_once()


def test_get_all_categories_exception(client, mocker):
    mock_query = mocker.patch("book_category.interface.book_category_view.BookCategoryQueries")
    mock_query().get_all.side_effect = Exception("DB down")

    response = client.get("/api/bookcategory/")

    assert response.status_code == 500
    assert response.data["detail"] == "Error retrieving book category list"


def test_post_category_created(client, mocker, make_book_category):
    mock_command = mocker.patch("book_category.interface.book_category_view.BookCategoryCommands")
    mock_command().create.return_value = make_book_category()

    response = client.post("/api/bookcategory/", {"name": "New Category"}, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["id"] == 1
    assert response.data["name"] == "Fiction"
    mock_command().create.assert_called_once()


def test_post_category_invalid(client):
    response = client.post("/api/bookcategory/", {}, format="json")

    assert response.status_code == 400
    assert "name" in response.data


def test_post_category_exception(client, mocker):
    mock_command = mocker.patch("book_category.interface.book_category_view.BookCategoryCommands")
    mock_command().create.side_effect = Exception("Unexpected error")

    response = client.post("/api/bookcategory/", {"name": "Fiction"}, format="json")

    assert response.status_code == 500
    assert response.data["detail"] == "Error creating book category"


def test_put_category_success(client, mocker, make_book_category):
    updated = make_book_category(name="Updated Category")
    mock_command = mocker.patch("book_category.interface.book_category_view.BookCategoryCommands")
    mock_command().update.return_value = updated

    response = client.put("/api/bookcategory/1/", {"name": updated.name}, format="json")

    assert response.status_code == 200
    assert response.data["name"] == "Updated Category"
    mock_command().update.assert_called_once()


def test_put_category_not_found(client, mocker):
    mock_command = mocker.patch("book_category.interface.book_category_view.BookCategoryCommands")
    mock_command().update.side_effect = ValueError("BookCategory not found")

    response = client.put("/api/bookcategory/999/", {"name": "X"}, format="json")

    assert response.status_code == 404
    assert response.data["detail"] == "BookCategory not found"


def test_put_category_invalid(client):
    response = client.put("/api/bookcategory/1/", {}, format="json")

    assert response.status_code == 400
    assert "name" in response.data


def test_put_category_exception(client, mocker):
    mock_command = mocker.patch("book_category.interface.book_category_view.BookCategoryCommands")
    mock_command().update.side_effect = Exception("Unexpected")

    response = client.put("/api/bookcategory/1/", {"name": "Test"}, format="json")

    assert response.status_code == 500
    assert response.data["detail"] == "Error updating book category"


def test_delete_category_success(client, mocker):
    mock_command = mocker.patch("book_category.interface.book_category_view.BookCategoryCommands")

    response = client.delete("/api/bookcategory/1/")

    assert response.status_code == 204
    mock_command().delete.assert_called_once_with(1)


def test_delete_category_not_found(client, mocker):
    mock_command = mocker.patch("book_category.interface.book_category_view.BookCategoryCommands")
    mock_command().delete.side_effect = ValueError("BookCategory not found")

    response = client.delete("/api/bookcategory/123/")

    assert response.status_code == 404
    assert response.data["detail"] == "BookCategory not found"


def test_delete_category_exception(client, mocker):
    mock_command = mocker.patch("book_category.interface.book_category_view.BookCategoryCommands")
    mock_command().delete.side_effect = Exception("Unexpected error")

    response = client.delete("/api/bookcategory/1/")

    assert response.status_code == 500
    assert response.data["detail"] == "Error deleting book category"
