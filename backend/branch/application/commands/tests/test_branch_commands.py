import pytest

from branch.application.commands.branch_commands import BranchCommands
from branch.domain.branch_entities import Branch


@pytest.fixture
def mock_repository(mocker):
    repo = mocker.patch("branch.application.commands.branch_commands.BranchRepository", autospec=True)
    return repo.return_value


@pytest.fixture
def commands(mock_repository):
    return BranchCommands()


@pytest.fixture
def valid_branch_data():
    return Branch(id=None, name="Main Branch", location="Downtown")


def test_create_branch(commands, mock_repository, valid_branch_data, mocker):
    created = Branch(**{**valid_branch_data.__dict__, "id": 1})
    mock_repository.create.return_value = created

    log_spy = mocker.spy(commands.logger, "info")
    result = commands.create(valid_branch_data)

    assert result == created
    mock_repository.create.assert_called_once_with(valid_branch_data)
    log_spy.assert_any_call("[BranchCommands] Creating new branch: Main Branch")
    log_spy.assert_any_call("[BranchCommands] Branch created successfully with ID: 1")


def test_update_branch_success(commands, mock_repository, valid_branch_data, mocker):
    branch_id = 1
    existing = Branch(**{**valid_branch_data.__dict__, "id": branch_id})
    updated_input = Branch(**{**valid_branch_data.__dict__})
    updated_result = Branch(**{**valid_branch_data.__dict__, "id": branch_id})

    mock_repository.get_by_id.return_value = existing
    mock_repository.update.return_value = updated_result

    log_spy = mocker.spy(commands.logger, "info")
    result = commands.update(branch_id, updated_input)

    assert result == updated_result
    assert updated_input.id == branch_id
    mock_repository.get_by_id.assert_called_once_with(branch_id)
    mock_repository.update.assert_called_once_with(branch_id, updated_input)
    log_spy.assert_any_call("[BranchCommands] Updating branch with ID: 1")
    log_spy.assert_any_call("[BranchCommands] Branch ID 1 updated successfully")


def test_update_branch_not_found(commands, mock_repository, valid_branch_data, mocker):
    mock_repository.get_by_id.return_value = None
    log_spy = mocker.spy(commands.logger, "warning")

    with pytest.raises(ValueError, match="Branch not found"):
        commands.update(999, valid_branch_data)

    mock_repository.get_by_id.assert_called_once_with(999)
    log_spy.assert_called_once_with("[BranchCommands] Attempt to update non-existent branch ID: 999")


def test_delete_branch_success(commands, mock_repository, mocker):
    mock_repository.get_by_id.return_value = Branch(id=1, name="Main", location="Loc")

    log_spy = mocker.spy(commands.logger, "info")
    commands.delete(1)

    mock_repository.get_by_id.assert_called_once_with(1)
    mock_repository.delete.assert_called_once_with(1)
    log_spy.assert_any_call("[BranchCommands] Deleting branch with ID: 1")
    log_spy.assert_any_call("[BranchCommands] Branch ID 1 deleted successfully")


def test_delete_branch_not_found(commands, mock_repository, mocker):
    mock_repository.get_by_id.return_value = None

    log_spy = mocker.spy(commands.logger, "warning")
    with pytest.raises(ValueError, match="Branch not found"):
        commands.delete(999)

    mock_repository.get_by_id.assert_called_once_with(999)
    log_spy.assert_called_once_with("[BranchCommands] Attempt to delete non-existent branch ID: 999")
