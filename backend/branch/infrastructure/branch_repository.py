import logging

from branch.domain.branch_command_interface import BranchCommandInterface
from branch.domain.branch_entities import Branch
from branch.domain.branch_query_interface import BranchQueryInterface
from .branch_model import BranchModel


class BranchRepository(BranchCommandInterface, BranchQueryInterface):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_all(self) -> list[Branch]:
        self.logger.info("[BranchRepository] Fetching all branches from database")
        branches = BranchModel.objects.all()
        return [self._to_entity(obj) for obj in branches]

    def get_by_id(self, branch_id: int) -> Branch:
        try:
            obj = BranchModel.objects.get(id=branch_id)
            self.logger.info(f"[BranchRepository] Branch {branch_id} fetched successfully")
            return self._to_entity(obj)
        except BranchModel.DoesNotExist:
            self.logger.warning(f"[BranchRepository] Branch {branch_id} not found in database")
            raise
        except Exception:
            self.logger.exception(f"[BranchRepository] Unexpected error fetching branch {branch_id}")
            raise

    def create(self, branch: Branch) -> Branch:
        try:
            data = branch.__dict__.copy()
            data.pop("id", None)
            obj = BranchModel.objects.create(**data)
            self.logger.info(f"[BranchRepository] Branch created with ID {obj.id}")
            return self._to_entity(obj)
        except Exception:
            self.logger.exception("[BranchRepository] Unexpected error creating branch")
            raise

    def update(self, branch_id: int, branch: Branch) -> Branch:
        try:
            data = branch.__dict__.copy()
            data.pop("id", None)
            updated = BranchModel.objects.filter(id=branch_id).update(**data)
            if updated == 0:
                self.logger.warning(f"[BranchRepository] Branch {branch_id} not found for update")
                raise BranchModel.DoesNotExist(f"Branch {branch_id} not found")

            obj = BranchModel.objects.get(id=branch_id)
            self.logger.info(f"[BranchRepository] Branch {branch_id} updated successfully")
            return self._to_entity(obj)
        except Exception:
            self.logger.exception(f"[BranchRepository] Unexpected error updating branch {branch_id}")
            raise

    def delete(self, branch_id: int) -> None:
        try:
            deleted, _ = BranchModel.objects.filter(id=branch_id).delete()
            if deleted == 0:
                self.logger.warning(f"[BranchRepository] Branch {branch_id} not found for deletion")
                raise BranchModel.DoesNotExist(f"Branch {branch_id} not found")
            self.logger.info(f"[BranchRepository] Branch {branch_id} deleted successfully")
        except Exception:
            self.logger.exception(f"[BranchRepository] Unexpected error deleting branch {branch_id}")
            raise

    def _to_entity(self, obj: BranchModel) -> Branch:
        return Branch(
            id=obj.id,
            name=obj.name,
            location=obj.location
        )
