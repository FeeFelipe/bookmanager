import pytest
from book_stock.application.queries.book_stock_queries import BookStockQueries
from book_stock.domain.book_stock_entities import BookStock
from book_stock.infrastructure.book_stock_model import BookStockModel


@pytest.fixture
def mock_repository(mocker):
    repo = mocker.patch("book_stock.application.queries.book_stock_queries.BookStockRepository", autospec=True)
    return repo.return_value


@pytest.fixture
def queries(mock_repository):
    return BookStockQueries()


@pytest.fixture
def make_book_stock():
    def _make_book_stock(**overrides):
        data = {
            "id": 1,
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


def test_get_all_book_stock(queries, mock_repository, mocker, make_book_stock):
    book1 = make_book_stock()
    book2 = make_book_stock(id=2, branch=20)
    mock_repository.get_all.return_value = [book1, book2]

    log_spy = mocker.spy(queries.logger, "info")
    result = queries.get_all()

    assert result == [book1, book2]
    mock_repository.get_all.assert_called_once()
    log_spy.assert_called_once_with("[BookStockQueries] Retrieved 2 book_stock records")


def test_get_by_id_found(queries, mock_repository, mocker, make_book_stock):
    mock_repository.get_by_id.return_value = make_book_stock()

    log_spy = mocker.spy(queries.logger, "info")
    result = queries.get_by_id(1)

    assert result.id == 1
    mock_repository.get_by_id.assert_called_once_with(1)
    log_spy.assert_called_once_with("[BookStockQueries] BookStock found with ID: 1")


def test_get_by_id_not_found(queries, mock_repository, mocker):
    mock_repository.get_by_id.side_effect = BookStockModel.DoesNotExist()
    log_spy = mocker.spy(queries.logger, "warning")

    result = queries.get_by_id(999)

    assert result is None
    mock_repository.get_by_id.assert_called_once_with(999)
    log_spy.assert_called_once_with("[BookStockQueries] BookStock with ID 999 not found")
