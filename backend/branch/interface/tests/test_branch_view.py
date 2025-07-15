import pytest
from rest_framework import status
from rest_framework.test import APIClient

from branch.domain.branch_entities import Branch


@pytest.fixture
def client(mocker):
    client = APIClient()
    client.force_authenticate(user=mocker.Mock())
    return client


@pytest.fixture
def make_branch():
    def _make_branch(**overrides):
        data = {
            "id": 1,
            "name": "Central Library",
            "location": "123 Main St"
        }
        data.update(overrides)
        return Branch(**data)

    return _make_branch


def test_get_branch_found(client, mocker, make_branch):
    mock_query = mocker.patch("branch.interface.branch_view.BranchQueries")
    mock_query().get_by_id.return_value = make_branch()

    response = client.get("/api/branch/1/")

    assert response.status_code == 200
    assert response.data["name"] == "Central Library"
    mock_query().get_by_id.assert_called_once_with(1)


def test_get_branch_not_found(client, mocker):
    mock_query = mocker.patch("branch.interface.branch_view.BranchQueries")
    mock_query().get_by_id.return_value = None

    response = client.get("/api/branch/999/")

    assert response.status_code == 404
    assert response.data["detail"] == "Branch not found"


def test_get_branch_unexpected_error(client, mocker):
    mock_query = mocker.patch("branch.interface.branch_view.BranchQueries")
    mock_query().get_by_id.side_effect = Exception("DB error")

    response = client.get("/api/branch/1/")

    assert response.status_code == 500
    assert response.data["detail"] == "Error retrieving branch"


def test_get_all_branches(client, mocker, make_branch):
    mock_query = mocker.patch("branch.interface.branch_view.BranchQueries")
    mock_query().get_all.return_value = [make_branch(), make_branch(id=2, name="Branch B")]

    response = client.get("/api/branch/")

    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]["name"] == "Central Library"
    assert response.data[1]["name"] == "Branch B"
    mock_query().get_all.assert_called_once()


def test_get_all_branches_unexpected_error(client, mocker):
    mock_query = mocker.patch("branch.interface.branch_view.BranchQueries")
    mock_query().get_all.side_effect = Exception("Unexpected failure")

    response = client.get("/api/branch/")

    assert response.status_code == 500
    assert response.data["detail"] == "Error retrieving branch list"


def test_post_branch_created(client, mocker, make_branch):
    mock_command = mocker.patch("branch.interface.branch_view.BranchCommands")
    mock_command().create.return_value = make_branch()

    response = client.post("/api/branch/", {
        "name": "Central Library",
        "location": "123 Main St"
    }, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["id"] == 1
    assert response.data["name"] == "Central Library"
    mock_command().create.assert_called_once()


def test_post_branch_invalid(client):
    response = client.post("/api/branch/", {}, format="json")

    assert response.status_code == 400
    assert "name" in response.data


def test_post_branch_unexpected_error(client, mocker):
    mock_command = mocker.patch("branch.interface.branch_view.BranchCommands")
    mock_command().create.side_effect = Exception("DB failure")

    response = client.post("/api/branch/", {
        "name": "Central Library",
        "location": "123 Main St"
    }, format="json")

    assert response.status_code == 500
    assert response.data["detail"] == "Error creating branch"


def test_put_branch_success(client, mocker, make_branch):
    mock_command = mocker.patch("branch.interface.branch_view.BranchCommands")
    mock_command().update.return_value = make_branch(name="Updated Branch")

    response = client.put("/api/branch/1/", {
        "name": "Updated Branch",
        "location": "Updated Location"
    }, format="json")

    assert response.status_code == 200
    assert response.data["name"] == "Updated Branch"
    mock_command().update.assert_called_once()


def test_put_branch_not_found(client, mocker):
    mock_command = mocker.patch("branch.interface.branch_view.BranchCommands")
    mock_command().update.side_effect = ValueError("Branch not found")

    response = client.put("/api/branch/999/", {
        "name": "Updated Branch",
        "location": "Updated Location"
    }, format="json")

    assert response.status_code == 404
    assert response.data["detail"] == "Branch not found"


def test_put_branch_invalid(client):
    response = client.put("/api/branch/1/", {}, format="json")

    assert response.status_code == 400
    assert "name" in response.data


def test_put_branch_unexpected_error(client, mocker):
    mock_command = mocker.patch("branch.interface.branch_view.BranchCommands")
    mock_command().update.side_effect = Exception("Internal error")

    response = client.put("/api/branch/1/", {
        "name": "Updated Branch",
        "location": "Updated Location"
    }, format="json")

    assert response.status_code == 500
    assert response.data["detail"] == "Error updating branch"


def test_delete_branch_success(client, mocker):
    mock_command = mocker.patch("branch.interface.branch_view.BranchCommands")

    response = client.delete("/api/branch/1/")

    assert response.status_code == 204
    mock_command().delete.assert_called_once_with(1)


def test_delete_branch_not_found(client, mocker):
    mock_command = mocker.patch("branch.interface.branch_view.BranchCommands")
    mock_command().delete.side_effect = ValueError("Branch not found")

    response = client.delete("/api/branch/999/")

    assert response.status_code == 404
    assert response.data["detail"] == "Branch not found"


def test_delete_branch_unexpected_error(client, mocker):
    mock_command = mocker.patch("branch.interface.branch_view.BranchCommands")
    mock_command().delete.side_effect = Exception("Unexpected crash")

    response = client.delete("/api/branch/1/")

    assert response.status_code == 500
    assert response.data["detail"] == "Error deleting branch"
