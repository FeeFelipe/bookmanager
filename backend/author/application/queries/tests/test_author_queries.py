import pytest

from author.application.queries.author_queries import AuthorQueries
from author.domain.author_entities import Author
from author.infrastructure.author_model import AuthorModel


@pytest.fixture
def mock_repository(mocker):
    repo = mocker.patch("author.application.queries.author_queries.AuthorRepository", autospec=True)
    return repo.return_value


@pytest.fixture
def queries(mock_repository):
    return AuthorQueries()


@pytest.fixture
def valid_author_data():
    return Author(id=1, name="Author A")


def test_get_all_authors(queries, mock_repository, mocker, valid_author_data):
    another_author = Author(**{**valid_author_data.__dict__, "id": 2, "name": "Author B"})
    mock_authors = [valid_author_data, another_author]
    mock_repository.get_all.return_value = mock_authors

    log_spy = mocker.spy(queries.logger, "info")
    result = queries.get_all()

    assert result == mock_authors
    mock_repository.get_all.assert_called_once()
    log_spy.assert_called_once_with("[AuthorQueries] Retrieved 2 author records")


def test_get_by_id_found(queries, mock_repository, mocker, valid_author_data):
    mock_repository.get_by_id.return_value = valid_author_data

    log_spy = mocker.spy(queries.logger, "info")
    result = queries.get_by_id(1)

    assert result == valid_author_data
    mock_repository.get_by_id.assert_called_once_with(1)
    log_spy.assert_called_once_with("[AuthorQueries] Author found with ID: 1")


def test_get_by_id_not_found(queries, mock_repository, mocker):
    mock_repository.get_by_id.side_effect = AuthorModel.DoesNotExist()
    log_spy = mocker.spy(queries.logger, "warning")

    result = queries.get_by_id(999)

    assert result is None
    mock_repository.get_by_id.assert_called_once_with(999)
    log_spy.assert_called_once_with("[AuthorQueries] Author with ID 999 not found")
