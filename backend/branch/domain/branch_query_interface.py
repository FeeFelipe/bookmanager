from abc import ABC, abstractmethod

from .branch_entities import Branch


class BranchQueryInterface(ABC):
    @abstractmethod
    def get_all(self) -> list[Branch]:
        pass

    @abstractmethod
    def get_by_id(self, branch_id: int) -> Branch:
        pass
