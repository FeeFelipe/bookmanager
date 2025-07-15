import pytest
from book.application.queries.book_queries import BookQueries
from book.domain.book_entities import Book
from book.infrastructure.repository.book_model import BookModel


@pytest.fixture
def make_book():
    def _make(**overrides):
        data = {
            "id": 1,
            "title": "Clean Code",
            "isbn": "1234567890123",
            "publisher": "Prentice Hall",
            "edition": "1st",
            "language": "English",
            "book_type": "Technical",
            "synopsis": "A book about writing clean code.",
            "publication_date": "2008-08-01",
            "authors": [],
            "categories": []
        }
        data.update(overrides)
        return Book(**data)
    return _make


@pytest.fixture
def mock_repository(mocker):
    repo = mocker.patch("book.application.queries.book_queries.BookRepository", autospec=True)
    return repo.return_value


@pytest.fixture
def queries(mock_repository):
    return BookQueries()


def test_get_all_books(queries, mock_repository, mocker, make_book):
    book_1 = make_book()
    book_2 = make_book(
        id=2,
        title="Brave New World",
        isbn="2222222222222",
        synopsis="Science fiction novel",
        publication_date="1932-08-18"
    )

    books = [book_1, book_2]
    mock_repository.get_all.return_value = books

    log_spy = mocker.spy(queries.logger, "info")
    result = queries.get_all()

    assert result == books
    mock_repository.get_all.assert_called_once()
    log_spy.assert_called_once_with("[BookQueries] Retrieved 2 book records")


def test_get_by_id_found(queries, mock_repository, mocker, make_book):
    book = make_book()
    mock_repository.get_by_id.return_value = book

    log_spy = mocker.spy(queries.logger, "info")
    result = queries.get_by_id(1)

    assert result == book
    mock_repository.get_by_id.assert_called_once_with(1)
    log_spy.assert_called_once_with("[BookQueries] Book found with ID: 1")


def test_get_by_id_not_found(queries, mock_repository, mocker):
    mock_repository.get_by_id.side_effect = BookModel.DoesNotExist()
    log_spy = mocker.spy(queries.logger, "warning")

    result = queries.get_by_id(999)

    assert result is None
    mock_repository.get_by_id.assert_called_once_with(999)
    log_spy.assert_called_once_with("[BookQueries] Book with ID 999 not found")
