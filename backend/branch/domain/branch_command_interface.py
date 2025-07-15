from abc import ABC, abstractmethod

from .branch_entities import Branch


class BranchCommandInterface(ABC):
    @abstractmethod
    def create(self, branch: Branch) -> Branch:
        pass

    @abstractmethod
    def update(self, branch_id: int, branch: Branch) -> Branch:
        pass

    @abstractmethod
    def delete(self, branch_id: int) -> None:
        pass
