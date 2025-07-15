import pytest

from book_category.application.queries.book_category_queries import BookCategoryQueries
from book_category.domain.book_category_entities import BookCategory
from book_category.infrastructure.book_category_model import BookCategoryModel


@pytest.fixture
def mock_repository(mocker):
    repo = mocker.patch("book_category.application.queries.book_category_queries.BookCategoryRepository", autospec=True)
    return repo.return_value


@pytest.fixture
def queries(mock_repository):
    return BookCategoryQueries()


@pytest.fixture
def valid_book_category_data():
    return BookCategory(id=1, name="Programming")


def test_get_all_book_categories(queries, mock_repository, mocker, valid_book_category_data):
    other = BookCategory(**{**valid_book_category_data.__dict__, "id": 2, "name": "Fiction"})
    mock_categories = [valid_book_category_data, other]
    mock_repository.get_all.return_value = mock_categories

    log_spy = mocker.spy(queries.logger, "info")
    result = queries.get_all()

    assert result == mock_categories
    mock_repository.get_all.assert_called_once()
    log_spy.assert_called_once_with("[BookCategoryQueries] Retrieved 2 book category records")


def test_get_by_id_found(queries, mock_repository, mocker, valid_book_category_data):
    mock_repository.get_by_id.return_value = valid_book_category_data

    log_spy = mocker.spy(queries.logger, "info")
    result = queries.get_by_id(1)

    assert result == valid_book_category_data
    mock_repository.get_by_id.assert_called_once_with(1)
    log_spy.assert_called_once_with("[BookCategoryQueries] BookCategory found with ID: 1")


def test_get_by_id_not_found(queries, mock_repository, mocker):
    mock_repository.get_by_id.side_effect = BookCategoryModel.DoesNotExist()
    log_spy = mocker.spy(queries.logger, "warning")

    result = queries.get_by_id(999)

    assert result is None
    mock_repository.get_by_id.assert_called_once_with(999)
    log_spy.assert_called_once_with("[BookCategoryQueries] BookCategory with ID 999 not found")
