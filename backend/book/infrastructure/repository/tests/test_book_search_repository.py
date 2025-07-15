import pytest
from book.infrastructure.repository.book_search_repository import BookSearchRepository


@pytest.fixture
def repository():
    return BookSearchRepository()


@pytest.fixture
def make_book_index_data():
    def _make(**overrides):
        data = {
            "isbn": "1234567890123",
            "title": "Sample Book",
            "synopsis": "A sample book.",
            "authors": ["Author One"],
            "categories": ["Category A"],
            "publication_date": "2023-01-01"
        }
        data.update(overrides)
        return data
    return _make


def test_index_book_success(mocker, repository, make_book_index_data):
    book = make_book_index_data()
    mock_index = mocker.patch("book.infrastructure.repository.book_search_repository.es_client.index")
    log_spy = mocker.spy(repository.logger, "info")

    repository.index_book(book)

    mock_index.assert_called_once_with(index="books", id="1234567890123", document=book)
    log_spy.assert_any_call("[BookSearchRepository] Book 1234567890123 indexed successfully")


def test_index_book_failure(mocker, repository, make_book_index_data):
    book = make_book_index_data()
    mocker.patch("book.infrastructure.repository.book_search_repository.es_client.index", side_effect=Exception("ES error"))
    log_spy = mocker.spy(repository.logger, "exception")

    with pytest.raises(Exception):
        repository.index_book(book)

    log_spy.assert_called_once_with("[BookSearchRepository] Failed to index book 1234567890123")


def test_search_books_success(mocker, repository):
    mock_response = {
        "hits": {
            "hits": [
                {"_source": {"title": "Book 1"}},
                {"_source": {"title": "Book 2"}},
            ]
        }
    }
    mock_search = mocker.patch("book.infrastructure.repository.book_search_repository.es_client.search", return_value=mock_response)
    log_spy = mocker.spy(repository.logger, "info")

    results = repository.search_books("Book")

    mock_search.assert_called_once()
    assert len(results) == 2
    assert results[0]["title"] == "Book 1"
    log_spy.assert_any_call("[BookSearchRepository] Found 2 results for query: 'Book'")


def test_search_books_failure(mocker, repository):
    mocker.patch("book.infrastructure.repository.book_search_repository.es_client.search", side_effect=Exception("Search failed"))
    log_spy = mocker.spy(repository.logger, "exception")

    with pytest.raises(Exception):
        repository.search_books("Book")

    log_spy.assert_called_once_with("[BookSearchRepository] Failed to search books with query: 'Book'")


def test_delete_book_success(mocker, repository):
    mock_delete = mocker.patch("book.infrastructure.repository.book_search_repository.es_client.delete")
    log_spy = mocker.spy(repository.logger, "info")

    repository.delete_book("1234567890123")

    mock_delete.assert_called_once_with(index="books", id="1234567890123", ignore=[404])
    log_spy.assert_any_call("[BookSearchRepository] Book 1234567890123 deleted from index")


def test_delete_book_failure(mocker, repository):
    mocker.patch("book.infrastructure.repository.book_search_repository.es_client.delete", side_effect=Exception("Delete error"))
    log_spy = mocker.spy(repository.logger, "exception")

    with pytest.raises(Exception):
        repository.delete_book("1234567890123")

    log_spy.assert_called_once_with("[BookSearchRepository] Failed to delete book with ISBN 1234567890123")
