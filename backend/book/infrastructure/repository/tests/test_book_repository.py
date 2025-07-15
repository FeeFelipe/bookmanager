import pytest
from book.domain.book_entities import Book
from book.infrastructure.repository.book_repository import BookRepository
from book.infrastructure.repository.book_model import BookModel
from django.db import IntegrityError


@pytest.fixture
def make_book_model(mocker):
    def _make_book_model(**overrides):
        mock = mocker.Mock(spec=BookModel)
        mock.id = overrides.get("id", 1)
        mock.title = overrides.get("title", "Book Title")
        mock.isbn = overrides.get("isbn", "1234567890123")
        mock.publisher = overrides.get("publisher", "Publisher")
        mock.edition = overrides.get("edition", "1st")
        mock.language = overrides.get("language", "English")
        mock.book_type = overrides.get("book_type", "Physical")
        mock.synopsis = overrides.get("synopsis", "A great book.")
        mock.publication_date = overrides.get("publication_date", "2022-01-01")
        mock.authors.all.return_value = []
        mock.categories.all.return_value = []
        return mock
    return _make_book_model


def test_get_all_books(mocker, make_book_model):
    mock_queryset = [make_book_model(), make_book_model(id=2)]
    mocker.patch("book.infrastructure.repository.book_model.BookModel.objects.all", return_value=mock_queryset)

    repo = BookRepository()
    result = repo.get_all()

    assert len(result) == 2
    assert isinstance(result[0], Book)


def test_get_by_id_found(mocker, make_book_model):
    mock_instance = make_book_model()
    mocker.patch("book.infrastructure.repository.book_model.BookModel.objects.get", return_value=mock_instance)

    repo = BookRepository()
    result = repo.get_by_id(1)

    assert isinstance(result, Book)
    assert result.id == 1


def test_get_by_id_not_found(mocker):
    mocker.patch("book.infrastructure.repository.book_model.BookModel.objects.get", side_effect=BookModel.DoesNotExist)

    repo = BookRepository()
    with pytest.raises(BookModel.DoesNotExist):
        repo.get_by_id(999)


def test_get_by_id_unexpected_exception(mocker):
    mocker.patch("book.infrastructure.repository.book_model.BookModel.objects.get", side_effect=Exception("DB error"))

    repo = BookRepository()
    with pytest.raises(Exception):
        repo.get_by_id(1)


def test_get_queryset_calls_logger(mocker):
    mock_all = mocker.patch("book.infrastructure.repository.book_model.BookModel.objects.all")

    repo = BookRepository()
    result = repo.get_queryset()

    mock_all.assert_called_once()
    assert result == mock_all.return_value


def test_create_book(mocker, make_book_model):
    mock_create = mocker.patch("book.infrastructure.repository.book_model.BookModel.objects.create")
    mock_instance = make_book_model()
    mock_create.return_value = mock_instance

    repo = BookRepository()
    book = repo._to_entity(mock_instance)

    result = repo.create(book)

    assert isinstance(result, Book)
    assert result.title == "Book Title"


def test_create_book_integrity_error(mocker, make_book_model):
    mocker.patch("book.infrastructure.repository.book_model.BookModel.objects.create", side_effect=IntegrityError("duplicate key"))

    repo = BookRepository()
    book = repo._to_entity(make_book_model())

    with pytest.raises(IntegrityError):
        repo.create(book)


def test_create_book_unexpected_exception(mocker, make_book_model):
    mocker.patch("book.infrastructure.repository.book_model.BookModel.objects.create", side_effect=Exception("DB error"))

    repo = BookRepository()
    book = repo._to_entity(make_book_model())

    with pytest.raises(Exception):
        repo.create(book)


def test_update_book_success(mocker, make_book_model):
    mock_filter = mocker.patch("book.infrastructure.repository.book_model.BookModel.objects.filter")
    mock_filter.return_value.update.return_value = 1

    mock_get = mocker.patch("book.infrastructure.repository.book_model.BookModel.objects.get")
    mock_get.return_value = make_book_model()

    repo = BookRepository()
    book = repo._to_entity(make_book_model())

    result = repo.update(book.id, book)

    assert isinstance(result, Book)
    assert result.id == book.id


def test_update_book_not_found(mocker, make_book_model):
    mock_filter = mocker.patch("book.infrastructure.repository.book_model.BookModel.objects.filter")
    mock_filter.return_value.update.return_value = 0

    repo = BookRepository()
    book = repo._to_entity(make_book_model(id=999))

    with pytest.raises(BookModel.DoesNotExist):
        repo.update(book.id, book)


def test_update_book_unexpected_exception(mocker, make_book_model):
    mock_filter = mocker.patch("book.infrastructure.repository.book_model.BookModel.objects.filter")
    mock_filter.return_value.update.return_value = 1

    mocker.patch("book.infrastructure.repository.book_model.BookModel.objects.get", side_effect=Exception("update error"))

    repo = BookRepository()
    book = repo._to_entity(make_book_model())

    with pytest.raises(Exception):
        repo.update(book.id, book)


def test_delete_book_success(mocker):
    mock_filter = mocker.patch("book.infrastructure.repository.book_model.BookModel.objects.filter")
    mock_filter.return_value.delete.return_value = (1, {})

    repo = BookRepository()
    repo.delete(1)

    mock_filter.return_value.delete.assert_called_once()


def test_delete_book_not_found(mocker):
    mock_filter = mocker.patch("book.infrastructure.repository.book_model.BookModel.objects.filter")
    mock_filter.return_value.delete.return_value = (0, {})

    repo = BookRepository()
    with pytest.raises(BookModel.DoesNotExist):
        repo.delete(999)


def test_delete_book_unexpected_exception(mocker):
    mock_filter = mocker.patch("book.infrastructure.repository.book_model.BookModel.objects.filter")
    mock_filter.return_value.delete.side_effect = Exception("DB error")

    repo = BookRepository()
    with pytest.raises(Exception):
        repo.delete(1)
