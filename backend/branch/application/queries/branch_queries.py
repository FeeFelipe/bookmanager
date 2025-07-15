import logging

from branch.domain.branch_entities import Branch
from branch.domain.branch_query_interface import BranchQueryInterface
from branch.infrastructure.branch_model import BranchModel
from branch.infrastructure.branch_repository import BranchRepository


class BranchQueries(BranchQueryInterface):
    def __init__(self):
        self.repository = BranchRepository()
        self.logger = logging.getLogger(__name__)

    def get_all(self) -> list[Branch]:
        branches = self.repository.get_all()
        self.logger.info(f"[BranchQueries] Retrieved {len(branches)} branch records")
        return branches

    def get_by_id(self, branch_id: int) -> Branch | None:
        try:
            branch = self.repository.get_by_id(branch_id)
            self.logger.info(f"[BranchQueries] Branch found with ID: {branch_id}")
            return branch
        except BranchModel.DoesNotExist:
            self.logger.warning(f"[BranchQueries] Branch with ID {branch_id} not found")
            return None
