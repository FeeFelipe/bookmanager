import pytest

from author.application.commands.author_commands import AuthorCommands
from author.domain.author_entities import Author


@pytest.fixture
def mock_repository(mocker):
    repo = mocker.patch("author.application.commands.author_commands.AuthorRepository", autospec=True)
    return repo.return_value


@pytest.fixture
def commands(mock_repository):
    return AuthorCommands()


@pytest.fixture
def valid_author_data():
    return Author(id=None, name="New Author")


def test_create_author(commands, mock_repository, mocker, valid_author_data):
    created_author = Author(
        **{**valid_author_data.__dict__, "id": 1}
    )
    mock_repository.create.return_value = created_author

    log_spy = mocker.spy(commands.logger, "info")
    result = commands.create(valid_author_data)

    assert result == created_author
    mock_repository.create.assert_called_once_with(valid_author_data)
    log_spy.assert_any_call("[AuthorCommands] Creating new author: New Author")
    log_spy.assert_any_call("[AuthorCommands] Author created successfully with ID: 1")


def test_update_author_success(commands, mock_repository, mocker, valid_author_data):
    existing = Author(
        **{**valid_author_data.__dict__, "id": 1, "name": "Old"}
    )
    updated = Author(
        **{**valid_author_data.__dict__, "id": 1, "name": "Updated"}
    )
    updated_input = Author(
        **{**valid_author_data.__dict__, "name": "Updated"}
    )

    mock_repository.get_by_id.return_value = existing
    mock_repository.update.return_value = updated

    log_spy = mocker.spy(commands.logger, "info")
    result = commands.update(1, updated_input)

    assert result == updated
    mock_repository.get_by_id.assert_called_once_with(1)
    mock_repository.update.assert_called_once_with(1, updated_input)
    log_spy.assert_any_call("[AuthorCommands] Updating author with ID: 1")
    log_spy.assert_any_call("[AuthorCommands] Author ID 1 updated successfully")


def test_update_author_not_found(commands, mock_repository, mocker, valid_author_data):
    mock_repository.get_by_id.return_value = None
    log_spy = mocker.spy(commands.logger, "warning")

    input_data = Author(
        **{**valid_author_data.__dict__, "name": "Fallback"}
    )

    with pytest.raises(ValueError, match="Author not found"):
        commands.update(999, input_data)

    mock_repository.get_by_id.assert_called_once_with(999)
    log_spy.assert_called_once_with("[AuthorCommands] Attempt to update non-existent author ID: 999")


def test_delete_author_success(commands, mock_repository, mocker, valid_author_data):
    mock_repository.get_by_id.return_value = Author(
        **{**valid_author_data.__dict__, "id": 1}
    )
    log_spy = mocker.spy(commands.logger, "info")

    commands.delete(1)

    mock_repository.get_by_id.assert_called_once_with(1)
    mock_repository.delete.assert_called_once_with(1)
    log_spy.assert_any_call("[AuthorCommands] Deleting author with ID: 1")
    log_spy.assert_any_call("[AuthorCommands] Author ID 1 deleted successfully")


def test_delete_author_not_found(commands, mock_repository, mocker):
    mock_repository.get_by_id.return_value = None
    log_spy = mocker.spy(commands.logger, "warning")

    with pytest.raises(ValueError, match="Author not found"):
        commands.delete(123)

    mock_repository.get_by_id.assert_called_once_with(123)
    log_spy.assert_called_once_with("[AuthorCommands] Attempt to delete non-existent author ID: 123")
