import pytest

from book_category.application.commands.book_category_commands import BookCategoryCommands
from book_category.domain.book_category_entities import BookCategory


@pytest.fixture
def mock_repository(mocker):
    repo = mocker.patch("book_category.application.commands.book_category_commands.BookCategoryRepository",
                        autospec=True)
    return repo.return_value


@pytest.fixture
def commands(mock_repository):
    return BookCategoryCommands()


@pytest.fixture
def valid_book_category_data():
    return BookCategory(id=None, name="Programming")


def test_create_book_category(commands, mock_repository, valid_book_category_data, mocker):
    created = BookCategory(**{**valid_book_category_data.__dict__, "id": 1})
    mock_repository.create.return_value = created

    log_spy = mocker.spy(commands.logger, "info")
    result = commands.create(valid_book_category_data)

    assert result == created
    mock_repository.create.assert_called_once_with(valid_book_category_data)
    log_spy.assert_any_call("[BookCategoryCommands] Creating new book category: Programming")
    log_spy.assert_any_call("[BookCategoryCommands] BookCategory created successfully with ID: 1")


def test_update_book_category_success(commands, mock_repository, valid_book_category_data, mocker):
    category_id = 1
    existing = BookCategory(**{**valid_book_category_data.__dict__, "id": category_id})
    updated_input = BookCategory(**{**valid_book_category_data.__dict__})
    updated_result = BookCategory(
        **{**valid_book_category_data.__dict__, "id": category_id, "name": "Software Engineering"})

    mock_repository.get_by_id.return_value = existing
    mock_repository.update.return_value = updated_result

    log_spy = mocker.spy(commands.logger, "info")
    result = commands.update(category_id, updated_input)

    assert result == updated_result
    assert updated_input.id == category_id
    mock_repository.get_by_id.assert_called_once_with(category_id)
    mock_repository.update.assert_called_once_with(category_id, updated_input)
    log_spy.assert_any_call("[BookCategoryCommands] Updating book category with ID: 1")
    log_spy.assert_any_call("[BookCategoryCommands] BookCategory ID 1 updated successfully")


def test_update_book_category_not_found(commands, mock_repository, valid_book_category_data, mocker):
    mock_repository.get_by_id.return_value = None
    log_spy = mocker.spy(commands.logger, "warning")

    with pytest.raises(ValueError, match="BookCategory not found"):
        commands.update(999, valid_book_category_data)

    mock_repository.get_by_id.assert_called_once_with(999)
    log_spy.assert_called_once_with("[BookCategoryCommands] Attempt to update non-existent book category ID: 999")


def test_delete_book_category_success(commands, mock_repository, mocker):
    mock_repository.get_by_id.return_value = BookCategory(id=1, name="Test")
    log_spy = mocker.spy(commands.logger, "info")

    commands.delete(1)

    mock_repository.get_by_id.assert_called_once_with(1)
    mock_repository.delete.assert_called_once_with(1)
    log_spy.assert_any_call("[BookCategoryCommands] Deleting book category with ID: 1")
    log_spy.assert_any_call("[BookCategoryCommands] BookCategory ID 1 deleted successfully")


def test_delete_book_category_not_found(commands, mock_repository, mocker):
    mock_repository.get_by_id.return_value = None
    log_spy = mocker.spy(commands.logger, "warning")

    with pytest.raises(ValueError, match="BookCategory not found"):
        commands.delete(999)

    mock_repository.get_by_id.assert_called_once_with(999)
    log_spy.assert_called_once_with("[BookCategoryCommands] Attempt to delete non-existent book category ID: 999")
