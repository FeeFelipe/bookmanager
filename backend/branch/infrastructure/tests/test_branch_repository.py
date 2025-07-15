import pytest

from branch.domain.branch_entities import Branch
from branch.infrastructure.branch_model import BranchModel
from branch.infrastructure.branch_repository import BranchRepository


@pytest.fixture
def make_branch_model(mocker):
    def _make(**overrides):
        mock = mocker.Mock(spec=BranchModel)
        mock.id = overrides.get("id", 1)
        mock.name = overrides.get("name", "Central Library")
        mock.location = overrides.get("location", "123 Main St")
        return mock

    return _make


def test_get_all_branches(mocker, make_branch_model):
    mock_queryset = [make_branch_model(), make_branch_model(id=2, name="Branch B")]
    mocker.patch("branch.infrastructure.branch_repository.BranchModel.objects.all", return_value=mock_queryset)

    repo = BranchRepository()
    result = repo.get_all()

    assert len(result) == 2
    assert result[0].name == "Central Library"
    assert result[1].name == "Branch B"


def test_get_by_id_found(mocker, make_branch_model):
    mock_instance = make_branch_model()
    mocker.patch("branch.infrastructure.branch_repository.BranchModel.objects.get", return_value=mock_instance)

    repo = BranchRepository()
    result = repo.get_by_id(1)

    assert result.id == 1
    assert result.name == "Central Library"


def test_get_by_id_not_found(mocker):
    mocker.patch("branch.infrastructure.branch_repository.BranchModel.objects.get",
                 side_effect=BranchModel.DoesNotExist)

    repo = BranchRepository()
    with pytest.raises(BranchModel.DoesNotExist):
        repo.get_by_id(999)


def test_get_by_id_unexpected_exception(mocker):
    mocker.patch("branch.infrastructure.branch_repository.BranchModel.objects.get", side_effect=Exception("DB error"))

    repo = BranchRepository()
    with pytest.raises(Exception):
        repo.get_by_id(1)


def test_create_branch(mocker, make_branch_model):
    mock_create = mocker.patch("branch.infrastructure.branch_repository.BranchModel.objects.create")
    mock_create.return_value = make_branch_model()

    repo = BranchRepository()
    branch = Branch(id=None, name="Central Library", location="123 Main St")

    result = repo.create(branch)

    assert result.id == 1
    assert result.name == "Central Library"


def test_create_branch_unexpected_exception(mocker):
    mocker.patch("branch.infrastructure.branch_repository.BranchModel.objects.create",
                 side_effect=Exception("Create error"))

    repo = BranchRepository()
    branch = Branch(id=None, name="New Branch", location="New Location")

    with pytest.raises(Exception):
        repo.create(branch)


def test_update_branch_success(mocker, make_branch_model):
    mock_filter = mocker.patch("branch.infrastructure.branch_repository.BranchModel.objects.filter")
    mock_filter.return_value.update.return_value = 1

    mock_get = mocker.patch("branch.infrastructure.branch_repository.BranchModel.objects.get")
    mock_get.return_value = make_branch_model()

    repo = BranchRepository()
    branch = Branch(id=1, name="Updated Branch", location="Updated Location")

    result = repo.update(1, branch)

    assert result.id == 1
    assert result.name == "Central Library"


def test_update_branch_not_found(mocker):
    mock_filter = mocker.patch("branch.infrastructure.branch_repository.BranchModel.objects.filter")
    mock_filter.return_value.update.return_value = 0

    repo = BranchRepository()
    branch = Branch(id=999, name="Updated", location="Updated")

    with pytest.raises(BranchModel.DoesNotExist):
        repo.update(999, branch)


def test_delete_branch_success(mocker):
    mock_filter = mocker.patch("branch.infrastructure.branch_repository.BranchModel.objects.filter")
    mock_filter.return_value.delete.return_value = (1, {})

    repo = BranchRepository()
    repo.delete(1)

    mock_filter.return_value.delete.assert_called_once()


def test_delete_branch_not_found(mocker):
    mock_filter = mocker.patch("branch.infrastructure.branch_repository.BranchModel.objects.filter")
    mock_filter.return_value.delete.return_value = (0, {})

    repo = BranchRepository()
    with pytest.raises(BranchModel.DoesNotExist):
        repo.delete(999)
