import pytest
from datetime import datetime
from unittest.mock import Mock

from author.domain.author_entities import Author
from author.infrastructure.author_model import AuthorModel
from author.infrastructure.author_repository import AuthorRepository


@pytest.fixture
def mock_author_model():
    mock = Mock()
    mock.configure_mock(
        id=1,
        name="Author A",
        created_at=datetime(2024, 1, 1, 10, 0),
        updated_at=datetime(2024, 1, 2, 12, 0),
    )
    mock.__str__ = lambda self=mock: mock.name
    return mock


@pytest.fixture
def repository():
    return AuthorRepository()


def test_get_all(repository, mocker, mock_author_model):
    mock_objs = [
        mock_author_model,
        Mock(id=2, name="Author B", created_at=None, updated_at=None)
    ]
    mock_qs = mocker.patch("author.infrastructure.author_repository.AuthorModel.objects")
    mock_qs.all.return_value = mock_objs

    result = repository.get_all()

    assert len(result) == 2
    assert isinstance(result[0], Author)
    assert result[0].name == "Author A"


def test_get_by_id_found(repository, mocker, mock_author_model):
    mock_get = mocker.patch("author.infrastructure.author_repository.AuthorModel.objects.get")
    mock_get.return_value = mock_author_model

    result = repository.get_by_id(1)

    assert isinstance(result, Author)
    assert result.id == 1
    assert result.name == "Author A"
    mock_get.assert_called_once_with(id=1)


def test_get_by_id_not_found(repository, mocker):
    mock_get = mocker.patch("author.infrastructure.author_repository.AuthorModel.objects.get")
    mock_get.side_effect = AuthorModel.DoesNotExist()

    with pytest.raises(AuthorModel.DoesNotExist):
        repository.get_by_id(999)


def test_get_by_id_unexpected_exception(repository, mocker):
    mock_get = mocker.patch("author.infrastructure.author_repository.AuthorModel.objects.get")
    mock_get.side_effect = Exception("unexpected error")

    with pytest.raises(Exception, match="unexpected error"):
        repository.get_by_id(999)


def test_create_author(repository, mocker):
    author = Author(id=None, name="Author A")

    mock_author_obj = mocker.Mock()
    mock_author_obj.id = 1
    mock_author_obj.name = "Author A"
    mock_create = mocker.patch("author.infrastructure.author_repository.AuthorModel.objects.create")
    mock_create.return_value = mock_author_obj

    result = repository.create(author)

    assert isinstance(result, Author)
    assert result.id == 1
    assert result.name == "Author A"
    mock_create.assert_called_once()


def test_create_author_unexpected_exception(repository, mocker):
    author = Author(id=None, name="Error Author")
    mock_create = mocker.patch("author.infrastructure.author_repository.AuthorModel.objects.create")
    mock_create.side_effect = Exception("create failed")

    with pytest.raises(Exception, match="create failed"):
        repository.create(author)


def test_update_author_success(repository, mocker):
    updated_author = Author(id=1, name="Updated Author")

    mock_filter = mocker.patch("author.infrastructure.author_repository.AuthorModel.objects.filter")
    mock_filter.return_value.update.return_value = 1

    mock_author_obj = mocker.Mock()
    mock_author_obj.id = 1
    mock_author_obj.name = "Updated Author"
    mock_get = mocker.patch("author.infrastructure.author_repository.AuthorModel.objects.get")
    mock_get.return_value = mock_author_obj

    result = repository.update(1, updated_author)

    assert isinstance(result, Author)
    assert result.id == 1
    assert result.name == "Updated Author"


def test_update_author_not_found(repository, mocker):
    updated_author = Author(id=999, name="Missing Author")
    mock_filter = mocker.patch("author.infrastructure.author_repository.AuthorModel.objects.filter")
    mock_filter.return_value.update.return_value = 0

    with pytest.raises(AuthorModel.DoesNotExist):
        repository.update(999, updated_author)


def test_update_author_unexpected_exception(repository, mocker):
    updated_author = Author(id=1, name="Error Author")
    mock_filter = mocker.patch("author.infrastructure.author_repository.AuthorModel.objects.filter")
    mock_filter.return_value.update.side_effect = Exception("update failed")

    with pytest.raises(Exception, match="update failed"):
        repository.update(1, updated_author)


def test_delete_author_success(repository, mocker):
    mock_filter = mocker.patch("author.infrastructure.author_repository.AuthorModel.objects.filter")
    mock_filter.return_value.delete.return_value = (1, {})

    repository.delete(1)
    mock_filter.assert_called_once_with(id=1)


def test_delete_author_not_found(repository, mocker):
    mock_filter = mocker.patch("author.infrastructure.author_repository.AuthorModel.objects.filter")
    mock_filter.return_value.delete.return_value = (0, {})

    with pytest.raises(AuthorModel.DoesNotExist):
        repository.delete(999)


def test_delete_author_unexpected_exception(repository, mocker):
    mock_filter = mocker.patch("author.infrastructure.author_repository.AuthorModel.objects.filter")
    mock_filter.return_value.delete.side_effect = Exception("delete failed")

    with pytest.raises(Exception, match="delete failed"):
        repository.delete(1)
