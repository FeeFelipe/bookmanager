import pytest

from branch.application.queries.branch_queries import BranchQueries
from branch.domain.branch_entities import Branch
from branch.infrastructure.branch_model import BranchModel


@pytest.fixture
def mock_repository(mocker):
    repo = mocker.patch("branch.application.queries.branch_queries.BranchRepository", autospec=True)
    return repo.return_value


@pytest.fixture
def queries(mock_repository):
    return BranchQueries()


@pytest.fixture
def valid_branch_data():
    return Branch(id=1, name="Main Branch", location="Downtown")


def test_get_all_branches(queries, mock_repository, mocker, valid_branch_data):
    other_branch = Branch(
        **{**valid_branch_data.__dict__, "id": 2, "name": "West Branch", "location": "Uptown"}
    )
    branches = [valid_branch_data, other_branch]
    mock_repository.get_all.return_value = branches

    log_spy = mocker.spy(queries.logger, "info")
    result = queries.get_all()

    assert result == branches
    mock_repository.get_all.assert_called_once()
    log_spy.assert_called_once_with("[BranchQueries] Retrieved 2 branch records")


def test_get_by_id_found(queries, mock_repository, mocker, valid_branch_data):
    mock_repository.get_by_id.return_value = valid_branch_data

    log_spy = mocker.spy(queries.logger, "info")
    result = queries.get_by_id(1)

    assert result == valid_branch_data
    mock_repository.get_by_id.assert_called_once_with(1)
    log_spy.assert_called_once_with("[BranchQueries] Branch found with ID: 1")


def test_get_by_id_not_found(queries, mock_repository, mocker):
    mock_repository.get_by_id.side_effect = BranchModel.DoesNotExist()
    log_spy = mocker.spy(queries.logger, "warning")

    result = queries.get_by_id(999)

    assert result is None
    mock_repository.get_by_id.assert_called_once_with(999)
    log_spy.assert_called_once_with("[BranchQueries] Branch with ID 999 not found")
