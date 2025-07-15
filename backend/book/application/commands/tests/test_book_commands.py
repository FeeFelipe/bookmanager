import pytest
from datetime import date
from book.domain.book_entities import Book
from book.application.commands.book_commands import BookCommands


@pytest.fixture
def make_book():
    def _make(**overrides):
        data = {
            "id": None,
            "title": "Clean Code",
            "isbn": "1234567890123",
            "publisher": "Prentice Hall",
            "edition": "1st",
            "language": "English",
            "book_type": "Technical",
            "synopsis": "A book about writing clean code.",
            "publication_date": date(2008, 8, 1),
            "authors": [],
            "categories": [],
        }
        data.update(overrides)
        return Book(**data)
    return _make


@pytest.fixture
def commands(mocker):
    mocker.patch("book.application.commands.book_commands.BookRepository")
    return BookCommands()


def test_create_book_sends_task(commands, mocker, make_book):
    book = make_book()
    mock_send = mocker.patch("book.application.commands.book_commands.create_book_task.send")
    log_spy = mocker.spy(commands.logger, "info")

    result = commands.create(book)

    mock_send.assert_called_once()
    assert isinstance(result, Book)
    assert result.title == book.title
    log_spy.assert_any_call("[BookCommands] Queuing book for creation: Clean Code")


def test_update_book_success(commands, mocker, make_book):
    book_id = 1
    updated_input = make_book()
    updated_result = make_book(id=book_id)

    mock_repo = commands.repository
    mock_repo.get_by_id.return_value = updated_input
    mock_repo.update.return_value = updated_result

    mock_search_repo = mocker.patch("book.application.commands.book_commands.BookSearchRepository")

    log_spy = mocker.spy(commands.logger, "info")

    result = commands.update(book_id, updated_input)

    assert result == updated_result
    assert updated_input.id == book_id
    mock_repo.get_by_id.assert_called_once_with(book_id)
    mock_repo.update.assert_called_once_with(book_id, updated_input)
    mock_search_repo.return_value.index_book.assert_called_once()
    log_spy.assert_any_call("[BookCommands] Updating book with ID: 1")
    log_spy.assert_any_call("[BookCommands] Book ID 1 updated successfully")


def test_update_book_not_found(commands, mocker, make_book):
    mock_repo = commands.repository
    mock_repo.get_by_id.return_value = None

    log_spy = mocker.spy(commands.logger, "warning")

    with pytest.raises(ValueError, match="Book not found"):
        commands.update(999, make_book())

    mock_repo.get_by_id.assert_called_once_with(999)
    log_spy.assert_called_once_with("[BookCommands] Attempt to update non-existent book ID: 999")


def test_delete_book_success(commands, mocker, make_book):
    book_id = 1
    book = make_book(id=book_id, isbn="123")
    mock_repo = commands.repository
    mock_repo.get_by_id.return_value = book

    mock_delete_book = mocker.patch("book.application.commands.book_commands.BookSearchRepository.delete_book")
    log_spy = mocker.spy(commands.logger, "info")

    commands.delete(book_id)

    mock_repo.get_by_id.assert_called_once_with(book_id)
    mock_repo.delete.assert_called_once_with(book_id)
    mock_delete_book.assert_called_once_with("123")
    log_spy.assert_any_call("[BookCommands] Deleting book with ID: 1")
    log_spy.assert_any_call("[BookCommands] Book ID 1 deleted successfully")


def test_delete_book_not_found(commands, mocker):
    mock_repo = commands.repository
    mock_repo.get_by_id.return_value = None
    log_spy = mocker.spy(commands.logger, "warning")

    with pytest.raises(ValueError, match="Book not found"):
        commands.delete(999)

    mock_repo.get_by_id.assert_called_once_with(999)
    log_spy.assert_called_once_with("[BookCommands] Attempt to delete non-existent book ID: 999")
