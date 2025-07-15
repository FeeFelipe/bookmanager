import pytest
from unittest.mock import Mock

from book_stock.domain.book_stock_entities import BookStock
from book_stock.infrastructure.book_stock_model import BookStockModel
from book_stock.infrastructure.book_stock_repository import BookStockRepository


@pytest.fixture
def make_book_stock_model(mocker):
    def _make(**overrides):
        book = overrides.get("book", mocker.Mock(id=101))
        branch = overrides.get("branch", mocker.Mock(id=202))

        mock = mocker.Mock()
        mock.id = overrides.get("id", 1)
        mock.book = book
        mock.branch = branch
        mock.shelf = overrides.get("shelf", "A1")
        mock.floor = overrides.get("floor", "1")
        mock.room = overrides.get("room", "B")
        mock.status = overrides.get("status", "available")
        return mock

    return _make


@pytest.fixture
def repository():
    return BookStockRepository()


def test_get_all(repository, mocker, make_book_stock_model):
    book1 = mocker.Mock(id=101)
    book2 = mocker.Mock(id=102)

    mock_objs = [
        make_book_stock_model(book=book1),
        make_book_stock_model(id=2, book=book2),
    ]
    mock_qs = mocker.patch("book_stock.infrastructure.book_stock_repository.BookStockModel.objects")
    mock_qs.all.return_value = mock_objs

    result = repository.get_all()

    assert len(result) == 2
    assert isinstance(result[0], BookStock)
    assert result[0].book.id == 101
    assert result[1].book.id == 102


def test_get_by_id_found(repository, mocker, make_book_stock_model):
    mock_obj = make_book_stock_model(id=1)

    mock_get = mocker.patch("book_stock.infrastructure.book_stock_repository.BookStockModel.objects.get")
    mock_get.return_value = mock_obj

    result = repository.get_by_id(1)

    assert isinstance(result, BookStock)
    assert result.id == 1


def test_get_by_id_not_found(repository, mocker):
    mock_get = mocker.patch("book_stock.infrastructure.book_stock_repository.BookStockModel.objects.get")
    mock_get.side_effect = BookStockModel.DoesNotExist()

    with pytest.raises(BookStockModel.DoesNotExist):
        repository.get_by_id(999)


def test_get_by_id_unexpected_exception(repository, mocker):
    mock_get = mocker.patch("book_stock.infrastructure.book_stock_repository.BookStockModel.objects.get")
    mock_get.side_effect = Exception("unexpected")

    with pytest.raises(Exception):
        repository.get_by_id(1)


def test_create_book_stock(repository, mocker, make_book_stock_model):
    mock_book = mocker.Mock(id=101)
    mock_branch = mocker.Mock(id=202)
    mock_obj = make_book_stock_model(book=mock_book, branch=mock_branch)

    mocker.patch("book_stock.infrastructure.book_stock_repository.BookModel.objects.get", return_value=mock_book)
    mocker.patch("book_stock.infrastructure.book_stock_repository.BranchModel.objects.get", return_value=mock_branch)
    mock_create = mocker.patch("book_stock.infrastructure.book_stock_repository.BookStockModel.objects.create")
    mock_create.return_value = mock_obj

    book_stock_data = BookStock(
        id=None,
        book=101,
        branch=202,
        shelf="A1",
        floor="1",
        room="B",
        status="available"
    )

    result = repository.create(book_stock_data)

    assert isinstance(result, BookStock)
    assert result.id == 1
    assert result.book.id == 101
    assert result.branch.id == 202


def test_create_book_stock_unexpected_exception(repository, mocker):
    mocker.patch("book_stock.infrastructure.book_stock_repository.BookModel.objects.get", side_effect=Exception("fail"))
    mocker.patch("book_stock.infrastructure.book_stock_repository.BranchModel.objects.get", return_value=Mock())

    book_stock_data = BookStock(
        id=None,
        book=101,
        branch=202,
        shelf="A1",
        floor="1",
        room="B",
        status="available"
    )

    with pytest.raises(Exception):
        repository.create(book_stock_data)


def test_update_book_stock_success(repository, mocker, make_book_stock_model):
    mock_book = mocker.Mock(id=105)
    mock_branch = mocker.Mock(id=205)
    mock_obj = make_book_stock_model(id=1, book=mock_book, branch=mock_branch, shelf="B2", floor="2", room="C")

    mocker.patch("book_stock.infrastructure.book_stock_repository.BookModel.objects.get", return_value=mock_book)
    mocker.patch("book_stock.infrastructure.book_stock_repository.BranchModel.objects.get", return_value=mock_branch)

    mock_filter = mocker.patch("book_stock.infrastructure.book_stock_repository.BookStockModel.objects.filter")
    mock_filter.return_value.update.return_value = 1

    mock_get = mocker.patch("book_stock.infrastructure.book_stock_repository.BookStockModel.objects.get")
    mock_get.return_value = mock_obj

    book_stock_data = BookStock(
        id=1,
        book=105,
        branch=205,
        shelf="B2",
        floor="2",
        room="C",
        status="available"
    )

    result = repository.update(1, book_stock_data)

    assert isinstance(result, BookStock)
    assert result.id == 1
    assert result.book.id == 105


def test_update_book_stock_not_found(repository, mocker):
    mock_book = mocker.Mock(id=999)
    mock_branch = mocker.Mock(id=999)

    mocker.patch("book_stock.infrastructure.book_stock_repository.BookModel.objects.get", return_value=mock_book)
    mocker.patch("book_stock.infrastructure.book_stock_repository.BranchModel.objects.get", return_value=mock_branch)

    mock_filter = mocker.patch("book_stock.infrastructure.book_stock_repository.BookStockModel.objects.filter")
    mock_filter.return_value.update.return_value = 0

    book_stock_data = BookStock(
        id=999,
        book=999,
        branch=999,
        shelf="X",
        floor="Y",
        room="Z",
        status="reserved"
    )

    with pytest.raises(BookStockModel.DoesNotExist):
        repository.update(999, book_stock_data)


def test_delete_book_stock_success(repository, mocker):
    mock_filter = mocker.patch("book_stock.infrastructure.book_stock_repository.BookStockModel.objects.filter")
    mock_filter.return_value.delete.return_value = (1, {})

    repository.delete(1)
    mock_filter.assert_called_once_with(id=1)


def test_delete_book_stock_not_found(repository, mocker):
    mock_filter = mocker.patch("book_stock.infrastructure.book_stock_repository.BookStockModel.objects.filter")
    mock_filter.return_value.delete.return_value = (0, {})

    with pytest.raises(BookStockModel.DoesNotExist):
        repository.delete(999)
