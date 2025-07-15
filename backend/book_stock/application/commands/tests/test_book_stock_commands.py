import pytest
from book_stock.application.commands.book_stock_commands import BookStockCommands
from book_stock.domain.book_stock_entities import BookStock


@pytest.fixture
def mock_repository(mocker):
    repo = mocker.patch(
        "book_stock.application.commands.book_stock_commands.BookStockRepository", autospec=True
    )
    return repo.return_value


@pytest.fixture
def commands(mock_repository):
    return BookStockCommands()


@pytest.fixture
def make_book_stock():
    def _make_book_stock(**overrides):
        data = {
            "id": None,
            "book": 1,
            "branch": 10,
            "shelf": "L200 D500",
            "floor": "first",
            "room": "204",
            "status": "available",
        }
        data.update(overrides)
        return BookStock(**data)

    return _make_book_stock


def test_create_book_stock(commands, mock_repository, make_book_stock, mocker):
    input_stock = make_book_stock()
    created = make_book_stock(id=100)
    mock_repository.create.return_value = created

    log_spy = mocker.spy(commands.logger, "info")
    result = commands.create(input_stock)

    assert result == created
    mock_repository.create.assert_called_once_with(input_stock)
    log_spy.assert_any_call("[BookStockCommands] Creating new book_stock: 1 - 10")
    log_spy.assert_any_call("[BookStockCommands] BookStock created successfully with ID: 100")


def test_update_book_stock_success(commands, mock_repository, make_book_stock, mocker):
    book_stock_id = 100
    existing = make_book_stock(id=book_stock_id)
    updated_input = make_book_stock()
    updated_result = make_book_stock(id=book_stock_id)

    mock_repository.get_by_id.return_value = existing
    mock_repository.update.return_value = updated_result

    log_spy = mocker.spy(commands.logger, "info")
    result = commands.update(book_stock_id, updated_input)

    assert result == updated_result
    assert updated_input.id == book_stock_id
    mock_repository.get_by_id.assert_called_once_with(book_stock_id)
    mock_repository.update.assert_called_once_with(book_stock_id, updated_input)
    log_spy.assert_any_call("[BookStockCommands] Updating book_stock with ID: 100")
    log_spy.assert_any_call("[BookStockCommands] BookStock ID 100 updated successfully")


def test_update_book_stock_not_found(commands, mock_repository, make_book_stock, mocker):
    mock_repository.get_by_id.return_value = None
    log_spy = mocker.spy(commands.logger, "warning")

    with pytest.raises(ValueError, match="BookStock not found"):
        commands.update(999, make_book_stock())

    mock_repository.get_by_id.assert_called_once_with(999)
    log_spy.assert_called_once_with("[BookStockCommands] Attempt to update non-existent book_stock ID: 999")


def test_delete_book_stock_success(commands, mock_repository, make_book_stock, mocker):
    mock_repository.get_by_id.return_value = make_book_stock(id=1)

    log_spy = mocker.spy(commands.logger, "info")
    commands.delete(1)

    mock_repository.get_by_id.assert_called_once_with(1)
    mock_repository.delete.assert_called_once_with(1)
    log_spy.assert_any_call("[BookStockCommands] Deleting book_stock with ID: 1")
    log_spy.assert_any_call("[BookStockCommands] BookStock ID 1 deleted successfully")


def test_delete_book_stock_not_found(commands, mock_repository, mocker):
    mock_repository.get_by_id.return_value = None

    log_spy = mocker.spy(commands.logger, "warning")
    with pytest.raises(ValueError, match="BookStock not found"):
        commands.delete(999)

    mock_repository.get_by_id.assert_called_once_with(999)
    log_spy.assert_called_once_with("[BookStockCommands] Attempt to delete non-existent book_stock ID: 999")
