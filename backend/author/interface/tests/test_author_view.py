import pytest
from rest_framework.test import APIClient

from author.domain.author_entities import Author


@pytest.fixture
def client(mocker):
    client = APIClient()
    client.force_authenticate(user=mocker.Mock())
    return client


@pytest.fixture
def make_author():
    def _make_author(**overrides):
        data = {
            "id": 1,
            "name": "Author A"
        }
        data.update(overrides)
        return Author(**data)

    return _make_author


def test_get_author_found(client, mocker, make_author):
    mock_query = mocker.patch("author.interface.author_view.AuthorQueries")
    mock_query().get_by_id.return_value = make_author()

    response = client.get("/api/author/1/")

    assert response.status_code == 200
    assert response.data["name"] == "Author A"


def test_get_author_not_found(client, mocker):
    mock_query = mocker.patch("author.interface.author_view.AuthorQueries")
    mock_query().get_by_id.return_value = None

    response = client.get("/api/author/999/")

    assert response.status_code == 404
    assert response.data["detail"] == "Author not found"


def test_get_author_exception(client, mocker):
    mock_query = mocker.patch("author.interface.author_view.AuthorQueries")
    mock_query().get_by_id.side_effect = Exception("error")

    response = client.get("/api/author/1/")

    assert response.status_code == 500
    assert response.data["detail"] == "Error retrieving author"


def test_get_all_authors(client, mocker, make_author):
    mock_query = mocker.patch("author.interface.author_view.AuthorQueries")
    mock_query().get_all.return_value = [
        make_author(),
        make_author(id=2, name="Author B")
    ]

    response = client.get("/api/author/")

    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]["name"] == "Author A"
    assert response.data[1]["name"] == "Author B"


def test_get_all_authors_exception(client, mocker):
    mock_query = mocker.patch("author.interface.author_view.AuthorQueries")
    mock_query().get_all.side_effect = Exception("db error")

    response = client.get("/api/author/")

    assert response.status_code == 500
    assert response.data["detail"] == "Error retrieving author list"


def test_post_author_created(client, mocker, make_author):
    mock_command = mocker.patch("author.interface.author_view.AuthorCommands")
    mock_command().create.return_value = make_author()

    response = client.post("/api/author/", {"name": "Author A"}, format="json")

    assert response.status_code == 201
    assert response.data["id"] == 1
    assert response.data["name"] == "Author A"


def test_post_author_invalid(client):
    response = client.post("/api/author/", {}, format="json")

    assert response.status_code == 400
    assert "name" in response.data


def test_post_author_exception(client, mocker):
    mock_command = mocker.patch("author.interface.author_view.AuthorCommands")
    mock_command().create.side_effect = Exception("unexpected")

    response = client.post("/api/author/", {"name": "Author A"}, format="json")

    assert response.status_code == 500
    assert response.data["detail"] == "Error creating author"


def test_put_author_success(client, mocker, make_author):
    mock_command = mocker.patch("author.interface.author_view.AuthorCommands")
    mock_command().update.return_value = make_author(name="Updated Author")

    response = client.put("/api/author/1/", {"name": "Updated Author"}, format="json")

    assert response.status_code == 200
    assert response.data["name"] == "Updated Author"


def test_put_author_not_found(client, mocker):
    mock_command = mocker.patch("author.interface.author_view.AuthorCommands")
    mock_command().update.side_effect = ValueError("Author not found")

    response = client.put("/api/author/999/", {"name": "Updated Author"}, format="json")

    assert response.status_code == 404
    assert response.data["detail"] == "Author not found"


def test_put_author_invalid(client):
    response = client.put("/api/author/1/", {}, format="json")

    assert response.status_code == 400
    assert "name" in response.data


def test_put_author_exception(client, mocker):
    mock_command = mocker.patch("author.interface.author_view.AuthorCommands")
    mock_command().update.side_effect = Exception("update failed")

    response = client.put("/api/author/1/", {"name": "Updated Author"}, format="json")

    assert response.status_code == 500
    assert response.data["detail"] == "Error updating author"


def test_delete_author_success(client, mocker):
    mock_command = mocker.patch("author.interface.author_view.AuthorCommands")

    response = client.delete("/api/author/1/")

    assert response.status_code == 204
    mock_command().delete.assert_called_once_with(1)


def test_delete_author_not_found(client, mocker):
    mock_command = mocker.patch("author.interface.author_view.AuthorCommands")
    mock_command().delete.side_effect = ValueError("Author not found")

    response = client.delete("/api/author/999/")

    assert response.status_code == 404
    assert response.data["detail"] == "Author not found"


def test_delete_author_exception(client, mocker):
    mock_command = mocker.patch("author.interface.author_view.AuthorCommands")
    mock_command().delete.side_effect = Exception("delete error")

    response = client.delete("/api/author/1/")

    assert response.status_code == 500
    assert response.data["detail"] == "Error deleting author"
