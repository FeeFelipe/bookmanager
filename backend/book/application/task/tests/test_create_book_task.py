import pytest
from book.application.task import create_book_task


@pytest.fixture
def valid_book_data():
    return {
        "id": None,
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


def test_create_book_success(mocker, valid_book_data):
    mock_repo = mocker.patch("book.application.task.create_book_task.BookRepository")
    mock_index = mocker.patch("book.application.task.create_book_task.BookSearchRepository")

    created_book = mocker.Mock()
    created_book.id = 1
    created_book.isbn = valid_book_data["isbn"]
    created_book.title = valid_book_data["title"]
    created_book.synopsis = valid_book_data["synopsis"]
    created_book.authors = []
    created_book.categories = []
    created_book.publication_date.isoformat.return_value = "2008-08-01"

    mock_repo.return_value.create.return_value = created_book
    log_spy = mocker.spy(create_book_task.logger, "info")

    create_book_task.create_book_task.fn(valid_book_data)

    mock_repo.return_value.create.assert_called_once()
    mock_index.return_value.index_book.assert_called_once()
    assert any("[BookWorker] Book created with ID 1" in str(c.args[0]) for c in log_spy.call_args_list)
    assert any("[BookWorker] Processing new book:" in str(c.args[0]) for c in log_spy.call_args_list)


def test_create_book_fails_to_create(mocker, valid_book_data):
    mock_repo = mocker.patch("book.application.task.create_book_task.BookRepository")
    mock_repo.return_value.create.return_value = None
    mock_index = mocker.patch("book.application.task.create_book_task.BookSearchRepository")

    log_spy = mocker.spy(create_book_task.logger, "error")

    create_book_task.create_book_task.fn(valid_book_data)

    mock_repo.return_value.create.assert_called_once()
    mock_index.return_value.index_book.assert_not_called()
    log_spy.assert_called_once_with("[BookWorker] Book creation failed, skipping Elasticsearch indexing.")


def test_create_book_unexpected_exception(mocker, valid_book_data):
    mock_repo = mocker.patch("book.application.task.create_book_task.BookRepository")
    mock_repo.return_value.create.side_effect = Exception("DB error")

    log_spy = mocker.spy(create_book_task.logger, "exception")

    with pytest.raises(Exception, match="DB error"):
        create_book_task.create_book_task.fn(valid_book_data)

    log_spy.assert_called_once_with("[BookWorker] Failed to create book")
