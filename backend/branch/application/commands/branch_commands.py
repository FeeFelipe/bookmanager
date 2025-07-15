import logging
from abc import ABC

from branch.domain.branch_command_interface import BranchCommandInterface
from branch.domain.branch_entities import Branch
from branch.infrastructure.branch_repository import BranchRepository


class BranchCommands(BranchCommandInterface, ABC):
    def __init__(self):
        self.repository = BranchRepository()
        self.logger = logging.getLogger(__name__)

    def create(self, branch: Branch) -> Branch:
        self.logger.info(f"[BranchCommands] Creating new branch: {branch.name}")
        created = self.repository.create(branch)
        self.logger.info(f"[BranchCommands] Branch created successfully with ID: {created.id}")
        return created

    def update(self, branch_id: int, branch: Branch) -> Branch:
        self.logger.info(f"[BranchCommands] Updating branch with ID: {branch_id}")
        existing = self.repository.get_by_id(branch_id)
        if not existing:
            self.logger.warning(f"[BranchCommands] Attempt to update non-existent branch ID: {branch_id}")
            raise ValueError("Branch not found")

        branch.id = branch_id
        updated = self.repository.update(branch_id, branch)
        self.logger.info(f"[BranchCommands] Branch ID {branch_id} updated successfully")
        return updated

    def delete(self, branch_id: int) -> None:
        self.logger.info(f"[BranchCommands] Deleting branch with ID: {branch_id}")
        branch = self.repository.get_by_id(branch_id)
        if not branch:
            self.logger.warning(f"[BranchCommands] Attempt to delete non-existent branch ID: {branch_id}")
            raise ValueError("Branch not found")

        self.repository.delete(branch_id)
        self.logger.info(f"[BranchCommands] Branch ID {branch_id} deleted successfully")
