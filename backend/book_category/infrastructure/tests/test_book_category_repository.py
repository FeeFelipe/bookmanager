import pytest

from book_category.domain.book_category_entities import BookCategory
from book_category.infrastructure.book_category_model import BookCategoryModel
from book_category.infrastructure.book_category_repository import BookCategoryRepository


@pytest.fixture
def make_book_category_model(mocker):
    def _make(**overrides):
        mock = mocker.Mock(spec=BookCategoryModel)
        mock.id = overrides.get("id", 1)
        mock.name = overrides.get("name", "Fiction")
        return mock

    return _make


def test_get_all_categories(mocker, make_book_category_model):
    mock_queryset = [make_book_category_model(), make_book_category_model(id=2, name="Science")]
    mocker.patch("book_category.infrastructure.book_category_repository.BookCategoryModel.objects.all",
                 return_value=mock_queryset)

    repo = BookCategoryRepository()
    result = repo.get_all()

    assert len(result) == 2
    assert result[0].name == "Fiction"
    assert result[1].name == "Science"


def test_get_by_id_found(mocker, make_book_category_model):
    mock_instance = make_book_category_model()
    mocker.patch("book_category.infrastructure.book_category_repository.BookCategoryModel.objects.get",
                 return_value=mock_instance)

    repo = BookCategoryRepository()
    result = repo.get_by_id(1)

    assert result.id == 1
    assert result.name == "Fiction"


def test_get_by_id_not_found(mocker):
    mocker.patch("book_category.infrastructure.book_category_repository.BookCategoryModel.objects.get",
                 side_effect=BookCategoryModel.DoesNotExist)

    repo = BookCategoryRepository()
    with pytest.raises(BookCategoryModel.DoesNotExist):
        repo.get_by_id(999)


def test_get_by_id_unexpected_error(mocker):
    mocker.patch("book_category.infrastructure.book_category_repository.BookCategoryModel.objects.get",
                 side_effect=Exception("fail"))

    repo = BookCategoryRepository()
    with pytest.raises(Exception, match="fail"):
        repo.get_by_id(1)


def test_create_book_category(mocker, make_book_category_model):
    mock_create = mocker.patch("book_category.infrastructure.book_category_repository.BookCategoryModel.objects.create")
    mock_instance = make_book_category_model()
    mock_create.return_value = mock_instance

    repo = BookCategoryRepository()
    category = BookCategory(id=None, name="History")

    result = repo.create(category)

    assert result.id == 1
    assert result.name == "Fiction"


def test_create_book_category_unexpected_error(mocker):
    mocker.patch("book_category.infrastructure.book_category_repository.BookCategoryModel.objects.create",
                 side_effect=Exception("creation failed"))

    repo = BookCategoryRepository()
    category = BookCategory(id=None, name="ErrorTest")

    with pytest.raises(Exception, match="creation failed"):
        repo.create(category)


def test_update_book_category_success(mocker, make_book_category_model):
    mock_filter = mocker.patch("book_category.infrastructure.book_category_repository.BookCategoryModel.objects.filter")
    mock_filter.return_value.update.return_value = 1

    mock_get = mocker.patch("book_category.infrastructure.book_category_repository.BookCategoryModel.objects.get")
    mock_get.return_value = make_book_category_model()

    repo = BookCategoryRepository()
    category = BookCategory(id=1, name="Biography")

    result = repo.update(1, category)

    assert result.id == 1
    assert result.name == "Fiction"


def test_update_book_category_not_found(mocker):
    mock_filter = mocker.patch("book_category.infrastructure.book_category_repository.BookCategoryModel.objects.filter")
    mock_filter.return_value.update.return_value = 0

    repo = BookCategoryRepository()
    category = BookCategory(id=999, name="Nonexistent")

    with pytest.raises(BookCategoryModel.DoesNotExist):
        repo.update(999, category)


def test_update_book_category_unexpected_error(mocker):
    mock_filter = mocker.patch("book_category.infrastructure.book_category_repository.BookCategoryModel.objects.filter")
    mock_filter.return_value.update.side_effect = Exception("update failed")

    repo = BookCategoryRepository()
    category = BookCategory(id=1, name="Fail")

    with pytest.raises(Exception, match="update failed"):
        repo.update(1, category)


def test_delete_book_category_success(mocker):
    mock_filter = mocker.patch("book_category.infrastructure.book_category_repository.BookCategoryModel.objects.filter")
    mock_filter.return_value.delete.return_value = (1, {})

    repo = BookCategoryRepository()
    repo.delete(1)


def test_delete_book_category_not_found(mocker):
    mock_filter = mocker.patch("book_category.infrastructure.book_category_repository.BookCategoryModel.objects.filter")
    mock_filter.return_value.delete.return_value = (0, {})

    repo = BookCategoryRepository()
    with pytest.raises(BookCategoryModel.DoesNotExist):
        repo.delete(999)
